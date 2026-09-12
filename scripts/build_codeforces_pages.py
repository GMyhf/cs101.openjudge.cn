#!/usr/bin/env python3
"""Rebuild the Codeforces problem pages from the fetched official statements.

`scripts/import_codeforces_markdown.py` could only dump the course Markdown into
a <pre> block: the statement stayed unrendered, it was cut at the first fence
(so every page stopped mid-sentence at "Examples input"), and the samples and
the official limits never made it onto the page at all. This builder replaces
that excerpt with the real statement, in the same shape as the hand-checked 4A
page, which `server.py` already knows how to read:

  * `<div id="pageTitle">` gives `catalog_title()` the heading,
  * `<dl class="problem-params">` carries source link and limits,
  * `<dl class="problem-content">` holds the statement, and its
    `样例输入` / `样例输出` pair is what `sample_io()` parses for 运行样例.

Codeforces writes its statements in LaTeX, so the inline math is converted to
Unicode and <sub>/<sup> rather than shipped as raw `$...$`; the site serves
plain mirrored HTML with no math renderer.
"""
import argparse
from html import escape, unescape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
CACHE = MIRROR / "statements"
PAGES = MIRROR / "pages"
REPORT_PATH = ROOT / "docs" / "codeforces-statements.md"

SYMBOLS = {
    r"\\times": "×", r"\\cdot": "·", r"\\ldots": "…", r"\\dots": "…", r"\\cdots": "…",
    r"\\vdots": "⋮", r"\\leq": "≤", r"\\le": "≤", r"\\geq": "≥", r"\\ge": "≥",
    r"\\neq": "≠", r"\\ne": "≠", r"\\approx": "≈", r"\\equiv": "≡", r"\\sim": "∼",
    r"\\pm": "±", r"\\mp": "∓", r"\\infty": "∞", r"\\to": "→", r"\\rightarrow": "→",
    r"\\leftarrow": "←", r"\\Rightarrow": "⇒", r"\\leftrightarrow": "↔",
    r"\\oplus": "⊕", r"\\otimes": "⊗", r"\\wedge": "∧", r"\\vee": "∨", r"\\lnot": "¬",
    r"\\cap": "∩", r"\\cup": "∪", r"\\subseteq": "⊆", r"\\subset": "⊂",
    r"\\supseteq": "⊇", r"\\in": "∈", r"\\notin": "∉", r"\\emptyset": "∅",
    r"\\forall": "∀", r"\\exists": "∃", r"\\sum": "∑", r"\\prod": "∏",
    r"\\lfloor": "⌊", r"\\rfloor": "⌋", r"\\lceil": "⌈", r"\\rceil": "⌉",
    r"\\langle": "⟨", r"\\rangle": "⟩", r"\\sqrt": "√", r"\\angle": "∠",
    r"\\alpha": "α", r"\\beta": "β", r"\\gamma": "γ", r"\\delta": "δ",
    r"\\epsilon": "ε", r"\\varepsilon": "ε", r"\\zeta": "ζ", r"\\eta": "η",
    r"\\theta": "θ", r"\\lambda": "λ", r"\\mu": "μ", r"\\nu": "ν", r"\\xi": "ξ",
    r"\\pi": "π", r"\\rho": "ρ", r"\\sigma": "σ", r"\\tau": "τ", r"\\phi": "φ",
    r"\\varphi": "φ", r"\\chi": "χ", r"\\psi": "ψ", r"\\omega": "ω",
    r"\\Delta": "Δ", r"\\Gamma": "Γ", r"\\Sigma": "Σ", r"\\Omega": "Ω", r"\\Phi": "Φ",
    r"\\bmod": " mod ", r"\\mod": " mod ", r"\\gcd": "gcd", r"\\lcm": "lcm",
    r"\\lt": "<", r"\\gt": ">", r"\\not\\equiv": "≢", r"\\not\\in": "∉", r"\\not=": "≠",
    r"\\dagger": "†", r"\\ddagger": "‡", r"\\ast": "∗", r"\\star": "⋆", r"\\circ": "∘",
    r"\\parallel": "∥", r"\\perp": "⊥", r"\\setminus": "\\", r"\\mid": "|",
    r"\\lim": "lim", r"\\binom": "C", r"\\overline": "", r"\\underline": "",
    r"\\min": "min", r"\\max": "max", r"\\log": "log", r"\\ln": "ln", r"\\bigl": "",
    r"\\bigr": "", r"\\Big": "", r"\\big": "", r"\\displaystyle": "", r"\\limits": "",
    r"\\quad": " ", r"\\qquad": "  ", r"\\,": " ", r"\;": " ", r"\\:": " ", r"\\!": "",
    r"\\left": "", r"\\right": "", r"\\colon": ":", r"\\dotsc": "…", r"\\dotsb": "…",
}
WRAPPERS = ("text", "textit", "textbf", "texttt", "textsf", "textrm", "mathrm", "mathit",
            "mathbf", "mathtt", "mathsf", "mathcal", "mathbb", "boldsymbol", "operatorname\\*?",
            "overline", "underline", "rm", "it", "bf", "tt")


