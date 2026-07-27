#!/usr/bin/env python3
"""把某一轮入库的参考实现，当成一次提交丢进**我们自己的判题器**，看过不过。

**为什么这条和平台复验不是一回事。** 平台复验（`t004_submit_round.py`）验的是「实现对不对」，
用的是平台自己那份数据。本站判题器验的是「**这份数据在本站可不可用**」——
用的是我们生成的数据、我们的机器、我们的限制。

两者会分开红。2026-07-27 实测：28321、18250、28405 三题的参考实现平台全是 Accepted，
在本站却 Time Limit Exceeded。原因不是判题器太严，是**我们生成的那几组太重**：
18250 第 8 组单组要 13.7 秒，而题面给这道题的总时间限制是 10000ms。

一份连它自己的参考实现都跑不过的数据，学生交上来只会看到莫名其妙的 TLE ——
那正好毁掉这个项目要给的「编写→提交→反馈错在哪组数据」这个闭环。

用法：
    python3 scripts/t004_judge_round.py 16
    python3 scripts/t004_judge_round.py 16 --only 28321,18250
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge as judge_module  # noqa: E402
from judge import judge  # noqa: E402

TESTS = ROOT / "data" / "openjudge" / "tests"
CANDIDATES = (("samplecode.py", "python"), ("samplecode.cpp", "cpp"))


def catalog_index():
    catalog = json.loads((ROOT / "data" / "openjudge" / "catalog.json").read_text(encoding="utf-8"))
    index = {}
    for item in catalog["problems"]:
        match = re.search(r"(\d+)$", item["id"])
        if match and item.get("test_cases"):
            index.setdefault(int(match.group(1)), item)
    return index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("round", help="轮次编号，例如 16")
    parser.add_argument("--only", help="只查这些题号，逗号分隔")
    opts = parser.parse_args()

    manifest = ROOT / "collab" / f"t004-round{opts.round}-manifest.json"
    if not manifest.is_file():
        raise SystemExit(f"找不到清单：{manifest}")
    only = {int(x) for x in opts.only.split(",")} if opts.only else None
    entries = json.loads(manifest.read_text(encoding="utf-8"))["entries"]
    index = catalog_index()

    results, failed, skipped = [], [], []
    for entry in entries:
        number = int(entry["local_number"])
        if only and number not in only:
            continue
        item = index.get(number)
        made = sorted(TESTS.glob(f"**/{number:05d}_made"))
        if not item or not made:
            skipped.append(number)
            continue
        for name, language in CANDIDATES:
            path = made[0] / name
            if path.is_file():
                break
        else:
            skipped.append(number)
            continue
        started = time.perf_counter()
        verdict = judge(item["book"], item["id"], language,
                        path.read_text(encoding="utf-8", errors="replace"))
        spent = time.perf_counter() - started
        row = {"local_number": number, "language": language,
               "case_seconds": judge_module.case_seconds(number),
               "status": verdict["status"], "case": verdict.get("case"),
               "wall_s": round(spent, 1)}
        results.append(row)
        if verdict["status"] != "Accepted":
            failed.append(number)
        print(f"  {number:05d} 每组{row['case_seconds']:2d}s ｜ {verdict['status']:<22}"
              f" {spent:5.1f}s" + ("" if verdict["status"] == "Accepted"
                                   else f"  ← 第{verdict.get('case','?')}组"), flush=True)

    out = ROOT / "collab" / f"t004-round{opts.round}-localjudge.json"
    out.write_text(json.dumps({"round": opts.round, "accepted": len(results) - len(failed),
                               "total": len(results), "not_accepted": failed,
                               "skipped": skipped, "results": results},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n本站判题器：Accepted {len(results) - len(failed)}/{len(results)}"
          f"；结果写入 {out.name}")
    if skipped:
        print(f"  跳过（无 catalog 条目或无参考实现）：{skipped}")
    if failed:
        print(f"**本站过不了：{failed}** —— 这几题的数据连自己的参考实现都跑不过，"
              f"学生交上来只会看到莫名其妙的 TLE。请压低那几组的规模，"
              f"或在报告里写清为什么只能这样")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
