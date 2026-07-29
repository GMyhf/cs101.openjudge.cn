#!/usr/bin/env python3
"""全库横扫：把「偶尔越出流程看一眼」变成每次跑闸门都做的事。

**为什么要有它。** 每轮复核问的是「这一轮怎么样」，而缺陷的范围是「这个仓库」。
2026-07-27 收官时我临时把全部报告扫了一遍，捞出两条挂了很久的：round5 的 4140 与
round9 的 15291 —— 它们的 `self_audit.failed` 一直非空，只是当轮没处理、之后每轮的
复核又只看当轮。`tools/check_pending_rework.py` 也管不到，因为它只管被显式记进
`pending_rework` 的项，而这两条当时根本没被记下来。

所以这里扫的是**已知失败模式在全库的残留**，每一条都对应一次真实事故：

  1. 任何轮次报告里 `self_audit.failed` 非空          （4140 / 15291）
  2. 退化约束：判据措辞像「非空」且反例是空串         （round14 的 27378 / 27778）
  3. `.out` 超过判题器 `RLIMIT_FSIZE` 2MB            （00000 因此被永久排除）
  4. 浮点输出里的循环小数                             （28748：题面允许 10^-6 容差，
                                                       我们却精确比对，会误杀）

**它不发现新的失败模式**，只保证旧的不复发。发现新模式这件事，到目前为止仍然靠人
偶尔越出流程去看一眼 —— 这条我没能变成规则，也不打算假装它变成了。

用法：
    python3 tools/full_sweep.py           # 有残留则退出码 1
    python3 tools/full_sweep.py --list    # 连干净的项目也列出来
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TESTS = ROOT / "data" / "openjudge" / "tests"
FSIZE_LIMIT = 2 * 1024 * 1024          # judge.py 的 RLIMIT_FSIZE
DEGENERATE = re.compile(r"is present|nonempty|non-?empty", re.I)
FLOAT_TOKEN = re.compile(r"^-?\d+\.\d+$")
# 小数位超过这个数就当成「循环小数四舍五入」——1/6、1/3 之类都会落在这边。
TERMINATING_DECIMALS = 6

# 已经算过账的例外。**不是把检查删掉，是把结论记下来**——
# 一个缺陷被接受和被忽略，从代码上看一模一样，区别只在有没有写下来。
ACCEPTED_REPEATING = {
    4140: "方程求解：答案是方程的根，题面明写「精确到小数点后9位」——"
          "9 位有效小数是题目本身的要求，不是四舍五入凑出来的。"
          "平台对它同样按精确值判，我们与平台一致。",
}


def report_entries():
    for path in sorted(ROOT.glob("collab/t0*-round*-report.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
        if isinstance(entries, dict):
            entries = [dict(v, local_number=k) for k, v in entries.items()]
        for entry in entries or []:
            yield path.name, entry


def made_dirs():
    for path in sorted(TESTS.glob("*/*_made")):
        match = re.search(r"/0*(\d+)_made$", str(path))
        if match:
            yield int(match.group(1)), path


def check_reported_failures():
    """1. 任何轮次的 self_audit.failed 非空。"""
    bad = []
    for source, entry in report_entries():
        failed = (entry.get("self_audit") or {}).get("failed")
        if failed:
            bad.append(f"{entry.get('local_number')}（{source}）: {failed}")
    return "报告里 self_audit.failed 非空", bad


def check_degenerate_constraints():
    """2. Catch empty non-constraints and one-label-for-the-whole-round checks.

    只看措辞会误伤 —— 30932 的 `tree root is present` 反例是 `"null\\n"`，空树是那题
    合法的输入格式，真实数据保持 True、反例翻 False，这条是好的。所以两个条件都要满足。
    """
    bad, by_source = [], {}
    for source, entry in report_entries():
        labels_list = [str(c[0]).strip() for c in (entry.get("constraints") or [])]
        labels = " ".join(labels_list)
        counter = entry.get("constraint_counterexample")
        if isinstance(counter, (list, tuple)):
            counter = counter[0] if counter else ""
        counter_text = str(counter or "").strip()
        if DEGENERATE.search(labels) and not counter_text:
            bad.append(f"{entry.get('local_number')}（{source}）: {labels[:50]!r} 反例={counter_text!r}")
        by_source.setdefault(source, []).append((entry.get("local_number"), set(labels_list)))

    for source, rows in by_source.items():
        if len(rows) < 2:
            continue
        shared = set.intersection(*(labels for _number, labels in rows)) if rows else set()
        for label in sorted(shared):
            bad.append(f"{source}: {len(rows)} 题共用同一约束 {label[:80]!r}")
    return "退化约束（非空占位+空反例，或整轮共用同一判据）", bad


def check_output_size():
    """3. .out 超过判题器 2MB —— 学生的正确解法会被 Output Limit Exceeded 打掉。"""
    bad = []
    for number, made in made_dirs():
        for path in (made / "data").glob("*.out"):
            if path.stat().st_size > FSIZE_LIMIT:
                bad.append(f"{number}: {path.name} {path.stat().st_size / 1048576:.2f}MB")
                break
    return f"输出超过判题器 {FSIZE_LIMIT // 1048576}MB 上限", bad


def check_merged_judge():
    """5. T-028 的报告必须带「合并后真判过」的实测，而且是 passed。

    为什么是机械判据而不是复核时人眼看：**交叉验证只验「答案对不对」，
    验不出「对但太慢」。** 2026-07-29 的 01384 就是这么溜过去的 ——
    参考解法逐 token 复算出了全部存档输出、平台也判 Accepted，
    但在本地合并后的数据上是 Time Limit Exceeded（卡在一份 117KB 的 2008 压测文件上）。
    当轮报告写的是「20/20 Accepted」，因为那一步根本没跑。

    人已定复核改成「攒几轮一起看」，所以这条更不能留给人眼：
    **字段缺了就是红**，等同于「你没跑这一步」。
    只查 T-028 起的批次，早于这条规则的 t002/t003/t004 不追溯。
    """
    bad = []
    for source, entry in report_entries():
        if not source.startswith("t028-"):
            continue
        merged = entry.get("merged_judge") or {}
        if not merged:
            bad.append(f"{entry.get('local_number')}（{source}）: 没有 merged_judge —— 合并后真判这一步没跑")
        elif merged.get("status") != "passed":
            bad.append(f"{entry.get('local_number')}（{source}）: merged_judge="
                       f"{merged.get('status')} verdict={merged.get('verdict')}")
    return "T-028 报告缺「合并后真判」的实测或未通过", bad


def check_repeating_decimals():
    """4. 浮点输出里的循环小数。

    题面给容差（如 28748 的「绝对误差不超过 10^-6」）而判题器只有 token 精确比对时，
    像 1/6 = 0.166666667 这种值会误杀 —— 另一个同样正确、只是累加顺序不同的实现
    可能给出 0.166666666。数据这头躲开就没这问题。
    """
    bad = []
    for number, made in made_dirs():
        outs = sorted((made / "data").glob("*.out"))
        repeating = 0
        total = 0
        for path in outs[:6]:
            for token in path.read_text(errors="replace").split()[:400]:
                if not FLOAT_TOKEN.match(token):
                    continue
                total += 1
                if len(token.split(".")[1].rstrip("0")) > TERMINATING_DECIMALS:
                    repeating += 1
        if total and repeating / total > 0.2 and number not in ACCEPTED_REPEATING:
            bad.append(f"{number}: {repeating}/{total} 个浮点输出是循环小数")
    return "浮点输出里的循环小数（token 精确比对会误杀）", bad


def check_annotated_sample_outputs():
    """Guard the parser's # truncation precondition for every mirrored statement."""
    from html import unescape
    from server import SAMPLE_ANY, parse_sample_sections

    catalog_path = ROOT / "data" / "openjudge" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "标记式样例输出的首行安全前提", ["catalog.json 不可读"]
    bad = []
    marked = 0
    for item in catalog.get("problems", []):
        page = ROOT / "data" / "openjudge" / "pages" / f"{item['book']}__{item['id']}.html"
        try:
            text = page.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        match = re.search(r'<dt>样例输入</dt>\s*<dd>(.*?)</dd>\s*<dt>样例输出</dt>\s*<dd>(.*?)</dd>', text, re.S)
        if not match:
            continue
        plain = lambda chunk: unescape(re.sub(r"</?pre[^>]*>|<[^>]+>", "", chunk.strip())).strip("\n")
        raw_input, raw_output = plain(match.group(1)), plain(match.group(2))
        if not (SAMPLE_ANY.search(raw_input) or SAMPLE_ANY.search(raw_output)):
            continue
        marked += 1
        # 必须关掉截断再看：截断会把「首行就是 #」的输出削成空串，
        # 拿截断后的结果去验，这个检查永远看不见自己要防的那件事。
        sections = parse_sample_sections(raw_input + "\n" + raw_output,
                                         truncate_explanations=False)
        for index, case in enumerate(sections, 1):
            first = next((line.strip() for line in case["output"].splitlines() if line.strip()), "")
            if first.startswith("#"):
                bad.append(f"{item['book']}__{item['id']} 样例 {index}: 输出首行 {first!r}")
    return f"标记式样例输出的首行安全前提（已扫描 {marked} 题）", bad


CHECKS = (check_reported_failures, check_degenerate_constraints,
          check_output_size, check_repeating_decimals, check_annotated_sample_outputs,
          check_merged_judge)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="连干净的项目也列出来")
    opts = parser.parse_args()

    total = 0
    for check in CHECKS:
        label, bad = check()
        total += len(bad)
        if bad or opts.list:
            mark = f"**{len(bad)} 处**" if bad else "干净"
            print(f"  [{mark}] {label}")
            for line in bad[:12]:
                print(f"      {line}")
            if len(bad) > 12:
                print(f"      …另有 {len(bad) - 12} 处")
    if total:
        print(f"全库横扫：**{total} 处残留**")
        return 1
    print(f"全库横扫：{len(list(made_dirs()))} 份数据，{sum(1 for _ in report_entries())} 条报告记录，干净")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
