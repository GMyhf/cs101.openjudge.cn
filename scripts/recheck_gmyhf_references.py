#!/usr/bin/env python3
"""逐题复判下载清单中的现有参考解，报告绑定参考代码与当前活跃输入输出的 SHA256。

用法：python3 scripts/recheck_gmyhf_references.py /tmp/gmyhf-references.json
契约扫描：python3 scripts/recheck_gmyhf_references.py --contracts /tmp/gmyhf-contracts.json
报告中的 AC 只表示现有参考解与答案一致，输入合法性仍需另行检查。
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import judge  # noqa: E402


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review(output):
    rows = json.loads((ROOT / "collab/gmyhf-download-materialize.json").read_text())["materialized"]
    catalog = json.loads((ROOT / "data/openjudge/catalog.json").read_text())["problems"]
    results = []
    for index, row in enumerate(rows, 1):
        aliases = [p for p in catalog if p.get("global_number") == row["global_number"]
                   and p.get("source", "openjudge") == "openjudge"]
        problem = next((p for p in aliases if p["book"] == "practice"), aliases[0])
        directory = ROOT / "data/openjudge/tests" / row["bucket"] / (row["local_id"] + "_made")
        refs = [("python3", directory / "samplecode.py"),
                ("cpp", directory / "samplecode.cpp"),
                ("cpp", directory / "samplecode_ac.cpp")]
        language, source = next(((lang, path) for lang, path in refs if path.is_file()), (None, None))
        result = (judge.judge(problem["book"], problem["id"], language, source.read_text(),
                              collect_case_times=True) if source else {"status": "Missing Reference"})
        result = {k: v for k, v in result.items() if k in
                  ("status", "cases", "case", "time_ms", "memory_kb", "timing_audit", "message")}
        if "timing_audit" in result:
            result["timing_audit"].pop("cases", None)
        item = judge.catalog_item(problem["book"], problem["id"])
        pairs = [{"input": case["input"], "input_sha256": digest(judge.MIRROR / case["input"]),
                  "output": case["output"], "output_sha256": digest(judge.MIRROR / case["output"])}
                 for case in item["test_cases"]]
        result.update(global_number=row["global_number"], title=row["title"],
                      book=problem["book"], problem=problem["id"],
                      reference=str(source.relative_to(ROOT)) if source else None,
                      language=language, reference_sha256=digest(source) if source else None,
                      case_snapshot_sha256=hashlib.sha256(json.dumps(pairs, sort_keys=True).encode()).hexdigest())
        results.append(result)
        output.write_text(json.dumps({"verified_at": datetime.now(timezone.utc).isoformat(),
                                      "entries": results}, ensure_ascii=False, indent=2) + "\n")
        print(index, "/", len(rows), row["global_number"], result["status"], flush=True)


def contract_driver(number):
    """先查原文；只有空行无语义的题才兼容生成器对末尾换行的限制。"""
    sys.path.insert(0, str(ROOT / "tools"))
    from full_sweep import VALID_DRIVER
    if number == 16531:
        return VALID_DRIVER
    return VALID_DRIVER.replace(
        'verdict = valid(text) if len(parameters) == 1 else valid(key, text)',
        'verdict = valid(text) if len(parameters) == 1 else valid(key, text)\n'
        '        if verdict is not True:\n'
        '            text = text.rstrip("\\n") + "\\n"\n'
        '            verdict = valid(text) if len(parameters) == 1 else valid(key, text)')


def contracts(output):
    rows = json.loads((ROOT / "collab/gmyhf-download-materialize.json").read_text())["materialized"]
    results = []
    for item in rows:
        base = ROOT / "data/openjudge/tests" / item["bucket"]
        module = base / (item["local_id"] + "_made/producecase.py")
        data = base / (item["local_id"] + "_GMyhf/data")
        row = {"global_number": item["global_number"]}
        if not module.exists() or not re.search(r"^def valid\(", module.read_text(), re.M):
            row["status"] = "missing"
        elif item["global_number"] == 31069:
            # 独立检查使用频数计算长度和离线扫描，不展开 A×B。
            from check_gmyhf_remaining import forbidden
            invalid = []
            for path in sorted(data.glob('*.in'), key=lambda p: int(p.stem)):
                try:
                    forbidden(path.read_text(encoding='utf-8'))
                except ValueError as exc:
                    invalid.append(f'{path.name}: {exc}')
            row.update(status='checked_independent', invalid=invalid)
        else:
            with tempfile.TemporaryDirectory(prefix="gmyhf-contract-acceptance-") as work:
                try:
                    result = subprocess.run([sys.executable, "-c", contract_driver(item['global_number']), str(module), str(data),
                                             item["local_id"]], cwd=work, text=True,
                                            capture_output=True, timeout=30)
                except subprocess.TimeoutExpired:
                    row["status"] = "timeout"
                else:
                    row.update(status="checked" if result.returncode == 0 else "error",
                               invalid=json.loads(result.stdout) if result.returncode == 0
                               else result.stderr[-300:])
        results.append(row)
        output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print("完成契约筛查", len(results), flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--contracts":
        contracts(Path(sys.argv[2]))
    elif len(sys.argv) == 2:
        review(Path(sys.argv[1]))
    else:
        raise SystemExit(__doc__)
