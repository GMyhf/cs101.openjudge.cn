#!/usr/bin/env python3
"""Import standard Codeforces entries described by a local course Markdown file.

The source document is a solution collection, not an authoritative Codeforces
mirror. We therefore preserve its explanatory excerpt and link every entry to
the official problem page, while keeping the local catalog independent of live
upstream requests. April Fools sections are intentionally excluded: their
custom/non-algorithmic tasks do not have a dependable exact-output policy.
"""
import argparse
from html import escape
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
CATALOG_PATH = MIRROR / "catalog.json"
TEST_INDEX_PATH = MIRROR / "test_index.json"
PAGES = MIRROR / "pages"
REPORT_PATH = ROOT / "docs" / "codeforces-import.md"
MIN_EXACT_CASES = 20

URL = re.compile(
    r"https?://codeforces\.com/(?:problemset/problem/(\d+)/([A-Za-z]\d*)|"
    r"contest/(\d+)/problem/([A-Za-z]\d*))", re.I)
HEADING = re.compile(r"^(#{2,3})\s+(.*)$")
HEADING_ID = re.compile(r"(?:\[)?(\d+)\s*([A-Za-z]\d*)(?:[.\]\s:]|$)")
SAMPLE_LABEL = re.compile(r"^\s*(?:sample\s*)?(input|output)\s*:?\s*$", re.I)
FENCE = re.compile(r"^\s*```[^`]*\s*$")
INTERACTIVE = re.compile(r"\binteractive\b", re.I)
MULTIPLE_OUTPUT = re.compile(
    r"output any|any of them|multiple solutions|several solutions|not unique|multiple good", re.I)


def canonical(match):
    contest, suffix, contest_alt, suffix_alt = match.groups()
    return f"{contest or contest_alt}{(suffix or suffix_alt).upper()}"


def title_for(heading, problem_id):
    text = re.sub(r"^[#\s⭐]+", "", heading).strip().strip("[]")
    match = re.search(r"\d+\s*[A-Za-z]\d*[.\]\s:]+(.+)", text)
    title = match.group(1).strip(" []") if match else ""
    return title or problem_id


def markdown_excerpt(lines):
    """Keep the statement/editorial introduction, not submitted source code."""
    kept = []
    for line in lines:
        if line.strip().startswith("```"):
            break
        if URL.search(line):
            continue
        kept.append(line.rstrip())
    text = "\n".join(kept).strip()
    return text[:12000] or "题解文档未提供可提取的题目摘要，请查看官方原题链接。"


def fenced_block_after(lines, index):
    """Return the fenced sample directly following a Markdown input/output label."""
    for start in range(index + 1, min(index + 4, len(lines))):
        if FENCE.match(lines[start]):
            body = []
            for line in lines[start + 1:]:
                if FENCE.match(line):
                    return "\n".join(body).strip("\n")
                body.append(line.rstrip())
            return None
        if lines[start].strip():
            return None
    return None


def sample_pairs(lines):
    """Extract explicit sample input/output pairs, never solution code blocks."""
    pending, pairs = None, []
    for index, line in enumerate(lines):
        label = SAMPLE_LABEL.match(line)
        if label is None:
            continue
        block = fenced_block_after(lines, index)
        if block is None:
            continue
        if label.group(1).lower() == "input":
            pending = block
        elif pending is not None:
            pairs.append({"input": pending, "output": block})
            pending = None
    return pairs


def parse_markdown(source):
    lines = source.read_text(encoding="utf-8").splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2)))

    sections = []
    for pos, (start, level, heading) in enumerate(headings):
        end = next((next_start for next_start, next_level, _ in headings[pos + 1:]
                    if next_level <= level), len(lines))
        official = next((match for line in lines[start:end] for match in URL.finditer(line)), None)
        if official is None:
            continue
        group = next((text for group_start, group_level, text in reversed(headings[:pos + 1])
                      if group_level == 2 and group_start <= start), "")
        problem_id = canonical(official)
        heading_match = HEADING_ID.search(heading)
        score = 2 if heading_match and f"{heading_match.group(1)}{heading_match.group(2).upper()}" == problem_id else 1
        sections.append({
            "id": problem_id,
            "url": f"https://codeforces.com/problemset/problem/{official.group(1) or official.group(3)}/{(official.group(2) or official.group(4)).upper()}",
            "title": title_for(heading, problem_id),
            "excerpt": markdown_excerpt(lines[start + 1:end]),
            "line": start + 1,
            "section": group,
            "score": score,
            "samples": sample_pairs(lines[start:end]),
            "interactive": bool(INTERACTIVE.search("\n".join(lines[start:end]))),
            "multiple_output": bool(MULTIPLE_OUTPUT.search("\n".join(lines[start:end]))),
        })

    selected, excluded = {}, {}
    for item in sections:
        target = excluded if "april fools" in item["section"].lower() else selected
        prior = target.get(item["id"])
        if prior is None or item["score"] >= prior["score"]:
            target[item["id"]] = item
    return selected, excluded


def page_html(item):
    return """<!doctype html>
<html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><title>{id}: {title}</title></head>
<body><div id=\"pageTitle\"><h2>{id}: {title}</h2></div>
<dl class=\"problem-params\"><dt>来源</dt><dd><a href=\"{url}\" rel=\"noopener\">Codeforces {id}</a></dd>
<dt>本地状态</dt><dd>题解摘要已导入；判题数据请按题目另行补充。</dd></dl>
<dl class=\"problem-content\"><dt>题解摘要</dt><dd><pre>{excerpt}</pre></dd>
<dt>原题</dt><dd><p>完整题面、限制与样例请查看 <a href=\"{url}\" rel=\"noopener\">Codeforces 原题</a>。</p></dd></dl>
</body></html>
""".format(id=escape(item["id"]), title=escape(item["title"]), url=escape(item["url"], quote=True),
           excerpt=escape(item["excerpt"]))


