#!/usr/bin/env python3
"""从镜像题面里抽出每题的时间/内存限制，写成 data/openjudge/limits.json。

判题器原来对所有题一律 CPU 4s。但题目本身的限时差得很远：已交付的 465 题里有 63 题
的平台限时超过 4000ms（最高 65536ms）。18250「冰阔落 I」第 8 组就卡在这上面——数据完全
合规（题面 n,m ≤ 50000），平台给 10000ms，而我们只给 4s，于是学生同等水平的正确解法
在本站必然 TLE。

**两种限时要分清**：OpenJudge 页面上的「总时间限制」是整次提交的总量，
「单个测试点时间限制」才是每组的。有 203 道题两者都给了（如 30313 是 10000/1000），
其余只给总量。我们的判题器是逐组跑的，所以：
  · 有单点限时 -> 用单点
  · 只有总限时 -> 用总限时（偏宽松，宁可放过也不误杀；总量另有预算兜底）
"""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "data" / "openjudge"


def main():
    limits, seen = {}, Counter()
    for path in sorted((MIRROR / "pages").glob("*.html")):
        match = re.search(r"__[A-Z]?(\d+)\.html$", path.name)
        if not match:
            continue
        number = int(match.group(1))
        text = html.unescape(re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8", errors="replace")))
        total = re.search(r"总时间限制\s*:?\s*(\d+)\s*ms", text)
        per_case = re.search(r"单个测试点时间限制\s*:?\s*(\d+)\s*ms", text)
        memory = re.search(r"内存限制\s*:?\s*(\d+)\s*kB", text)
        if not (total or per_case):
            continue
        row = {
            "total_ms": int(total.group(1)) if total else None,
            "case_ms": int(per_case.group(1)) if per_case else None,
            "memory_kb": int(memory.group(1)) if memory else None,
        }
        # 同一题号可能有多份题面（不同题库），取最宽松的一份，避免误杀。
        old = limits.get(number)
        if old is None or (row["case_ms"] or row["total_ms"] or 0) > (old["case_ms"] or old["total_ms"] or 0):
            limits[number] = row
        seen[bool(per_case)] += 1

    out = {"source": "data/openjudge/pages/*.html", "count": len(limits),
           "with_case_limit": seen[True], "total_only": seen[False],
           "limits": {str(k): v for k, v in sorted(limits.items())}}
    (MIRROR / "limits.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
    print(f"抽出 {len(limits)} 题的限制；其中 {seen[True]} 题给了单个测试点限时")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
