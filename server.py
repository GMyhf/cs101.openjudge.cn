#!/usr/bin/env python3
"""Small local course portal for cs101.openjudge.cn."""
from http import cookies
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import contextlib
import threading
import json
import hashlib
import hmac
import os
import secrets
import smtplib
import sqlite3
import time
import urllib.error
import urllib.request
import re
from email.message import EmailMessage
from html import escape, unescape
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
from judge import judge, language_version, problem_exists, run_sample

ROOT = Path(__file__).parent
DB = Path(os.environ.get("CS101_DB", ROOT / "data" / "course.db"))
MIRROR = ROOT / "data" / "openjudge"
# 唯一对外分发的目录。白名单是后缀而不是「除了 xx 以外」——
# 排除法每加一种新文件就要记得再排一次，迟早漏掉一个。
# 253/1849 道题的样例是「手写标注」式的：题面把多组样例塞进两个 <dl> 里，
# 用 `sample1 in:` 这样的行分段，而不是上游那种一组输入一组输出。
# 分隔行的写法在题库里散得很开（逐页统计过）：编号在关键词前（`Sample1 Input:`）
# 或后（`Sample Input1:`、`Sample Input 1:`）；关键词有 in/input/out/output，
# 还有一处把 Input 打成了 `Iutput`（routine__16530）；冒号有半角、全角、以及没有；
# 编号用过罗马数字（practice__20163）；还有一页把编号和关键词拆成两行（practice__20125）。
# 不能写 `sample\b`：`sample1` 里 e 和 1 之间没有词边界，最常见的那种写法反而匹配不上。
SAMPLE_ANY = re.compile(r'^[ \t]*sample', re.I | re.M)
SAMPLE_MARKER = re.compile(r'^[ \t]*sample[ \t]*(?P<a>\d+)?[ \t]*'
                           r'(?P<kind>input|output|iutput|in|out)[ \t]*'
                           r'(?P<b>\d+|[ivx]+)?[ \t]*[:：]?[ \t]*$', re.I)
SAMPLE_INDEX_ONLY = re.compile(r'^[ \t]*sample[ \t]*(?P<n>\d+)[ \t]*[:：]?[ \t]*$', re.I)
SAMPLE_KIND_ONLY = re.compile(r'^[ \t]*(?P<kind>input|output|iutput)[ \t]*'
                              r'(?P<n>\d+)?[ \t]*[:：][ \t]*$', re.I)
# 输出段里 `#` 开头的行往后全是讲解，而且讲解常常续到不带 `#` 的下一行
# （pctbook__M16531 就是），所以是**截断**而不是逐行过滤。
# 只在输出段截断：输入段的 `#` 可能是真数据 —— practice__19949 的 `###John###` 就是。
# 全库核过：253 道标记式题目里，输出段第一行就是 `#` 的有 0 道，截断不会吃掉真输出。
SAMPLE_EXPLAIN = re.compile(r'^[ \t]*(?:#|(?:解释|说明|注意|提示)[:：])')
ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5,
         "vi": 6, "vii": 7, "viii": 8, "ix": 9, "x": 10}


def parse_sample_sections(text):
    """把标注式样例切成 [{input, output}, ...]，解析不出就返回空列表。"""
    sections, seen, pending, current = [], {"input": 0, "output": 0}, None, None
    for line in text.split("\n"):
        kind = number = None
        marker = SAMPLE_MARKER.match(line)
        if marker:
            kind, number = marker.group("kind"), marker.group("a") or marker.group("b")
        else:
            index_only = SAMPLE_INDEX_ONLY.match(line)
            if index_only:
                pending, current = int(index_only.group("n")), None
                continue
            kind_only = SAMPLE_KIND_ONLY.match(line)
            if kind_only:
                kind, number = kind_only.group("kind"), kind_only.group("n")
        if kind is None:
            if current is not None:
                current["lines"].append(line)
            continue
        kind = "input" if kind.lower() in ("in", "input", "iutput") else "output"
        if number is None:
            index = pending
        elif number.isdigit():
            index = int(number)
        else:
            index = ROMAN.get(number.lower())
        if index is None:                       # 没编号就按出现顺序配对
            seen[kind] += 1
            index = seen[kind]
        else:
            seen[kind] = max(seen[kind], index)
            pending = index
        current = {"kind": kind, "index": index, "lines": []}
        sections.append(current)
    cases = {}
    for section in sections:
        body = section["lines"]
        if section["kind"] == "output":
            cut = next((i for i, line in enumerate(body) if SAMPLE_EXPLAIN.match(line)), None)
            if cut is not None:
                body = body[:cut]
        cases.setdefault(section["index"], {})[section["kind"]] = "\n".join(body).strip("\n")
    return [{"input": case.get("input", ""), "output": case.get("output", "")}
            for _, case in sorted(cases.items())
            if case.get("input", "").strip() or case.get("output", "").strip()]


JUDGE_SLOTS = set()
JUDGE_SLOTS_LOCK = threading.Lock()


@contextlib.contextmanager
def judging_slot(user):
    """同一用户同时只允许一个判题/运行在跑。

    ThreadingHTTPServer 每个并发请求都直接在 HTTP 线程上拉起编译器/解释器，
    改动前这里没有任何节流 —— 连点提交就能把机器打满。「运行样例」按钮
    把这个暴露面放大了，所以随本轮一起收口（人拍板，见 PLAN Decision Log）。
    锁只护 set 本身，判题过程不持锁：判一次最长 300 秒，持锁会把整台机器串起来。
    """
    key = (user or "").lower()
    with JUDGE_SLOTS_LOCK:
        busy = key in JUDGE_SLOTS
        if not busy:
            JUDGE_SLOTS.add(key)
    if busy:
        yield False
        return
    try:
        yield True
    finally:
        with JUDGE_SLOTS_LOCK:
            JUDGE_SLOTS.discard(key)


STATIC_DIR = (ROOT / "static").resolve()
STATIC_TYPES = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon",
                ".woff2": "font/woff2"}
BOOK_META = {
    "practice": {"name": "题库（包括计概、数算题目）", "count": 985},
    "pctbook": {"name": "计算思维算法实践", "count": 215},
    "routine": {"name": "数算 2025Spring每日选作", "count": 203},
    "2025sp_routine": {"name": "数算 2025Spring每日选作", "count": 73},
    "dsapre": {"name": "数算预习题", "count": 101},
    "25dsapre": {"name": "数算 2025Spring预习题", "count": 35},
    "2024fallroutine": {"name": "数算 2024Fall每日选作", "count": 93},
    "2024sp_routine": {"name": "数算 2024Spring每日选作", "count": 154},
}
SMTP_ENV_FILE = ROOT / "data" / ".smtp.env"
DEFAULT_PUBLIC_URL = "http://10.129.81.235:8000"

if SMTP_ENV_FILE.is_file() and os.environ.get("CS101_LOAD_DOTENV", "1") != "0":
    for line in SMTP_ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

ADMIN_USER = os.environ.get("CS101_ADMIN_USER", "GMyhf")
PASSWORD_FILE = ROOT / "data" / ".admin_password"
ADMIN_PASSWORD = os.environ.get("CS101_ADMIN_PASSWORD") or (PASSWORD_FILE.read_text(encoding="utf-8").strip() if PASSWORD_FILE.is_file() else "")
TOKENS = set()
SESSION_USERS = {}
# token -> 最近一次带着有效会话发请求的时间戳。
# 「在线」必须有时效：TOKENS 只在登出时才缩小，拿它当在线数会把「三天前登录过、
# 浏览器一直没关」也算进去 —— 那不是在线，是从没登出。
SESSION_SEEN = {}
ONLINE_WINDOW_SECONDS = 300
CATALOG_TITLE_CACHE = {}
CATALOG_RAW_CACHE = None
CATALOG_RAW_MTIME = None
CATALOG_FULL_CACHE = None
CAPTCHA_CHALLENGES = {}

COURSE = {
    "title": "计算机科学导论",
    "term": "2026 春季学期",
    "teacher": "GMyhf",
    "notice": "CS101 题库发布",
}
PROBLEMS = [
    {"id": "A1001", "title": "求两个整数的和", "chapter": "基础语法", "difficulty": "入门", "rate": 94, "solved": 1284},
    {"id": "A1002", "title": "输出第二个整数", "chapter": "基础语法", "difficulty": "入门", "rate": 91, "solved": 1198},
    {"id": "A1003", "title": "温度转换", "chapter": "基础语法", "difficulty": "入门", "rate": 87, "solved": 1086},
    {"id": "A1004", "title": "字符三角形", "chapter": "循环结构", "difficulty": "基础", "rate": 82, "solved": 976},
    {"id": "A1005", "title": "数字反转", "chapter": "循环结构", "difficulty": "基础", "rate": 76, "solved": 904},
    {"id": "A1006", "title": "最大公约数", "chapter": "函数与递归", "difficulty": "进阶", "rate": 69, "solved": 735},
]