def strip_braces(text):
    """Unwrap `{...}` groups whose braces only exist to bind a LaTeX argument."""
    out, depth = [], 0
    for char in text:
        if char == "{":
            depth += 1
        elif char == "}":
            depth = max(depth - 1, 0)
        else:
            out.append(char)
    return "".join(out)


def balanced_group(text, start):
    """Return (content, end) for the `{...}` group that starts at `text[start]`."""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
    return text[start + 1:], len(text)


def render_matrix(body):
    """Render `\\matrix{a & b \\cr c & d}` as rows instead of leaking braces."""
    while True:
        match = re.search(r"\\matrix\s*\{", body)
        if match is None:
            return body
        inner, end = balanced_group(body, match.end() - 1)
        rows = [" ".join(cell.strip() for cell in row.split("&"))
                for row in re.split(r"\\\\|\\cr", inner) if row.strip()]
        body = body[:match.start()] + " / ".join(rows) + body[end:]


def render_math(body):
    """Turn one `$...$` span into HTML: Unicode symbols plus <sub>/<sup>."""
    body = re.sub(r"\\not\s*\\equiv", "≢", body)
    body = re.sub(r"\\not\s*\\in", "∉", body)
    body = re.sub(r"\\not\s*\\subset(eq)?", "⊄", body)
    body = re.sub(r"\\not\s*=", "≠", body)
    body = re.sub(r"\\pmod\s*\{([^{}]*)\}|\\pmod\s+(\S+)",
                  lambda match: f" (mod {match.group(1) or match.group(2)})", body)
    body = re.sub(r"\\textcolor\s*\{[^{}]*\}", "", body)
    body = re.sub(r"\\color\s*\{[^{}]*\}", "", body)
    body = re.sub(r"\\pmod\s*\{([^{}]*)\}", r" (mod \1)", body)
    while True:
        match = re.search(r"\\x(right|left)arrow\s*\{", body)
        if match is None:
            break
        label, end = balanced_group(body, match.end() - 1)
        arrow = "→" if match.group(1) == "right" else "←"
        body = f"{body[:match.start()]}<SUP>{label}</SUP>{arrow}{body[end:]}"
    body = render_matrix(body)
    for wrapper in WRAPPERS:
        pattern = re.compile(r"\\" + wrapper + r"\s*\{")
        while True:
            match = pattern.search(body)
            if match is None:
                break
            inner, end = balanced_group(body, match.end() - 1)
            body = body[:match.start()] + inner + body[end:]
    while True:
        match = re.search(r"\\d?frac\s*\{", body)
        if match is None:
            break
        numerator, end = balanced_group(body, match.end() - 1)
        denominator, end = balanced_group(body, end) if end < len(body) and body[end] == "{" else ("", end)
        wrap = lambda part: part if re.fullmatch(r"[\w.^_]*", part.strip()) else f"({part.strip()})"
        body = f"{body[:match.start()]}{wrap(numerator)}/{wrap(denominator)}{body[end:]}"
    body = body.replace(r"\{", "\x01").replace(r"\}", "\x02")
    for command, symbol in SYMBOLS.items():
        # A plain replacement string would read "\\" in `\setminus` as a template escape.
        body = re.sub(command + r"(?![A-Za-z])", lambda match, text=symbol: text, body)
    body = body.replace("<=", "≤").replace(">=", "≥").replace("!=", "≠")
    body = escape(body, quote=False)

    def script(match):
        tag = "sub" if match.group(1) == "_" else "sup"
        raw = match.group(2)
        return f"<{tag}>{strip_braces(raw)}</{tag}>"

    body = re.sub(r"([_^])(\{[^{}]*\}|[A-Za-z0-9+\-]|\\?\S)", script, body)
    body = strip_braces(body)
    body = body.replace("\x01", "{").replace("\x02", "}")
    body = body.replace("&lt;SUP&gt;", "<sup>").replace("&lt;/SUP&gt;", "</sup>")
    body = re.sub(r"\s+", " ", body).strip()
    return f"<em>{body}</em>" if body else ""


