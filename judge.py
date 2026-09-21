"""Local multi-language judge for the mirrored OpenJudge test pairs."""
import json
import multiprocessing
import os
import resource
import shutil
import signal
import subprocess
import tempfile
import threading
import time
import re
from pathlib import Path

ROOT = Path(__file__).parent
MIRROR = ROOT / "data" / "openjudge"
PROBLEM_KEYS_CACHE = None
PROBLEM_KEYS_VERSION = None
PROBLEM_KEYS_LOCK = threading.Lock()

# —— 按文件版本失效的缓存，键怎么取（2026-09-16）——
#
# 文件时间戳不是连续的：内核给 mtime 用的是粗粒度时钟。实测 2000 次连写，
# **开发机 zfs 与线上 xfs 都是每 1ms 才跳一次**，连续两次写有 65%~94% 拿到
# **同一个** `st_mtime_ns`。所以「只比 mtime」的缓存分不出「同一 tick 内的两次修改」。
#
# 这不只是理论上的洞，它一直在咬人：`test_template_is_reread_when_it_changes` 与
# `test_problem_exists_caches_until_catalog_changes` 都是「写探针 → 读 → 写回原样 → 再读」，
# 两次写落在同一 tick，缓存就继续吐探针那一版 —— 干净树上连跑 5 次红 4 次。
# （手册 §7 另记着一条 `errors=1` 的假红，那条是抛异常、至今没定位，**不是这一条**。）
#
# 键里带上大小（和静态文件 ETag 的 `size-mtime` 一个做法），再加一条：文件**刚改过**
# 的窗口内一律不信缓存 —— 窗口取 50ms，是实测 tick 的 50 倍，代价只是改动后的几十毫秒
# 里多读几次，之后照常缓存。两条合起来，「同一 tick 内改两次」才真的挡得住。
STAT_FRESH_WINDOW_NS = 50 * 1000 * 1000


def file_version(path):
    """缓存键：`(mtime_ns, size)`；文件刚改过就返回 `None`，意思是「这次别信缓存」。

    用 `abs()` 是因为时间戳可能落在未来（时钟回拨、从别处拷进来的文件）：附近
    ±50ms 一律当「刚改过」从严处理，而远在未来的时间戳按老样子缓存 —— 否则一份
    时间戳错到明年的 `catalog.json` 会让 4MB 的目录每个请求都重读一遍。
    """
    stat = path.stat()
    if abs(time.time_ns() - stat.st_mtime_ns) < STAT_FRESH_WINDOW_NS:
        return None
    return (stat.st_mtime_ns, stat.st_size)


# CPython 与 PyPy3 都跑 .py 源码，但是两个独立解释器：本机 PyPy 是 Python 3.9，
# 宿主 CPython 是 3.12，语法能力并不一致，所以 PyPy 的语法检查必须交给它自己做。
CPYTHON_LANGUAGES = {"python", "py", "python3"}
PYPY_LANGUAGES = {"pypy", "pypy3"}
DOTNET_LANGUAGES = {"dotnet", "dotnet10", "csharp", "fsharp", "vbnet"}
FILE_BASED_DOTNET_LANGUAGES = {"dotnet", "dotnet10", "csharp"}
SWIFT_LANGUAGES = {"swift"}
OBJC_LANGUAGES = {"objc", "objective-c", "objectivec"}
# 只做语法检查、不执行用户代码；compile() 本身不运行被编译的源码。
SYNTAX_CHECK = "import sys;compile(open(sys.argv[1],encoding='utf-8').read(),sys.argv[1],'exec')"

# —— 按题限时（2026-07-27，人已拍板）——
#
# 原来对所有题一律 CPU 4s、整次无上限。现在按题读限时。
#
# 题面写的那个数字是**给 C/C++ 的**，而且是**所有测试点的时间限制总和**。
# 解释型语言另有倍率（人 2026-07-27 给出）：Python ×10、PyPy3 ×3、C/C++ ×1。
# 漏掉倍率就会把 Python 提交按 C++ 的尺子量 —— 18250 的 Python 时限本该是
# 10000ms × 10 = 100 秒，我第一版只给了 10 秒，于是把「实现慢」误判成了「数据太重」。
LANGUAGE_TIME_MULTIPLIER = {"python": 10, "py": 10, "python3": 10, "pypy": 3, "pypy3": 3,
                            "c": 1, "cpp": 1, "c++": 1, "dotnet": 1, "dotnet10": 1,
                            "csharp": 2, "fsharp": 2, "vbnet": 2,
                            "swift": 1, "objc": 1, "objective-c": 1, "objectivec": 1}
CASE_FLOOR_S = 4
CASE_CAP_S = 20
# 整次提交的墙钟硬顶。改动前这一项无界：组数最多的一题有 150 组，150 × 5s = 750 秒。
TOTAL_HARD_CAP_S = 300
SPECIAL_CHECKER_TIMEOUT_S = 1.0
SAMPLE_STDIN_LIMIT = 64 * 1024
SAMPLE_OUTPUT_LIMIT = 64 * 1024
DOTNET_ADDRESS_SPACE = 2 * 768 * 1024 * 1024
DOTNET_FILE_SIZE = 16 * 1024 * 1024
LIMITS_CACHE = {}


def problem_limits(number):
    """取该题的限时（毫秒）。取不到就退回默认，绝不因为查不到而变严。

    「总时间限制」是整次提交的总量，「单个测试点时间限制」才是每组的；判题器逐组跑，
    所以有单点限时就用单点，只有总限时就用总限时（偏宽松，宁可放过不误杀，
    总量另有预算兜底）。
    """
    if not LIMITS_CACHE:
        path = MIRROR / "limits.json"
        try:
            LIMITS_CACHE.update(json.loads(path.read_text(encoding="utf-8"))["limits"])
        except (OSError, ValueError, KeyError):
            LIMITS_CACHE["__missing__"] = True
    row = LIMITS_CACHE.get(str(number))
    return row if isinstance(row, dict) else None


def total_budget_seconds(number, language, case_count):
    """整次提交的墙钟预算（秒）。

    用**总时间限制**（所有测试点之和），乘语言倍率。只给了单点限时的，按
    `单点 × 组数` 折算。下限取 `case_count × CASE_FLOOR_S` —— 改动前是每组 4s、
    整次无上限，这条保证新预算**绝不比改动前更严**。
    """
    row = problem_limits(number) or {}
    multiplier = LANGUAGE_TIME_MULTIPLIER.get(str(language).lower(), 1)
    stated = row.get("total_ms") or ((row.get("case_ms") or 0) * max(1, case_count))
    scaled = stated * multiplier / 1000
    floor = max(1, case_count) * CASE_FLOOR_S
    return min(TOTAL_HARD_CAP_S, max(floor, scaled))


def case_seconds(number, language="python", case_count=1):
    """单组的 CPU 秒数。

    用**单个测试点时间限制**；只给了总限时的，退回总限时（一组不可能比整次还久）。
    **查不到就保持改动前的 4s** —— 没有信息的时候不该放宽。
    """
    row = problem_limits(number) or {}
    stated = row.get("case_ms") or row.get("total_ms")
    if not stated:
        return CASE_FLOOR_S
    multiplier = LANGUAGE_TIME_MULTIPLIER.get(str(language).lower(), 1)
    return int(max(CASE_FLOOR_S, min(CASE_CAP_S, stated * multiplier / 1000)))


def _limits(cpu_seconds=CASE_FLOOR_S, address_space_bytes=768 * 1024 * 1024,
            file_size_bytes=2 * 1024 * 1024):
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_size_bytes, file_size_bytes))
    resource.setrlimit(resource.RLIMIT_AS, (address_space_bytes, address_space_bytes))

