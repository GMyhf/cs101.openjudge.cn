"""Local multi-language judge for the mirrored OpenJudge test pairs."""
import json
import os
import resource
import shutil
import signal
import subprocess
import tempfile
import time
import re
from pathlib import Path

ROOT = Path(__file__).parent
MIRROR = ROOT / "data" / "openjudge"

# CPython 与 PyPy3 都跑 .py 源码，但是两个独立解释器：本机 PyPy 是 Python 3.9，
# 宿主 CPython 是 3.12，语法能力并不一致，所以 PyPy 的语法检查必须交给它自己做。
CPYTHON_LANGUAGES = {"python", "py", "python3"}
PYPY_LANGUAGES = {"pypy", "pypy3"}
# 只做语法检查、不执行用户代码；compile() 本身不运行被编译的源码。
SYNTAX_CHECK = "import sys;compile(open(sys.argv[1],encoding='utf-8').read(),sys.argv[1],'exec')"

# —— 按题限时（2026-07-27，人已拍板）——
#
# 原来对所有题一律 CPU 4s。但题目本身的限时差得很远：已交付的 465 题里 63 题的平台限时
# 超过 4000ms（最高 65536ms）。18250「冰阔落 I」第 8 组就卡在这上面——数据完全合规
# （题面 n,m ≤ 50000），平台给 10000ms，我们只给 4s，学生同等水平的正确解法必然 TLE。
#
# 三条边界，缺一不可：
#   · CASE_FLOOR_S —— **绝不比今天更严**。题目限时低于 4s 的一律仍按 4s 判，
#     否则今天能过的提交明天会突然挂掉（我们的机器和语言组合本来就比平台慢）。
#   · CASE_CAP_S —— 单组上限。不能让 65536ms 那种题把服务器占住。
#   · TOTAL_BUDGET_S —— **新加的**整次提交墙钟总预算。今天这一项实际上是无界的：
#     最多的一题有 150 组，150 × 5s = 750 秒。加了预算之后，放宽单组的同时，
#     整体暴露面反而从 750s 收到 60s。
CASE_FLOOR_S = 4
CASE_CAP_S = 15
TOTAL_BUDGET_S = 60
LIMITS_CACHE = {}


def problem_limits(number):
    """取该题的限时（毫秒）。取不到就退回默认，绝不因为查不到而变严。

    「总时间限制」是整次提交的总量，「单个测试点时间限制」才是每组的；判题器逐组跑，
    所以有单点限时就用单点，只有总限时就用总限时（偏宽松，宁可放过不误杀，
    总量另有 TOTAL_BUDGET_S 兜底）。
    """
    if not LIMITS_CACHE:
        path = MIRROR / "limits.json"
        try:
            LIMITS_CACHE.update(json.loads(path.read_text(encoding="utf-8"))["limits"])
        except (OSError, ValueError, KeyError):
            LIMITS_CACHE["__missing__"] = True
    row = LIMITS_CACHE.get(str(number))
    if not isinstance(row, dict):
        return None
    return row.get("case_ms") or row.get("total_ms")