def inline(text):
    """Render one paragraph of Codeforces Markdown to HTML."""
    pieces, index = [], 0
    pattern = re.compile(r"\$(.+?)\$|!\[(.*?)\]\((\S+?)\)|\[(.*?)\]\((\S+?)\)|`([^`]+)`"
                         r"|\*\*(.+?)\*\*|(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", re.S)
    for match in pattern.finditer(text):
        pieces.append(plain(text[index:match.start()]))
        index = match.end()
        if match.group(1) is not None:
            pieces.append(render_math(match.group(1)))
        elif match.group(3) is not None:
            pieces.append(f'<img src="{escape(match.group(3), quote=True)}" '
                          f'alt="{escape(match.group(2) or "illustration", quote=True)}">')
        elif match.group(5) is not None:
            pieces.append(f'<a href="{escape(match.group(5), quote=True)}" rel="noopener">'
                          f'{plain(match.group(4))}</a>')
        elif match.group(6) is not None:
            pieces.append(f"<code>{escape(match.group(6), quote=False)}</code>")
        elif match.group(7) is not None:
            pieces.append(f"<strong>{plain(match.group(7))}</strong>")
        else:
            pieces.append(f"<em>{plain(match.group(8))}</em>")
    pieces.append(plain(text[index:]))
    rendered = "".join(pieces).strip()
    rendered = re.sub(r"(?<=[(\[]) +(?=<em>)", "", rendered)
    rendered = re.sub(r"(?<=</em>) +(?=[)\].,;:?!])", "", rendered)
    return rendered


def plain(text):
    return escape(re.sub(r"\\([\\`*_{}\[\]()#+\-.!<>|~])", r"\1", text), quote=False)


LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\\?[.)])\s+")


def normalise(text):
    """Undo the wrapping the mirror leaves on Codeforces' own Markdown.

    Codeforces delimits inline math with `$$$`; the mirror rewrites most of it
    to `$ ... $` but not all (2131C keeps 52 spans). A few statements also carry
    HTML fragments and escaped entities where the conversion gave up: `<br>` in
    474A, `</p><p>` in 1881C, `&lt;` in the four old comparison-heavy ones.
    """
    text = unescape(text.replace("\r\n", "\n").replace("\r", "\n"))
    # 474A's keyboard layout arrives as one code span whose rows are <br>: keep
    # the rows, because "which key sits left of which" is the whole problem.
    text = re.sub(r"`([^`]*?</?br\s*/?>[^`]*?)`",
                  lambda match: "\n\n```\n"
                  + "\n".join(line for line in re.sub(r"</?br\s*/?>", "\n", match.group(1), flags=re.I).split("\n")
                               if line.strip())
                  + "\n```\n\n", text, flags=re.I | re.S)
    text = re.sub(r"</?p\s*/?>|</?br\s*/?>", "\n\n", text, flags=re.I)
    text = re.sub(r"\$\$+", "$", text)
    if "\\matrix" in text:
        text = render_matrix(text)
        for wrapper in WRAPPERS:
            text = re.sub(r"\\" + wrapper + r"\s*\{([^{}]*)\}", r"\1", text)
    return text