# 子进程环境固定成这一份：用户代码就跑在里面，多一个目录就是多一片可执行面。
CHILD_PATH = "/usr/local/bin:/usr/bin:/bin"
LANGUAGE_VERSION_CACHE = {}

def _toolchain_probe(executable, *args, timeout=5):
    """探测工具链版本；**本机没装或探测失败就返回 None，绝不抛异常。**

    2026-07-27 的教训：`language_version` 里直接 `subprocess.run(["swiftc", "--version"])`，
    本机没装 Swift 就抛 FileNotFoundError，把**整个提交页**打成连接直接断。
    一个「查版本号显示给用户看」的辅助功能，没有理由让页面打不开。
    g++/gcc/clang 当时是同样的写法，只是本机恰好装了才没暴露。
    """
    path = shutil.which(executable)
    if path is None:
        return None
    try:
        result = subprocess.run([path, *args], capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return (result.stdout or "") + (result.stderr or "")


def language_version(language):
    """Return the actual toolchain label used for a submission."""
    key = str(language).lower()
    if key in LANGUAGE_VERSION_CACHE:
        return LANGUAGE_VERSION_CACHE[key]
    if key in CPYTHON_LANGUAGES:
        value = f"Python3({'.'.join(map(str, __import__('sys').version_info[:2]))})"
    elif key in PYPY_LANGUAGES:
        raw = _toolchain_probe("pypy3", "--version")
        match = re.search(r"PyPy\s+(\d+\.\d+(?:\.\d+)?)", raw) if raw else None
        value = f"PyPy3({match.group(1) if match else ('unknown' if raw else '未安装')})"
    elif key == "cpp":
        raw = _toolchain_probe("g++", "--version")
        match = re.search(r"\b(\d+\.\d+)(?:\.\d+)?\b", raw) if raw else None
        value = f"G++({match.group(1) if match else ('unknown' if raw else '未安装')}(with c++17))"
    elif key == "c":
        raw = _toolchain_probe("gcc", "--version")
        match = re.search(r"\b(\d+\.\d+)(?:\.\d+)?\b", raw) if raw else None
        value = f"GCC({match.group(1) if match else ('unknown' if raw else '未安装')})"
    elif key in DOTNET_LANGUAGES:
        labels = {"csharp": "C#", "fsharp": "F#", "vbnet": "VB.NET"}
        value = f"{labels.get(key, '.NET')} (.NET SDK 10)"
    elif key in SWIFT_LANGUAGES:
        raw = _toolchain_probe("swiftc", "--version")
        match = re.search(r"Swift version\s+([\d.]+)", raw) if raw else None
        value = f"Swift({match.group(1) if match else ('unknown' if raw else '未安装')})"
    elif key in OBJC_LANGUAGES:
        raw = _toolchain_probe("clang", "--version")
        match = re.search(r"clang version\s+([\d.]+)", raw) if raw else None
        value = f"Objective-C(Clang {match.group(1) if match else ('unknown' if raw else '未安装')})"
    else:
        value = str(language)
    LANGUAGE_VERSION_CACHE[key] = value
    return value

def _run(command, stdin=None, cwd=None, timeout=5, cpu_seconds=CASE_FLOOR_S,
         address_space_bytes=768 * 1024 * 1024, file_size_bytes=2 * 1024 * 1024):
    # 墙钟比 CPU 多给 1 秒，和原来 (CPU 4 / 墙钟 5) 的关系保持一致。
    return subprocess.run(command, input=stdin, cwd=cwd, capture_output=True, timeout=timeout,
                          preexec_fn=lambda: _limits(cpu_seconds, address_space_bytes, file_size_bytes),
                          env={"PATH": CHILD_PATH, "HOME": str(cwd)})

def _compile_run(command, cwd, timeout=30):
    """Run a trusted compiler without applying limits intended for student code."""
    return subprocess.run(command, cwd=cwd, capture_output=True, timeout=timeout,
                          env={"PATH": CHILD_PATH, "HOME": str(cwd)})

def prepare_program(work, language, source, warmup_input=b""):
    """把源码变成一条可执行命令，或给出编译期裁定。

    从 judge() 里原样抽出来，好让「运行样例」复用同一条沙箱路径 ——
    新端点要是自己抄一份编译逻辑，两边迟早会漂，而漂掉的那一半就是沙箱。
    返回 (command, None) 或 (None, 裁定字典)。
    warmup_input 只给 .NET file-based app 预热用（它靠首次运行产出 build 缓存）。
    """
    if language in DOTNET_LANGUAGES:
        dotnet = shutil.which("dotnet")
        if dotnet is None:
            return None, {"status": "Language Unavailable", "message": ".NET SDK 10 未安装，换一种语言提交。"}
        if language in FILE_BASED_DOTNET_LANGUAGES:
            # .NET SDK 10 file-based apps need no generated project. The first
            # run creates the build cache; execute its DLL afterwards so the
            # SDK CLI itself never runs inside the user-code address limit.
            source_path = work / "Program.cs"
            source_path.write_text(source, encoding="utf-8")
            compile_result = subprocess.run(
                [dotnet, "run", "--file", str(source_path), "--nologo"],
                cwd=work, input=warmup_input, capture_output=True, timeout=30,
                env={"PATH": CHILD_PATH, "HOME": str(work), "DOTNET_GCHeapHardLimit": "268435456"})
            artifacts = list((work / ".local" / "share" / "dotnet" / "runfile").glob(
                "*/bin/debug/Program.dll"))
            if not artifacts:
                message = (compile_result.stderr + compile_result.stdout).decode(errors="replace")[-4000:]
                return None, {"status": "Compile Error", "message": message}
            command = [dotnet, str(artifacts[0])]
        else:
            source_names = {"fsharp": "Program.fs", "vbnet": "Program.vb"}
            source_path = work / source_names[language]
            source_path.write_text(source, encoding="utf-8")
            project_suffix = {"fsharp": ".fsproj", "vbnet": ".vbproj"}[language]
            project = work / ("Judge" + project_suffix)
            explicit_compile = '    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>\n'
            project.write_text(
                '<Project Sdk="Microsoft.NET.Sdk">\n'
                '  <PropertyGroup>\n'
                '    <OutputType>Exe</OutputType>\n'
                '    <TargetFramework>net10.0</TargetFramework>\n'
                '    <ImplicitUsings>disable</ImplicitUsings>\n'
                '    <Nullable>disable</Nullable>\n'
                + explicit_compile +
                '  </PropertyGroup>\n'
                f'  <ItemGroup><Compile Include="{source_path.name}" /></ItemGroup>\n'
                '</Project>\n', encoding="utf-8")
            compile_result = subprocess.run(
                [dotnet, "build", str(project), "--nologo", "-c", "Release", "-o", str(work / "out")],
                cwd=work, capture_output=True, timeout=30,
                env={"PATH": CHILD_PATH, "HOME": str(work), "DOTNET_GCHeapHardLimit": "268435456"})
            if compile_result.returncode:
                message = (compile_result.stderr + compile_result.stdout).decode(errors="replace")[-4000:]
                return None, {"status": "Compile Error", "message": message}
            command = [str(work / "out" / "Judge")]
    elif language in SWIFT_LANGUAGES | OBJC_LANGUAGES:
        ext = ".swift" if language in SWIFT_LANGUAGES else ".m"
        source_path = work / ("main" + ext)
        source_path.write_text(source, encoding="utf-8")
        compiler = shutil.which("swiftc" if language in SWIFT_LANGUAGES else "clang")
        if compiler is None:
            return None, {"status": "Language Unavailable", "message": "本机没有安装对应的 Swift/Objective-C 编译器。"}
        executable = work / "main"
        flags = ["-O"] if language in SWIFT_LANGUAGES else ["-O2", "-fobjc-runtime=gnustep-1.9"]
        compile_result = _compile_run([compiler, *flags, str(source_path), "-o", str(executable)], cwd=work)
        if compile_result.returncode:
            return None, {"status": "Compile Error", "message": compile_result.stderr.decode(errors="replace")[-4000:]}
        command = [str(executable)]
    else:
        ext = ".py" if language in CPYTHON_LANGUAGES | PYPY_LANGUAGES else ".c" if language == "c" else ".cpp"
        source_path = work / ("main" + ext); source_path.write_text(source, encoding="utf-8")
    if language in DOTNET_LANGUAGES | SWIFT_LANGUAGES | OBJC_LANGUAGES:
        pass
    elif ext == ".py":
        interpreter = "pypy3" if language in PYPY_LANGUAGES else "python3"
        # 必须解析成绝对路径再交给子进程：shutil.which 查的是**本进程**的 PATH，
        # 而子进程拿的是上面那份受限 PATH，两者不一致时裸名字会 FileNotFoundError
        # （judge 不接这个异常，服务端就变成 500 而不是给出判定）。
        # 走绝对路径既修掉这点，又不用往子进程 PATH 里塞目录。
        interpreter_path = shutil.which(interpreter)
        if interpreter_path is None:
            return None, {"status": "Language Unavailable", "message": f"本机没有安装 {interpreter}，换一种语言提交。"}
        if interpreter == "python3":
            try:
                compile(source, str(source_path), "exec")
            except (SyntaxError, ValueError) as error:
                return None, {"status": "Compile Error", "message": str(error)[-4000:]}
        else:
            # 不能用宿主 CPython 的 compile() 代劳：PyPy3 是另一个版本的解释器，
            # 语法判定必须由它自己给出，否则会把 CE 误判成 RE。
            check = _run([interpreter_path, "-I", "-c", SYNTAX_CHECK, str(source_path)], cwd=work, timeout=15)
            if check.returncode:
                return None, {"status": "Compile Error", "message": check.stderr.decode(errors="replace")[-4000:]}
        command = [interpreter_path, "-I", str(source_path)]
    else:
        executable = work / "main"
        compile_result = _run(["g++" if ext == ".cpp" else "gcc", "-O2", "-std=c++17" if ext == ".cpp" else "-std=c11", str(source_path), "-o", str(executable)], cwd=work, timeout=15)
        if compile_result.returncode:
            return None, {"status": "Compile Error", "message": compile_result.stderr.decode(errors="replace")[-4000:]}
        command = [str(executable)]
    return command, None


def run_sample(book, problem_id, language, source, stdin):
    item = catalog_item(book, problem_id) if book else None
    return unshift_prefix_lines(item, _run_sample(item, book, problem_id, language, source, stdin))


def _run_sample(item, book, problem_id, language, source, stdin):
    """跑一次用户给的输入，只回显输出，不比对、不入库。

    沙箱一条没放宽：命令来自同一个 prepare_program，执行走同一个 _run，
    因此 RLIMIT_CPU / RLIMIT_FSIZE / RLIMIT_AS、env 白名单、python3 -I
    和临时目录隔离与判题完全一致（SandboxContractTests 钉的就是这一点）。
    """
    if not isinstance(source, str) or not source.strip():
        return {"status": "Empty Source", "message": "代码不能为空。"}
    if len(source.encode()) > 512 * 1024:
        return {"status": "Source Too Large", "message": "代码不能超过 512 KiB。"}
    stdin = stdin if isinstance(stdin, str) else ""
    if len(stdin.encode()) > SAMPLE_STDIN_LIMIT:
        return {"status": "Input Too Large", "message": "样例输入不能超过 64 KiB。"}
    language = language.lower()
    digits = re.search(r"(\d+)$", str(problem_id))
    number = int(digits.group(1)) if digits else None
    cpu_seconds = case_seconds(number, language, 1)
    payload = stdin.encode()
    source, failure = apply_code_prefix(item, language, source)
    if failure is not None:
        return failure
    if item and item.get("interactor"):
        return _run_interactive_sample(item, language, source, payload, cpu_seconds)
    with tempfile.TemporaryDirectory(prefix="cs101-run-") as temp:
        work = Path(temp)
        command, failure = prepare_program(work, language, source, warmup_input=payload)
        if failure is not None:
            return failure
        started = time.perf_counter()
        run_address_space = DOTNET_ADDRESS_SPACE if language in DOTNET_LANGUAGES else 768 * 1024 * 1024
        run_file_size = DOTNET_FILE_SIZE if language in DOTNET_LANGUAGES else 2 * 1024 * 1024
        try:
            result = _run(command, stdin=payload, cwd=work, timeout=cpu_seconds + 1,
                          cpu_seconds=cpu_seconds, address_space_bytes=run_address_space,
                          file_size_bytes=run_file_size)
        except subprocess.TimeoutExpired:
            return {"status": "Time Limit Exceeded",
                    "message": f"运行超过 {cpu_seconds + 1} 秒。"}
        metrics = {"time_ms": round((time.perf_counter() - started) * 1000),
                   "memory_kb": int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)}
        if result.returncode in {-signal.SIGXCPU, -signal.SIGKILL}:
            return {"status": "Time Limit Exceeded", **metrics, "message": "超过 CPU 限制。"}
        stdout = result.stdout.decode(errors="replace")[:SAMPLE_OUTPUT_LIMIT]
        stderr = result.stderr.decode(errors="replace")[-4000:]
        if result.returncode != 0:
            return {"status": "Runtime Error", **metrics, "stdout": stdout,
                    "stderr": stderr, "message": stderr}
        row = {"status": "OK", **metrics, "stdout": stdout, "stderr": stderr}
        if item and item.get("checker"):
            # 答案不唯一：拿不到参考答案就不判；输入恰好是某组测试数据（样例就是第 0 组）才判
            case = _matching_case(item, payload)
            if case is None:
                row["checker"] = {"ok": None, "message": "本题答案不唯一，自定义输入无法判定对错。"}
            else:
                ok, message = run_checker(item["checker"], payload, result.stdout,
                                          (MIRROR / case["output"]).read_bytes())
                row["checker"] = {"ok": ok, "message": message if ok is not None else "判题器出错，请联系管理员。"}
        return row


