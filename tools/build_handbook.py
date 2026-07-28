#!/usr/bin/env python3
"""把 docs/DEV_HANDBOOK.md 渲染成自包含的网页 docs/dev-handbook.html。

    python3 tools/build_handbook.py

**Markdown 是唯一事实源**，HTML 是产物 —— 不要手改 HTML，改了会被下次构建覆盖。

只用标准库：这个项目的规矩是零第三方依赖（README「单文件极简风格」），
为一份文档引入 markdown 库不划算。因此这里只实现手册**实际用到**的语法子集：

    #/##/### 标题、段落、`- ` 与 `1. ` 列表、竖线表格、``` 代码块、
    > 引用、--- 分隔线、`行内代码`、**粗体**、[链接](url)

遇到子集之外的语法会原样输出，不会静默吃掉内容。

两件值得说明的事：

**标题 id 沿用 GitHub 的 slug 规则**，因为手册正文里的目录用的就是
`#2-计算概论与程序设计基础` 这种 GitHub 风格锚点 —— 换一套规则会让目录全断。
构建时会校验每个目录链接都指向真实存在的标题，对不上就直接报错退出。

**代码引用自动变成 GitHub 链接**：`judge.py:100` 或 `server.py · _limits`
渲染成指向仓库的链接，读者可以直接跳到源码。
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "DEV_HANDBOOK.md"
OUT = ROOT / "docs" / "dev-handbook.html"
REPO_BLOB = "https://github.com/GMyhf/cs101.openjudge.cn/blob/main/"

TITLE = "CS101 判题系统开发教学手册"
SUBTITLE = "用一个真在跑的判题系统学计算机"
DESCRIPTION = ("以 cs101.openjudge.cn 本机判题服务为案例的计算机课程教学手册："
               "计算概论、数据结构与算法、操作系统、计算机网络、数据库、"
               "计算机安全、软件工程与系统运维。")

# 仓库里真实存在、值得自动链到源码的文件。只列这些，避免把普通文字误判成路径。
LINKABLE = [
    "server.py", "judge.py", "tools/backup_db.py", "tools/handoff.py",
    "tools/release.sh", "tools/build_handbook.py", "scripts/loadtest_judge.py",
    "scripts/smoke_languages.py", "scripts/index_tests.py", "scripts/crawl_openjudge.py",
    "tests/test_server.py", "tests/test_judge.py", "tests/test_backup.py",
    "tests/test_units.py", "tests/test_t004_common.py",
    "deploy/cs101.service", "deploy/cs101-backup.service", "deploy/cs101-backup.timer",
    "collab/PLAN.md", "collab/HANDOFF.md", "docs/用户手册.md", "docs/管理员手册.md",
    "README.md", "static/theme.css",
]


def slugify(text):
    """GitHub 风格锚点。手册正文的目录依赖这一套规则，改了目录就全断。"""
    text = re.sub(r"`", "", text)
    text = re.sub(r"[^\w一-鿿\s-]", "", text).strip().lower()
    return re.sub(r"\s+", "-", text)


def link_code_reference(code_text):
    """`judge.py:100` / `server.py · _limits` → 指向 GitHub 的链接。"""
    raw = code_text.strip()
    for path in sorted(LINKABLE, key=len, reverse=True):
        if not raw.startswith(path):
            continue
        rest = raw[len(path):]
        line = re.match(r"^:(\d+)", rest)
        href = REPO_BLOB + path + (f"#L{line.group(1)}" if line else "")
        return f'<a class="src" href="{href}">{html.escape(raw)}</a>'
    return None


def render_inline(text):
    """行内元素。先转义，再按「代码 → 链接 → 粗体」的顺序还原。"""
    placeholders = []

    def stash(markup):
        placeholders.append(markup)
        return f"\x00{len(placeholders) - 1}\x00"

    # 行内代码要在转义之前摘出来，否则代码里的 < > 会被处理两次
    def take_code(match):
        inner = match.group(1)
        linked = link_code_reference(inner)
        return stash(linked or f"<code>{html.escape(inner)}</code>")

    text = re.sub(r"`([^`]+)`", take_code, text)

    def take_link(match):
        label, href = match.group(1), match.group(2)
        return stash(f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", take_link, text)

    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)

    for index, markup in enumerate(placeholders):
        text = text.replace(f"\x00{index}\x00", markup)
    return text


def render(markdown):
    lines = markdown.split("\n")
    out, headings = [], []
    index, in_code = 0, False

    def close(tag_stack):
        while tag_stack:
            out.append(f"</{tag_stack.pop()}>")

    open_tags = []
    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                close(open_tags)
                language = line[3:].strip()
                out.append(f'<pre class="code" data-lang="{html.escape(language)}"><code>')
                in_code = True
            index += 1
            continue
        if in_code:
            out.append(html.escape(line))
            index += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", line)
        if heading:
            close(open_tags)
            level, text = len(heading.group(1)), heading.group(2).strip()
            anchor = slugify(text)
            if level >= 2:
                headings.append((level, text, anchor))
            out.append(f'<h{level} id="{anchor}">'
                       f'<a class="anchor" href="#{anchor}">#</a>{render_inline(text)}</h{level}>')
            index += 1
            continue

        if re.match(r"^\s*---+\s*$", line):
            close(open_tags)
            out.append("<hr>")
            index += 1
            continue

        # 表格：一行竖线 + 一行分隔
        if line.strip().startswith("|") and index + 1 < len(lines) \
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[index + 1]):
            close(open_tags)
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            out.append('<div class="table-wrap"><table><thead><tr>')
            out += [f"<th>{render_inline(c)}</th>" for c in cells(line)]
            out.append("</tr></thead><tbody>")
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                out.append("<tr>")
                out += [f"<td>{render_inline(c)}</td>" for c in cells(lines[index])]
                out.append("</tr>")
                index += 1
            out.append("</tbody></table></div>")
            continue

        if line.startswith(">"):
            close(open_tags)
            quoted = []
            while index < len(lines) and lines[index].startswith(">"):
                quoted.append(lines[index].lstrip(">").strip())
                index += 1
            out.append("<blockquote>" + render_inline(" ".join(quoted)) + "</blockquote>")
            continue

        bullet = re.match(r"^(\s*)-\s+(.*)$", line)
        number = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if bullet or number:
            want = "ul" if bullet else "ol"
            if open_tags[-1:] != [want]:
                close(open_tags)
                out.append(f"<{want}>")
                open_tags.append(want)
            out.append(f"<li>{render_inline((bullet or number).group(2))}</li>")
            index += 1
            continue

        if not line.strip():
            close(open_tags)
            index += 1
            continue

        close(open_tags)
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip() \
                and not re.match(r"^(#{1,4}\s|```|>|\s*[-*]\s|\s*\d+\.\s|\|)", lines[index]) \
                and not re.match(r"^\s*---+\s*$", lines[index]):
            paragraph.append(lines[index])
            index += 1
        out.append("<p>" + render_inline(" ".join(p.strip() for p in paragraph)) + "</p>")

    close(open_tags)
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out), headings


STYLE = """
:root{color-scheme:light;
  --ink:#16231d;--muted:#6b7a72;--line:#dfe7e1;--bg:#f4f7f4;--panel:#fff;
  --soft:#eef3ef;--accent:#237a50;--accent-soft:#e5f3eb;--warn:#c87828;--danger:#b04f43}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;
  --ink:#e6ece8;--muted:#94a49b;--line:#2f3a34;--bg:#141917;--panel:#181e1b;
  --soft:#202923;--accent:#8fd6ab;--accent-soft:#1e3a2a;--warn:#dcc07a;--danger:#e59a90}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.75 system-ui,-apple-system,"Segoe UI","Noto Sans CJK SC",sans-serif}
a{color:var(--accent)}
.masthead{background:var(--panel);border-bottom:1px solid var(--line);padding:44px 24px 34px}
.masthead .inner{max-width:1180px;margin:0 auto}
.masthead h1{margin:0 0 8px;font-size:clamp(26px,4vw,40px);line-height:1.2;letter-spacing:-.01em}
.masthead p{margin:0;color:var(--muted);font-size:16px}
.masthead .repo{margin-top:14px;font-size:14px}
.layout{max-width:1180px;margin:0 auto;padding:0 24px 80px;
  display:grid;grid-template-columns:246px minmax(0,1fr);gap:44px;align-items:start}
nav.toc{position:sticky;top:20px;max-height:calc(100vh - 40px);overflow:auto;
  padding:20px 0;font-size:14px;line-height:1.6}
nav.toc b{display:block;color:var(--muted);font-size:12px;letter-spacing:.08em;
  text-transform:uppercase;margin-bottom:10px}
nav.toc a{display:block;padding:4px 10px;border-left:2px solid transparent;
  color:var(--ink);text-decoration:none;border-radius:0 5px 5px 0}
nav.toc a:hover{background:var(--soft);color:var(--accent)}
nav.toc a.sub{padding-left:22px;color:var(--muted);font-size:13px}
nav.toc a.active{border-left-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
main{min-width:0;padding-top:20px}
h2{font-size:26px;margin:52px 0 14px;padding-bottom:9px;border-bottom:2px solid var(--line)}
h3{font-size:19px;margin:32px 0 10px}
h4{font-size:16px;margin:24px 0 8px;color:var(--muted)}
h1,h2,h3,h4{scroll-margin-top:20px}
.anchor{float:left;margin-left:-1.1em;padding-right:.35em;color:var(--line);
  text-decoration:none;font-weight:400}
h2:hover .anchor,h3:hover .anchor,h4:hover .anchor{color:var(--accent)}
p{margin:0 0 15px}
code{font:13.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
  background:var(--soft);padding:2px 6px;border-radius:4px;word-break:break-word}
a.src{background:var(--accent-soft);color:var(--accent);text-decoration:none;
  padding:2px 6px;border-radius:4px;font:13.5px ui-monospace,SFMono-Regular,Menlo,monospace}
a.src:hover{text-decoration:underline}
pre.code{background:var(--panel);border:1px solid var(--line);border-radius:9px;
  padding:15px 17px;overflow:auto;margin:0 0 17px}
pre.code code{background:none;padding:0;font-size:13px;line-height:1.65;white-space:pre}
blockquote{margin:0 0 17px;padding:13px 17px;border-left:3px solid var(--accent);
  background:var(--soft);border-radius:0 7px 7px 0;color:var(--ink)}
.table-wrap{overflow-x:auto;margin:0 0 18px}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--soft);font-weight:650}
ul,ol{margin:0 0 15px;padding-left:24px}
li{margin:5px 0}
li>code{white-space:nowrap}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}
footer{max-width:1180px;margin:0 auto;padding:26px 24px 60px;color:var(--muted);
  font-size:14px;border-top:1px solid var(--line)}
