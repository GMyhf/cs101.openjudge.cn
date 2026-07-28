"""Local multi-language judge for the mirrored OpenJudge test pairs."""
import json
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
PROBLEM_KEYS_MTIME_NS = None
PROBLEM_KEYS_LOCK = threading.Lock()

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
        return {"status": "OK", **metrics, "stdout": stdout, "stderr": stderr}


def problem_exists(book, problem_id):
    """Return whether a requested run/submit target is in the local catalog.

    Cache only lookup keys and refresh them when catalog.json changes. This
    keeps the judge independent from server.py's catalog cache.
    """
    global PROBLEM_KEYS_CACHE, PROBLEM_KEYS_MTIME_NS
    catalog_path = MIRROR / "catalog.json"
    try:
        mtime_ns = catalog_path.stat().st_mtime_ns
    except OSError:
        return False
    with PROBLEM_KEYS_LOCK:
        if PROBLEM_KEYS_CACHE is None or mtime_ns != PROBLEM_KEYS_MTIME_NS:
            try:
                catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return False
            PROBLEM_KEYS_CACHE = frozenset(
                (p.get("book"), p.get("id"))
                for p in catalog.get("problems", [])
                if isinstance(p, dict)
            )
            PROBLEM_KEYS_MTIME_NS = mtime_ns
        return (book, problem_id) in PROBLEM_KEYS_CACHE


def judge(book, problem_id, language, source):
    catalog_path = MIRROR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    item = next((p for p in catalog["problems"] if p["book"] == book and p["id"] == problem_id), None)
    if item is None: return {"status": "Problem Not Found", "message": "本地题库中没有这道题。"}
    cases = item.get("test_cases", [])
    if not cases: return {"status": "No Test Data", "message": "这道题暂时没有测试数据，等待补充。"}
    if not isinstance(source, str) or not source.strip(): return {"status": "Empty Source", "message": "提交代码不能为空。"}
    if len(source.encode()) > 512 * 1024: return {"status": "Source Too Large", "message": "代码不能超过 512 KiB。"}
    language = language.lower()
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
            try: result = _run(command, stdin=input_data, cwd=work, timeout=cpu_seconds + 1,
                               cpu_seconds=cpu_seconds, address_space_bytes=run_address_space,
                               file_size_bytes=run_file_size)
            except subprocess.TimeoutExpired:
                return {"status": "Time Limit Exceeded", "case": index, "time_ms": round((time.perf_counter() - overall_started) * 1000),
                        "memory_kb": int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss),
                        "message": f"单组测试超过 {cpu_seconds + 1} 秒。"}
            memory_kb = int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            peak_memory = max(peak_memory, memory_kb)
            last_metrics = {"time_ms": round((time.perf_counter() - overall_started) * 1000), "memory_kb": peak_memory}
            actual = result.stdout.decode(errors="replace")
            metrics = {"time_ms": round((time.perf_counter() - overall_started) * 1000), "memory_kb": peak_memory}
            if len(actual.encode()) > 2 * 1024 * 1024: return {"status": "Output Limit Exceeded", "case": index, **metrics}
            if result.returncode in {-signal.SIGXCPU, -signal.SIGKILL}: return {"status": "Time Limit Exceeded", "case": index, **metrics, "message": "单组测试超过 CPU 限制。"}
            if result.returncode != 0: return {"status": "Runtime Error", "case": index, **metrics, "message": result.stderr.decode(errors="replace")[-4000:]}
            if actual.split() != expected.split(): return {"status": "Wrong Answer", "case": index, **metrics, "expected_tokens": len(expected.split()), "actual_tokens": len(actual.split())}
    return {"status": "Accepted", "cases": len(cases), **last_metrics}