def _matching_case(item, payload):
    wanted = payload.split()
    for case in item.get("test_cases", []):
        path = MIRROR / case["input"]
        try:
            if path.stat().st_size <= 4 * len(payload) + 64 and path.read_bytes().split() == wanted:
                return case
        except OSError:
            continue
    return None


def _run_interactive_sample(item, language, source, payload, cpu_seconds):
    """交互题的「运行样例」：输入框里是交互器读的隐藏数据（样例即第 0 组），回显交互过程。"""
    if not payload.strip():
        payload = (MIRROR / item["test_cases"][0]["input"]).read_bytes()
    case = _matching_case(item, payload)
    answer = (MIRROR / case["output"]).read_bytes() if case else b""
    with tempfile.TemporaryDirectory(prefix="cs101-run-") as temp:
        work = Path(temp)
        command, failure = prepare_program(work, language, source)
        if failure is not None:
            return failure
        run_address_space = DOTNET_ADDRESS_SPACE if language in DOTNET_LANGUAGES else 768 * 1024 * 1024
        run_file_size = DOTNET_FILE_SIZE if language in DOTNET_LANGUAGES else 2 * 1024 * 1024
        outcome = run_interactive(command, item["interactor"], payload, answer, work, cpu_seconds,
                                  run_address_space, run_file_size, keep_transcript=True)
    verdict = INTERACTIVE_VERDICTS[outcome["outcome"]]
    message = outcome["message"]
    if verdict == "Judge Error":
        message = "交互器读不懂这份输入（格式要和第 0 组一致），或交互器出错。"
    return {"status": "OK", "time_ms": outcome["time_ms"], "memory_kb": outcome["memory_kb"],
            "stdout": outcome.get("transcript", ""), "stderr": outcome["stderr"],
            "interactive": {"verdict": verdict, "message": message}}