# 提交页。判题结果不再直接 dump JSON —— 项目的立意是「反馈错在哪组数据」，
# 所以 WA 要把 case 编号、期望/实际 token 数摆出来，TLE/RE 要把判题器的 message 摆出来。
SUBMIT_PAGE = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__PROBLEM__ 提交代码 · CS101</title>
<link rel="stylesheet" href="/static/theme.css">
<script>
// 主题引导必须在首屏绘制前跑完，否则深色用户会先看到一帧白。
// 也因为这里总会写上 data-theme，theme.css 里的深色才只需要一个块。
(function(){try{var t=localStorage.getItem('cs101-theme');
if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();
</script>
<style>
 /* 全屏工作台：页面本身永不滚动，滚动只发生在 .pane-body 里。
    每一层 flex/grid 子项都要 min-height:0，少一处内容就会把面板撑破。 */
 html,body{height:100%}
 body.app{display:flex;flex-direction:column;height:100dvh;overflow:hidden}
 .crumb{display:flex;align-items:baseline;gap:8px;min-width:0;color:var(--muted);font-size:13px}
 .crumb-id{font:700 13px var(--font-mono);color:var(--accent)}
 .crumb-title{color:var(--ink);font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 .auth-chip{font-size:13px;white-space:nowrap}
 .theme-toggle{padding:5px 10px;font-size:13px}

 .workspace-layout{flex:1;min-height:0;display:grid;
   grid-template-columns:minmax(320px,1fr) 10px minmax(420px,1.1fr);padding:var(--pane-gap)}
 .pane-col{display:grid;grid-template-rows:minmax(140px,1fr) 10px minmax(96px,220px) auto;
   min-height:0;min-width:0}

 /* ---- 题面 ---- */
 .statement-panel h2{font-size:21px;line-height:1.3;margin:0 0 14px}
 .statement-panel .problem-params{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 4px;
   margin:0 0 20px;padding:9px 12px;border:1px solid var(--line);border-radius:var(--radius-sm);
   background:var(--soft);font-size:12.5px;color:var(--muted)}
 .statement-panel .problem-params dt{font-weight:600}
 .statement-panel .problem-params dd{margin:0 16px 0 0;color:var(--ink);font-variant-numeric:tabular-nums}
 .statement-panel .problem-content{display:block;margin:0}
 .statement-panel .problem-content dt{font-size:15px;font-weight:700;margin:22px 0 8px;
   padding-bottom:5px;border-bottom:1px solid var(--line)}
 .statement-panel .problem-content dt:first-child{margin-top:0}
 .statement-panel .problem-content dd{margin:0}
 .statement-panel .problem-content pre{overflow:auto;margin:9px 0;padding:12px 14px;
   border:1px solid var(--line);border-radius:var(--radius-sm);background:var(--soft);
   font:12.5px/1.6 var(--font-mono)}

 /* ---- 编辑器 ---- */
 /* 透明 textarea 叠在高亮层上。两层的字体/行高/padding 必须逐项一致，
    差一点点光标就会和文字错位；字号由 --code-size 同时驱动两层。 */
 .editor{flex:1;min-height:0;display:flex;overflow:hidden;background:var(--panel)}
 .gutter{flex:0 0 auto;padding:12px 8px 12px 12px;text-align:right;color:var(--gutter-fg);
   background:var(--gutter-bg);border-right:1px solid var(--line);user-select:none;
   white-space:pre;overflow:hidden}
 .codewrap{position:relative;flex:1;min-width:0}
 .gutter,.codewrap pre,.codewrap textarea{font:var(--code-size)/1.5 var(--font-mono);tab-size:4}
 .codewrap pre,.codewrap textarea{margin:0;padding:12px;border:0;white-space:pre;overflow:auto;
   width:100%;height:100%;min-height:0}
 .codewrap pre{position:absolute;inset:0;pointer-events:none;color:var(--ink);background:transparent}
 .codewrap textarea{position:relative;background:transparent;color:transparent;caret-color:var(--ink);
   resize:none;outline:none}
 .t-com{color:var(--tok-com);font-style:italic}
 .t-str{color:var(--tok-str)}
 .t-num{color:var(--tok-num)}
 .t-kw{color:var(--tok-kw);font-weight:600}
 .t-pre{color:var(--tok-pre)}
 .t-match{background:var(--tok-match-bg);border-radius:2px;box-shadow:0 0 0 1px var(--tok-match-ring)}
 .pane-editor select{min-width:186px;padding:5px 9px;font-size:13px}
 .pane-editor .pane-tools button{padding:5px 9px;font-size:12px}

 /* ---- 判题结果 ---- */
 .verdict-head{display:flex;align-items:center;gap:11px;flex-wrap:wrap}
 .verdict-title{font-size:18px;font-weight:700;margin:0}
 .metrics{display:flex;flex-wrap:wrap;gap:8px;margin-top:13px}
 .snip{margin-top:13px}
 .snip-h{color:var(--muted);font-size:12.5px;margin-bottom:4px}
 .editor-state{font-size:12.5px;color:var(--muted)}
 .placeholder{color:var(--muted);font-size:13.5px}

 /* ---- 样例 ---- */
 .sample-tabs{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:12px}
 .sample-pick{cursor:pointer;font:inherit;font-size:12px}
 .sample-pick.on{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
 .sample-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
 .sample-h{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--muted);margin-bottom:5px}
 .sample-box{margin:0;height:148px;overflow:auto;padding:10px;border:1px solid var(--line);
   border-radius:var(--radius-sm);background:var(--soft);font:12.5px/1.55 var(--font-mono);
   white-space:pre;width:100%;color:var(--ink)}
 textarea.sample-box{resize:none;outline:none}
 textarea.sample-box:focus{border-color:var(--accent)}

 /* ---- 底部动作条 ---- */
 .action-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 2px 0}
 .action-buttons{display:flex;gap:10px}

 /* ---- 提交记录 ---- */
 .history-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
 .history-heading h2{font-size:16px;margin:0}
 .history-heading button{padding:5px 10px;font-size:12.5px}
 .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-bottom:18px}
 .stat-card{border:1px solid var(--line);border-radius:var(--radius-sm);background:var(--soft);padding:12px 14px}
 .stat-card b{display:block;font-size:22px;line-height:1.15;font-variant-numeric:tabular-nums}
 .stat-card span{color:var(--muted);font-size:12px}

 @media(max-width:900px){
   body.app{height:auto;overflow:auto}
   .workspace-layout{grid-template-columns:1fr;gap:var(--pane-gap)}
   .splitter{display:none}
   .pane-col{grid-template-rows:none;gap:var(--pane-gap);order:1}
   .pane-left{order:2}
   .editor{flex:none;height:56vh}
   .pane-body{max-height:72vh}
   .crumb{display:none}
   .sample-grid{grid-template-columns:1fr}
 }
</style>
<body class="app">
<header class="topbar">
  <a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a>
  <div class="crumb"><span class="crumb-id">__PROBLEM__</span><span>·</span><span class="crumb-title">__BOOK_NAME__</span></div>
  <nav class="topnav">
    <a href="/problems/">题库目录</a>
    <a href="/history/">提交记录</a>
    <a href="/help/">说明</a>
    <button id="theme" type="button" class="ghost theme-toggle">深色</button>
    <span id="auth" class="auth-chip muted">正在检查登录状态…</span>
  </nav>
</header>
<main class="workspace-layout" id="workspace">
  <section class="pane pane-left">
    <nav class="pane-tabs" role="tablist">
      <button class="pane-tab" type="button" role="tab" aria-selected="true" data-panel="paneStatement">题目描述</button>
      <button class="pane-tab" type="button" role="tab" aria-selected="false" data-panel="paneHistory">提交记录</button>
      <button class="pane-tab" type="button" role="tab" aria-selected="false" data-panel="paneStats">统计</button>
      <span class="pane-tools"><button id="copyStatement" class="ghost" type="button">复制 Markdown</button></span>
    </nav>
    <div class="pane-body statement-panel" id="paneStatement" role="tabpanel">
      <h2>__STATEMENT_TITLE__</h2>
      <dl class="problem-params">__STATEMENT_PARAMS__</dl>
      <dl class="problem-content">__STATEMENT_CONTENT__</dl>
    </div>
    <div class="pane-body" id="paneHistory" role="tabpanel" hidden>
      <div class="history-heading"><h2>我的提交记录</h2><button id="historyToggle" class="ghost" type="button">看全部</button></div>
      <div id="histbox" class="muted">…</div>
    </div>
    <div class="pane-body" id="paneStats" role="tabpanel" hidden>
      <div id="statsbox" class="muted">…</div>
    </div>
  </section>
  <div class="splitter splitter-v" id="splitter" role="separator" aria-orientation="vertical" aria-label="调整题面和编辑器宽度" tabindex="0"></div>
  <form id="form" class="pane-col">
    <section class="pane pane-editor">
      <div class="pane-tabs">
        <span class="pane-tab" aria-selected="true">代码</span>
        <span class="pane-tools">
          <select name="language" aria-label="选择语言">
            __LANGUAGE_OPTIONS__
          </select>
          <button id="fontDown" class="ghost" type="button" title="缩小字号">A-</button>
          <button id="fontUp" class="ghost" type="button" title="放大字号">A+</button>
          <button id="resetCode" class="ghost" type="button" title="清空代码">清空</button>
        </span>
      </div>
      <div class="editor">
        <div class="gutter" id="gutter">1</div>
        <div class="codewrap">
          <pre id="hl" aria-hidden="true"></pre>
          <textarea name="source" id="src" placeholder="在这里粘贴代码" spellcheck="false"
                    autocomplete="off" autocapitalize="off"></textarea>
        </div>
      </div>
    </section>
    <div class="splitter splitter-h" id="splitterH" role="separator" aria-orientation="horizontal" aria-label="调整编辑器和结果高度" tabindex="0"></div>
    <section class="pane pane-result">
      <nav class="pane-tabs" role="tablist">
        <button class="pane-tab" type="button" role="tab" aria-selected="true" data-panel="verdict">判题结果</button>
        <button class="pane-tab" type="button" role="tab" aria-selected="false" data-panel="samples">样例</button>
        <span class="pane-tools"><span class="editor-state">准备提交</span></span>
      </nav>
      <div class="pane-body" id="verdict" role="tabpanel"><div class="placeholder">提交后在这里显示判题结果。</div></div>
      <div class="pane-body" id="samples" role="tabpanel" hidden>
        <div class="sample-tabs" id="sampleTabs" hidden></div>
        <div class="sample-grid">
          <div><div class="sample-h">输入<span class="muted">（可改）</span></div><textarea id="sampleIn" class="sample-box" spellcheck="false" autocomplete="off"></textarea></div>
          <div><div class="sample-h">预期输出</div><pre id="sampleExp" class="sample-box"></pre></div>
          <div><div class="sample-h">实际输出<span id="sampleVerdict"></span></div><pre id="sampleGot" class="sample-box muted">点「运行样例」后显示。</pre></div>
        </div>
      </div>
    </section>
    <div class="action-bar">
      <span class="editor-state" id="runState"></span>
      <span class="action-buttons">
        <button id="run" type="button" class="ghost">运行样例</button>
        <button id="go" type="submit" class="primary">提交并判题</button>
      </span>
    </div>
  </form>
</main>
<script>
const BOOK = "__BOOK__", PROBLEM = "__PROBLEM__";
const SAMPLES = __SAMPLE_JSON__;
const CLS = { "Accepted": "b-ac", "Wrong Answer": "b-wa" };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// ---- 面板拖拽 ----------------------------------------------------------
// 横竖两条共用一套逻辑：差别只在读哪个坐标、写哪个 grid 轴。
// 位置只存在本浏览器，存的是比例而不是像素，换个窗口大小才不会跑偏。
function makeSplitter(bar, opts) {
  const apply = value => {
    const span = opts.span();
    const size = Math.max(opts.min, Math.min(span - opts.minOther, value));
    opts.write(size);
    try { localStorage.setItem(opts.key, String(size / span)); } catch (err) {}
    return size;
  };
  bar.addEventListener('pointerdown', e => {
    bar.classList.add('dragging'); bar.setPointerCapture(e.pointerId); apply(opts.read(e));
  });
  bar.addEventListener('pointermove', e => { if (bar.hasPointerCapture(e.pointerId)) apply(opts.read(e)); });
  bar.addEventListener('pointerup', e => { bar.releasePointerCapture(e.pointerId); bar.classList.remove('dragging'); });
  // 元素本来就有 role="separator" 和 tabindex="0"，却一直没有键盘处理 —— 补上
  bar.addEventListener('keydown', e => {
    const step = { ArrowLeft: -16, ArrowRight: 16, ArrowUp: -16, ArrowDown: 16 }[e.key];
    if (step === undefined && e.key !== 'Home') return;
    e.preventDefault();
    apply(e.key === 'Home' ? opts.span() * opts.home : opts.current() + step);
  });
  const saved = (() => { try { return Number(localStorage.getItem(opts.key)); } catch (err) { return NaN; } })();
  requestAnimationFrame(() => apply(opts.span() * (saved > 0 && saved < 1 ? saved : opts.home)));
}

const workspace = document.querySelector('#workspace');
const paneCol = document.querySelector('#form');
const actionBar = document.querySelector('.action-bar');
makeSplitter(document.querySelector('#splitter'), {
  key: 'cs101-split-ratio', home: 0.44, min: 320, minOther: 430,
  span: () => workspace.clientWidth,
  read: e => e.clientX - workspace.getBoundingClientRect().left,
  current: () => document.querySelector('.pane-left').getBoundingClientRect().width,
  write: size => { workspace.style.gridTemplateColumns = size + 'px 10px minmax(0,1fr)'; },
});
makeSplitter(document.querySelector('#splitterH'), {
  key: 'cs101-split-v', home: 0.3, min: 96, minOther: 190,
  span: () => paneCol.clientHeight - actionBar.offsetHeight,
  read: e => paneCol.getBoundingClientRect().bottom - actionBar.offsetHeight - e.clientY,
  current: () => document.querySelector('.pane-result').getBoundingClientRect().height,
  write: size => { paneCol.style.gridTemplateRows = 'minmax(0,1fr) 10px ' + size + 'px auto'; },
});

// ---- 标签页 ------------------------------------------------------------
for (const group of document.querySelectorAll('.pane-tabs[role="tablist"]')) {
  const tabs = group.querySelectorAll('.pane-tab[data-panel]');
  for (const tab of tabs) tab.addEventListener('click', () => {
    for (const other of tabs) {
      const on = other === tab;
      other.setAttribute('aria-selected', String(on));
      document.querySelector('#' + other.dataset.panel).hidden = !on;
    }
    if (tab.dataset.panel === 'paneStats') loadStats();
  });
}
function showTab(panel) {
  const tab = document.querySelector('.pane-tab[data-panel="' + panel + '"]');
  if (tab) tab.click();
}

function markdownInline(node) {
  if (node.nodeType === Node.TEXT_NODE) return node.nodeValue.replace(/[ \t]+/g, ' ');
  if (node.nodeType !== Node.ELEMENT_NODE) return '';
  const tag = node.tagName.toLowerCase();
  if (tag === 'br') return '\n';
  if (tag === 'pre') return '\n```\n' + node.innerText.trimEnd() + '\n```\n';
  const inner = Array.from(node.childNodes).map(markdownInline).join('');
  if (tag === 'strong' || tag === 'b') return '**' + inner.trim() + '**';
  if (tag === 'em' || tag === 'i') return '*' + inner.trim() + '*';
  if (tag === 'code') return '`' + inner.trim() + '`';
  if (tag === 'a') return '[' + inner.trim() + '](' + node.getAttribute('href') + ')';
  return inner;
}
function statementMarkdown() {
  const root = document.querySelector('.statement-panel');
  const title = root.querySelector('h2').innerText.trim();
  const params = [];
  const paramNodes = root.querySelector('.problem-params');
  if (paramNodes) {
    const children = Array.from(paramNodes.children);
    for (let i = 0; i < children.length; i += 2) {
      if (children[i + 1]) params.push('- **' + children[i].innerText.trim() + '** ' + children[i + 1].innerText.trim());
    }
  }
  const sections = [];
  const content = root.querySelector('.problem-content');
  for (const node of content.children) {
    if (node.tagName.toLowerCase() === 'dt') sections.push('## ' + node.innerText.trim());
    if (node.tagName.toLowerCase() === 'dd') {
      const value = markdownInline(node).replace(/\n{3,}/g, '\n\n').trim();
      if (value) sections.push(value);
    }
  }
  return ['# ' + title, params.join('\n'), sections.join('\n\n')].filter(Boolean).join('\n\n') + '\n';
}
copyStatement.addEventListener('click', async () => {
  const text = statementMarkdown();
  try {
    if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
    else { const box = document.createElement('textarea'); box.value = text; box.style.position = 'fixed'; box.style.opacity = '0'; document.body.appendChild(box); box.select(); document.execCommand('copy'); box.remove(); }
    copyStatement.textContent = '已复制';
    setTimeout(() => { copyStatement.textContent = '复制 Markdown'; }, 1400);
  } catch (err) { copyStatement.textContent = '复制失败'; }
});

fetch("/api/me", { credentials: "same-origin" }).then(r => r.json()).then(me => {
  auth.innerHTML = me.authenticated
    ? '已登录：<b>' + esc(me.user) + '</b>'
    : '<a href="/auth/login/">请先登录后提交</a>';
  loadHistory();
});
// ---- 语法高亮 / 括号匹配 / 自动缩进 -------------------------------------
// 不引外部库。三件事共用同一次扫描：高亮要知道 token 边界，括号匹配要跳过
// 字符串和注释里的括号，缺了这层共享就会把 "(" 里的括号也配上。
const PY_KW = "False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|"
            + "except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|"
            + "return|try|while|with|yield";
const C_KW  = "auto|bool|break|case|char|class|const|constexpr|continue|default|delete|do|double|"
            + "else|enum|extern|false|float|for|goto|if|inline|int|long|namespace|new|nullptr|"
            + "operator|private|protected|public|return|short|signed|sizeof|static|struct|switch|"
            + "template|this|throw|true|try|typedef|typename|union|unsigned|using|virtual|void|"
            + "volatile|while";
const NUM = /\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b/y;
const SPECS = {
  python: [
    ["com", /#[^\n]*/y],
    ["str", /(["]{3}|''')[\s\S]*?\1|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/y],
    ["num", NUM],
    ["kw", new RegExp("\\b(?:" + PY_KW + ")\\b", "y")],
  ],
  c: [
    ["com", /\/\/[^\n]*|\/\*[\s\S]*?\*\//y],
    ["pre", /#[a-z]+/y],
    ["str", /"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/y],
    ["num", NUM],
    ["kw", new RegExp("\\b(?:" + C_KW + ")\\b", "y")],
  ],
};
SPECS.cpp = SPECS.c;
SPECS.pypy3 = SPECS.python;      // PyPy3 就是 Python 语法，高亮与缩进规则共用一套

// 一次扫描出所有 token 区间；高亮和括号匹配都基于它，保证两者看到的是同一份切分。
function scan(code, lang) {
  const specs = SPECS[lang] || SPECS.python;
  const tokens = [];
  let i = 0;
  while (i < code.length) {
    let hit = null;
    for (const spec of specs) {
      spec[1].lastIndex = i;
      const m = spec[1].exec(code);
      if (m && m.index === i && m[0]) { hit = [spec[0], m[0]]; break; }
    }
    if (hit) { tokens.push([hit[0], i, i + hit[1].length]); i += hit[1].length; }
    else i++;
  }
  return tokens;
}

function inToken(tokens, pos) {
  for (const t of tokens) if (pos >= t[1] && pos < t[2]) return true;
  return false;
}

const OPEN = "([{", CLOSE = ")]}";

// 光标处（或其左侧）若是括号，返回它与配对括号的下标。字符串/注释里的括号一律不参与。
function bracketMatch(code, pos, lang) {
  const tokens = scan(code, lang);
  for (const at of [pos, pos - 1]) {
    if (at < 0 || at >= code.length) continue;
    const ch = code[at];
    if (inToken(tokens, at)) continue;
    const o = OPEN.indexOf(ch), c = CLOSE.indexOf(ch);
    if (o < 0 && c < 0) continue;
    const step = o >= 0 ? 1 : -1;
    const want = o >= 0 ? CLOSE[o] : OPEN[c];
    let depth = 0;
    for (let k = at; k >= 0 && k < code.length; k += step) {
      if (inToken(tokens, k)) continue;
      if (code[k] === ch) depth++;
      else if (code[k] === want) { depth--; if (!depth) return [at, k].sort((x, y) => x - y); }
    }
    return null;                      // 有括号但没配上：不标，也不去标别的
  }
  return null;
}

// 回车后应插入的缩进：沿用本行缩进；python 行尾是 ":" 或 c 系行尾是 "{" 则多缩一级。
function indentFor(code, pos, lang) {
  const lineStart = code.lastIndexOf("\n", pos - 1) + 1;
  const line = code.slice(lineStart, pos);
  const base = (line.match(/^[ \t]*/) || [""])[0];
  const trimmed = line.replace(/\s+$/, "");
  const opens = (lang === "python" || lang === "pypy3") ? trimmed.endsWith(":") : trimmed.endsWith("{");
  return base + (opens ? "    " : "");
}

// ---- 括号/引号自动补全 --------------------------------------------------
// 纯函数：给定当前文本、选区和按下的键，返回要做的编辑，或 null 表示走浏览器默认行为。
// 返回 {from, to, insert, caret}，caret 是应用后的绝对光标位置。
const PAIRS = { "(": ")", "[": "]", "{": "}", '"': '"', "'": "'" };
const CLOSERS = ")]}";

// 右侧是这些时才自动补全：行尾、空白、右括号。避免把 f|oo 变成 f(|)oo。
function closeOk(next) {
  return next === undefined || next === "\n" || /\s/.test(next) || CLOSERS.indexOf(next) >= 0;
}

function pairAction(value, start, end, key) {
  const next = value[start];

  if (key === "Backspace" && start === end && start > 0) {
    const left = value[start - 1];
    if (PAIRS[left] && PAIRS[left] === next) {          // 空的一对，一次删掉两个
      return { from: start - 1, to: start + 1, insert: "", caret: start - 1 };
    }
    return null;
  }

  if (start !== end) {                                  // 有选区：用这对把它裹起来
    if (!PAIRS[key]) return null;
    const picked = value.slice(start, end);
    return { from: start, to: end, insert: key + picked + PAIRS[key], caret: end + 2 };
  }

  // 输入右括号而右边正好就是它：跳过去，不再插一个
  if ((CLOSERS.indexOf(key) >= 0 || key === '"' || key === "'") && next === key) {
    return { from: start, to: start, insert: "", caret: start + 1 };
  }

  if (PAIRS[key] && closeOk(next)) {
    return { from: start, to: start, insert: key + PAIRS[key], caret: start + 1 };
  }
  return null;
}

function esc2(s) { return esc(s); }

function highlight(code, lang, marks) {
  const tokens = scan(code, lang);
  const mark = marks || [];
  let out = "", i = 0, ti = 0;
  const wrap = (text, cls) => '<span class="' + cls + '">' + esc2(text) + "</span>";
  while (i < code.length) {
    if (ti < tokens.length && tokens[ti][1] === i) {
      const t = tokens[ti++];
      out += wrap(code.slice(t[1], t[2]), "t-" + t[0]);
      i = t[2];
      continue;
    }
    if (mark.indexOf(i) >= 0) { out += wrap(code[i], "t-match"); i++; continue; }
    // 连续的普通字符整段转义，避免逐字符拼串
    let j = i;
    while (j < code.length && !(ti < tokens.length && tokens[ti][1] === j) && mark.indexOf(j) < 0) j++;
    out += esc2(code.slice(i, j));
    i = j;
  }
  return out;
}

function paintEditor() {
  const code = src.value;
  const lang = form.language.value;
  const pair = document.activeElement === src ? bracketMatch(code, src.selectionStart, lang) : null;
  // 末尾补一个换行：最后一行为空时高亮层会比 textarea 少一行高度，滚动就对不齐
  hl.innerHTML = highlight(code + "\n", lang, pair);
  gutter.textContent = Array.from({ length: code.split("\n").length }, (_, k) => k + 1).join("\n");
  hl.scrollTop = src.scrollTop; hl.scrollLeft = src.scrollLeft;
}

src.addEventListener("input", paintEditor);
src.addEventListener("click", paintEditor);
src.addEventListener("keyup", paintEditor);
src.addEventListener("blur", paintEditor);
src.addEventListener("scroll", () => { hl.scrollTop = src.scrollTop; hl.scrollLeft = src.scrollLeft; });
form.language.addEventListener("change", paintEditor);
src.addEventListener("keydown", e => {
  if (e.key === "Tab") {
    e.preventDefault();
    src.setRangeText("    ", src.selectionStart, src.selectionEnd, "end");
    paintEditor();
  } else if (e.key === "Enter") {
    e.preventDefault();
    const indent = indentFor(src.value, src.selectionStart, form.language.value);
    src.setRangeText("\n" + indent, src.selectionStart, src.selectionEnd, "end");
    paintEditor();
  } else if (e.key === "Backspace" || PAIRS[e.key] || CLOSERS.indexOf(e.key) >= 0) {
    const act = pairAction(src.value, src.selectionStart, src.selectionEnd, e.key);
    if (!act) return;                        // 没命中就走浏览器默认行为（含撤销栈）
    e.preventDefault();
    src.setRangeText(act.insert, act.from, act.to, "end");
    src.selectionStart = src.selectionEnd = act.caret;
    paintEditor();
  }
});

// ---- 字号 / 清空 --------------------------------------------------------
const SIZE_KEY = "cs101-code-size";
function applySize(px) {
  const size = Math.max(11, Math.min(20, px));
  document.documentElement.style.setProperty('--code-size', size + 'px');
  try { localStorage.setItem(SIZE_KEY, String(size)); } catch (err) {}
  paintEditor();
}
fontUp.onclick = () => applySize(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--code-size')) + 1);
fontDown.onclick = () => applySize(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--code-size')) - 1);
resetCode.onclick = () => { src.value = ""; paintEditor(); src.focus(); };
try { const saved = Number(localStorage.getItem(SIZE_KEY)); if (saved) applySize(saved); } catch (err) {}

// ---- 主题 --------------------------------------------------------------
// 首屏那段引导脚本已经写好 data-theme，这里只负责切换和记住。
const THEME_KEY = "cs101-theme";
function applyTheme(name) {
  document.documentElement.dataset.theme = name;
  theme.textContent = name === "dark" ? "浅色" : "深色";
  try { localStorage.setItem(THEME_KEY, name); } catch (err) { /* 隐私模式下忽略 */ }
}
theme.onclick = () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
applyTheme(document.documentElement.dataset.theme === "dark" ? "dark" : "light");

paintEditor();

function badge(status) {
  const cls = CLS[status] || (status === "No Test Data" || status === "Problem Not Found" ? "b-info" : "b-other");
  return '<span class="badge ' + cls + '">' + esc(status) + "</span>";
}
function chip(label, value) {
  return '<span class="chip">' + esc(label) + '<b>' + esc(value) + '</b></span>';
}

function renderVerdict(data) {
  const metrics = [];
  // 「错在哪组数据」是这个页面存在的理由，所以它排第一个
  if (data.case !== undefined) metrics.push(chip("出错的数据组", "第 " + data.case + " 组"));
  if (data.cases !== undefined) metrics.push(chip("通过", data.cases + " 组全过"));
  if (data.time_ms !== undefined) metrics.push(chip("用时", data.time_ms + " ms"));
  if (data.memory_kb !== undefined) metrics.push(chip("内存", data.memory_kb + " kB"));
  if (data.expected_tokens !== undefined)
    metrics.push(chip("输出规模", "期望 " + data.expected_tokens + " / 实际 " + data.actual_tokens + " token"));
  if (data.source_bytes !== undefined) metrics.push(chip("代码长度", data.source_bytes + " B"));
  if (data.language_version) metrics.push(chip("语言", data.language_version));
  // failing_input 只在管理员打开开关时才由服务端下发；关着时这里根本收不到。
  let snippet = "";
  if (data.failing_input) {
    const f = data.failing_input;
    const tail = f.truncated ? "（共 " + f.total_lines + " 行 / " + f.total_chars + " 字符，已截断）" : "";
    snippet = '<div class="snip"><div class="snip-h">第 ' + data.case + ' 组的输入 ' + tail
            + '</div><pre class="msg">' + esc(f.text) + "</pre></div>";
  }
  if (data.expected_output) {
    const o = data.expected_output;
    const tail = o.truncated ? "（内容过长，已截断）" : "";
    snippet += '<div class="snip"><div class="snip-h">第 ' + data.case + ' 组对应 .out 期望输出 ' + tail
            + '</div><pre class="msg source">' + esc(o.text) + "</pre></div>";
  }
  verdict.innerHTML = '<div class="verdict-head">' + badge(data.status)
    + '<span class="verdict-title">' + esc(data.status === "Accepted" ? "通过" : data.status) + '</span></div>'
    + (metrics.length ? '<div class="metrics">' + metrics.join("") + "</div>" : "")
    + (data.message ? '<pre class="msg">' + esc(data.message) + "</pre>" : "")
    + snippet;
  showTab('verdict');
}

// ---- 运行样例 ----------------------------------------------------------
// 与提交走同一套沙箱，但不写 submissions 表、不计入统计。
// 253 道题的题面把多组样例用 `sample1 in:` 这类行标注在一起，服务端已经切好，
// 这里只负责让用户挑一组。只有一组时不显示切换条。
const SAMPLE_CASES = (SAMPLES.cases && SAMPLES.cases.length)
  ? SAMPLES.cases : [{ input: SAMPLES.input || "", output: SAMPLES.output || "" }];
let sampleIdx = 0;
function selectSample(i) {
  sampleIdx = i;
  sampleIn.value = SAMPLE_CASES[i].input;
  sampleExp.textContent = SAMPLE_CASES[i].output;
  sampleGot.textContent = "点「运行样例」后显示。";
  sampleGot.classList.add("muted");
  sampleVerdict.innerHTML = "";
  if (SAMPLE_CASES.length > 1) {
    sampleTabs.hidden = false;
    sampleTabs.innerHTML = SAMPLE_CASES.map((c, k) =>
      '<button type="button" class="chip sample-pick' + (k === i ? " on" : "") + '" data-i="' + k + '">样例 ' + (k + 1) + "</button>").join("");
  }
}
sampleTabs.addEventListener("click", e => {
  const hit = e.target.closest("[data-i]");
  if (hit) selectSample(Number(hit.dataset.i));
});
selectSample(0);
let busy = false;
function setBusy(on, note) {
  busy = on;
  go.disabled = on; run.disabled = on;
  for (const el of document.querySelectorAll('.editor-state')) el.textContent = note;
}
run.addEventListener('click', async () => {
  if (busy) return;
  showTab('samples');
  setBusy(true, "运行中…");
  sampleVerdict.innerHTML = "";
  sampleGot.textContent = "";
  sampleGot.classList.add("muted");
  try {
    const r = await fetch("/api/run", { method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ book: BOOK, problem: PROBLEM, language: form.language.value,
                             source: src.value, stdin: sampleIn.value }) });
    const data = await r.json();
    if (r.status === 401) { sampleGot.textContent = "请先登录后再运行。"; }
    else if (data.status !== "OK") {
      sampleGot.classList.remove("muted");
      sampleGot.textContent = data.message || data.status;
      sampleVerdict.innerHTML = badge(data.status);
    } else {
      sampleGot.classList.remove("muted");
      sampleGot.textContent = data.stdout || (data.stderr ? "" : "（没有输出）");
      if (data.stderr) sampleGot.textContent += "\n--- stderr ---\n" + data.stderr;
      // 与判题器同一条比对规则：按 token 比，不计空白差异
      const want = SAMPLE_CASES[sampleIdx].output || "";
      const same = data.stdout.trim().split(/\s+/).join(" ") === want.trim().split(/\s+/).join(" ");
      sampleVerdict.innerHTML = '<span class="badge ' + (same ? "b-ac" : "b-wa") + '">'
        + (same ? "与样例一致" : "与样例不一致") + "</span>";
    }
  } catch (err) {
    sampleGot.classList.remove("muted");
    sampleGot.textContent = String(err);
  }
  setBusy(false, "准备提交");
});

form.onsubmit = async e => {
  e.preventDefault();
  if (busy) return;
  setBusy(true, "判题中…");
  verdict.innerHTML = '<div class="placeholder">判题中，请稍候…</div>';
  showTab('verdict');
  const body = Object.fromEntries(new FormData(form));
  body.book = BOOK; body.problem = PROBLEM;
  try {
    const r = await fetch("/api/submit", { method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await r.json();
    if (r.status === 401) verdict.innerHTML = '<div class="verdict-head">' + badge("需要登录")
      + '</div><p class="placeholder"><a href="/auth/login/">先登录</a>后再提交。</p>';
    else { renderVerdict(data); loadHistory(historyAll); }
  } catch (err) {
    verdict.innerHTML = '<div class="verdict-head">' + badge("提交失败") + '</div><pre class="msg">' + esc(err) + "</pre>";
  }
  setBusy(false, "准备提交");
};

let historyAll = false;
let lastRows = [];
async function loadHistory(showAll = false) {
  const params = new URLSearchParams({ book: BOOK, problem: PROBLEM });
  if (!showAll) params.set("mine", "1");
  const r = await fetch("/api/submissions?" + params, { credentials: "same-origin" });
  if (r.status === 401) { histbox.textContent = "登录后可以看到提交记录。"; return; }
  lastRows = (await r.json()).submissions;
  if (!lastRows.length) { histbox.textContent = showAll ? "这道题还没有提交记录。" : "你还没有提交这道题。"; return; }
  const relativeTime = value => { const then = Date.parse(String(value).replace(" ", "T") + "Z"); if (Number.isNaN(then)) return value; const minutes = Math.max(0, Math.floor((Date.now() - then) / 60000)); if (minutes < 1) return "刚刚"; if (minutes < 60) return minutes + "分钟前"; const hours = Math.floor(minutes / 60); return hours < 24 ? hours + "小时前" : Math.floor(hours / 24) + "天前"; };
  histbox.innerHTML = "<table><thead><tr><th>提交人</th><th>结果</th><th>内存</th><th>时间</th><th>代码长度</th><th>语言</th><th>提交时间</th><th>代码/详情</th></tr></thead><tbody>"
    + lastRows.map(s => {
        const d = s.detail || {};
        const note = d.case !== undefined ? "第 " + d.case + " 组"
                   : d.cases !== undefined ? d.cases + " 组全过" : "";
        const memory = d.memory_kb !== undefined ? d.memory_kb + "kB" : "";
        const elapsed = d.time_ms !== undefined ? d.time_ms + "ms" : "";
        const size = d.source_bytes !== undefined ? d.source_bytes + " B" : (s.source ? new TextEncoder().encode(s.source).length + " B" : "");
        const code = s.source ? "<details><summary>查看代码</summary><pre class='msg source'>" + esc(s.source) + "</pre></details>" : "";
        const blocks = [];
        if (d.case !== undefined) blocks.push("<div><b>出错的数据组：</b>第 " + esc(d.case) + " 组</div>");
        if (d.expected_tokens !== undefined) blocks.push("<div><b>输出规模：</b>期望 " + esc(d.expected_tokens) + " 个 token，实际 " + esc(d.actual_tokens) + " 个</div>");
        if (d.message) blocks.push("<pre class='msg source'>" + esc(d.message) + "</pre>");
        if (d.failing_input) blocks.push("<pre class='msg source'>" + esc(d.failing_input.text || "") + "</pre>");
        if (d.expected_output) blocks.push("<pre class='msg source'>" + esc(d.expected_output.text || "") + "</pre>");
        const detail = blocks.length ? "<details" + (s.result === "Accepted" ? "" : " open") + "><summary>查看判题详情</summary>" + blocks.join("") + "</details>" : "";
        // 改动前这里只输出 7 个 <td> 而表头有 8 列：算好的 size 从未渲染，
        // 于是「代码长度」往右每一列都错位一格。补上它。
        return "<tr><td>" + esc(s.user || "") + "</td><td>" + badge(s.result)
             + "</td><td class='num muted'>" + esc(memory) + "</td><td class='num muted'>" + esc(elapsed)
             + "</td><td class='num muted'>" + esc(size)
             + "</td><td class='num muted'>" + esc((s.detail && s.detail.language_version) || s.language || "")
             + "</td><td class='num' title='" + esc(s.created) + "'>" + esc(relativeTime(s.created)) + "</td><td>" + code + detail + "<div class='muted'>" + esc(note) + "</div></td></tr>";
      }).join("") + "</tbody></table>";
}
historyToggle.addEventListener('click', () => {
  historyAll = !historyAll;
  historyToggle.textContent = historyAll ? '只看我的' : '看全部';
  loadHistory(historyAll);
});

// 统计只用这道题的提交记录算，不去拉整份 catalog（那是几百 KB）。
async function loadStats() {
  const params = new URLSearchParams({ book: BOOK, problem: PROBLEM, limit: "500" });
  const r = await fetch("/api/submissions?" + params, { credentials: "same-origin" });
  if (r.status === 401) { statsbox.textContent = "登录后可以看到统计。"; return; }
  const rows = (await r.json()).submissions;
  if (!rows.length) { statsbox.textContent = "这道题还没有提交记录。"; return; }
  const accepted = rows.filter(s => s.result === "Accepted");
  const solvers = new Set(accepted.map(s => (s.user || "").toLowerCase()));
  const people = new Set(rows.map(s => (s.user || "").toLowerCase()));
  const byStatus = new Map();
  for (const s of rows) byStatus.set(s.result, (byStatus.get(s.result) || 0) + 1);
  const cards = [
    ["提交次数", rows.length], ["通过次数", accepted.length],
    ["通过率", Math.round(accepted.length / rows.length * 100) + "%"],
    ["提交人数", people.size], ["通过人数", solvers.size],
  ];
  statsbox.innerHTML = '<div class="stat-grid">'
    + cards.map(c => '<div class="stat-card"><b>' + esc(c[1]) + "</b><span>" + esc(c[0]) + "</span></div>").join("")
    + '</div><table><thead><tr><th>结果</th><th>次数</th></tr></thead><tbody>'
    + [...byStatus].sort((a, b) => b[1] - a[1]).map(([k, v]) =>
        "<tr><td>" + badge(k) + "</td><td class='num'>" + v + "</td></tr>").join("")
    + "</tbody></table>";
}
</script></html>"""


def init_db():
    DB.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as db:
        db.execute("create table if not exists submissions (id integer primary key, user text, problem text, result text, created text default current_timestamp)")
        db.execute("create table if not exists users (username text primary key, password_hash text not null, created text default current_timestamp)")
        db.execute("create table if not exists settings (key text primary key, value text not null)")
        # 历史库里没有这几列；用 ALTER 补，已存在则跳过（create table if not exists 加不了列）。
        existing = {row[1] for row in db.execute("pragma table_info(submissions)")}
        for column in ("book text", "language text", "detail text", "source text"):
            if column.split()[0] not in existing:
                db.execute(f"alter table submissions add column {column}")
        user_columns = {row[1] for row in db.execute("pragma table_info(users)")}
        for column in ("email text", "active integer default 1", "activation_token_hash text", "activation_expires integer", "reset_token_hash text", "reset_expires integer"):
            if column.split()[0] not in user_columns:
                db.execute(f"alter table users add column {column}")
        db.execute("update users set active = 1 where activation_token_hash is null")

# 「出错那组的输入片段」开关。默认**关**：管理员忘了考前关掉是泄题，
# 忘了课后打开只是少点帮助——两种疏忽的代价不对称，所以默认取保守的一侧。
REVEAL_KEY = "reveal_failing_input"
SNIPPET_CHARS = 400
SNIPPET_LINES = 12


def get_setting(key, default=""):
    with sqlite3.connect(DB) as db:
        row = db.execute("select value from settings where key = ?", (key,)).fetchone()
    return row[0] if row else default


def set_setting(key, value):
    with sqlite3.connect(DB) as db:
        db.execute("insert into settings(key, value) values (?, ?)"
                   " on conflict(key) do update set value = excluded.value", (key, value))


BOOKS_KEY = "reveal_books"        # {book: "on"/"off"}，覆盖全局
WINDOWS_KEY = "reveal_windows"    # [{start, end, note}]，命中即强制关闭


def online_users(now=None):
    """最近 ONLINE_WINDOW_SECONDS 秒内有过请求的**不同用户数**。

    按用户名去重，不是按会话：同一个人开两个标签页是一个人。
    过期的打点顺手清掉，免得字典无限长。
    """
    now = time.time() if now is None else now
    for token, seen in list(SESSION_SEEN.items()):
        if token not in TOKENS or now - seen > ONLINE_WINDOW_SECONDS:
            SESSION_SEEN.pop(token, None)
    return len({SESSION_USERS.get(token) for token in SESSION_SEEN
                if SESSION_USERS.get(token)})


def site_stats():
    """站点统计。**每一个数都由数据算出来。**

    这里原来写着 `"accepted": 1284, "streak": 12` —— 两个凭空编的数字。
    当时没有任何页面调用 /api/stats，所以没人看见；但只要有人把它接上去，
    站上就会对学生显示编造的成绩。假数字不会因为暂时没人看就变得无害。
    `streak` 已删掉：没有任何数据能算出它，与其编一个不如不给。
    """
    with sqlite3.connect(DB) as db:
        submissions = db.execute("select count(*) from submissions").fetchone()[0]
        accepted = db.execute(
            "select count(*) from submissions where result = 'Accepted'").fetchone()[0]
        solved = db.execute(
            "select count(distinct problem) from submissions where result = 'Accepted'").fetchone()[0]
        users = db.execute("select count(*) from users").fetchone()[0]
    return {"submissions": submissions, "accepted": accepted, "solved_problems": solved,
            "users": users, "online": online_users(),
            "online_window_seconds": ONLINE_WINDOW_SECONDS}


def reveal_enabled():
    """全局默认：**展示失败那组的输入片段**（人拍板 2026-07-27，选了「帮助最大」这一档）。

    取舍是清楚的：露出输入，学生就可能照着硬编码；不露，WA 时他只看得到
    「第 N 组错了、期望 1 个 token、实际 1 个 token」，等于没有反馈——
    而这个项目的本意就是「编写→提交→**反馈错在哪组数据**」。

    两道闸没变，仍然管用：**考试时段内一票否决**（`active_window`），
    以及**按题库覆盖**。想临时关掉某个题库或整场考试，都不用改这里。
    """
    return get_setting(REVEAL_KEY, "on") == "on"


def _json_setting(key, fallback):
    try:
        value = json.loads(get_setting(key, fallback))
    except json.JSONDecodeError:
        return json.loads(fallback)
    return value if type(value) is type(json.loads(fallback)) else json.loads(fallback)


def reveal_books():
    return _json_setting(BOOKS_KEY, "{}")


def reveal_windows():
    return _json_setting(WINDOWS_KEY, "[]")


def active_window(now=None):
    """命中的考试时段。时段只能让结果更严，不能更松——加时段永远不会意外放开。"""
    now = now or datetime.now()
    for window in reveal_windows():
        try:
            start = datetime.fromisoformat(window["start"])
            end = datetime.fromisoformat(window["end"])
        except (KeyError, TypeError, ValueError):
            # 坏条目一律视为命中（宁可误关，不可误开）：按「不命中」处理的话，
            # 一条被手改坏的时段会静默失去考试保护，而误关是看得见、可修的。
            return {"start": "?", "end": "?", "note": "时段配置损坏，已按考试模式处理",
                    "malformed": True, "raw": window}
        if start <= now <= end:
            return window
    return None


def reveal_effective(book, now=None):
    """某题库此刻是否展示片段：考试时段一票否决，其次题库覆盖，最后全局默认。"""
    if active_window(now) is not None:
        return False
    override = reveal_books().get(book)
    if override in ("on", "off"):
        return override == "on"
    return reveal_enabled()


def failing_input_snippet(book, problem_id, case_index):
    """取出错那组的输入片段。只给输入，绝不给期望输出——那是答案。"""
    catalog_path = MIRROR / "catalog.json"
    if not catalog_path.is_file():
        return None
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    item = next((p for p in catalog["problems"] if p["book"] == book and p["id"] == problem_id), None)
    cases = (item or {}).get("test_cases") or []
    if not 1 <= case_index <= len(cases):
        return None
    path = MIRROR / cases[case_index - 1]["input"]
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    clipped = "\n".join(lines[:SNIPPET_LINES])
    truncated = len(lines) > SNIPPET_LINES or len(clipped) > SNIPPET_CHARS
    return {"text": clipped[:SNIPPET_CHARS], "truncated": truncated,
            "total_lines": len(lines), "total_chars": len(text)}

def failing_output_snippet(book, problem_id, case_index):
    """Read the expected .out for the failing case and cap only the UI payload."""
    catalog_path = MIRROR / "catalog.json"
    if not catalog_path.is_file():
        return None
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    item = next((p for p in catalog["problems"] if p["book"] == book and p["id"] == problem_id), None)
    cases = (item or {}).get("test_cases") or []
    if not 1 <= case_index <= len(cases):
        return None
    path = MIRROR / cases[case_index - 1]["output"]
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    return {"text": text[:4000], "truncated": len(text) > 4000,
            "total_lines": len(text.splitlines()), "total_chars": len(text)}

def catalog_title(item):
    """Read the real heading from the mirrored statement, once per process."""
    key = (item.get("book", ""), item.get("id", ""))
    if key in CATALOG_TITLE_CACHE:
        return CATALOG_TITLE_CACHE[key]
    page = MIRROR / "pages" / f"{key[0]}__{key[1]}.html"
    title = key[1]
    if page.is_file():
        text = page.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'<div id="pageTitle"><h2>(.*?)</h2>', text, re.S)
        if match:
            title = re.sub(r"<[^>]+>", "", unescape(match.group(1))).strip() or title
    CATALOG_TITLE_CACHE[key] = title
    return title


def catalog_raw():
    """Read the catalog once per file version instead of once per request."""
    global CATALOG_RAW_CACHE, CATALOG_RAW_MTIME, CATALOG_FULL_CACHE
    catalog_path = MIRROR / "catalog.json"
    if not catalog_path.is_file():
        return {"problems": []}
    mtime = catalog_path.stat().st_mtime_ns
    if CATALOG_RAW_CACHE is None or CATALOG_RAW_MTIME != mtime:
        CATALOG_RAW_CACHE = json.loads(catalog_path.read_text(encoding="utf-8"))
        CATALOG_RAW_MTIME = mtime
        CATALOG_FULL_CACHE = None
    return CATALOG_RAW_CACHE


def catalog_full_payload():
    """Build the complete directory response only once per catalog version."""
    global CATALOG_FULL_CACHE
    if CATALOG_FULL_CACHE is None:
        raw = catalog_raw()
        problems = raw.get("problems", [])
        def problem_key(item):
            match = re.search(r"(\d+)$", item.get("id", ""))
            return int(match.group(1)) if match else (item.get("book", ""), item.get("id", ""))
        all_keys = {problem_key(item) for item in problems}
        tested_keys = {problem_key(item) for item in problems if (item.get("test_count") or 0) > 0}
        CATALOG_FULL_CACHE = {
            **raw,
            "problems": [{**item, "title": catalog_title(item)} for item in problems],
            "unique_total": len(all_keys),
            "unique_tested_count": len(tested_keys),
            "book_meta": BOOK_META,
        }
    with sqlite3.connect(DB) as db:
        local_stats = {
            (row[0] or "", row[1] or ""): {
                "accepted_count": row[3],
                "attempt_count": row[2],
                "pass_rate": f"{row[3] / row[2] * 100:.1f}%" if row[2] else "—",
            }
            for row in db.execute(
                """select book, problem,
                          count(distinct lower(user)),
                          count(distinct case when result = 'Accepted' then lower(user) end)
                     from submissions group by book, problem"""
            )
        }
    return {
        **CATALOG_FULL_CACHE,
        "problems": [
            {**item, **local_stats.get((item.get("book", ""), item.get("id", "")), {
                "pass_rate": "—", "accepted_count": 0, "attempt_count": 0,
            })}
            for item in CATALOG_FULL_CACHE["problems"]
        ],
    }


def catalog_summary_payload():
    """Return only the fields needed by the fast homepage catalog."""
    raw = catalog_raw()
    problems = raw.get("problems", [])
    def problem_key(item):
        match = re.search(r"(\d+)$", item.get("id", ""))
        return int(match.group(1)) if match else (item.get("book", ""), item.get("id", ""))

    all_keys = {problem_key(item) for item in problems}
    tested_keys = {problem_key(item) for item in problems if (item.get("test_count") or 0) > 0}
    return {
        "total": len(all_keys),
        "tested_count": len(tested_keys),
        "problems": [
            {
                "book": item.get("book", ""),
                "id": item.get("id", ""),
                "path": item.get("path", ""),
                "test_count": item.get("test_count", 0),
                "title": catalog_title(item),
            }
            for item in problems if (item.get("test_count") or 0) >= 5
        ],
        "book_meta": BOOK_META,
    }


def password_hash(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"cs101-local-user", 120000).hex()


def same_username(left, right):
    return str(left).strip().casefold() == str(right).strip().casefold()

def valid_password(stored, password):
    return stored == password_hash(password)

def new_captcha():
    left, right = secrets.randbelow(8) + 2, secrets.randbelow(8) + 2
    token = secrets.token_urlsafe(18)
    CAPTCHA_CHALLENGES[token] = (str(left + right), time.time() + 600)
    return token, f"{left} + {right} = ?"

def valid_captcha(token, answer):
    challenge = CAPTCHA_CHALLENGES.pop(str(token), None)
    if not challenge or challenge[1] < time.time():
        return False
    return hmac.compare_digest(challenge[0], str(answer).strip())

def reset_token_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()

def send_account_email(recipient, subject, body):
    smtp_host = os.environ.get("CS101_SMTP_HOST")
    if not smtp_host:
        return False
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ.get("CS101_SMTP_FROM", os.environ.get("CS101_SMTP_USER", ""))
    message["To"] = recipient
    message.set_content(body)
    try:
        port = int(os.environ.get("CS101_SMTP_PORT", "465"))
        smtp_class = smtplib.SMTP_SSL if port == 465 else smtplib.SMTP
        with smtp_class(smtp_host, port, timeout=15) as smtp:
            if port != 465:
                smtp.starttls()
            user, password = os.environ.get("CS101_SMTP_USER"), os.environ.get("CS101_SMTP_PASSWORD")
            if user and password:
                smtp.login(user, password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException, ValueError):
        return False
    return True


def public_base_url():
    """Return the address users on the LAN can open from emailed links."""
    return os.environ.get("CS101_PUBLIC_URL", DEFAULT_PUBLIC_URL).rstrip("/")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _touch(self, token_value):
        """记一次「这个会话此刻还活着」。在线数只认这个，不认 TOKENS 的大小。"""
        if token_value in TOKENS:
            SESSION_SEEN[token_value] = time.time()

    def authorized(self):
        raw = self.headers.get("Cookie", "")
        jar = cookies.SimpleCookie(raw)
        token = jar.get("session")
        if token is None or token.value not in TOKENS:
            return False
        self._touch(token.value)
        return True

    def current_user(self):
        raw = self.headers.get("Cookie", "")
        token = cookies.SimpleCookie(raw).get("session")
        if not token or token.value not in TOKENS:
            return None
        self._touch(token.value)
        return SESSION_USERS.get(token.value)

    def send_html(self, body):
        if isinstance(body, str): body = body.encode("utf-8")
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def send_static(self, file, content_type):
        body = file.read_bytes()
        self.send_response(200); self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def local_page(self, page):
        text = page.read_text(encoding="utf-8", errors="replace")
        text = text.replace("http://cs101.openjudge.cn/", "/")
        text = text.replace("https://cs101.openjudge.cn/", "/")
        text = text.replace("http://cs101.openjudge.cn", "/")
        text = text.replace("https://cs101.openjudge.cn", "/")
        return text

    def problem_parts(self, page, book, problem):
        text = self.local_page(page)
        title_match = re.search(r'<div id="pageTitle"><h2>(.*?)</h2>', text, re.S)
        title_html = title_match.group(1).strip() if title_match else f"{problem} 题目"
        title = re.sub(r"<[^>]+>", "", unescape(title_html)).strip()
        params = re.search(r'<dl class="problem-params">(.*?)</dl>', text, re.S)
        content = re.search(r'<dl class="problem-content">(.*?)</dl>', text, re.S)
        stats = re.search(r'<div class="problem-statistics[^>]*>.*?<dl>(.*?)</dl>', text, re.S)
        params_html = params.group(1).strip() if params else ""
        content_html = content.group(1).strip() if content else "<dt>提示</dt><dd>题面暂未解析。</dd>"
        stats_html = stats.group(1).strip() if stats else ""
        return title, params_html, content_html, stats_html

    def sample_io(self, page):
        """题面里的样例输入/输出，给「运行样例」用。

        服务端出这份数据而不是让前端去刮 DOM：镜像页的结构是已知的，
        全部 1849 页都恰有一组 `样例输入`/`样例输出`（构建本功能前逐页验过），
        在这里解析一次比在浏览器里猜 DOM 稳。
        """
        text = self.local_page(page)
        match = re.search(r'<dt>样例输入</dt>\s*<dd>(.*?)</dd>\s*<dt>样例输出</dt>\s*<dd>(.*?)</dd>',
                          text, re.S)
        if not match:
            return {"input": "", "output": "", "cases": []}
        def plain(chunk):
            chunk = re.sub(r"</?pre[^>]*>", "", chunk.strip())
            return unescape(re.sub(r"<[^>]+>", "", chunk)).strip("\n")
        raw_input, raw_output = plain(match.group(1)), plain(match.group(2))
        cases = []
        if SAMPLE_ANY.search(raw_input) or SAMPLE_ANY.search(raw_output):
            # 标注式题面里两个 <dl> 的分工是乱的：T27237 把样例 1 的输入和输出
            # 一起塞进「样例输入」，样例 2 整组塞进「样例输出」。所以合起来再切。
            cases = parse_sample_sections(raw_input + "\n" + raw_output)
        if not cases:
            cases = [{"input": raw_input, "output": raw_output}]
        return {"input": cases[0]["input"], "output": cases[0]["output"], "cases": cases}

    def submission_page(self, page, book, problem):
        title, params_html, content_html, _ = self.problem_parts(page, book, problem)
        language_options = "".join(
            f'<option value="{key}">{escape(language_version(key))}</option>'
            for key in ("python", "pypy3", "cpp", "c", "csharp", "fsharp", "vbnet", "swift", "objc")
        )
        return (SUBMIT_PAGE.replace("__BOOK__", escape(book))
                .replace("__BOOK_NAME__", escape(BOOK_META.get(book, {}).get("name", book)))
                .replace("__PROBLEM__", escape(problem))
                .replace("__LANGUAGE_OPTIONS__", language_options)
                .replace("__STATEMENT_TITLE__", escape(title))
                .replace("__STATEMENT_PARAMS__", params_html)
                .replace("__SAMPLE_JSON__", json.dumps(self.sample_io(page), ensure_ascii=False)
                         .replace("</", "<\\/"))
                .replace("__STATEMENT_CONTENT__", content_html))

    def help_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>说明 · CS101</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){try{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();</script><style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:820px;margin:auto;padding:0 24px}.top{height:72px;display:flex;align-items:center;justify-content:space-between}.brand{display:flex;gap:11px;align-items:center;text-decoration:none;color:var(--ink);font-weight:750}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg)}.back{color:var(--green);text-decoration:none}.panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:30px 34px;box-shadow:0 12px 34px rgba(34,63,45,.06)}h1{font-size:30px;margin:0 0 7px}h2{font-size:18px;margin:28px 0 8px;padding-top:20px;border-top:1px solid var(--line)}p{color:var(--muted)}.rule{padding:14px 16px;border-left:3px solid var(--warn);background:var(--soft);color:var(--ink)}code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);padding:2px 5px;border-radius:4px}@media(max-width:600px){.shell{padding:0 16px}.panel{padding:24px 20px}.top{height:62px}}
</style></head><body><header class="top shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><a class="back" href="/">返回首页</a></header><main class="shell"><section class="panel"><h1>帮助/说明</h1><p>这里使用本机测试数据判题，提交页右侧选择语言后即可提交代码并查看每组数据的结果。</p><h2>时间与内存倍率</h2><div class="rule">Python ×10 · PyPy3 ×3 · C/C++/Swift/Objective-C ×1 · C#/F#/VB.NET ×2<br>C#/F#/VB.NET 内存 ×2</div><h2>题面限制的含义</h2><p>题面显示的时限按 C/C++ 计算，是全部测试点限时之和。其他语言按照上面的倍率执行；内存限制仅对 C#、F#、VB.NET 按 2 倍计算。</p><h2>提交结果</h2><p>提交记录会保留提交人、结果、语言、运行时间、内存和代码。出现错误时，判题详情会标出出错的数据组，并展示对应的输入、期望输出和实际输出。</p></section></main></body></html>"""

    def account_page(self, register=False):
        title = "注册 CS101 账号" if register else "登录 CS101"
        captcha_token, captcha_question = new_captcha() if register else ("", "")
        fields = f"""<label>邮箱地址<input name="email" type="email" required autocomplete="email" placeholder="name@example.com"></label>
<label>用户名<input name="username" required minlength="2" maxlength="32" autocomplete="username"></label>
<label>密码<input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
<label>确认密码<input name="confirm_password" type="password" required minlength="8" autocomplete="new-password"></label>
<label>人机验证 <span class="captcha-question">{escape(captcha_question)}</span><input name="captcha_answer" inputmode="numeric" required placeholder="请输入计算结果"><input type="hidden" name="captcha_token" value="{captcha_token}"></label>""" if register else """<label>用户名<input name="username" required autocomplete="username"></label>
<label>密码<input name="password" type="password" required autocomplete="current-password"></label>"""
        endpoint = "/api/user/register" if register else "/api/user/login"
        links = "<a href='/auth/login/'>已有账号？登录</a>" if register else "<a href='/auth/forgot/'>忘记密码？</a> · <a href='/register/'>点此注册</a>"
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){{try{{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}}catch(e){{document.documentElement.dataset.theme='light';}}}})();</script><style>
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}.shell{{max-width:460px;margin:0 auto;padding:70px 20px}}.brand{{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}}.mark{{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}}.panel{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}}h1{{font-size:28px;line-height:1.2;margin:0 0 6px}}.intro{{color:var(--muted);margin:0 0 23px}}label{{display:block;margin:16px 0 6px;font-weight:600}}input{{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;background:var(--panel);font:inherit;outline:none}}input:focus{{border-color:var(--green);box-shadow:0 0 0 3px var(--accent-soft)}}button{{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}}a{{color:var(--green)}}.links{{margin:19px 0 0;color:var(--muted);font-size:14px;text-align:center}}.error{{min-height:22px;color:var(--red);margin:12px 0 0}}.captcha-question{{display:inline-block;margin-left:5px;color:var(--green);font-family:ui-monospace,monospace}}@media(max-width:520px){{.shell{{padding:35px 16px}}.panel{{padding:24px}}}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><h1>{title}</h1><p class="intro">{'创建账号后即可提交代码并查看判题记录。' if register else '登录后继续使用提交与判题功能。'}</p><form id="account">{fields}<p id="error" class="error"></p><button>提交</button></form><p class="links">{links} · <a href="/">返回首页</a></p></section></main><script>const form=document.querySelector('#account'),error=document.querySelector('#error');form.onsubmit=async e=>{{e.preventDefault();error.textContent='';const data=Object.fromEntries(new FormData(form));if(data.confirm_password!==undefined&&data.password!==data.confirm_password){{error.textContent='两次输入的密码不一致';return}}const r=await fetch('{endpoint}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}});const d=await r.json();if(r.ok){{if(d.activation_link){{error.style.color='#237a50';error.innerHTML='注册成功，请点击激活链接：<a href="'+d.activation_link+'">激活账号</a>';form.querySelector('button').disabled=true}}else location.href='/'}}else error.textContent=d.error||'操作失败'}};</script></body></html>"""

    def activation_page(self, token):
        with sqlite3.connect(DB) as db:
            row = db.execute("select username from users where activation_token_hash = ? and activation_expires > ? and active = 0",
                             (reset_token_hash(token), int(time.time()))).fetchone()
            if row:
                db.execute("update users set active = 1, activation_token_hash = null, activation_expires = null where username = ?", (row[0],))
                message, detail = "账号已激活", "现在可以登录 CS101 题库。"
            else:
                message, detail = "激活链接无效或已过期", "请重新注册或联系管理员。"
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{message} · CS101</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){{try{{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}}catch(e){{document.documentElement.dataset.theme='light';}}}})();</script><style>body{{margin:0;background:#f4f7f4;color:#16231d;font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:#fff;border:1px solid #dfe7e1;border-radius:10px;padding:30px}}h1{{margin:0 0 10px}}p{{color:#6c7b73}}a{{color:#237a50}}</style></head><body><main><section><h1>{message}</h1><p>{detail}</p><p><a href="/auth/login/">前往登录</a></p></section></main></body></html>"""

    def forgot_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>找回密码 · CS101</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){try{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();</script><style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:460px;margin:0 auto;padding:70px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}h1{font-size:28px;line-height:1.2;margin:0 0 6px}.intro{color:var(--muted);margin:0 0 23px}label{display:block;margin:16px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;font:inherit;outline:none}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}a{color:var(--green)}.message{color:var(--muted);margin-top:15px;word-break:break-word}@media(max-width:520px){.shell{padding:35px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><h1>忘记密码？</h1><p class="intro">输入注册邮箱，我们会生成一次性密码重置链接。</p><form id="forgot"><label>邮箱地址<input name="email" type="email" required autocomplete="email"></label><button>发送重置链接</button></form><p id="message" class="message"></p><p><a href="/auth/login/">返回登录</a> · <a href="/register/">点此注册</a></p></section></main><script>forgot.onsubmit=async e=>{e.preventDefault();message.textContent='正在处理…';const r=await fetch('/api/user/forgot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(forgot)))});const d=await r.json();message.innerHTML=d.reset_link?'邮件服务尚未配置，请使用本机重置链接：<a href="'+d.reset_link+'">立即重置密码</a>':'如果该邮箱已注册，重置链接已发送或正在等待管理员配置邮件服务。';}</script></body></html>"""

    def reset_page(self, token):
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>重置密码 · CS101</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){{try{{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}}catch(e){{document.documentElement.dataset.theme='light';}}}})();</script><style>body{{margin:0;background:#f4f7f4;color:#16231d;font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:#fff;border:1px solid #dfe7e1;border-radius:10px;padding:30px}}h1{{margin:0 0 20px}}label{{display:block;margin:14px 0 6px;font-weight:600}}input{{width:100%;padding:11px;box-sizing:border-box;border:1px solid var(--line);border-radius:6px;font:inherit}}button{{width:100%;margin-top:20px;padding:11px;background:#16231d;color:var(--bg);border:0;border-radius:6px;font:inherit}}a{{color:#237a50}}#message{{color:#b04f43}}</style></head><body><main><section><h1>设置新密码</h1><form id="reset"><label>新密码<input name="password" type="password" minlength="8" required autocomplete="new-password"></label><label>确认密码<input name="confirm_password" type="password" minlength="8" required autocomplete="new-password"></label><p id="message"></p><button>保存新密码</button></form><p><a href="/auth/login/">返回登录</a></p></section></main><script>reset.onsubmit=async e=>{{e.preventDefault();message.textContent='';const d=Object.fromEntries(new FormData(reset));if(d.password!==d.confirm_password){{message.textContent='两次输入的密码不一致';return}}d.token={json.dumps(token)};const r=await fetch('/api/user/reset',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});const x=await r.json();if(r.ok){{message.style.color='#237a50';message.textContent='密码已更新，请返回登录。';reset.querySelector('button').disabled=true}}else message.textContent=x.error||'重置失败'}};</script></body></html>"""

    def account_settings_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>账户设置 · CS101</title>
<link rel="stylesheet" href="/static/theme.css"><script>(function(){try{var t=localStorage.getItem('cs101-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();</script><style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:520px;margin:0 auto;padding:52px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:24px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}.topline{display:flex;justify-content:space-between;align-items:start;gap:15px;margin-bottom:22px}h1{font-size:28px;line-height:1.2;margin:0 0 5px}.muted{color:var(--muted);margin:0}.back{color:var(--green);text-decoration:none;font-size:14px}h2{font-size:16px;margin:0 0 14px;padding-top:22px;border-top:1px solid var(--line)}label{display:block;margin:14px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;font:inherit;outline:none}input:focus{border-color:var(--green);box-shadow:0 0 0 3px var(--accent-soft)}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}.message{min-height:22px;color:var(--red);margin:12px 0 0}.logout{display:block;width:100%;margin-top:12px;padding:10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);font:inherit;cursor:pointer}@media(max-width:520px){.shell{padding:30px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><div class="topline"><div><h1>账户设置</h1><p id="user" class="muted">正在读取账户…</p></div><a class="back" href="/">返回首页</a></div><h2>修改密码</h2><form id="change"><label>当前密码<input name="current_password" type="password" required autocomplete="current-password"></label><label>新密码<input name="new_password" type="password" minlength="8" required autocomplete="new-password"></label><label>确认新密码<input name="confirm_password" type="password" minlength="8" required autocomplete="new-password"></label><p id="message" class="message"></p><button>保存新密码</button></form><button id="logout" class="logout">退出登录</button></section></main><script>
fetch('/api/me').then(r=>r.json()).then(d=>{if(!d.authenticated)location.href='/auth/login/';else user.textContent='用户名：'+d.user}).catch(()=>location.href='/auth/login/');
change.onsubmit=async e=>{e.preventDefault();message.textContent='';const d=Object.fromEntries(new FormData(change));if(d.new_password!==d.confirm_password){message.textContent='两次输入的新密码不一致';return}const r=await fetch('/api/user/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const x=await r.json();if(r.ok){message.style.color='#237a50';message.textContent='密码已更新。';change.reset()}else message.textContent=x.error||'修改失败'};
logout.onclick=async()=>{await fetch('/api/logout',{method:'POST'});location.href='/'};
</script></body></html>"""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        decoded_path = unquote(path)
        if any(part == ".." for part in decoded_path.split("/")):
            self.send_json({"error": "Not found"}, 404); return
        if path == "/auth/login/":
            self.send_html(self.account_page()); return
        if path == "/register/":
            self.send_html(self.account_page(register=True)); return
        if path == "/auth/forgot/":
            self.send_html(self.forgot_page()); return
        if path == "/auth/activate/":
            token = parse_qs(parsed.query).get("token", [""])[0]
            self.send_html(self.activation_page(token)); return
        if path == "/auth/reset/":
            token = parse_qs(parsed.query).get("token", [""])[0]
            self.send_html(self.reset_page(token)); return
        if path == "/help/":
            self.send_html(self.help_page()); return
        if path == "/account/":
            if not self.authorized():
                self.send_response(302); self.send_header("Location", "/auth/login/"); self.end_headers(); return
            self.send_html(self.account_settings_page()); return
        submit_page = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/([^/]+)/submit/", path)
        if submit_page:
            book, problem_id = submit_page.groups()
            page = MIRROR / "pages" / f"{book}__{problem_id}.html"
            if page.is_file():
                self.send_html(self.submission_page(page, book, problem_id)); return
        local_book = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/", path)
        if local_book:
            page_number = parse_qs(parsed.query).get("page", ["1"])[0]
            page = MIRROR / "books" / f"{local_book.group(1)}__{page_number}.html"
            if page.is_file():
                self.send_html(self.local_page(page)); return
        local_problem = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/([^/]+)/", path)
        if local_problem:
            book, problem = local_problem.groups()
            page = MIRROR / "pages" / f"{book}__{problem}.html"
            if page.is_file():
                self.send_html(self.submission_page(page, book, problem)); return
        if path == "/api/course":
            self.send_json({"course": COURSE, "problems": PROBLEMS, "authenticated": self.authorized()})
            return
        if path == "/api/me":
            self.send_json({"authenticated": self.authorized(), "user": self.current_user()})
            return
        if path == "/api/stats":
            self.send_json(site_stats())
            return
        if path == "/api/settings":
            book = parse_qs(parsed.query).get("book", [""])[0]
            self.send_json({REVEAL_KEY: reveal_enabled(), "books": reveal_books(),
                            "windows": reveal_windows(), "active_window": active_window(),
                            "effective": reveal_effective(book) if book else None,
                            "is_admin": same_username(self.current_user() or "", ADMIN_USER)})
            return
        if path in ("/admin", "/admin/"):
            page = ROOT / "admin.html"
            if page.is_file():
                self.send_html(page.read_text(encoding="utf-8")); return
        if path == "/api/submissions":
            user = self.current_user()
            if user is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            mine = parse_qs(parsed.query).get("mine", [""])[0] == "1"
            query_book = parse_qs(parsed.query).get("book", [""])[0]
            query_problem = parse_qs(parsed.query).get("problem", [""])[0]
            try:
                limit = min(max(int(parse_qs(parsed.query).get("limit", ["50"])[0]), 1), 500)
            except ValueError:
                limit = 50
            with sqlite3.connect(DB) as db:
                filters, values = [], []
                if query_book:
                    filters.append("book = ?"); values.append(query_book)
                if query_problem:
                    filters.append("problem = ?"); values.append(query_problem)
                if mine:
                    filters.append("lower(user) = lower(?)"); values.append(user)
                else:
                    pass
                where = (" where " + " and ".join(filters)) if filters else ""
                rows = db.execute("select user, problem, result, created, book, language, detail, source from submissions"
                                  + where + " order by id desc limit ?", (*values, limit)).fetchall()
            is_admin = same_username(user, ADMIN_USER)
            self.send_json({"user": user, "submissions": [
                {"user": r[0], "problem": r[1], "result": r[2], "created": r[3], "book": r[4], "language": r[5],
                 "detail": json.loads(r[6]) if r[6] and (is_admin or same_username(r[0] or "", user)) else {},
                 "source": (r[7] or "") if (is_admin or same_username(r[0] or "", user)) else ""} for r in rows]})
            return
        if path in ("/history", "/history/"):
            page = ROOT / "history.html"
            if page.is_file():
                self.send_html(page.read_text(encoding="utf-8")); return
        if path in ("/problems", "/problems/"):
            page = ROOT / "problems.html"
            if page.is_file():
                self.send_html(page.read_text(encoding="utf-8")); return
        if path == "/api/catalog":
            if parse_qs(parsed.query).get("summary") == ["1"]:
                self.send_json(catalog_summary_payload()); return
            self.send_json(catalog_full_payload()); return
        # 静态分发只有两条出口：首页，和 static/ 下的白名单后缀。
        # 改动前这里是 `ROOT / decoded_path`，只要文件在 ROOT 底下就发 ——
        # `ROOT in file.parents` 防的是「逃出 ROOT」，防不住「ROOT 里的东西不该全公开」。
        # 实测 GET /data/course.db 能下到整个 SQLite 库（口令哈希 + 全部提交），
        # GET /data/.admin_password 走的是同一条路径。.gitignore 挡的是 git，不是 HTTP。
        if path in ("/", ""):
            file = ROOT / "index.html"
            if file.is_file():
                self.send_static(file, "text/html; charset=utf-8"); return
        if decoded_path.startswith("/static/"):
            file = (STATIC_DIR / decoded_path[len("/static/"):]).resolve()
            # resolve() 之后再判包含，符号链接就指不出 static/ 了
            if STATIC_DIR in file.parents and file.is_file() and file.suffix in STATIC_TYPES:
                self.send_static(file, STATIC_TYPES[file.suffix]); return
        # Keep the real OpenJudge URL space usable locally: problem, login,
        # statistics, search, and contest pages are fetched through this host.
        try:
            upstream = urllib.request.Request("http://cs101.openjudge.cn" + self.path, headers={"User-Agent": "CS101 local mirror"})
            with urllib.request.urlopen(upstream, timeout=15) as response:
                body = response.read()
                content_type = response.headers.get("Content-Type", "text/html; charset=UTF-8")
            if "text/html" in content_type:
                text = body.decode("utf-8", errors="replace")
                text = text.replace("http://cs101.openjudge.cn", "")
                text = text.replace("https://cs101.openjudge.cn", "")
                body = text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        except (urllib.error.URLError, TimeoutError):
            pass
        self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        size = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(size)
        if "application/x-www-form-urlencoded" in self.headers.get("Content-Type", ""):
            data = {key: values[0] for key, values in parse_qs(raw.decode("utf-8", errors="replace")).items()}
        else:
            try: data = json.loads(raw or b"{}")
            except json.JSONDecodeError: self.send_json({"error": "Invalid JSON"}, 400); return
        if path == "/api/user/register":
            email = str(data.get("email", "")).strip().lower()
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", email):
                self.send_json({"error": "请输入有效的邮箱地址"}, 400); return
            if len(username) < 2 or len(username) > 32 or not re.fullmatch(r"[\w\u4e00-\u9fff-]+", username):
                self.send_json({"error": "用户名需为 2-32 个字母、数字、下划线、中文或短横线"}, 400); return
            if len(password) < 8:
                self.send_json({"error": "密码至少需要 8 位"}, 400); return
            if password != str(data.get("confirm_password", "")):
                self.send_json({"error": "两次输入的密码不一致"}, 400); return
            if not valid_captcha(data.get("captcha_token", ""), data.get("captcha_answer", "")):
                self.send_json({"error": "人机验证失败，请刷新注册页面后重试"}, 400); return
            if same_username(username, ADMIN_USER):
                self.send_json({"error": "该用户名不可注册"}, 409); return
            activation_token = secrets.token_urlsafe(32)
            try:
                with sqlite3.connect(DB) as db:
                    if db.execute("select 1 from users where lower(username) = lower(?) or lower(email) = ?", (username, email)).fetchone():
                        self.send_json({"error": "用户名或邮箱已存在"}, 409); return
                    db.execute("insert into users(username, password_hash, email, active, activation_token_hash, activation_expires) values (?, ?, ?, 0, ?, ?)",
                               (username, password_hash(password), email, reset_token_hash(activation_token), int(time.time()) + 86400))
            except sqlite3.IntegrityError:
                self.send_json({"error": "用户名或邮箱已存在"}, 409); return
            base = public_base_url()
            activation_link = f"{base}/auth/activate/?token={activation_token}"
            sent = send_account_email(email, "激活你的 CS101 账号", f"请在 24 小时内点击以下链接激活账号：\n{activation_link}\n")
            self.send_json({"ok": True} if sent else {"ok": True, "activation_link": activation_link}); return
        if path == "/api/user/login":
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            accepted = same_username(username, ADMIN_USER) and password == ADMIN_PASSWORD
            session_user = ADMIN_USER if accepted else None
            if not accepted:
                with sqlite3.connect(DB) as db:
                    row = db.execute("select username, password_hash, active from users where lower(username) = lower(?)", (username,)).fetchone()
                    accepted = row is not None and valid_password(row[1], password)
                    if accepted:
                        session_user = row[0]
                        active = row[2]
                        if not active:
                            self.send_json({"error": "账号尚未激活，请先点击邮箱中的激活链接"}, 403); return
            if not accepted:
                self.send_json({"error": "用户名或密码不正确"}, 401); return
            token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = session_user; SESSION_SEEN[token] = time.time()
            self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/"); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
        if path == "/api/user/change-password":
            username = self.current_user()
            if username is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            if same_username(username, ADMIN_USER):
                self.send_json({"error": "管理员密码由 CS101_ADMIN_PASSWORD 或密码文件管理"}, 403); return
            current = str(data.get("current_password", ""))
            new_password = str(data.get("new_password", ""))
            if len(new_password) < 8:
                self.send_json({"error": "密码至少需要 8 位"}, 400); return
            if new_password != str(data.get("confirm_password", "")):
                self.send_json({"error": "两次输入的新密码不一致"}, 400); return
            with sqlite3.connect(DB) as db:
                row = db.execute("select password_hash from users where username = ?", (username,)).fetchone()
                if not row or not valid_password(row[0], current):
                    self.send_json({"error": "当前密码不正确"}, 400); return
                db.execute("update users set password_hash = ? where username = ?", (password_hash(new_password), username))
            self.send_json({"ok": True}); return
        if path == "/api/user/forgot":
            email = str(data.get("email", "")).strip().lower()
            generic = {"ok": True}
            with sqlite3.connect(DB) as db:
                row = db.execute("select username from users where email = ?", (email,)).fetchone()
                if row:
                    token = secrets.token_urlsafe(32)
                    db.execute("update users set reset_token_hash = ?, reset_expires = ? where email = ?",
                               (reset_token_hash(token), int(time.time()) + 1800, email))
            if not row:
                self.send_json(generic); return
            base = public_base_url()
            link = f"{base}/auth/reset/?token={token}"
            smtp_host = os.environ.get("CS101_SMTP_HOST")
            if smtp_host:
                if not send_account_email(email, "CS101 密码重置", f"请在 30 分钟内打开以下链接重置 CS101 密码：\n{link}\n"):
                    self.send_json({"error": "邮件发送失败，请稍后重试"}, 503); return
                self.send_json(generic); return
            self.send_json({"ok": True, "reset_link": link}); return
        if path == "/api/user/reset":
            token = str(data.get("token", ""))
            password, confirmation = str(data.get("password", "")), str(data.get("confirm_password", ""))
            if len(password) < 8:
                self.send_json({"error": "密码至少需要 8 位"}, 400); return
            if password != confirmation:
                self.send_json({"error": "两次输入的密码不一致"}, 400); return
            with sqlite3.connect(DB) as db:
                row = db.execute("select username from users where reset_token_hash = ? and reset_expires > ?",
                                 (reset_token_hash(token), int(time.time()))).fetchone()
                if not row:
                    self.send_json({"error": "重置链接无效或已过期"}, 400); return
                db.execute("update users set password_hash = ?, reset_token_hash = null, reset_expires = null where username = ?",
                           (password_hash(password), row[0]))
            self.send_json({"ok": True}); return
        if path == "/api/login":
            if same_username(data.get("username", ""), ADMIN_USER) and data.get("password") == ADMIN_PASSWORD:
                token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = ADMIN_USER; SESSION_SEEN[token] = time.time()
                self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/")
                self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
            self.send_json({"error": "账号或口令不正确"}, 401); return
        if path == "/api/auth/login/":
            if same_username(data.get("email", ""), ADMIN_USER) and data.get("password") == ADMIN_PASSWORD:
                token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = ADMIN_USER; SESSION_SEEN[token] = time.time()
                self.send_response(200)
                self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers(); self.wfile.write(b'{"ok":true}'); return
            self.send_json({"error": "账号或口令不正确"}, 401); return
        if path == "/api/logout":
            jar = cookies.SimpleCookie(self.headers.get("Cookie", "")); token = jar.get("session")
            if token: TOKENS.discard(token.value); SESSION_USERS.pop(token.value, None)
            self.send_response(200); self.send_header("Set-Cookie", "session=; Max-Age=0; Path=/"); self.end_headers(); return
        if path == "/api/settings":
            if not same_username(self.current_user() or "", ADMIN_USER):
                self.send_json({"error": "Forbidden"}, 403); return
            if REVEAL_KEY in data:
                set_setting(REVEAL_KEY, "on" if data[REVEAL_KEY] else "off")
            if "books" in data:
                # 前端下拉框发的是 "on"/"off" 字符串，而 "off" 是非空字符串、按真值判会存成 on。
                # 所以字符串按字面判，布尔按真值判，空值表示「跟随全局」（不落库）。
                books = {}
                for key, value in (data["books"] or {}).items():
                    if value in (None, ""):
                        continue
                    books[str(key)] = ("on" if value.lower() == "on" else "off") \
                        if isinstance(value, str) else ("on" if value else "off")
                set_setting(BOOKS_KEY, json.dumps(books, ensure_ascii=False))
            if "windows" in data:
                windows = []
                for w in (data["windows"] or []):
                    try:                      # 存进去之前先解析一遍，坏时段不落库
                        datetime.fromisoformat(w["start"]); datetime.fromisoformat(w["end"])
                    except (KeyError, TypeError, ValueError):
                        self.send_json({"error": "Invalid window"}, 400); return
                    if w["end"] < w["start"]:
                        self.send_json({"error": "Window ends before it starts"}, 400); return
                    windows.append({"start": w["start"], "end": w["end"], "note": str(w.get("note", ""))[:60]})
                set_setting(WINDOWS_KEY, json.dumps(windows, ensure_ascii=False))
            self.send_json({REVEAL_KEY: reveal_enabled(), "books": reveal_books(),
                            "windows": reveal_windows(), "active_window": active_window()}); return
        if path in {"/api/run", "/api/run/"} and self.authorized():
            # 「运行样例」：和提交走同一套沙箱，但不写 submissions 表、不计入统计。
            book, problem = data.get("book", ""), data.get("problem", "")
            if not problem_exists(book, problem):
                self.send_json({"status": "Problem Not Found", "message": "本地题库中没有这道题。"}, 404); return
            with judging_slot(self.current_user() or ADMIN_USER) as got_slot:
                if not got_slot:
                    self.send_json({"status": "Busy", "message": "上一次判题还在跑，等它结束再试。"}, 429); return
                self.send_json(run_sample(book, problem, data.get("language", "python"),
                                          data.get("source", ""), data.get("stdin", "")))
            return
        if path in {"/api/submit", "/api/submit/"} and self.authorized():
            book, problem = data.get("book", ""), data.get("problem", "")
            language = data.get("language", "python")
            with judging_slot(self.current_user() or ADMIN_USER) as got_slot:
                if not got_slot:
                    self.send_json({"status": "Busy", "message": "上一次判题还在跑，等它结束再试。"}, 429); return
                result = judge(book, problem, language, data.get("source", data.get("code", "")))
                submitted_source = str(data.get("source", data.get("code", "")))
                result["source_bytes"] = len(submitted_source.encode("utf-8"))
                result["language_version"] = language_version(language)
                # 开关关闭时片段根本不进 response —— 不是前端藏起来，是后端不发。
                if reveal_effective(book) and result.get("case"):
                    snippet = failing_input_snippet(book, problem, result["case"])
                    if snippet: result["failing_input"] = snippet
                if result.get("case"):
                    output = failing_output_snippet(book, problem, result["case"])
                    if output: result["expected_output"] = output
                # detail 存判题器返回的全部字段（case / expected_tokens / message…），
                # 历史页要靠它回答「错在哪组数据」，只存 status 是答不了的。
                detail = json.dumps({k: v for k, v in result.items() if k != "status"}, ensure_ascii=False)
                with sqlite3.connect(DB) as db:
                    db.execute("insert into submissions(user, problem, result, book, language, detail, source) values (?, ?, ?, ?, ?, ?, ?)",
                               (self.current_user() or ADMIN_USER, problem, result["status"], book, language, detail,
                                submitted_source))
                self.send_json(result); return
        self.send_json({"error": "Unauthorized"}, 401)

if __name__ == "__main__":
    init_db()
    host, port = os.environ.get("CS101_HOST", "0.0.0.0"), int(os.environ.get("CS101_PORT", "8000"))
    print(f"CS101 portal running at http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
