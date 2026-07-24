"""Local multi-language judge for the mirrored OpenJudge test pairs."""
import json
import os
import resource
import signal
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
MIRROR = ROOT / "data" / "openjudge"

def _limits():
    resource.setrlimit(resource.RLIMIT_CPU, (4, 4))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2 * 1024 * 1024, 2 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 * 1024, 768 * 1024 * 1024))

def _run(command, stdin=None, cwd=None, timeout=5):
    return subprocess.run(command, input=stdin, cwd=cwd, capture_output=True, timeout=timeout, preexec_fn=_limits, env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(cwd)})

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
        work = Path(temp); ext = ".py" if language in {"python", "py", "python3"} else ".c" if language == "c" else ".cpp"
        source_path = work / ("main" + ext); source_path.write_text(source, encoding="utf-8")
        if ext == ".py":
            try:
                compile(source, str(source_path), "exec")
            except (SyntaxError, ValueError) as error:
                return {"status": "Compile Error", "message": str(error)[-4000:]}
            command = ["python3", "-I", str(source_path)]
        else:
            executable = work / "main"
            compile_result = _run(["g++" if ext == ".cpp" else "gcc", "-O2", "-std=c++17" if ext == ".cpp" else "-std=c11", str(source_path), "-o", str(executable)], cwd=work, timeout=15)
            if compile_result.returncode: return {"status": "Compile Error", "message": compile_result.stderr.decode(errors="replace")[-4000:]}
            command = [str(executable)]
        for index, case in enumerate(cases, 1):
            input_data = (MIRROR / case["input"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            expected = (MIRROR / case["output"]).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
            try: result = _run(command, stdin=input_data, cwd=work)
            except subprocess.TimeoutExpired: return {"status": "Time Limit Exceeded", "case": index, "message": "单组测试超过 5 秒。"}
            actual = result.stdout.decode(errors="replace")
            if len(actual.encode()) > 2 * 1024 * 1024: return {"status": "Output Limit Exceeded", "case": index}
            if result.returncode in {-signal.SIGXCPU, -signal.SIGKILL}: return {"status": "Time Limit Exceeded", "case": index, "message": "单组测试超过 CPU 限制。"}
            if result.returncode != 0: return {"status": "Runtime Error", "case": index, "message": result.stderr.decode(errors="replace")[-4000:]}
            if actual.split() != expected.split(): return {"status": "Wrong Answer", "case": index, "expected_tokens": len(expected.split()), "actual_tokens": len(actual.split())}
    return {"status": "Accepted", "cases": len(cases)}