def check_syntax(language, source):
    """Playground 的「语法检查」：只编译、不执行。

    走同一个 prepare_program，所以语法判定与运行、判题完全一致 ——
    Python 用宿主 compile()、PyPy3 用它自己、C/C++ 用 gcc/g++，不另起一套规则。
    （.NET file-based 的编译本身就要跑一次程序，这一点与「运行」相同，没有额外放宽。）
    """
    if not isinstance(source, str) or not source.strip():
        return {"status": "Empty Source", "message": "代码不能为空。"}
    if len(source.encode()) > 512 * 1024:
        return {"status": "Source Too Large", "message": "代码不能超过 512 KiB。"}
    with tempfile.TemporaryDirectory(prefix="cs101-run-") as temp:
        _, failure = prepare_program(Path(temp), str(language).lower(), source)
    return failure or {"status": "OK", "message": "编译通过，没有发现语法错误。"}


# 编译器 / 解释器报错里的「第几行第几列」。编辑器靠它在行号栏打标记、点一下跳过去。
# 路径前缀一律只认沙箱里的源文件名：头文件里的报错（如 /usr/include/...）不指向用户代码。
DIAGNOSTIC_PATTERNS = (
    # gcc / g++ / clang / swiftc：main.cpp:3:5: error: expected ';'
    re.compile(r"main\.(?:c|cpp|m|swift):(\d+):(\d+):\s*(?:fatal\s+)?(error|warning|note):\s*(.+)"),
    # dotnet：Program.cs(3,5): error CS1002: ; expected [/tmp/.../Judge.csproj]
    re.compile(r"Program\.(?:cs|fs|vb)\((\d+),(\d+)\):\s*(error|warning)\s+([^\[\n]+)"),
)
PY_LINE = re.compile(r'main\.py"?, line (\d+)')
SANDBOX_PATH = re.compile(r"/tmp/cs101-run-[^/\s]+/")


def parse_diagnostics(text):
    """把报错文本切成 [{line, column, severity, message}]，最多 50 条。"""
    text = SANDBOX_PATH.sub("", text or "")
    found = []
    for pattern in DIAGNOSTIC_PATTERNS:
        for match in pattern.finditer(text):
            line, column, severity, message = match.groups()
            if severity == "note":
                continue
            found.append({"line": int(line), "column": int(column),
                          "severity": severity, "message": message.strip()})
    if not found:
        # Python：SyntaxError 是「msg (main.py, line 3)」，运行期是 traceback，
        # 取**最后一个**指向 main.py 的帧 —— 那才是出错的那一行。
        lines = PY_LINE.findall(text)
        if lines:
            last = [row for row in text.strip().splitlines() if row.strip()][-1].strip()
            message = re.sub(r"\s*\(main\.py, line \d+\)\s*$", "", last)
            found.append({"line": int(lines[-1]), "column": 0, "severity": "error", "message": message})
    return found[:50]


def problem_exists(book, problem_id):
    """Return whether a requested run/submit target is in the local catalog.

    Cache only lookup keys and refresh them when catalog.json changes. This
    keeps the judge independent from server.py's catalog cache.
    """
    global PROBLEM_KEYS_CACHE, PROBLEM_KEYS_VERSION
    catalog_path = MIRROR / "catalog.json"
    try:
        version = file_version(catalog_path)
    except OSError:
        return False
    with PROBLEM_KEYS_LOCK:
        if PROBLEM_KEYS_CACHE is None or version is None or version != PROBLEM_KEYS_VERSION:
            try:
                catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return False
            PROBLEM_KEYS_CACHE = frozenset(
                (p.get("book"), p.get("id"))
                for p in catalog.get("problems", [])
                if isinstance(p, dict)
            )
            PROBLEM_KEYS_VERSION = version
        return (book, problem_id) in PROBLEM_KEYS_CACHE


def outputs_match(actual, expected, comparison="tokens"):
    """Compare output using a catalog-selected contract.

    `case_insensitive_tokens` 是 2026-09-20 加的：Codeforces 有一批题的题面明写
    「YES/NO 大小写随意」（"You can output the answer in any case"），而我们只做 token
    精确比对 —— 数据里的期望输出是 `YES`，照官方样例写 `Yes` 的正确程序会被判 Wrong Answer。
    口径挂在 catalog 的 `comparison` 字段上，逐题按题面开，不改全局默认
    （像 1B 那种输出列名的题，大小写是有意义的）。
    """
    actual_tokens, expected_tokens = actual.split(), expected.split()
    if comparison == "case_insensitive_tokens":
        return ([token.lower() for token in actual_tokens]
                == [token.lower() for token in expected_tokens])
    if comparison != "float_tokens":
        return actual_tokens == expected_tokens
    if len(actual_tokens) != len(expected_tokens):
        return False
    try:
        return all(abs(float(left) - float(right)) <= 1e-6
                   for left, right in zip(actual_tokens, expected_tokens))
    except ValueError:
        return False