def report(source, imported, excluded, data_status):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    lines = [
        "# Codeforces 题解导入记录", "",
        f"- 导入源：`{source}`", f"- 导入源 SHA-256：`{digest}`",
        f"- 标准题：{len(imported)} 道；其中已有条目保留、缺失条目补入 Codeforces 题库。",
        "- 判题数据：仅已有数据的题目可提交判题；其余条目展示题解摘要和官方原题链接。", "",
        "## 测试数据状态", "",
        f"每题至少 {MIN_EXACT_CASES} 组互异、已验证的数据才会接入 token 精确判题。原文",
        "样例会保留，但不会因数量不足而被当作正式判题数据。交互、多解输出和无样例题",
        "同样保留为待补完整数据。", "",
        "| 状态 | 数量 |", "| --- | ---: |",
    ]
    for status, count in sorted((name, sum(value == name for value in data_status.values()))
                                for name in set(data_status.values())):
        lines.append(f"| {status} | {count} |")
    lines.extend([
        "", "## 未接入精确判题数据", "",
        "| 题目 | 状态 | 官方链接 |", "| --- | --- | --- |",
    ])
    for problem_id, status in sorted(data_status.items(), key=lambda pair: (int(re.match(r"\d+", pair[0]).group()), pair[0])):
        if status == "exact_tests":
            continue
        lines.append(f"| {problem_id} | {status} | {imported[problem_id]['url']} |")
    lines.extend([
        "", "## 未导入题目", "",
        "以下题目位于题解文档的 April Fools 专题。它们包含非标准或娱乐性判题机制，",
        "在没有逐题 special judge 策略前不进入本站的精确输出判题库。", "",
        "| 题目 | 文档行号 | 专题 | 官方链接 |", "| --- | ---: | --- | --- |",
    ])
    for item in sorted(excluded.values(), key=lambda row: (int(re.match(r"\d+", row["id"]).group()), row["id"])):
        lines.append(f"| {item['id']} | {item['line']} | {item['section']} | {item['url']} |")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="2020fall_Codeforces_problems.md path")
    args = parser.parse_args()
    imported, excluded = parse_markdown(args.source)
    if not imported:
        raise SystemExit("No standard Codeforces problem links found")

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    problems = catalog["problems"]
    existing = {(item.get("book"), item.get("id")): item for item in problems}
    added = 0
    data_status = {}
    PAGES.mkdir(parents=True, exist_ok=True)
    for problem_id, item in sorted(imported.items(), key=lambda pair: (int(re.match(r"\d+", pair[0]).group()), pair[0])):
        key = ("codeforces", problem_id)
        record = existing.get(key)
        if record is None:
            record = {"book": "codeforces", "id": problem_id,
                      "path": f"/codeforces/{problem_id}/", "source": "codeforces",
                      "source_url": item["url"], "tests": False, "test_count": 0,
                      "test_cases": []}
            problems.append(record)
            added += 1
        else:
            record.setdefault("source", "codeforces")
            record.setdefault("source_url", item["url"])
        if problem_id != "4A":
            if item["interactive"]:
                data_status[problem_id] = "interactive_requires_judge"
                record.update({"tests": False, "test_count": 0, "test_cases": [],
                               "data_status": "interactive_requires_judge"})
            elif item["multiple_output"]:
                data_status[problem_id] = "multiple_output_requires_special_judge"
                record.update({"tests": False, "test_count": 0, "test_cases": [],
                               "data_status": "multiple_output_requires_special_judge"})
            elif item["samples"]:
                cases = []
                data_dir = MIRROR / "tests" / "codeforces" / problem_id / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                for index, sample in enumerate(item["samples"]):
                    input_path = data_dir / f"{index}.in"
                    output_path = data_dir / f"{index}.out"
                    input_path.write_text(sample["input"] + "\n", encoding="utf-8")
                    output_path.write_text(sample["output"] + "\n", encoding="utf-8")
                    cases.append({"input": str(input_path.relative_to(MIRROR)),
                                  "output": str(output_path.relative_to(MIRROR))})
                if len(cases) >= MIN_EXACT_CASES:
                    record.update({"tests": True, "test_count": len(cases), "test_cases": cases,
                                   "sample_count": len(cases), "data_status": "exact_tests"})
                    data_status[problem_id] = "exact_tests"
                else:
                    record.update({"tests": False, "test_count": 0, "test_cases": [],
                                   "sample_count": len(cases),
                                   "data_status": "insufficient_sample_cases"})
                    data_status[problem_id] = "insufficient_sample_cases"
            else:
                data_status[problem_id] = "no_extractable_sample"
                record["data_status"] = "no_extractable_sample"
        page = PAGES / f"codeforces__{problem_id}.html"
        if problem_id != "4A":
            page.write_text(page_html(item), encoding="utf-8")

    catalog["count"] = len(problems)
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report(args.source, imported, excluded, data_status)
    test_index = json.loads(TEST_INDEX_PATH.read_text(encoding="utf-8"))
    test_index["catalog"] = catalog
    test_index["matched_catalog_problems"] = sum(bool(row.get("test_cases")) for row in problems)
    TEST_INDEX_PATH.write_text(json.dumps(test_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {name: sum(value == name for value in data_status.values()) for name in set(data_status.values())}
    print(f"standard={len(imported)} added={added} excluded={len(excluded)} total={len(problems)} data={counts}")


if __name__ == "__main__":
    main()