def case_seconds(number):
    """该题每组的 CPU 秒数，夹在 [CASE_FLOOR_S, CASE_CAP_S] 之间。"""
    stated = problem_limits(number)
    if not stated:
        return CASE_FLOOR_S
    return max(CASE_FLOOR_S, min(CASE_CAP_S, -(-int(stated) // 1000)))


def _limits(cpu_seconds=CASE_FLOOR_S):
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2 * 1024 * 1024, 2 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 * 1024, 768 * 1024 * 1024))

# 子进程环境固定成这一份：用户代码就跑在里面，多一个目录就是多一片可执行面。
CHILD_PATH = "/usr/local/bin:/usr/bin:/bin"
LANGUAGE_VERSION_CACHE = {}

def language_version(language):
    """Return the actual toolchain label used for a submission."""
    key = str(language).lower()
    if key in LANGUAGE_VERSION_CACHE:
        return LANGUAGE_VERSION_CACHE[key]
    if key in CPYTHON_LANGUAGES:
        value = f"Python3({'.'.join(map(str, __import__('sys').version_info[:2]))})"
    elif key in PYPY_LANGUAGES:
        executable = shutil.which("pypy3")
        version_result = subprocess.run([executable or "pypy3", "--version"], capture_output=True, text=True, timeout=5)
        raw = version_result.stdout + version_result.stderr
        match = re.search(r"PyPy\s+(\d+\.\d+(?:\.\d+)?)", raw)
        value = f"PyPy3({match.group(1) if match else 'unknown'})"
    elif key == "cpp":
        raw = subprocess.run(["g++", "--version"], capture_output=True, text=True, timeout=5).stdout
        match = re.search(r"\b(\d+\.\d+)(?:\.\d+)?\b", raw)
        value = f"G++({match.group(1) if match else 'unknown'}(with c++17))"
    elif key == "c":
        raw = subprocess.run(["gcc", "--version"], capture_output=True, text=True, timeout=5).stdout
        match = re.search(r"\b(\d+\.\d+)(?:\.\d+)?\b", raw)
        value = f"GCC({match.group(1) if match else 'unknown'})"
    else:
        value = str(language)
    LANGUAGE_VERSION_CACHE[key] = value
    return value

def _run(command, stdin=None, cwd=None, timeout=5, cpu_seconds=CASE_FLOOR_S):
    # 墙钟比 CPU 多给 1 秒，和原来 (CPU 4 / 墙钟 5) 的关系保持一致。
    return subprocess.run(command, input=stdin, cwd=cwd, capture_output=True, timeout=timeout,
                          preexec_fn=lambda: _limits(cpu_seconds),
                          env={"PATH": CHILD_PATH, "HOME": str(cwd)})

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
        work = Path(temp); ext = ".py" if language in CPYTHON_LANGUAGES | PYPY_LANGUAGES else ".c" if language == "c" else ".cpp"
        source_path = work / ("main" + ext); source_path.write_text(source, encoding="utf-8")
        if ext == ".py":
            interpreter = "pypy3" if language in PYPY_LANGUAGES else "python3"
            # 必须解析成绝对路径再交给子进程：shutil.which 查的是**本进程**的 PATH，
            # 而子进程拿的是上面那份受限 PATH，两者不一致时裸名字会 FileNotFoundError
            # （judge 不接这个异常，服务端就变成 500 而不是给出判定）。
            # 走绝对路径既修掉这点，又不用往子进程 PATH 里塞目录。
            interpreter_path = shutil.which(interpreter)
            if interpreter_path is None:
                return {"status": "Language Unavailable", "message": f"本机没有安装 {interpreter}，换一种语言提交。"}
            if interpreter == "python3":
                try:
                    compile(source, str(source_path), "exec")
                except (SyntaxError, ValueError) as error:
                    return {"status": "Compile Error", "message": str(error)[-4000:]}
            else:
                # 不能用宿主 CPython 的 compile() 代劳：PyPy3 是另一个版本的解释器，
                # 语法判定必须由它自己给出，否则会把 CE 误判成 RE。
                check = _run([interpreter_path, "-I", "-c", SYNTAX_CHECK, str(source_path)], cwd=work, timeout=15)
                if check.returncode:
                    return {"status": "Compile Error", "message": check.stderr.decode(errors="replace")[-4000:]}
            command = [interpreter_path, "-I", str(source_path)]
        else:
            executable = work / "main"
            compile_result = _run(["g++" if ext == ".cpp" else "gcc", "-O2", "-std=c++17" if ext == ".cpp" else "-std=c11", str(source_path), "-o", str(executable)], cwd=work, timeout=15)
            if compile_result.returncode: return {"status": "Compile Error", "message": compile_result.stderr.decode(errors="replace")[-4000:]}
            command = [str(executable)]
        overall_started = time.perf_counter()
        peak_memory = 0
        last_metrics = {}
        digits = re.search(r"(\d+)$", str(problem_id))
        cpu_seconds = case_seconds(int(digits.group(1))) if digits else CASE_FLOOR_S
        for index, case in enumerate(cases, 1):
            # 整次提交的墙钟总预算。放宽单组的同时必须把总量收住：最多的一题有 150 组，
            # 按单组上限算就是 150 × 16s，那是把服务器交出去。
            if time.perf_counter() - overall_started > TOTAL_BUDGET_S:
                return {"status": "Time Limit Exceeded", "case": index,
                        "time_ms": round((time.perf_counter() - overall_started) * 1000),
                        "memory_kb": peak_memory,
                        "message": f"整次提交超过 {TOTAL_BUDGET_S} 秒总预算。"}
            input_data = (MIRROR / case["input"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            expected = (MIRROR / case["output"]).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
            try: result = _run(command, stdin=input_data, cwd=work, timeout=cpu_seconds + 1, cpu_seconds=cpu_seconds)
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
