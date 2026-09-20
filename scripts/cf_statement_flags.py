#!/usr/bin/env python3
"""从镜像下来的 Codeforces 结构化题面里读出**判题口径**相关的事实。

判题口径不该靠手工清单维护：题面说「答案大小写随意」，数据就得配
`case_insensitive_tokens`，否则照官方样例写 `Yes` 的正确程序会被 token 精确比对判错
（2026-09-20 实测，见 `judge.outputs_match`）。两条生成链路
（`scripts/build_codeforces_basic_data.py` 与 `tools/activate_codeforces_rebuilds.py`）
共用这里的判断，免得两边漂移。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATEMENTS = ROOT / "data" / "openjudge" / "statements"
ANY_CASE = re.compile(r"in any case|any case \(upper|upper or lower", re.I)


def statement_text(problem_id):
    path = STATEMENTS / f"{problem_id}.json"
    if not path.is_file():
        return ""
    try:
        statement = json.loads(path.read_text(encoding="utf-8"))["statement"]
    except (OSError, json.JSONDecodeError, KeyError):
        return ""
    return " ".join(((statement.get("formatO") or "")
                     + " " + (statement.get("description") or "")).split())


def allows_any_case(problem_id):
    """题面是否明写「答案大小写随意」。"""
    return bool(ANY_CASE.search(statement_text(problem_id)))
