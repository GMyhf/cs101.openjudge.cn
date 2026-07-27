#!/usr/bin/env python3
"""Index OpenJudge .in/.out pairs according to numeric problem IDs."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
TESTS = MIRROR / "tests"
BUCKETS = {"1000-1999", "2000-2999", "3000-3682", "4000-8210", "10000-19963", "20000-29982", "30000-"}

def numeric(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None

def directory_numeric(value):
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None


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
    by_number = {}
    for bucket in BUCKETS:
        root = TESTS / bucket
        if not root.is_dir(): continue
        for directory in root.iterdir():
            if not directory.is_dir(): continue
            number = directory_numeric(directory.name)
            if number is None: continue
            pairs = []
            test_files = list(directory.glob("*.in")) + list((directory / "data").glob("*.in"))
            output_files = list(directory.glob("*.out")) + list((directory / "data").glob("*.out"))
            inputs = {p.stem: p for p in test_files}
            outputs = {p.stem: p for p in output_files}
            for stem in sorted(inputs.keys() & outputs.keys()):
                pairs.append({"input": str(inputs[stem].relative_to(MIRROR)), "output": str(outputs[stem].relative_to(MIRROR))})
            if pairs:
                by_number.setdefault(number, []).extend(pairs)

    catalog_path = MIRROR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    stats = book_stats()
    matched = 0
    for item in catalog["problems"]:
        number = numeric(item["id"])
        cases = by_number.get(number, [])
        item["tests"] = bool(cases)
        item["test_count"] = len(cases)
        item["test_cases"] = cases
        item.update({key: value for key, value in stats.get((item["book"], item["id"]), {}).items()
                     if key != "id"})
        if cases: matched += 1
    (MIRROR / "test_index.json").write_text(json.dumps({"buckets": sorted(BUCKETS), "matched_catalog_problems": matched, "indexed_problem_numbers": len(by_number), "catalog": catalog}, ensure_ascii=False, indent=2), encoding="utf-8")
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"indexed {len(by_number)} numeric problem directories; {matched}/{len(catalog['problems'])} catalog problems have tests")

if __name__ == "__main__": main()
