#!/usr/bin/env python3
"""Index OpenJudge .in/.out pairs according to global problem numbers."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
TESTS = MIRROR / "tests"
BUCKETS = {"1000-1999", "2000-2999", "3000-3682", "4000-8210", "10000-19963", "20000-29982", "30000-"}

# 这三个桶不是抓来的平台数据，是**某人 2008 年的工作目录**（人拍板 2026-07-29 排除）。
#
# 证据：三个桶合计 11,075 + 12,043 + 1,890 个文件的时间戳是 2008 年，里面混着 915 + 777
# + 202 个 `.c/.cpp/.java/.pas/.dpr/.p` 解法源码；数据文件名是 `mydata` / `pig` / `radar`
# / `g` / `e` 这种随手起的，不是平台那种 `1.in` / `2.in` 编号。
#
# 为什么必须排除，而不只是「看着不整齐」：**这些数据在判题里是真算数的** ——
# `main()` 见到 `.in`/`.out` 成对就收，同题号的多个目录还会合并。2026-07-29 实测
# 01384：参考解法在平台上是 Accepted，在本地却 Time Limit Exceeded，卡的正是
# `1000-1999/1384/pig.in`（117KB，单跑 38.4 秒，而生成的 21 组全部 ≤0.20 秒）。
# **学生在平台过、在我们这挂**，而挂的原因是一份 2008 年的私人压力测试文件。
#
# `*_made/` 不受影响。`*_GMyhf/` 只允许在非存档桶启用：管理页编辑权限能证明
# 所有权，但不能把 2008 私人工作目录变回平台数据，01384/pig.in 这条红线不绕过。
# 代价记在这里，不藏着：**498 条 catalog 记录（246 个唯一题号）因此掉到零测试数据**，
# 要靠 T-028 逐批补回来。
ARCHIVE_BUCKETS = {"1000-1999", "2000-2999", "3000-3682"}


def is_archive(bucket, directory_name):
    """2008 存档目录（已验证入库的项目数据除外）。"""
    return bucket in ARCHIVE_BUCKETS and not directory_name.endswith("_made")


def numeric(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None

def directory_numeric(value):
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None


class GlobalNumberParser(HTMLParser):
    """Read the globally unique problem number from a mirrored problem page."""

    def __init__(self):
        super().__init__()
        self.in_dt = False
        self.in_dd = False
        self.label = []
        self.value = []
        self.expect_global_number = False
        self.global_number = None

    def handle_starttag(self, tag, attrs):
        if tag == "dt":
            self.in_dt = True
            self.label = []
        elif tag == "dd" and self.expect_global_number:
            self.in_dd = True
            self.value = []

    def handle_data(self, data):
        if self.in_dt:
            self.label.append(data)
        elif self.in_dd:
            self.value.append(data)

    def handle_endtag(self, tag):
        if tag == "dt" and self.in_dt:
            self.in_dt = False
            self.expect_global_number = "".join(self.label).strip() == "全局题号"
        elif tag == "dd" and self.in_dd:
            self.in_dd = False
            value = "".join(self.value).strip()
            if value.isdigit():
                self.global_number = int(value)
            self.expect_global_number = False


def read_global_number(page):
    parser = GlobalNumberParser()
    parser.feed(page.read_text(encoding="utf-8", errors="replace"))
    if parser.global_number is None:
        raise ValueError(f"missing global problem number in {page}")
    return parser.global_number


def catalog_global_numbers(catalog):
    """Return per-entry and practice-local-ID mappings to global numbers."""
    per_entry = {}
    practice = {}
    for item in catalog["problems"]:
        key = (item["book"], item["id"])
        page = MIRROR / "pages" / f"{item['book']}__{item['id']}.html"
        global_number = read_global_number(page)
        per_entry[key] = global_number
        if item["book"] == "practice":
            local_number = numeric(item["id"])
            if local_number in practice and practice[local_number] != global_number:
                raise ValueError(f"practice ID {item['id']} maps to multiple global numbers")
            practice[local_number] = global_number
    return per_entry, practice


def test_directory_global_numbers(per_entry, practice):
    """Map total-library IDs, with an unambiguous sub-book fallback."""
    choices = {}
    for (book, problem_id), global_number in per_entry.items():
        local_number = numeric(problem_id)
        choices.setdefault(local_number, set()).add(global_number)
    result = dict(practice)
    for local_number, global_numbers in choices.items():
        if local_number not in result and len(global_numbers) == 1:
            result[local_number] = next(iter(global_numbers))
    return result


class BookStatsParser(HTMLParser):
    """Read the statistics columns already present in mirrored book pages."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell_class = None
        self.cell_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = {}
        elif tag == "td" and self.row is not None:
            self.cell_class = attrs.get("class", "")
            self.cell_text = []

    def handle_data(self, data):
        if self.cell_class is not None:
            self.cell_text.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell_class is not None:
            self.row[self.cell_class] = " ".join("".join(self.cell_text).split())
            self.cell_class = None
            self.cell_text = []
        elif tag == "tr" and self.row:
            problem_id = self.row.get("problem-id")
            if problem_id:
                self.rows.append({
                    "id": problem_id,
                    "pass_rate": self.row.get("ratio"),
                    "accepted_count": self.row.get("accepted"),
                    "attempt_count": self.row.get("submissions"),
                })
            self.row = None


