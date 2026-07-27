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

    def test_per_problem_time_limit_moves_only_the_cpu_dial(self):
        """按题限时（2026-07-27 人已拍板）只准动 CPU 那一项。

        文件大小和地址空间是另外两条防线，跟「这道题该给多少时间」无关；
        把它们一起放宽就是借着一次授权改动扩大了三倍的面。
        """
        seen = {}
        with mock.patch.object(resource, "setrlimit", lambda k, v: seen.__setitem__(k, v)):
            judge_module._limits(12)
        self.assertEqual(seen[resource.RLIMIT_CPU], (12, 12))
        self.assertEqual(seen[resource.RLIMIT_FSIZE], (2 * 1024 * 1024, 2 * 1024 * 1024))
        self.assertEqual(seen[resource.RLIMIT_AS], (768 * 1024 * 1024, 768 * 1024 * 1024))

    def test_per_problem_limit_is_never_stricter_than_the_old_flat_four_seconds(self):
        """下限：题目限时再短，也不能比改动前更严。

        改动前一律 4s。若照搬题面（很多题只给 1000ms），今天能过的提交明天会突然挂 ——
        我们的机器和语言组合本来就比平台慢，题面那个数字不是给我们这套环境定的。
        """
        for stated_ms in (60, 500, 1000, 2000, 3000, 4000):
            with mock.patch.object(judge_module, "LIMITS_CACHE",
                                   {"1": {"total_ms": stated_ms, "case_ms": None}}):
                self.assertGreaterEqual(judge_module.case_seconds(1, "cpp", 1), 4,
                                        f"{stated_ms}ms 被判严了")
                # 整次预算也不能比改动前（每组 4s、整次无上限）更严
                self.assertGreaterEqual(
                    judge_module.total_budget_seconds(1, "cpp", 21), 21 * 4, f"{stated_ms}ms")

    def test_per_problem_limit_is_capped(self):
        """上限：65536ms 那种题不能真给 65 秒，否则一次提交就能占住服务器。"""
        with mock.patch.object(judge_module, "LIMITS_CACHE",
                               {"1": {"total_ms": 65536, "case_ms": None}}):
            self.assertEqual(judge_module.case_seconds(1, "python", 21), judge_module.CASE_CAP_S)
            self.assertLessEqual(judge_module.total_budget_seconds(1, "python", 21),
                                 judge_module.TOTAL_HARD_CAP_S)

    def test_unknown_problem_falls_back_to_the_floor_not_to_zero(self):
        """查不到限时必须退回 4s，不能因为查不到就变严 —— 缺数据不该罚提交者。"""
        with mock.patch.object(judge_module, "LIMITS_CACHE", {"__missing__": True}):
            self.assertEqual(judge_module.case_seconds(99999, "python", 1), 4)
        with mock.patch.object(judge_module, "LIMITS_CACHE", {"1": {"total_ms": None, "case_ms": None}}):
            self.assertEqual(judge_module.case_seconds(1, "python", 1), 4)

    def test_per_case_limit_wins_over_the_total(self):
        """页面上「总时间限制」是整次的量，「单个测试点时间限制」才是每组的。

        判题器逐组跑，两者都给时必须用单点值（203 道题两者都给，如 30313 是 10000/1000）。
        用错会把每组放宽到整次的额度。
        """
        with mock.patch.object(judge_module, "LIMITS_CACHE",
                               {"1": {"total_ms": 10000, "case_ms": 6000}}):
            # 单点 6000ms × C++ 倍率 1 = 6 秒；若误用总限时会变成 10 秒
            self.assertEqual(judge_module.case_seconds(1, "cpp", 1), 6)

    def test_interpreted_languages_get_their_multiplier(self):
        """题面那个数字是给 C/C++ 的：Python ×10、PyPy3 ×3（人 2026-07-27 给出）。

        漏掉倍率就是拿 C++ 的尺子量 Python —— 我第一版漏了，于是把 18250「实现慢」
        误判成了「数据太重」，还据此写了一份打回。
        """
        with mock.patch.object(judge_module, "LIMITS_CACHE",
                               {"1": {"total_ms": 10000, "case_ms": None}}):
            cpp = judge_module.total_budget_seconds(1, "cpp", 1)
            pypy = judge_module.total_budget_seconds(1, "pypy3", 1)
            python = judge_module.total_budget_seconds(1, "python", 1)
        self.assertEqual(cpp, 10)
        self.assertEqual(pypy, 30)
        self.assertEqual(python, 100)
        # 未知语言不得凭空获得倍率
        with mock.patch.object(judge_module, "LIMITS_CACHE",
                               {"1": {"total_ms": 10000, "case_ms": None}}):
            self.assertEqual(judge_module.total_budget_seconds(1, "rust", 1), 10)

    def test_whole_submission_has_a_wall_clock_budget(self):
        """新加的总预算：放宽单组的同时，整次提交必须收住。

        改动前这一项实际上是无界的 —— 组数最多的一题有 150 组，150 × 5s = 750 秒。
        """
        self.assertLessEqual(judge_module.TOTAL_HARD_CAP_S, 600)
        slow = "import time\na, b = map(int, input().split())\ntime.sleep(0.2)\nprint(a + b)\n"
        with mock.patch.object(judge_module, "TOTAL_HARD_CAP_S", 0):
            result = judge(BOOK, PROBLEM, "python", slow)
        self.assertEqual(result["status"], "Time Limit Exceeded")
        self.assertIn("总预算", result["message"])
        # 预算够用时，同一份代码必须能过 —— 否则这条断言证明不了是预算起的作用
        self.assertEqual(judge(BOOK, PROBLEM, "python", slow)["status"], "Accepted")

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
                self.assertIsNotNone(fn, language)
                # 按题限时之后 preexec_fn 是个闭包，不再是 _limits 本身，所以不能比身份。
                # 改成**验行为**：把它调起来，三条限制必须一条不少地设上 —— 这比原来的
                # 身份断言更强，因为「叫 _limits」不等于「真的设了限制」。
                seen = {}
                with mock.patch.object(resource, "setrlimit", lambda k, v: seen.__setitem__(k, v)):
                    fn()
                self.assertEqual(sorted(seen), sorted([resource.RLIMIT_CPU, resource.RLIMIT_FSIZE,
                                                       resource.RLIMIT_AS]), language)
                self.assertEqual(seen[resource.RLIMIT_FSIZE], (2 * 1024 * 1024, 2 * 1024 * 1024))
                self.assertEqual(seen[resource.RLIMIT_AS], (768 * 1024 * 1024, 768 * 1024 * 1024))
                self.assertGreaterEqual(seen[resource.RLIMIT_CPU][0], judge_module.CASE_FLOOR_S)
                self.assertLessEqual(seen[resource.RLIMIT_CPU][0], judge_module.CASE_CAP_S)


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