def _special_output_matches_core(kind, input_data, actual):
    if kind == "subtree_parity_tree":
        try:
            values = list(map(int, input_data.decode().split())); queries = list(zip(values[1::2], values[2::2]))
            # 题面里那条彩蛋规则：t == 2 时每组的 x 要加一。2026-09-20 之前特判和数据
            # 都没实现它，而 21 组数据的 t 全是 2 —— 照题面写的程序会被判错。
            if values[0] == 2: queries = [(x + 1, y) for x, y in queries]
            tokens = actual.split(); cursor = 0
            for even_count, odd_count in queries:
                n = even_count + odd_count; possible = even_count <= n // 2 and not (n % 2 == 0 and even_count == 0)
                if cursor >= len(tokens): return False
                decision = tokens[cursor].upper(); cursor += 1
                if decision == "NO":
                    if possible: return False
                    continue
                if decision != "YES" or cursor + 2 * (n - 1) > len(tokens): return False
                edges = [(int(tokens[cursor+i*2])-1, int(tokens[cursor+i*2+1])-1) for i in range(n-1)]; cursor += 2*(n-1)
                graph = [[] for _ in range(n)]
                for a,b in edges:
                    if not (0 <= a < n and 0 <= b < n): return False
                    graph[a].append(b); graph[b].append(a)
                parent = [-2]*n; parent[0] = -1; order=[0]
                for node in order:
                    for nxt in graph[node]:
                        if parent[nxt] == -2: parent[nxt]=node; order.append(nxt)
                if len(order) != n: return False
                size = [1]*n
                for node in reversed(order[1:]): size[parent[node]] += size[node]
                if sum(value % 2 == 0 for value in size) != even_count or sum(value % 2 for value in size) != odd_count: return False
            return cursor == len(tokens)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "min_divisible_by_six_subarrays":
        try:
            from itertools import permutations
            values = list(map(int, input_data.decode().split()))[2:]
            output = list(map(int, actual.split()))
            if sorted(output) != sorted(values): return False
            def score(sequence):
                total = 0
                for left in range(len(sequence)):
                    product = 1
                    for right in range(left, len(sequence)):
                        product *= sequence[right]
                        if product % 6 == 0: total += 1
                return total
            best = min(score(candidate) for candidate in permutations(values))
            return score(output) == best
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "distinct_adjacent_gcd":
        try:
            import math
            sizes = list(map(int, input_data.decode().split()))[1:]
            values = list(map(int, actual.split())); cursor = 0
            for n in sizes:
                part = values[cursor:cursor+n]; cursor += n
                if len(part) != n or any(value < 1 or value > 10**18 for value in part): return False
                if len({math.gcd(a,b) for a,b in zip(part,part[1:])}) != n-1: return False
            return cursor == len(values)
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "max_median_blocks":
        try:
            sizes = list(map(int, input_data.decode().split()))[1:]
            values = list(map(int, actual.split())); cursor = 0
            for n in sizes:
                part = values[cursor:cursor+3*n]; cursor += 3*n
                if len(part) != 3*n or sorted(part) != list(range(1,3*n+1)):
                    return False
                if sum(sorted(part[index:index+3])[1] for index in range(0,3*n,3)) != 2*n*n:
                    return False
            return cursor == len(values)
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "maximize_min":
        try:
            values = list(map(int, input_data.decode().split()))[1:]
            output = list(map(int, actual.split()))
            return len(values) == len(output) and all(-67 <= y <= 67 and y >= x for x, y in zip(values, output))
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "matrix_beauty":
        try:
            from itertools import product, permutations
            tokens = list(map(int, input_data.decode().split()))
            output = list(map(int, actual.split()))
            def mex(values):
                value = 0
                while value in values: value += 1
                return value
            cursor = 0
            for index in range(tokens[0]):
                n, m = tokens[1 + index * 2:3 + index * 2]
                if cursor + 1 + n * m > len(output): return False
                beauty, flat = output[cursor], output[cursor+1:cursor+1+n*m]; cursor += 1+n*m
                rows = [flat[row*m:(row+1)*m] for row in range(n)]
                if any(sorted(row) != list(range(m)) for row in rows): return False
                actual_beauty = mex([mex([rows[row][col] for row in range(n)]) for col in range(m)])
                best = max(mex([mex([candidate[row][col] for row in range(n)]) for col in range(m)]) for candidate in product(list(permutations(range(m))), repeat=n))
                if beauty != actual_beauty or beauty != best: return False
            return cursor == len(output)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "good_permutation":
        try:
            import math
            input_tokens = list(map(int, input_data.decode().split()))
            sizes = input_tokens[1:]
            values = list(map(int, actual.split()))
            cursor = 0
            for n in sizes:
                part = values[cursor:cursor+n]; cursor += n
                bad = sum(math.gcd(a, b) == math.gcd(a, c) == math.gcd(b, c) == 1 for a, b, c in zip(part, part[1:], part[2:]))
                if len(part) != n or sorted(part) != list(range(1, n + 1)) or bad > 6:
                    return False
            return cursor == len(values)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "weather_permutation":
        try:
            values = list(map(int, input_data.decode().split()))
            output = list(map(int, actual.split()))
            t = values[0]; cursor = 1; out_cursor = 0
            for _ in range(t):
                n, k = values[cursor:cursor + 2]; cursor += 2
                forecast = values[cursor:cursor+n]; cursor += n
                actual_values = values[cursor:cursor+n]; cursor += n
                part = output[out_cursor:out_cursor+n]; out_cursor += n
                if (len(part) != n or sorted(part) != sorted(actual_values)
                        or any(abs(a-b) > k for a, b in zip(forecast, part))):
                    return False
            return out_cursor == len(output)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "tile_jump_path":
        try:
            text = input_data.decode().split()[1]
            tokens = list(map(int, actual.split()))
            cost, length = tokens[:2]; path = tokens[2:]
            if length != len(path) or not path or path[0] != 1 or path[-1] != len(text): return False
            chars = [ord(text[index - 1]) for index in path]
            increasing = ord(text[0]) <= ord(text[-1])
            lo, hi = min(ord(text[0]), ord(text[-1])), max(ord(text[0]), ord(text[-1]))
            maximum_length = sum(lo <= ord(char) <= hi for char in text)
            return (len(set(path)) == len(path) and length == maximum_length
                    and cost == abs(ord(text[0]) - ord(text[-1]))
                    and all(lo <= char <= hi for char in chars)
                    and all((a <= b if increasing else a >= b) for a,b in zip(chars,chars[1:]))
                    and sum(abs(a-b) for a,b in zip(chars,chars[1:])) == cost)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "shortest_path":
        try:
            import heapq
            values = list(map(int, input_data.decode().split()))
            nodes, edges = values[0], values[1]
            graph = [[] for _ in range(nodes + 1)]; weights = {}
            for index in range(edges):
                a, b, w = values[2 + index * 3:5 + index * 3]
                graph[a].append((b, w)); graph[b].append((a, w))
                weights[a, b] = weights[b, a] = min(weights.get((a, b), w), w)
            dist = [10**30] * (nodes + 1); dist[1] = 0; queue = [(0, 1)]
            while queue:
                cost, node = heapq.heappop(queue)
                if cost != dist[node]: continue
                for nxt, weight in graph[node]:
                    if cost + weight < dist[nxt]: dist[nxt] = cost + weight; heapq.heappush(queue, (dist[nxt], nxt))
            tokens = list(map(int, actual.split()))
            if tokens == [-1]: return dist[nodes] == 10**30
            return bool(tokens) and tokens[0] == 1 and tokens[-1] == nodes and all((a, b) in weights for a, b in zip(tokens, tokens[1:])) and sum(weights[a, b] for a, b in zip(tokens, tokens[1:])) == dist[nodes]
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "coprime_divisor_pairs":
        try:
            values = list(map(int, input_data.decode().split()[1:]))
            tokens = list(map(int, actual.split()))
            if len(tokens) != 2 * len(values):
                return False
            first, second = tokens[:len(values)], tokens[len(values):]
            import math
            for value, left, right in zip(values, first, second):
                if left == right == -1:
                    # A prime power has no two nontrivial coprime divisors.
                    temp, distinct, divisor = value, 0, 2
                    while divisor * divisor <= temp:
                        if temp % divisor == 0:
                            distinct += 1
                            while temp % divisor == 0:
                                temp //= divisor
                        divisor += 1
                    if temp > 1:
                        distinct += 1
                    if distinct > 1:
                        return False
                elif (left <= 1 or right <= 1 or value % left or value % right
                      or math.gcd(left + right, value) != 1):
                    return False
            return True
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "round_number_decomposition":
        try:
            values = list(map(int, input_data.decode().split()))
            tokens = list(map(int, actual.split()))
            t = values[0]; in_cursor = 1; out_cursor = 0
            for _ in range(t):
                value = values[in_cursor]; in_cursor += 1
                if out_cursor >= len(tokens): return False
                count = tokens[out_cursor]; out_cursor += 1
                parts = tokens[out_cursor:out_cursor+count]; out_cursor += count
                if (count != len(parts) or sum(parts) != value
                        or not all(part > 0 and str(part).rstrip("0").isdigit()
                                   and len(str(part).rstrip("0")) == 1 for part in parts)):
                    return False
            return out_cursor == len(tokens)
        except (UnicodeDecodeError, ValueError, IndexError):
            return False
    if kind == "n_digit_divisible":
        try:
            n, divisor = map(int, input_data.decode().split()[:2])
            tokens = actual.split()
            if tokens == ["-1"]:
                return n == 1 and divisor == 10
            return (len(tokens) == 1 and tokens[0].isdigit() and tokens[0][0] != "0"
                    and len(tokens[0]) == n and int(tokens[0]) % divisor == 0)
        except (UnicodeDecodeError, ValueError):
            return False
    if kind == "pairwise_sum_triple":
        # 1154A：黑板上是 a+b、a+c、b+c、a+b+c 四个数，**输出顺序任意**。
        try:
            board = sorted(map(int, input_data.decode().split()))
            values = list(map(int, actual.split()))
        except (UnicodeDecodeError, ValueError):
            return False
        if len(board) != 4 or len(values) != 3 or any(value <= 0 for value in values):
            return False
        a, b, c = values
        return sorted([a + b, a + c, b + c, a + b + c]) == board
    if kind == "divisible_by_8_subsequence":
        try:
            from itertools import combinations
            text = input_data.decode().split()[0]
            tokens = actual.split()
            if tokens == ["NO"]:
                # Divisibility by eight depends only on the last three digits.
                # Any longer valid subsequence therefore has a valid suffix of
                # length 1..3, so this is equivalent to the old 2**n search.
                return not any(int("".join(chars)) % 8 == 0
                               for length in range(1, min(3, len(text)) + 1)
                               for chars in combinations(text, length))
            if len(tokens) != 2 or tokens[0] != "YES":
                return False
            iterator = iter(text)
            return tokens[1].isdigit() and int(tokens[1]) % 8 == 0 and all(char in iterator for char in tokens[1])
        except (UnicodeDecodeError, IndexError):
            return False
    if kind != "concat_divisible":
        return False
    try:
        values = list(map(int, input_data.decode().split()))
        count, xs = values[0], values[1:]
        tokens = actual.split()
        if count < 1 or len(xs) != count or len(tokens) != count:
            return False
        ys = list(map(int, tokens))
    except (UnicodeDecodeError, ValueError, IndexError):
        return False
    return all(0 < y < 10**9 and int(str(x) + str(y)) % (x + y) == 0
               for x, y in zip(xs, ys))