def render_blocks(text):
    """Render a statement field: paragraphs, lists and fenced/indented code."""
    text = normalise(text).strip("\n")
    if not text.strip():
        return ""
    html, lines, index = [], text.split("\n"), 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.lstrip().startswith("```"):
            body, index = [], index + 1
            while index < len(lines) and not lines[index].lstrip().startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1
            html.append("<pre>" + escape("\n".join(body), quote=False) + "</pre>")
            continue
        if LIST_ITEM.match(line):
            ordered = bool(re.match(r"^\s*\d+\\?[.)]\s+", line))
            items = []
            while index < len(lines) and (LIST_ITEM.match(lines[index]) or
                                          (lines[index].strip() and items and lines[index].startswith((" ", "\t")))):
                if LIST_ITEM.match(lines[index]):
                    items.append(LIST_ITEM.sub("", lines[index]).strip())
                else:
                    items[-1] += " " + lines[index].strip()
                index += 1
                while index < len(lines) and not lines[index].strip() and index + 1 < len(lines) \
                        and LIST_ITEM.match(lines[index + 1]):
                    index += 1
            tag = "ol" if ordered else "ul"
            html.append(f"<{tag}>" + "".join(f"<li>{inline(item)}</li>" for item in items) + f"</{tag}>")
            continue
        paragraph = []
        while index < len(lines) and lines[index].strip() and not LIST_ITEM.match(lines[index]) \
                and not lines[index].lstrip().startswith("```"):
            paragraph.append(lines[index].strip())
            index += 1
        rendered = inline(" ".join(paragraph))
        if rendered:
            html.append(f"<p>{rendered}</p>")
    return "".join(html)


def limit_text(time_ms, memory_kb):
    rows = []
    if time_ms:
        seconds = time_ms / 1000
        value = f"{seconds:g}"
        rows.append(f"<dt>Time limit</dt><dd>{value} second{'' if seconds == 1 else 's'}</dd>")
    if memory_kb:
        rows.append(f"<dt>Memory limit</dt><dd>{memory_kb // 1000} megabytes</dd>")
    return "".join(rows)


def sample_rows(samples):
    """Lay the samples out the way `server.py:sample_io()` reads them back.

    One sample is a plain input/output pair. Several are written as the marker
    form the mirrored pages already use (pctbook__E18188 among them): all but
    the last sample under 样例输入, the last one under 样例输出, so that the two
    <dd> blocks concatenated stay one ordered marker stream.
    """
    if not samples:
        return "<dt>样例输入</dt><dd><pre></pre></dd>\n<dt>样例输出</dt><dd><pre></pre></dd>"
    if len(samples) == 1:
        return (f"<dt>样例输入</dt><dd><pre>{escape(samples[0]['input'].strip(chr(10)), quote=False)}</pre></dd>\n"
                f"<dt>样例输出</dt><dd><pre>{escape(samples[0]['output'].strip(chr(10)), quote=False)}</pre></dd>")

    def block(index, sample):
        return (f"样例输入{index}\n{sample['input'].strip(chr(10))}\n"
                f"样例输出{index}\n{sample['output'].strip(chr(10))}")

    head = "\n\n".join(block(index, sample) for index, sample in enumerate(samples[:-1], 1))
    tail = block(len(samples), samples[-1])
    return (f"<dt>样例输入</dt><dd><pre>{escape(head, quote=False)}</pre></dd>\n"
            f"<dt>样例输出</dt><dd><pre>{escape(tail, quote=False)}</pre></dd>")


def page_html(data):
    statement = data["statement"]
    title = f"{data['id'][len(re.match(r'[0-9]+', data['id']).group()):]}. {data['name']}"
    field = lambda name: statement.get(name) or ""
    sections = [("Description", render_blocks(field("background") + "\n\n" + field("description"))),
                ("Input", render_blocks(field("formatI"))),
                ("Output", render_blocks(field("formatO")))]
    content = "\n".join(f"<dt>{name}</dt><dd>{body}</dd>" for name, body in sections if body)
    note = render_blocks(field("hint"))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Codeforces {escape(data['id'])}: {escape(title)}</title></head>
