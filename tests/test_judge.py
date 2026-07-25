"""判题核心回归测试。

夹具自带在 `tests/fixtures/mirror/` 下并已入库，不依赖 `data/openjudge/tests/**`
（那批抓取数据按人拍板决策不入库），因此新克隆的仓库也能跑通交接闸门。
"""
import resource
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import judge as judge_module
from judge import judge


FIXTURE_MIRROR = Path(__file__).resolve().parent / "fixtures" / "mirror"
BOOK = "t001"
PROBLEM = "SUM2"          # 两组数据：1 2 -> 3、10 20 -> 30
SUM_SOURCE = "a, b = map(int, input().split())\nprint(a + b)\n"


class JudgeCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        patcher = mock.patch.object(judge_module, "MIRROR", FIXTURE_MIRROR)
        patcher.start()
        cls.addClassCleanup(patcher.stop)

    def test_accepts_token_equivalent_output(self):
        # 正确解法，但输出裹上多余空白：token 比对语义应判 AC，且两组数据都要跑到。
        source = "a, b = map(int, input().split())\nprint('  ', a + b, '  ')\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Accepted")
        self.assertEqual(result["cases"], 2)

    def test_wrong_answer_reports_the_failing_case(self):
        # 第 1 组正确、第 2 组错误：必须报出错在第 2 组，而不是笼统的 WA。
        source = "a, b = map(int, input().split())\nprint(3 if a == 1 else 0)\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Wrong Answer")
        self.assertEqual(result["case"], 2)

    def test_compile_error_is_distinct_from_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "def broken(:\n    pass\n")
        self.assertEqual(result["status"], "Compile Error")

    def test_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "raise RuntimeError('T001')\n")
        self.assertEqual(result["status"], "Runtime Error")
        self.assertEqual(result["case"], 1)

    def test_wall_clock_timeout_is_reported_as_tle(self):
        # 只睡不烧 CPU，RLIMIT_CPU 不会触发，确定性地走墙钟超时分支。
        result = judge(BOOK, PROBLEM, "python", "import time\ntime.sleep(30)\n")
        self.assertEqual(result["status"], "Time Limit Exceeded")
        self.assertIn("5 秒", result["message"])

    def test_cpu_limit_kill_is_reported_as_tle(self):
        # RLIMIT_CPU 与 5 秒墙钟是竞争关系，忙等无法稳定命中 CPU 分支；
        # 直接自发 SIGXCPU 才能确定性地钉住信号分类那一行。
        source = "import os, signal\nos.kill(os.getpid(), signal.SIGXCPU)\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Time Limit Exceeded")
        self.assertIn("CPU", result["message"])

    def test_output_limit_is_enforced(self):
        source = "print('x' * (2 * 1024 * 1024 + 1))\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Output Limit Exceeded")

    def test_problem_without_test_data_is_reported(self):
        result = judge(BOOK, "NODATA", "python", SUM_SOURCE)
        self.assertEqual(result["status"], "No Test Data")


if __name__ == "__main__":
    unittest.main()


class SandboxContractTests(unittest.TestCase):
    """红线 1 的机械判据：判题沙箱的限制值必须钉死，不能被后续改动悄悄放宽。

    这个项目一路的教训是「立了标准而没有机械判据等于没立」——
    「判题沙箱未放宽」此前只是每轮交接里手写的一句话，没人能验。这里把它变成用例：
    改动任何一项限制都会红。2026-07-26 加 PyPy3 时，靠它确认了新解释器走的是同一套限制。
    """

    @classmethod
    def setUpClass(cls):
        patcher = mock.patch.object(judge_module, "MIRROR", FIXTURE_MIRROR)
        patcher.start()
        cls.addClassCleanup(patcher.stop)

    def test_resource_limits_are_pinned(self):
        seen = {}
        real = resource.setrlimit
        with mock.patch.object(resource, "setrlimit", lambda k, v: seen.__setitem__(k, v)):
            judge_module._limits()
        self.assertEqual(seen[resource.RLIMIT_CPU], (4, 4))
        self.assertEqual(seen[resource.RLIMIT_FSIZE], (2 * 1024 * 1024, 2 * 1024 * 1024))
        self.assertEqual(seen[resource.RLIMIT_AS], (768 * 1024 * 1024, 768 * 1024 * 1024))
        self.assertIs(resource.setrlimit, real)

    def test_child_environment_is_the_fixed_minimal_set(self):
        """子进程环境必须恰好是 {PATH, HOME}，且 PATH 是那份固定的最小集。

        用户代码就跑在这个子进程里，PATH 上多一个目录就是多一片可执行面。
        2026-07-26 修 pypy3 查找问题时曾有过「把解释器目录塞进子进程 PATH」的写法，
        改成解析绝对路径后就不必动 PATH 了 —— 这条把结果钉住。
        """
        seen = []
        real_run = judge_module.subprocess.run

        def spy(command, **kwargs):
            seen.append(kwargs.get("env"))
            return real_run(command, **kwargs)

        for language in ("python", "pypy3"):
            if language == "pypy3" and not shutil.which("pypy3"):
                continue
            with mock.patch.object(judge_module.subprocess, "run", spy):
                judge(BOOK, PROBLEM, language, SUM_SOURCE)
        self.assertTrue(seen)
        for env in seen:
            self.assertEqual(sorted(env), ["HOME", "PATH"])
            self.assertEqual(env["PATH"], "/usr/local/bin:/usr/bin:/bin")

    def test_interpreter_outside_the_child_path_still_runs(self):
        """解释器装在子进程 PATH 之外（比如 ~/.local/bin/pypy3）时也必须能判题。

        这条钉的是 Codex 在 `1bd4603` 抓到的真 bug：`shutil.which()` 查的是**本进程**的
        PATH，子进程拿的却是受限 PATH，两者不一致时裸名字会 FileNotFoundError；
        `judge()` 不接这个异常，服务端就变成 500 而不是给出判定。
        """
        real = shutil.which("pypy3") or shutil.which("python3")
        with tempfile.TemporaryDirectory() as folder:
            elsewhere = Path(folder) / "opt"
            elsewhere.mkdir()
            shim = elsewhere / "pypy3"         # 装在子进程 PATH 之外
            shim.symlink_to(real)
            empty = Path(folder) / "empty"
            empty.mkdir()
            # 子进程 PATH 里一个解释器都没有：只有把命令解析成绝对路径才跑得起来。
            # 少了这一层，本机 /usr/bin/pypy3 恰好在标准 PATH 上，裸名字照样能跑，
            # 这条用例就变成了测不出差别的假覆盖（2026-07-26 变异自检抓到过一次）。
            with mock.patch.object(judge_module, "CHILD_PATH", str(empty)), \
                 mock.patch.object(judge_module.shutil, "which", return_value=str(shim)):
                result = judge(BOOK, PROBLEM, "pypy3", SUM_SOURCE)
        self.assertEqual(result["status"], "Accepted", result)

    def test_run_defaults_to_five_second_wall_clock(self):
        import inspect
        self.assertEqual(inspect.signature(judge_module._run).parameters["timeout"].default, 5)

    def test_every_interpreter_goes_through_the_same_limits(self):
        """新增语言不能绕开 _limits：判题跑的每个子进程都必须带上它。"""
        calls = []
        real_run = judge_module.subprocess.run

        def spy(command, **kwargs):
            calls.append(kwargs.get("preexec_fn"))
            return real_run(command, **kwargs)

        for language in ("python", "pypy3", "cpp"):
            if language == "pypy3" and not shutil.which("pypy3"):
                continue
            calls.clear()
            with mock.patch.object(judge_module.subprocess, "run", spy):
                judge(BOOK, PROBLEM, language,
                      SUM_SOURCE if language != "cpp" else CPP_SOURCE)
            self.assertTrue(calls, language)
            for fn in calls:
                self.assertIs(fn, judge_module._limits, language)