def book_stats():
    stats = {}
    for page in sorted((MIRROR / "books").glob("*.html")):
        book = page.name.split("__", 1)[0]
        parser = BookStatsParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for row in parser.rows:
            stats[(book, row["id"])] = row
    return stats

def main():
    catalog_path = MIRROR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    per_entry_global, practice_global = catalog_global_numbers(catalog)
    directory_global = test_directory_global_numbers(per_entry_global, practice_global)
    made_by_global_number = {}
    gmyhf_by_global_number = {}
    legacy_by_global_number = {}
    for bucket in BUCKETS:
        root = TESTS / bucket
        if not root.is_dir(): continue
        for directory in sorted(root.iterdir()):
            if not directory.is_dir(): continue
            if is_archive(bucket, directory.name): continue
            number = directory_numeric(directory.name)
            if number is None: continue
            global_number = directory_global.get(number)
            # Most directories use IDs from `practice`. A few mirrored problems
            # currently exist only in a sub-book, so accept that suffix only when
            # it maps to exactly one global problem.
            if global_number is None: continue
            pairs = []
            test_files = list(directory.glob("*.in")) + list((directory / "data").glob("*.in"))
            output_files = list(directory.glob("*.out")) + list((directory / "data").glob("*.out"))
            inputs = {p.stem: p for p in test_files}
            outputs = {p.stem: p for p in output_files}
            for stem in sorted(inputs.keys() & outputs.keys()):
                pairs.append({"input": str(inputs[stem].relative_to(MIRROR)), "output": str(outputs[stem].relative_to(MIRROR))})
            if pairs:
                if directory.name.endswith("_GMyhf"):
                    target = gmyhf_by_global_number
                elif directory.name.endswith("_made"):
                    target = made_by_global_number
                else:
                    target = legacy_by_global_number
                target.setdefault(global_number, []).extend(pairs)

    # Priority is verified GMyhf-owned platform data, then generated data, then legacy.
    # `_GMyhf` is materialized only when the admin page grants Edit and the original
    # cases pass the recorded oracle audit. If that audit finds any problem, no
    # `_GMyhf` directory is created and `_made` remains active.
    by_global_number = dict(legacy_by_global_number)
    by_global_number.update(made_by_global_number)
    by_global_number.update(gmyhf_by_global_number)

    stats = book_stats()
    matched = 0
    for item in catalog["problems"]:
        global_number = per_entry_global[(item["book"], item["id"])]
        cases = by_global_number.get(global_number, [])
        item["global_number"] = global_number
        item["tests"] = bool(cases)
        item["test_count"] = len(cases)
        item["test_cases"] = cases
        item.update({key: value for key, value in stats.get((item["book"], item["id"]), {}).items()
                     if key != "id"})
        if cases: matched += 1
    (MIRROR / "test_index.json").write_text(json.dumps({"buckets": sorted(BUCKETS), "matched_catalog_problems": matched, "indexed_problem_numbers": len(by_global_number), "catalog": catalog}, ensure_ascii=False, indent=2), encoding="utf-8")
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"indexed {len(by_global_number)} global problems; {matched}/{len(catalog['problems'])} catalog problems have tests")

if __name__ == "__main__": main()