<body><div id="pageTitle"><h2>{escape(title)}</h2></div>
<dl class="problem-params">
<dt>Source</dt><dd><a href="{escape(data['source_url'], quote=True)}" rel="noopener">Codeforces {escape(data['id'])}</a></dd>
{limit_text(data.get('time_limit_ms'), data.get('memory_limit_kb'))}
</dl>
<dl class="problem-content">
{content}
{sample_rows(data['samples'])}{f'\n<dt>Note</dt><dd>{note}</dd>' if note else ''}
</dl>
</body></html>
"""


def report(records):
    """Write down what every page was built from, so a page can be re-checked."""
    lines = [
        "# Codeforces 原题题面", "",
        "题面由 `scripts/fetch_codeforces_statements.py` 抓取、"
        "`scripts/build_codeforces_pages.py` 渲染成 `data/openjudge/pages/codeforces__*.html`。",
        "抓回来的原文留在 `data/openjudge/statements/<题号>.json`，页面可以随时按它重建、复核。", "",
        "## 来源", "",
        "`codeforces.com` 对本机返回 Cloudflare 403，`m1.codeforces.com` 镜像把每个页面都挡在登录后，",
        "所以题面取自洛谷的 Codeforces 远程评测镜像：它的页面数据里带 Codeforces 英文原文",
        "（`content`：description / formatI / formatO / hint）、全部官方样例和官方时限内存。",
        "每条记录都同时保留 `source_url`（Codeforces 原题）和 `mirror_url`（抓取地址）。", "",
        "交叉验证：4A 的时限内存（1 秒 / 64 MB）与本站此前人工核对过的 4A 页面逐字相同；",
        "158 道题的样例全部能被 `server.py:sample_io()` 原样切回抓取到的官方样例。", "",
        "## 重新抓取与重建", "",
        "```bash",
        "python3 scripts/fetch_codeforces_statements.py            # 只抓缺的；--refresh 全部重抓",
        "python3 scripts/build_codeforces_pages.py                 # 重建题面页并刷新本文件",
        "python3 scripts/mirror_openjudge_images.py                # 新题面引入的插图要进本地镜像",
        "```", "",
        "全部 158 道都由本脚本渲染。4A 曾是唯一人工写的那页（也正是它让人看出其余 157 页不对），",
        "现在也换成了抓回来的原文：官方限制与那一版逐字相同，正文补回 Codeforces 的原始表述和 Note。", "",
        "## 覆盖", "",
        f"- 题目：{len(records)} 道", 
        f"- 有 Note（官方样例解释）：{sum(1 for item in records if (item['statement'].get('hint') or '').strip())} 道",
        f"- 多组样例：{sum(1 for item in records if len(item['samples']) > 1)} 道",
        f"- 带插图：{sum(1 for item in records if '![' in json.dumps(item['statement'], ensure_ascii=False))} 道", "",
        "| 题目 | 标题 | 时限 | 内存 | 样例 | 抓取日期 | 官方链接 |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for item in records:
        lines.append(f"| {item['id']} | {item['name']} | {item['time_limit_ms'] / 1000:g} s | "
                     f"{item['memory_limit_kb'] // 1000} MB | {len(item['samples'])} | "
                     f"{item['fetched']} | {item['source_url']} |")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*", help="problem ids; default: every cached statement")
    parser.add_argument("--out", type=Path, default=PAGES, help="write pages here instead of the mirror")
    parser.add_argument("--keep", nargs="*", default=[],
                        help="ids whose existing page is left untouched")
    args = parser.parse_args()
    ids = args.ids or sorted(path.stem for path in CACHE.glob("*.json"))
    args.out.mkdir(parents=True, exist_ok=True)
    written, records = 0, []
    for problem_id in sorted(ids, key=lambda name: (int(re.match(r"\d+", name).group()), name)):
        data = json.loads((CACHE / f"{problem_id}.json").read_text(encoding="utf-8"))
        records.append(data)
        if problem_id in args.keep and args.out == PAGES:
            continue
        (args.out / f"codeforces__{problem_id}.html").write_text(page_html(data), encoding="utf-8")
        written += 1
    if args.out == PAGES and not args.ids:
        report(records)
    print(f"pages={written} out={args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
