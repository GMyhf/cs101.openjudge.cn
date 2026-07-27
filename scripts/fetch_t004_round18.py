#!/usr/bin/env python3
"""Fetch the existing Accepted source for T-004 round18."""
import html
import http.cookiejar
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round18-manifest.json"


def main():
    user, password = os.environ.get("OJ_USER"), os.environ.get("OJ_PASS")
    if not user or not password:
        raise SystemExit("set OJ_USER and OJ_PASS in the environment")
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    body = urllib.parse.urlencode({"email": user, "password": password}).encode()
    login = opener.open(urllib.request.Request(
        "http://cs101.openjudge.cn/api/auth/login/", data=body), timeout=60)
    if json.loads(login.read()).get("result") != "SUCCESS":
        raise SystemExit("OJ login failed")
    for entry in json.loads(MANIFEST.read_text())["entries"]:
        number = int(entry["local_number"]); accepted = entry["existing_accepted"]
        url = accepted["source_url"]
        page = opener.open(url, timeout=60).read().decode("utf-8", "replace")
        match = re.search(r'<pre class="sh_[^"]*">(.*?)</pre>', page, re.S)
        if not match:
            raise SystemExit(f"source not found for {number}")
        source = html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))
        header = (
            f"# External reference: {entry['submit_path']}statistics/\n"
            f"# Accepted submission: {accepted['solution_id']}\n"
            f"# Source: {url}\n"
            "# License: not declared on the submission page; no license is inferred.\n\n"
        )
        (ROOT / f"scripts/t004_platform_accepted_{number}.py").write_text(header + source)
        print(number, accepted["solution_id"])


if __name__ == "__main__":
    main()