CPP_SOURCE = "#include <cstdio>\nint main(){int a,b;scanf(\"%d %d\",&a,&b);printf(\"%d\\n\",a+b);}\n"


class PyPy3Tests(unittest.TestCase):
    """PyPy3 档（人拍板 2026-07-26 加入；红线 1 已获签字）。"""

    @classmethod
    def setUpClass(cls):
        patcher = mock.patch.object(judge_module, "MIRROR", FIXTURE_MIRROR)
        patcher.start()
        cls.addClassCleanup(patcher.stop)

    @unittest.skipUnless(shutil.which("pypy3"), "本机没有 pypy3")
    def test_pypy3_accepts_a_correct_solution(self):
        result = judge(BOOK, PROBLEM, "pypy3", SUM_SOURCE)
        self.assertEqual(result["status"], "Accepted")
        self.assertEqual(result["cases"], 2)

    @unittest.skipUnless(shutil.which("pypy3"), "本机没有 pypy3")
    def test_pypy3_syntax_error_is_compile_error_not_runtime_error(self):
        # 语法检查交给 PyPy 自己：宿主 CPython 是 3.12、PyPy 是 3.9，两者语法能力不同，
        # 用宿主 compile() 代劳会把 CE 误判成 RE。
        result = judge(BOOK, PROBLEM, "pypy3", "def f(:\n    pass\n")
        self.assertEqual(result["status"], "Compile Error")

    @unittest.skipUnless(shutil.which("pypy3"), "本机没有 pypy3")
    def test_pypy3_runtime_error_stays_runtime_error(self):
        result = judge(BOOK, PROBLEM, "pypy3", "raise SystemExit(3)\n")
        self.assertEqual(result["status"], "Runtime Error")

    def test_missing_interpreter_is_reported_not_crashed(self):
        # 部署机上可能没装 pypy3：要给出可读状态，而不是抛异常或误判成 RE。
        with mock.patch.object(judge_module.shutil, "which", return_value=None):
            result = judge(BOOK, PROBLEM, "pypy3", SUM_SOURCE)
        self.assertEqual(result["status"], "Language Unavailable")
        self.assertIn("pypy3", result["message"])

    @unittest.skipUnless(shutil.which("pypy3"), "本机没有 pypy3")
    def test_pypy3_and_python3_are_actually_different_interpreters(self):
        # 这条防的是「加了语言其实还在跑 CPython」的假覆盖：
        # 让代码把自己的实现名打出来，两档必须给出不同的结果。
        source = "import sys\nprint(sys.implementation.name)\n"
        seen = {}
        real_run = judge_module.subprocess.run

        def spy(command, **kwargs):
            out = real_run(command, **kwargs)
            # command[0] 现在是绝对路径（见 judge.py 里解析 interpreter_path 的注释），
            # 所以按 basename 归类。
            name = Path(command[0]).name
            if name in ("python3", "pypy3") and "-c" not in command:
                seen[name] = out.stdout.decode().strip()
            return out

        for language in ("python", "pypy3"):
            with mock.patch.object(judge_module.subprocess, "run", spy):
                judge(BOOK, PROBLEM, language, source)
        self.assertEqual(seen.get("python3"), "cpython")
        self.assertEqual(seen.get("pypy3"), "pypy")