def _special_checker_worker(connection, kind, input_data, actual):
    try:
        connection.send(bool(_special_output_matches_core(kind, input_data, actual)))
    except BaseException:
        connection.send(False)
    finally:
        connection.close()


def special_output_matches(kind, input_data, actual):
    """Run a special checker out of process with a non-negotiable wall limit.

    Checkers validate untrusted output and some necessarily inspect a search
    space. A malformed or future near-limit test must not be able to hold a
    server request after the submitted program has already finished.
    """
    if not kind:
        return False
    parent, child = multiprocessing.get_context("fork").Pipe(duplex=False)
    worker = multiprocessing.get_context("fork").Process(
        target=_special_checker_worker, args=(child, kind, input_data, actual), daemon=True)
    try:
        worker.start()
        child.close()
        if not parent.poll(SPECIAL_CHECKER_TIMEOUT_S):
            worker.terminate()
            worker.join()
            return False
        matched = bool(parent.recv())
        worker.join()
        return matched and worker.exitcode == 0
    except (EOFError, OSError):
        return False
    finally:
        parent.close()
        if worker.is_alive():
            worker.terminate()
            worker.join()


# ---- 特判与交互 ---------------------------------------------------------------
# 「答案不唯一」的题用逐题 checker.py，交互题用逐题 interactor.py，二者都放在该题
# 数据目录的根上，由索引器写进 catalog 的 `checker` / `interactor`（相对 MIRROR 的路径）。
# 它们是仓库里受信任的代码，但读的是学生程序的输出，所以照样走 _run 的限制与 env 白名单；
# 学生程序本身的执行路径一条没变。
#
# checker 约定：python3 -I checker.py <输入> <学生输出> <参考答案>
#   退出码 0 = 通过、42 = 答案错误；stdout 第一行是给学生看的一句话（不泄露数据）。
#   （不用 1：Python 未捕获的异常也退 1，会把判题器自己的 bug 变成冤判的 WA。）
#   其他退出码或超时 = 判题器自身出错，给 "Judge Error"，绝不算到学生头上。
# interactor 约定：python3 -I interactor.py <输入> <参考答案>
#   stdin 读学生程序的输出，stdout 写给学生程序；退出码 0 = 通过、42 = 答案错误，
#   stderr 最后一行是给学生看的一句话；其他退出码 = 判题器出错。
WRONG_ANSWER_EXIT = 42
CHECKER_CPU_S = 10
INTERACTOR_CPU_S = 20
INTERACTION_OUTPUT_LIMIT = 16 * 1024 * 1024
INTERACTION_STDERR_KEEP = 64 * 1024
CODE_PREFIX_LANGUAGES = {"python", "py", "python3"}


INTERACTIVE_VERDICTS = {"accepted": "Accepted", "wrong": "Wrong Answer", "tle": "Time Limit Exceeded",
                        "re": "Runtime Error", "ole": "Output Limit Exceeded", "judge_error": "Judge Error"}


def catalog_item(book, problem_id):
    try:
        catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return next((p for p in catalog.get("problems", [])
                 if p.get("book") == book and p.get("id") == problem_id), None)


def apply_code_prefix(item, language, source):
    """「预设代码」题（如 29986）：平台把交互库拼在学生代码前面。返回 (source, failure)。"""
    prefix = (item or {}).get("code_prefix")
    if not prefix:
        return source, None
    if language not in CODE_PREFIX_LANGUAGES:
        return None, {"status": "Language Unavailable",
                      "message": "这道题的预设代码是 Python，只能用 Python 3 提交。"}
    text = (MIRROR / prefix).read_text(encoding="utf-8")
    return text.rstrip("\n") + "\n" + source, None


def unshift_prefix_lines(item, result):
    """报错里的行号减去预设代码的行数，指回学生自己写的那一行（编辑器靠它打标记）。"""
    prefix = (item or {}).get("code_prefix")
    if not prefix or not isinstance(result, dict) or not isinstance(result.get("message"), str):
        return result
    offset = len((MIRROR / prefix).read_text(encoding="utf-8").rstrip("\n").split("\n"))
    def shift(match):
        line = int(match.group(2)) - offset
        return f"{match.group(1)}{line}" if line > 0 else f"{match.group(1)}{match.group(2)}（预设代码）"
    result["message"] = re.sub(r'(main\.py"?, line )(\d+)', shift, result["message"])
    if isinstance(result.get("stderr"), str):
        result["stderr"] = re.sub(r'(main\.py"?, line )(\d+)', shift, result["stderr"])
    return result


def _trusted_python():
    return shutil.which("python3") or "/usr/bin/python3"


def run_checker(checker, input_data, output_data, answer_data):
    """跑逐题 checker。返回 (True/False/None, 一句话)；None 表示判题器自身出错。"""
    with tempfile.TemporaryDirectory(prefix="cs101-check-") as temp:
        work = Path(temp)
        files = []
        for name, data in (("input.txt", input_data), ("output.txt", output_data), ("answer.txt", answer_data)):
            (work / name).write_bytes(data if isinstance(data, bytes) else data.encode())
            files.append(str(work / name))
        try:
            result = _run([_trusted_python(), "-I", str(MIRROR / checker), *files], cwd=work,
                          timeout=CHECKER_CPU_S + 2, cpu_seconds=CHECKER_CPU_S)
        except subprocess.TimeoutExpired:
            return None, "checker 超时"
    message = result.stdout.decode(errors="replace").strip().splitlines()
    message = message[0][:300] if message else ""
    if result.returncode == 0:
        return True, message
    if result.returncode == WRONG_ANSWER_EXIT:
        return False, message
    return None, (result.stderr.decode(errors="replace")[-2000:] or f"checker 退出码 {result.returncode}")


