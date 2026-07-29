#!/usr/bin/env python3
"""跨批次返工欠账的机械核对——从清单读「要求」，从产物读「现实」。

为什么要单独有这个脚本：

`common.pending_rework_status` 是在**构建时**算的，结果写进当轮报告。可是
「没做返工」恰恰意味着那些题的数据不会被重新构建——于是报告里那句结论会一直
停在上次算出来的样子。round13 就是这个形状：`self_audit.failed` 全空是真的，
20 题的自检确实全过，而 round12 留下的三条返工一组数据都没动，`failed` 管不着它。

所以这里**不读任何报告里缓存的结论**：只读 `collab/t004-round*-manifest.json`
里记着的 `pending_rework`（要求）和 `data/openjudge/tests/**` 里的 `.in`（现实），
每次现算。已经做完的项会自动变绿，做完之后留在清单里也不会误报。

用法：
    python3 tools/check_pending_rework.py          # 有未完成项则退出码 1
    python3 tools/check_pending_rework.py --list    # 连已完成的一起列出来
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import t004_common as common  # noqa: E402

TESTS = ROOT / "data" / "openjudge" / "tests"


def collect():
    """把各轮清单里带 machine_gate 的返工项汇总起来，后出现的覆盖先出现的。"""
    items = {}
    for path in sorted(ROOT.glob("collab/t0*-round*-manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for item in manifest.get("pending_rework", []):
            if item.get("machine_gate"):
                items[int(item["local_number"])] = (path.name, item)
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="连已完成的一起列出")
    opts = parser.parse_args()

    items = collect()
    if not items:
        print("跨批次返工核对：清单里没有带 machine_gate 的返工项")
        return 0

    verdict = common.pending_rework_status([v[1] for v in items.values()], TESTS)
    by_number = {int(row["local_number"]): row for row in verdict["items"]}
    failed = []
    for number, (source, _) in sorted(items.items()):
        row = by_number[number]
        bad = row["status"] != "passed"
        if bad:
            failed.append(number)
        if bad or opts.list:
            print(f"  {number} [{source}] {row['metric']}: "
                  f"实测 {row['actual_maximum']} / 目标 ≥{row['target_minimum']} "
                  f"-> {row['status']}")

    if failed:
        print(f"跨批次返工核对：**{len(failed)} 项未完成** {failed}")
        return 1
    print(f"跨批次返工核对：{len(items)} 项全部完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
