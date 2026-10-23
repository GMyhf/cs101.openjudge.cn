#!/usr/bin/env python3
"""按后台权限抓取 GMyhf 可编辑题目的原始 .in/.out 数据。

判定规则（人话版）：`/admin/problems/` 列表行里有「编辑」链接，且对应
`/admin/problems/edit/?id=N` 页面上真的渲染出 `/admin/download` 的「下载」
链接 —— 两者都满足才算「后台明确提供编辑和下载权限」，只抓这些题。

落盘位置 `data/openjudge/tests/admin_download/<全局题号>/`：
- 不在 `index_tests.py · BUCKETS` 里，不参与判题索引；
- 被 .gitignore 的 `data/openjudge/tests/**` 盖住，默认不入库；
- 与已验证入库的 `*_GMyhf/`（audit_gmyhf_data 产物）互不干扰。

口令只从 OJ_USER/OJ_PASS 读（红线 2），脚本不接收、不打印、不落盘凭据。
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import threading
import time
import urllib.parse

import oj_submit
from audit_gmyhf_data import parse_admin_page

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_ROOT = ROOT / "data" / "openjudge" / "tests" / "admin_download"
WORKERS = 4
REQUEST_PAUSE = 0.15          # 每个工作线程每次请求后的间隔，别把后台打满
DOWNLOAD_LINK = re.compile(
    r'href="(/admin/download\?problem_id=(\d+)&filename=([^"]+))"')
SAFE_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\.(?:in|out)$")

_thread = threading.local()


def session():
    """每线程一个登录会话：urllib opener 不是线程安全的。"""
    if not getattr(_thread, "session", None):
        _thread.session = oj_submit.Session().login()
    return _thread.session


def get_bytes(url):
    for attempt in range(4):
        try:
            with session()._opener.open(session()._request(url), timeout=60) as response:
                return response.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    raise AssertionError("unreachable")


def get_text(url):
    return get_bytes(url).decode("utf-8", "replace")


def editable_problems():
    """后台题目列表里 operation 列带 /admin/problems/edit/ 的行（含分页）。"""
    first = get_text(f"{oj_submit.HOST}/admin/problems/")
    entries, pages = parse_admin_page(first)
    max_page = max(pages, default=1)
    for page_number in range(2, max_page + 1):
        page = get_text(f"{oj_submit.HOST}/admin/problems/?page={page_number}")
        entries.extend(parse_admin_page(page)[0])
        print(f"admin list: page {page_number}/{max_page}, "
              f"editable so far {len(entries)}", flush=True)
        time.sleep(REQUEST_PAUSE)
    by_number = {}
    for entry in entries:
        by_number[entry["global_number"]] = entry
    return [by_number[number] for number in sorted(by_number)]


def downloadable_files(entry):
    """编辑页上渲染出的 .in/.out 下载链接；没有就是没给下载权限/没数据。"""
    html = get_text(urllib.parse.urljoin(oj_submit.HOST, entry["edit_url"]))
    time.sleep(REQUEST_PAUSE)
    files = []
    for href, problem_id, filename in DOWNLOAD_LINK.findall(html):
        if int(problem_id) != entry["global_number"]:
            continue
        if not SAFE_FILENAME.match(filename):
            continue
        files.append(filename)
    return sorted(set(files))


def download_one(number, directory, filename, force):
    target = directory / filename
    url = f"{oj_submit.HOST}/admin/download?problem_id={number}&filename={urllib.parse.quote(filename)}"
    if target.is_file() and not force:
        head = session()._opener.open(
            session()._request(url), timeout=60)
        with head:
            length = head.headers.get("Content-Length")
        time.sleep(REQUEST_PAUSE)
        if length is not None and target.stat().st_size == int(length):
            return {"filename": filename, "bytes": target.stat().st_size,
                    "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                    "skipped": True}
    payload = get_bytes(url)
    time.sleep(REQUEST_PAUSE)
    target.write_bytes(payload)
    return {"filename": filename, "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-only", action="store_true",
                        help="只枚举权限和文件清单，不下载")
    parser.add_argument("--force", action="store_true",
                        help="忽略已有文件，全部重新下载")
    args = parser.parse_args()

    session()  # 主线程先登录，口令缺失时尽早报错
    entries = editable_problems()
    print(f"editable problems: {len(entries)}", flush=True)

    plans = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(downloadable_files, entry): entry for entry in entries}
        done = 0
        for future in as_completed(futures):
            entry = futures[future]
            number = entry["global_number"]
            try:
                files = future.result()
            except Exception as exc:
                plans[number] = {"title": entry["title"], "error": str(exc)[:200]}
            else:
                if files:
                    plans[number] = {"title": entry["title"], "files": files}
                else:
                    plans[number] = {"title": entry["title"], "files": [],
                                     "note": "编辑页没有下载链接"}
            done += 1
            if done % 50 == 0:
                print(f"edit pages: {done}/{len(entries)}", flush=True)

    planned = sum(len(p.get("files", [])) for p in plans.values())
    with_data = sum(1 for p in plans.values() if p.get("files"))
    print(f"downloadable problems: {with_data}/{len(entries)}, files: {planned}",
          flush=True)

    manifest = {
        "policy": ("后台列表行含 /admin/problems/edit/ 且编辑页渲染出 "
                   "/admin/download 链接的题；只取 .in/.out"),
        "source": f"{oj_submit.HOST}/admin/problems/",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "download_root": str(DOWNLOAD_ROOT.relative_to(ROOT)),
        "editable_count": len(entries),
        "downloadable_count": with_data,
        "planned_files": planned,
        "problems": {str(number): plan for number, plan in plans.items()},
    }

    if not args.list_only:
        DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
        work = [(number, plan["files"]) for number, plan in plans.items()
                if plan.get("files")]
        downloaded = {"files": 0, "bytes": 0}
        lock = threading.Lock()

        def fetch_problem(number, files):
            directory = DOWNLOAD_ROOT / str(number)
            directory.mkdir(parents=True, exist_ok=True)
            records = [download_one(number, directory, name, args.force)
                       for name in files]
            with lock:
                downloaded["files"] += len(records)
                downloaded["bytes"] += sum(r["bytes"] for r in records)
                manifest["problems"][str(number)] = {
                    "title": plans[number]["title"], "files": records}
                if downloaded["files"] % 200 < len(records):
                    print(f"downloaded: {downloaded['files']}/{planned} files",
                          flush=True)

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = [pool.submit(fetch_problem, number, files)
                       for number, files in work]
            for future in as_completed(futures):
                future.result()
        manifest["downloaded_files"] = downloaded["files"]
        manifest["downloaded_bytes"] = downloaded["bytes"]
        print(f"downloaded {downloaded['files']} files, "
              f"{downloaded['bytes']} bytes", flush=True)

    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    (DOWNLOAD_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"manifest: {DOWNLOAD_ROOT / 'manifest.json'}", flush=True)


if __name__ == "__main__":
    main()
