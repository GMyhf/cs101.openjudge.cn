#!/usr/bin/env python3
"""把私有题库（server.PRIVATE_BOOKS）里的题写进 catalog。

私有题不是抓来的，没有 OpenJudge 全局题号，`scripts/index_tests.py` 按 `source`
跳过它们、原样保留（与 Codeforces 同一口径）。所以 catalog 条目与 test_cases 由这里写：
数据在 `tests/<题库>/<题号>_made/data/`，题面在 `pages/<题库>__<题号>.html`。

    python3 tools/activate_private_problems.py private 1000000
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "data" / "openjudge"
CATALOG = MIRROR / "catalog.json"


def cases_for(book: str, problem_id: str):
    root = MIRROR / "tests" / book / f"{problem_id}_made"
    if not (root / "producecase.py").is_file() or not any(
            (root / name).is_file() for name in ("samplecode.py", "samplecode.cpp")):
        raise ValueError(f"{book}/{problem_id}: 缺 producecase.py 或 samplecode")
    if not (MIRROR / "pages" / f"{book}__{problem_id}.html").is_file():
        raise ValueError(f"{book}/{problem_id}: 缺题面 pages/{book}__{problem_id}.html")
    data = root / "data"
    count = len(list(data.glob("*.in")))
    cases = []
    for index in range(count):
        input_path, output_path = data / f"{index}.in", data / f"{index}.out"
        if not input_path.is_file() or not output_path.is_file():
            raise ValueError(f"{book}/{problem_id}: 第 {index} 组不成对")
        cases.append({"input": str(input_path.relative_to(MIRROR)),
                      "output": str(output_path.relative_to(MIRROR))})
    if not cases or len({(MIRROR / case["input"]).read_bytes() for case in cases}) != count:
        raise ValueError(f"{book}/{problem_id}: 没有数据或输入有重复")
    return root, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", help="私有题库名，如 private")
    parser.add_argument("problem", nargs="+", help="题号")
    options = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = {(item.get("book"), item.get("id")): item for item in catalog["problems"]}
    for problem_id in options.problem:
        root, cases = cases_for(options.book, problem_id)
        row = rows.get((options.book, problem_id))
        if row is None:
            row = {"book": options.book, "id": problem_id}
            catalog["problems"].append(row)
        row.update({"path": f"/{options.book}/{problem_id}/", "source": "private",
                    "tests": True, "test_count": len(cases), "test_cases": cases})
        # 与 scripts/index_tests.py 的 JUDGE_HOOK_FILES 同一口径
        for field, name in (("checker", "checker.py"), ("interactor", "interactor.py"),
                            ("code_prefix", "preset_code.py")):
            if (root / name).is_file():
                row[field] = str((root / name).relative_to(MIRROR))
            else:
                row.pop(field, None)
    catalog["count"] = len(catalog["problems"])
    # 与 index_tests.py 一致：规范 JSON 产物末尾没有换行
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"activated {len(options.problem)} problems in {options.book}")


if __name__ == "__main__":
    main()