@media(max-width:900px){
  .layout{grid-template-columns:1fr;gap:0;padding:0 18px 60px}
  nav.toc{position:static;max-height:none;border-bottom:1px solid var(--line);margin-bottom:18px}
  .masthead{padding:30px 18px 24px}
}
@media print{nav.toc{display:none}.layout{display:block}a{color:inherit}}
"""

SCRIPT = """
(function(){
  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
  var seen=[];
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      var id=e.target.id;
      if(e.isIntersecting){if(seen.indexOf(id)<0)seen.push(id)}
      else{var i=seen.indexOf(id);if(i>=0)seen.splice(i,1)}
    });
    links.forEach(function(a){a.classList.remove('active')});
    if(seen.length&&map[seen[0]])map[seen[0]].classList.add('active');
  },{rootMargin:'0px 0px -75% 0px'});
  [].slice.call(document.querySelectorAll('h2[id],h3[id]')).forEach(function(h){io.observe(h)});
})();
"""


def main():
    if not SRC.is_file():
        print(f"找不到 {SRC}", file=sys.stderr)
        return 1
    markdown = SRC.read_text(encoding="utf-8")

    # 手册开头那段 H1 与引言块由页头承担，正文从目录之后开始
    body_md = markdown
    match = re.search(r"^## 目录.*?^---\s*$", markdown, re.S | re.M)
    if match:
        body_md = markdown[match.end():]

    body, headings = render(body_md)

    # 校验：正文里的目录链接必须都能落到真实标题上，否则点了就是死链
    anchors = {anchor for _, _, anchor in headings}
    broken = [a for a in re.findall(r"\]\(#([^)]+)\)", markdown) if a not in anchors]
    if broken:
        print(f"目录锚点对不上真实标题：{broken}", file=sys.stderr)
        return 1

    toc = []
    for level, text, anchor in headings:
        if level > 3:
            continue
        label = re.sub(r"`", "", text)
        css = "" if level == 2 else ' class="sub"'
        toc.append(f'<a href="#{anchor}"{css}>{html.escape(label)}</a>')

    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)}——{html.escape(SUBTITLE)}</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<meta property="og:title" content="{html.escape(TITLE)}">
<meta property="og:description" content="{html.escape(DESCRIPTION)}">
<meta property="og:type" content="article">
<style>{STYLE}</style>
</head>
<body>
<header class="masthead"><div class="inner">
  <h1>{html.escape(TITLE)}</h1>
  <p>{html.escape(SUBTITLE)}</p>
  <p class="repo"><a href="https://github.com/GMyhf/cs101.openjudge.cn">GitHub 仓库</a>
    · <a href="{REPO_BLOB}docs/DEV_HANDBOOK.md">Markdown 源文件</a>
    · <a href="{REPO_BLOB}collab/PLAN.md">事故与决策原始记录</a></p>
</div></header>
<div class="layout">
<nav class="toc"><b>目录</b>{''.join(toc)}</nav>
<main>
{body}
</main>
</div>
<footer>
  本页由 <code>tools/build_handbook.py</code> 从 <code>docs/DEV_HANDBOOK.md</code> 生成 ——
  Markdown 是唯一事实源，请勿手改此文件。
</footer>
<script>{SCRIPT}</script>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"✅ {OUT.relative_to(ROOT)}  {len(page.encode()):,} 字节  "
          f"{len(headings)} 个标题  {len(toc)} 条目录")
    return 0


if __name__ == "__main__":
    sys.exit(main())
