#!/usr/bin/env python3
"""把「题面对输入的原话」和「数据的实际极值」并排记进 `collab/input-domains.json`。

**为什么是记账而不是判据。** 数据越不越界，机械判据只在「约束能绑到输入里的某个位置」
时可靠（那部分已经写成 `tests/test_input_constraints.py` 的逐题契约）。剩下两类判不了：
题面压根没写上界、约束写在「提示」或「数据范围与约定」段。对这两类硬上判据只会制造噪音 ——
T-042 留下的「数据里的整数超过题面提到的所有数值」那条，2026-09-20 重跑一遍
**143 个候选里 0 个真缺陷**。

所以这里做的是 `tools/full_sweep.py` 第 10 条的全库版：把两半钉在同一条记录里，各自可验 ——
引文必须在题面里**逐字**出现（防转述、防凭印象），极值必须能从 `data/` 重算（防写个好看的数字）。
矛盾就藏不住了，而且**数据一旦重建，极值变化会连同题面原话一起出现在 diff 里**。

用法：
    python3 scripts/build_input_domains.py          # 重建记账（逐字节可复现）
    python3 scripts/build_input_domains.py --check  # 只比对，不写盘
"""
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from full_sweep import QUOTE_BOUND, generated_extremes  # noqa: E402

MIRROR = ROOT / "data" / "openjudge"
LEDGER = ROOT / "collab" / "input-domains.json"
QUOTE_LIMIT = 300          # 引文截断长度；截断后仍是题面的逐字前缀
BOUND_NUMBER = re.compile(r"(?<![\d.])(\d[\d,]*)(?![\d])")


def statement_text(book, problem_id):
    """镜像题面的纯文本。与 `full_sweep.statement_text` 同一口径（裸 `<` 先转义）。"""
    page = MIRROR / "pages" / f"{book}__{problem_id}.html"
    if not page.is_file():
        return ""
    raw = page.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<(?![/a-zA-Z!])", "&lt;", raw)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())


def codeforces_text(problem_id):
    path = MIRROR / "statements" / f"{problem_id}.json"
    if not path.is_file():
        return ""
    statement = json.loads(path.read_text(encoding="utf-8"))["statement"]
    return " ".join(statement.get("formatI", "").split())


def input_section(text):
    """题面的「输入」段：从「输入」到「输出」之间，取前 QUOTE_LIMIT 个字符。"""
    start = -1
    for head in ("输入", "Input"):
        start = text.find(head)
        if start >= 0:
            break
    if start < 0:
        return ""
    stop = len(text)
    for tail in ("输出", "Output", "样例输入"):
        found = text.find(tail, start + 2)
        if found > 0:
            stop = min(stop, found)
    return text[start:stop].strip()[:QUOTE_LIMIT].strip()


def data_digest(directory):
    """这份数据的指纹：按题号排序，把每组输入的字节喂进 sha256。

    闸门核指纹而不是重算极值 —— 重算要把 260MB 的输入逐 token 解析一遍，
    `full_sweep` 会从 20 秒涨到 2 分钟。指纹对得上，就说明极值是从**这些字节**量出来的。
    """
    digest = hashlib.sha256()
    cases = sorted((directory / "data").glob("*.in"),
                   key=lambda item: (len(item.stem), item.stem))
    for path in cases:
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return len(cases), digest.hexdigest()


def active_dirs():
    """catalog 实际引用到的数据目录 → 用哪条 catalog 记录的题面。"""
    catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
    seen = {}
    for problem in catalog.get("problems", []):
        for case in problem.get("test_cases") or []:
            parts = str(case.get("input", "")).split("/")
            if len(parts) < 3:
                continue
            directory = "/".join(parts[:3])
            seen.setdefault(directory, (problem["book"], problem["id"]))
    return dict(sorted(seen.items()))


def quote_bounds(quote):
    """引文里出现的数值（含千分位），用来和实际极值并排摆着看。"""
    values = []
    for match in BOUND_NUMBER.finditer(quote):
        raw = match.group(1).replace(",", "")
        if raw.isdigit() and len(raw) <= 18:
            values.append(int(raw))
    return max(values) if values else None


def build():
    entries = {}
    for directory, (book, problem_id) in active_dirs().items():
        if book == "codeforces":
            source, text = "codeforces_statement", codeforces_text(problem_id)
            quote = " ".join(text.split())[:QUOTE_LIMIT].strip()
        else:
            source, text = "mirror_page", statement_text(book, problem_id)
            quote = input_section(text)
        extremes = generated_extremes(MIRROR / directory)
        case_count, digest = data_digest(MIRROR / directory)
        entries[directory] = {
            "book": book,
            "id": problem_id,
            "source": source,
            "statement_quote": quote,
            "quote_has_bound": bool(QUOTE_BOUND.search(quote)),
            "quote_max_number": quote_bounds(quote),
            "generated_extremes": extremes,
            "case_count": case_count,
            "data_digest": digest,
        }
    return {
        "note": "题面对输入的原话（逐字）与数据实际极值并排记账。由 "
                "scripts/build_input_domains.py 生成，tools/full_sweep.py 第 15 条盯着。"
                "引文没有数值范围（quote_has_bound=false）不是缺陷，是「这段题面本来就没写上界」，"
                "记下来是为了让它可见。",
        "updated": "2026-09-20",
        "count": len(entries),
        "without_bound": sum(1 for row in entries.values() if not row["quote_has_bound"]),
        "entries": entries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只比对，不写盘")
    options = parser.parse_args()
    ledger = build()
    text = json.dumps(ledger, ensure_ascii=False, indent=2) + "\n"
    if options.check:
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.is_file() else ""
        if current != text:
            print("collab/input-domains.json 与重建结果不一致，跑一次不带 --check 的构建")
            return 1
        print(f"input-domains 记账一致：{ledger['count']} 条")
        return 0
    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {LEDGER.relative_to(ROOT)}: {ledger['count']} 条，"
          f"其中引文没有数值范围的 {ledger['without_bound']} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
