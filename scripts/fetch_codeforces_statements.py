#!/usr/bin/env python3
"""Fetch the original Codeforces statements behind the local Codeforces book.

codeforces.com answers this host with a Cloudflare challenge and the m1 mirror
puts every page behind a login, so the statements come from Luogu's Codeforces
remote-judge mirror instead. Its problem payload carries the untouched English
Codeforces text (`content`), the Chinese translation (`contenu`), every sample
and the official time/memory limits, which is exactly what the local pages lost
when they were built from the course Markdown.

Only the fields the page builder needs are stored, so the cache stays reviewable
next to the generated pages.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
CACHE = MIRROR / "statements"
CATALOG_PATH = MIRROR / "catalog.json"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
DELAY = 1.5


def catalog_ids():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return [item["id"] for item in catalog["problems"] if item.get("book") == "codeforces"]


def embedded_json(page):
    """Pull Luogu's page payload out of the HTML it is inlined into."""
    start = page.find('{"instance":"main"')
    if start < 0:
        raise ValueError("no page payload")
    depth, in_string, escaped = 0, False, False
    for index in range(start, len(page)):
        char = page[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(page[start:index + 1])
    raise ValueError("unterminated page payload")


def fetch(problem_id, attempts=3):
    url = f"https://www.luogu.com.cn/problem/CF{problem_id}"
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
    for attempt in range(1, attempts + 1):
        try:
            page = urllib.request.urlopen(request, timeout=40).read().decode("utf-8", "replace")
            return embedded_json(page)["data"]["problem"]
        except (urllib.error.URLError, ValueError, KeyError, TimeoutError) as error:
            if attempt == attempts:
                raise
            time.sleep(DELAY * 4 * attempt)


def record(problem_id, problem):
    english = problem.get("content") or {}
    chinese = problem.get("contenu") or {}
    if (english.get("locale") or "") != "en":
        # Only the English payload is the Codeforces original; a page whose
        # `content` fell back to another locale must not be filed as one.
        english = (problem.get("translations") or {}).get("en") or {}
    limits = problem.get("limits") or {}
    return {
        "id": problem_id,
        "name": problem.get("name", ""),
        "source_url": ((problem.get("vjudge") or {}).get("link")
                       or f"https://codeforces.com/problemset/problem/{problem_id[:-1]}/{problem_id[-1]}"),
        "mirror_url": f"https://www.luogu.com.cn/problem/CF{problem_id}",
        "fetched": time.strftime("%Y-%m-%d"),
        "time_limit_ms": (limits.get("time") or [None])[0],
        "memory_limit_kb": (limits.get("memory") or [None])[0],
        "statement": {key: english.get(key, "") for key in ("description", "formatI", "formatO", "hint", "background")},
        "translation": {key: chinese.get(key, "") for key in ("description", "formatI", "formatO", "hint", "background")}
        if (chinese.get("locale") or "") == "zh-CN" else {},
        "samples": [{"input": pair[0], "output": pair[1]} for pair in (problem.get("samples") or [])],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*", help="problem ids; default: every Codeforces catalog entry")
    parser.add_argument("--refresh", action="store_true", help="refetch ids already cached")
    args = parser.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    ids = args.ids or catalog_ids()
    failures = []
    for position, problem_id in enumerate(ids, 1):
        target = CACHE / f"{problem_id}.json"
        if target.is_file() and not args.refresh:
            continue
        try:
            data = record(problem_id, fetch(problem_id))
        except Exception as error:  # noqa: BLE001 - one bad id must not stop the sweep
            failures.append((problem_id, f"{type(error).__name__}: {error}"))
            print(f"[{position}/{len(ids)}] {problem_id} FAILED {type(error).__name__}", flush=True)
            time.sleep(DELAY)
            continue
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[{position}/{len(ids)}] {problem_id} {data['name']} "
              f"samples={len(data['samples'])} limits={data['time_limit_ms']}ms/{data['memory_limit_kb']}KB", flush=True)
        time.sleep(DELAY)
    if failures:
        print("\nfailed:", flush=True)
        for problem_id, reason in failures:
            print(f"  {problem_id}: {reason}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