def _pump(source_fd, sink_fd, state, key, transcript, tag):
    """把一端的输出原样搬到另一端。sink 断开后继续读干净，免得上游写满管道卡住。"""
    sink_open = sink_fd is not None
    while True:
        try:
            chunk = os.read(source_fd, 65536)
        except OSError:
            chunk = b""
        if not chunk:
            break
        state[key] += len(chunk)
        if transcript is not None and state["transcript_bytes"] < SAMPLE_OUTPUT_LIMIT:
            transcript.append((tag, chunk))
            state["transcript_bytes"] += len(chunk)
        if key == "student_bytes" and state[key] > INTERACTION_OUTPUT_LIMIT:
            state["output_exceeded"] = True
        if sink_open:
            view = memoryview(chunk)
            try:
                while view:
                    view = view[os.write(sink_fd, view):]
            except OSError:
                sink_open = False
    if sink_fd is not None:
        try:
            os.close(sink_fd)
        except OSError:
            pass


def _drain(source_fd, keep):
    while True:
        try:
            chunk = os.read(source_fd, 65536)
        except OSError:
            break
        if not chunk:
            break
        keep.append(chunk)
        while sum(map(len, keep)) > INTERACTION_STDERR_KEEP and len(keep) > 1:
            keep.pop(0)


