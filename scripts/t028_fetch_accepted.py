#!/usr/bin/env python3
"""Fetch the three platform-Accepted references needed by T-028 rounds 6/7."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import oj_submit

ROOT = Path(__file__).resolve().parents[1]
SELECTIONS = {
    2791: ("49065965", "Python3"),
    1481: ("42325727", "Python3"),
    1753: ("50209622", "Python3"),
    1276: ("51703514", "Python3"),
    2818: ("46311221", "Python3"),
}


def source_from_page(page):
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S | re.I)
    sources = [html.unescape(re.sub(r"<[^>]+>", "", block)) for block in blocks]
    sources = [source for source in sources if len(source.strip()) > 100]
    if len(sources) != 1:
        raise RuntimeError(f"expected one source block, found {len(sources)}")
    return "\n".join(line.rstrip() for line in sources[0].strip().splitlines()) + "\n"


def main():
    session = oj_submit.Session().login()
    for number, (solution_id, language) in SELECTIONS.items():
        url = f"{oj_submit.HOST}/practice/solution/{solution_id}/"
        page = session._get(url)
        if "Accepted" not in page or language not in page:
            raise RuntimeError(f"{number}: selected page is not {language} Accepted")
        source = source_from_page(page)
        header = (f"# External reference: statistics page /practice/{number:05d}/\n"
                  f"# Accepted submission: {solution_id}\n"
                  f"# Source: http://cs101.openjudge.cn/practice/solution/{solution_id}/\n"
                  "# License: not declared on the submission page; no license is inferred.\n\n")
        output = ROOT / "scripts" / f"t028_platform_accepted_{number:05d}.py"
        output.write_text(header + source, encoding="utf-8")
        print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
