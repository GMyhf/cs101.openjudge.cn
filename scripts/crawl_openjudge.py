#!/usr/bin/env python3
"""Mirror the public CS101 problem catalog and problem pages locally."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "openjudge"
BASE = "http://cs101.openjudge.cn"
BOOKS = ["pctbook", "2025sp_routine", "25dsapre", "2024fallroutine", "2024sp_routine", "dsapre", "routine", "practice"]

def fetch(path):
    req = Request(BASE + path, headers={"User-Agent": "CS101 local catalog mirror"})
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("/"): self.hrefs.append(href.split("?", 1)[0])

def problem_links(book, html):
    prefix = f"/{book}/"
    found = set()
    for href in LinksFrom(html):
        match = re.fullmatch(re.escape(prefix) + r"([^/]+)/", href)
        if match and match.group(1) not in {"ranking", "status", "clarify"}:
            found.add(href)
    return found

def LinksFrom(html):
    parser = Links(); parser.feed(html); return parser.hrefs

def main():
    DATA.mkdir(parents=True, exist_ok=True); (DATA / "pages").mkdir(exist_ok=True); (DATA / "books").mkdir(exist_ok=True)
    catalog = []
    for book in BOOKS:
        seen = set(); page = 1
        while page <= 250:
            suffix = "" if page == 1 else f"?page={page}"
            html = fetch(f"/{book}/{suffix}")
            (DATA / "books" / f"{book}__{page}.html").write_text(html, encoding="utf-8")
            links = problem_links(book, html)
            fresh = links - seen
            if not fresh: break
            seen.update(fresh)
            for href in sorted(fresh):
                problem_id = href.strip("/").split("/")[-1]
                catalog.append({"book": book, "id": problem_id, "path": href, "tests": False})
            print(f"{book}: page {page}, +{len(fresh)}, total {len(seen)}", flush=True)
            page += 1
        if not seen: raise RuntimeError(f"No problems found for {book}")

    def save(item):
        target = DATA / "pages" / f"{item['book']}__{item['id']}.html"
        if not target.exists() or target.stat().st_size < 200:
            target.write_text(fetch(item["path"]), encoding="utf-8")
        return item

    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(save, item) for item in catalog]
        done = 0
        for future in as_completed(futures):
            future.result(); done += 1
            if done % 50 == 0: print(f"details: {done}/{len(catalog)}", flush=True)
    (DATA / "catalog.json").write_text(json.dumps({"source": BASE, "updated": time.strftime("%Y-%m-%d"), "count": len(catalog), "problems": catalog}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"mirrored {len(catalog)} problem pages into {DATA}")

if __name__ == "__main__": main()