def run_interactive(command, interactor, input_data, answer_data, cwd, cpu_seconds,
                    address_space_bytes, file_size_bytes, keep_transcript=False):
    """学生程序与 interactor 对跑一组，判题器居中转发（好限制输出量、留交互记录）。

    返回 dict：outcome ∈ {accepted, wrong, tle, re, ole, judge_error}，另带 message、
    student_returncode、time_ms、memory_kb、stderr、transcript。
    """
    wall_seconds = 2 * cpu_seconds + 2          # 交互题等对方回应不耗 CPU，墙钟给到两倍
    with tempfile.TemporaryDirectory(prefix="cs101-interact-") as temp:
        jury = Path(temp)
        (jury / "input.txt").write_bytes(input_data)
        (jury / "answer.txt").write_bytes(answer_data)
        student = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd,
            preexec_fn=lambda: _limits(cpu_seconds, address_space_bytes, file_size_bytes),
            env={"PATH": CHILD_PATH, "HOME": str(cwd)})
        judge_proc = subprocess.Popen(
            [_trusted_python(), "-I", str(MIRROR / interactor), str(jury / "input.txt"), str(jury / "answer.txt")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=jury,
            preexec_fn=lambda: _limits(INTERACTOR_CPU_S),
            env={"PATH": CHILD_PATH, "HOME": str(jury)})
        state = {"student_bytes": 0, "jury_bytes": 0, "transcript_bytes": 0, "output_exceeded": False}
        transcript = [] if keep_transcript else None
        student_err, jury_err = [], []
        # 线程直接读写 fd：先 dup 出来，再关掉 Popen 上的文件对象，免得两边各关一次
        s_in, s_out, s_err = (os.dup(stream.fileno()) for stream in (student.stdin, student.stdout, student.stderr))
        j_in, j_out, j_err = (os.dup(stream.fileno()) for stream in (judge_proc.stdin, judge_proc.stdout, judge_proc.stderr))
        for stream in (student.stdin, student.stdout, student.stderr,
                       judge_proc.stdin, judge_proc.stdout, judge_proc.stderr):
            stream.close()
        threads = [
            threading.Thread(target=_pump, args=(s_out, j_in, state, "student_bytes", transcript, ">"), daemon=True),
            threading.Thread(target=_pump, args=(j_out, s_in, state, "jury_bytes", transcript, "<"), daemon=True),
            threading.Thread(target=_drain, args=(s_err, student_err), daemon=True),
            threading.Thread(target=_drain, args=(j_err, jury_err), daemon=True),
        ]
        for thread in threads:
            thread.start()
        started = time.perf_counter()
        deadline = started + wall_seconds
        student_usage = None
        killed_student = timed_out = False
        grace_until = None
        student_first = None                    # 谁先退出决定 RE 与 WA 谁优先
        while True:
            if student.returncode is None:
                pid, status, usage = os.wait4(student.pid, os.WNOHANG)
                if pid:
                    student.returncode = os.waitstatus_to_exitcode(status)
                    student_usage = usage
                    if student_first is None:
                        student_first = judge_proc.poll() is None
            if judge_proc.poll() is not None and student_first is None:
                student_first = False
            now = time.perf_counter()
            if student.returncode is not None and judge_proc.returncode is not None:
                break
            if state["output_exceeded"] and student.returncode is None:
                student.kill(); killed_student = True
            if now > deadline:
                timed_out = True
                break
            if judge_proc.returncode is not None and student.returncode is None:
                # interactor 已给出结论：给学生程序一小段时间自己退出
                grace_until = grace_until or now + 1.0
                if now > grace_until:
                    student.kill(); killed_student = True
            if student.returncode is not None and judge_proc.returncode is None:
                grace_until = grace_until or now + 5.0
                if now > grace_until:
                    judge_proc.kill()
            time.sleep(0.002)
        for proc in (student, judge_proc):
            if proc.returncode is None or timed_out:
                try:
                    proc.kill()
                except OSError:
                    pass
        if student.returncode is None:
            _, status, student_usage = os.wait4(student.pid, 0)
            student.returncode = os.waitstatus_to_exitcode(status)
        judge_proc.wait()
        for thread in threads:
            thread.join(timeout=2)
    elapsed_ms = round((time.perf_counter() - started) * 1000)
    memory_kb = int(student_usage.ru_maxrss) if student_usage else 0
    student_rc, jury_rc = student.returncode, judge_proc.returncode
    jury_message = b"".join(jury_err).decode(errors="replace").strip().splitlines()
    jury_message = jury_message[-1][:300] if jury_message else ""
    row = {"student_returncode": student_rc, "time_ms": elapsed_ms, "memory_kb": memory_kb,
           "stderr": b"".join(student_err).decode(errors="replace")[-4000:], "message": jury_message}
    if transcript is not None:
        lines = []
        for tag, chunk in transcript:
            lines.extend(f"{tag} {line}" for line in chunk.decode(errors="replace").splitlines())
        row["transcript"] = "\n".join(lines)[:SAMPLE_OUTPUT_LIMIT]
    if timed_out:
        return {**row, "outcome": "tle", "message": f"单组交互超过 {wall_seconds} 秒墙钟（程序可能在等输入却没先 flush 输出）。"}
    if student_rc == -signal.SIGXCPU or (student_rc == -signal.SIGKILL and not killed_student):
        return {**row, "outcome": "tle", "message": "单组测试超过 CPU 限制。"}
    if state["output_exceeded"]:
        return {**row, "outcome": "ole", "message": "交互中输出超过 16 MiB。"}
    if student_first and student_rc != 0 and student_rc != -signal.SIGPIPE:
        # 程序先自己崩了，interactor 只看到「提前 EOF」；报 RE 比报 WA 有用。
        # 反过来 interactor 先判了 WA、程序随后读到 EOF 才崩的，仍是 WA。
        return {**row, "outcome": "re", "message": row["stderr"] or f"退出码 {student_rc}"}
    if jury_rc == WRONG_ANSWER_EXIT:
        return {**row, "outcome": "wrong"}
    if jury_rc == 0:
        if killed_student:
            return {**row, "outcome": "tle", "message": "交互已结束，但程序没有退出。"}
        if student_rc != 0:
            return {**row, "outcome": "re", "message": row["stderr"] or f"退出码 {student_rc}"}
        return {**row, "outcome": "accepted"}
    # interactor 既没判通过也没判错：它自己崩了（学生先崩的情况上面已经按 RE 返回）
    return {**row, "outcome": "judge_error",
            "message": b"".join(jury_err).decode(errors="replace")[-2000:] or f"interactor 退出码 {jury_rc}"}


def judge(book, problem_id, language, source, collect_case_times=False):
    item = catalog_item(book, problem_id)
    return unshift_prefix_lines(item, _judge(item, book, problem_id, language, source, collect_case_times))


def _judge(item, book, problem_id, language, source, collect_case_times):
    if item is None: return {"status": "Problem Not Found", "message": "本地题库中没有这道题。"}
    cases = item.get("test_cases", [])
    if not cases: return {"status": "No Test Data", "message": "这道题暂时没有测试数据，等待补充。"}
    if not isinstance(source, str) or not source.strip(): return {"status": "Empty Source", "message": "提交代码不能为空。"}
    if len(source.encode()) > 512 * 1024: return {"status": "Source Too Large", "message": "代码不能超过 512 KiB。"}
    language = language.lower()
    source, failure = apply_code_prefix(item, language, source)
    if failure is not None:
        return failure
    with tempfile.TemporaryDirectory(prefix="cs101-judge-") as temp:
        work = Path(temp)
        command, failure = prepare_program(
            work, language, source,
            warmup_input=(MIRROR / cases[0]["input"]).read_bytes() if language in DOTNET_LANGUAGES else b"")
        if failure is not None:
            return failure
        overall_started = time.perf_counter()
        peak_memory = 0
        last_metrics = {}
        digits = re.search(r"(\d+)$", str(problem_id))
        number = int(digits.group(1)) if digits else None
        budget_seconds = total_budget_seconds(number, language, len(cases))
        cpu_seconds = case_seconds(number, language, len(cases))
        case_timings = []
        for index, case in enumerate(cases, 1):
            # 题面的限时语义是「所有测试点之和」，所以总量这一层必须真的存在；
            # 同时它也是服务器的护栏 —— 改动前整次提交是无界的（150 组 × 5s = 750 秒）。
            if time.perf_counter() - overall_started > budget_seconds:
                return {"status": "Time Limit Exceeded", "case": index,
                        "time_ms": round((time.perf_counter() - overall_started) * 1000),
                        "memory_kb": peak_memory,
                        "message": f"整次提交超过 {budget_seconds:.0f} 秒总预算"
                                   f"（{language} 倍率 ×{LANGUAGE_TIME_MULTIPLIER.get(language, 1)}）。"}
            input_data = (MIRROR / case["input"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            expected = (MIRROR / case["output"]).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
            run_address_space = DOTNET_ADDRESS_SPACE if language in DOTNET_LANGUAGES else 768 * 1024 * 1024
            run_file_size = DOTNET_FILE_SIZE if language in DOTNET_LANGUAGES else 2 * 1024 * 1024
            if item.get("interactor"):
                outcome = run_interactive(command, item["interactor"], input_data,
                                          (MIRROR / case["output"]).read_bytes(), work, cpu_seconds,
                                          run_address_space, run_file_size)
                if collect_case_times:
                    case_timings.append({"case": index, "time_ms": outcome["time_ms"],
                                         "case_limit_ms": cpu_seconds * 1000,
                                         "ratio": round(outcome["time_ms"] / (cpu_seconds * 1000), 4)})
                peak_memory = max(peak_memory, outcome["memory_kb"])
                last_metrics = {"time_ms": round((time.perf_counter() - overall_started) * 1000), "memory_kb": peak_memory}
                verdict = INTERACTIVE_VERDICTS[outcome["outcome"]]
                if verdict != "Accepted":
                    row = {"status": verdict, "case": index, **last_metrics}
                    if verdict == "Judge Error":
                        print(f"judge error: {book}/{problem_id} case {index}: {outcome['message']}", flush=True)
                        row["message"] = f"第 {index} 组的交互器出错，这不是你的问题，请联系管理员。"
                    elif outcome["message"]:
                        row["message"] = outcome["message"]
                    return row
                continue
            case_started = time.perf_counter()
            try: result = _run(command, stdin=input_data, cwd=work, timeout=cpu_seconds + 1,
                               cpu_seconds=cpu_seconds, address_space_bytes=run_address_space,
                               file_size_bytes=run_file_size)
            except subprocess.TimeoutExpired:
                return {"status": "Time Limit Exceeded", "case": index, "time_ms": round((time.perf_counter() - overall_started) * 1000),
                        "memory_kb": int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss),
                        "message": f"单组测试超过 {cpu_seconds + 1} 秒。"}
            case_elapsed_ms = round((time.perf_counter() - case_started) * 1000)
            if collect_case_times:
                case_timings.append({
                    "case": index,
                    "time_ms": case_elapsed_ms,
                    "case_limit_ms": cpu_seconds * 1000,
                    "ratio": round(case_elapsed_ms / (cpu_seconds * 1000), 4),
                })
            memory_kb = int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            peak_memory = max(peak_memory, memory_kb)
            last_metrics = {"time_ms": round((time.perf_counter() - overall_started) * 1000), "memory_kb": peak_memory}
            actual = result.stdout.decode(errors="replace")
            metrics = {"time_ms": round((time.perf_counter() - overall_started) * 1000), "memory_kb": peak_memory}
            if len(actual.encode()) > 2 * 1024 * 1024: return {"status": "Output Limit Exceeded", "case": index, **metrics}
            if result.returncode in {-signal.SIGXCPU, -signal.SIGKILL}: return {"status": "Time Limit Exceeded", "case": index, **metrics, "message": "单组测试超过 CPU 限制。"}
            if result.returncode != 0: return {"status": "Runtime Error", "case": index, **metrics, "message": result.stderr.decode(errors="replace")[-4000:]}
            checker = item.get("special_checker")
            checker_message = ""
            if item.get("checker"):
                matched, checker_message = run_checker(item["checker"], input_data, result.stdout,
                                                       (MIRROR / case["output"]).read_bytes())
                if matched is None:
                    print(f"judge error: {book}/{problem_id} case {index}: {checker_message}", flush=True)
                    return {"status": "Judge Error", "case": index, **metrics,
                            "message": f"第 {index} 组的判题器出错，这不是你的问题，请联系管理员。"}
            elif checker:
                matched = special_output_matches(checker, input_data, actual)
            else:
                matched = outputs_match(actual, expected, item.get("comparison", "tokens"))
            # 实际输出是学生自己程序打印的，不涉及泄题；只截断 UI 载荷（它会整份进 submissions.detail）。
            if not matched: return {"status": "Wrong Answer", "case": index, **metrics, "expected_tokens": len(expected.split()), "actual_tokens": len(actual.split()),
                                    **({"message": checker_message} if checker_message else {}),
                                    "actual_output": {"text": actual[:4000], "truncated": len(actual) > 4000,
                                                      "total_lines": len(actual.splitlines()), "total_chars": len(actual)}}
    accepted = {"status": "Accepted", "cases": len(cases), **last_metrics}
    if collect_case_times:
        max_case = max(case_timings, key=lambda row: row["ratio"])
        accepted["timing_audit"] = {
            "status": "passed" if max_case["ratio"] <= 0.75 else "insufficient_margin",
            "required_max_ratio": 0.75,
            "max_case": max_case,
            "cases": case_timings,
        }
    return accepted
