#!/usr/bin/env python3
"""Small local course portal for cs101.openjudge.cn."""
from http import cookies
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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
from judge import judge

ROOT = Path(__file__).parent
DB = Path(os.environ.get("CS101_DB", ROOT / "data" / "course.db"))
MIRROR = ROOT / "data" / "openjudge"
ADMIN_USER = os.environ.get("CS101_ADMIN_USER", "GMyhf")
PASSWORD_FILE = ROOT / "data" / ".admin_password"
ADMIN_PASSWORD = os.environ.get("CS101_ADMIN_PASSWORD") or (PASSWORD_FILE.read_text(encoding="utf-8").strip() if PASSWORD_FILE.is_file() else "")
TOKENS = set()
SESSION_USERS = {}
CATALOG_TITLE_CACHE = {}
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
<title>本地提交 - __PROBLEM__</title>
<style>
 :root{--ink:#17221d;--muted:#6b7a72;--line:#d9e0da;--bg:#f7f9f7}
 *{box-sizing:border-box}
 body{font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);
      max-width:900px;margin:0 auto;padding:28px 20px 60px}
 h1{font-size:24px;margin:0 0 4px}
 .sub{color:var(--muted);margin:0 0 20px}
 .sub a{color:#3d8b68}
 /* 编辑器：透明 textarea 叠在高亮层上。两层的字体/行高/padding 必须逐项一致，
    差一点点光标就会和文字错位。 */
 .editor{display:flex;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:#fff}
 .gutter{flex:0 0 auto;padding:12px 8px 12px 12px;text-align:right;color:#aab4ad;background:#fbfcfb;
         border-right:1px solid var(--line);user-select:none;white-space:pre}
 .codewrap{position:relative;flex:1;min-width:0}
 .gutter,.codewrap pre,.codewrap textarea{font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;tab-size:4}
 .codewrap pre,.codewrap textarea{margin:0;padding:12px;border:0;white-space:pre;overflow:auto;width:100%;height:360px}
 .codewrap pre{position:absolute;inset:0;pointer-events:none;color:var(--ink)}
 .codewrap textarea{position:relative;background:transparent;color:transparent;caret-color:var(--ink);
          resize:vertical;outline:none}
 .t-com{color:#7a8a80;font-style:italic}
 .t-str{color:#2f7d55}
 .t-num{color:#8a6d1f}
 .t-kw{color:#9a3d8f;font-weight:600}
 .t-pre{color:#3d6b8b}
 .t-match{background:#ffe9a8;border-radius:2px;box-shadow:0 0 0 1px #d8b84a}
 button.ghost{background:#fff;color:var(--ink);border-color:var(--line)}
 /* 暗色：只改变量与几处硬编码色，结构不动 */
 :root[data-theme="dark"]{--ink:#e6ece8;--muted:#94a49b;--line:#2f3a34;--bg:#1b211e}
 :root[data-theme="dark"] body{background:#141917}
 :root[data-theme="dark"] .editor,
 :root[data-theme="dark"] .codewrap pre,
 :root[data-theme="dark"] select,
 :root[data-theme="dark"] pre.msg{background:#181e1b}
 :root[data-theme="dark"] .gutter{background:#151a18;color:#5c6a63}
 :root[data-theme="dark"] button{background:#e6ece8;color:#141917;border-color:#e6ece8}
 :root[data-theme="dark"] button.ghost{background:#1b211e;color:var(--ink);border-color:var(--line)}
 :root[data-theme="dark"] .t-com{color:#7f8f86}
 :root[data-theme="dark"] .t-str{color:#7fc99b}
 :root[data-theme="dark"] .t-num{color:#d8b667}
 :root[data-theme="dark"] .t-kw{color:#d78fd0}
 :root[data-theme="dark"] .t-pre{color:#87b3d8}
 :root[data-theme="dark"] .t-match{background:#5a4a1a;box-shadow:0 0 0 1px #b8952f}
 :root[data-theme="dark"] .b-ac{background:#1e3a2a;color:#8fd6ab}
 :root[data-theme="dark"] .b-wa{background:#3d2320;color:#e59a90}
 :root[data-theme="dark"] .b-other{background:#39301a;color:#dcc07a}
 :root[data-theme="dark"] .b-info{background:#242c33;color:#a8b6c2}
 .row{display:flex;gap:10px;align-items:center;margin:12px 0}
 select,button{padding:9px 14px;border:1px solid var(--line);border-radius:5px;font:inherit;background:#fff}
 button{background:#17221d;color:#fff;border-color:#17221d;cursor:pointer}
 button[disabled]{opacity:.55;cursor:default}
 .verdict{border:1px solid var(--line);border-radius:6px;padding:14px 16px;margin-top:16px;background:var(--bg)}
 .badge{display:inline-block;padding:2px 10px;border-radius:999px;font-weight:600;font-size:13px}
 .b-ac{background:#e7f3ec;color:#2f7d55}.b-wa{background:#fdeceb;color:#b04f43}
 .b-other{background:#fdf4e3;color:#8a6d1f}.b-info{background:#eef1f4;color:#55606b}
 dl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:12px 0 0}
 dt{color:var(--muted)}dd{margin:0;font-variant-numeric:tabular-nums}
 pre.msg{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);
         border-radius:5px;padding:10px;margin:12px 0 0;font:12px/1.5 ui-monospace,monospace;max-height:220px;overflow:auto}
 h2{font-size:16px;margin:30px 0 8px}
 table{width:100%;border-collapse:collapse;font-size:14px}
 th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line)}
 th{color:var(--muted);font-size:12px;font-weight:600}
 td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
 .muted{color:var(--muted)}
 .snip{margin-top:12px}
 .snip-h{color:var(--muted);font-size:13px;margin-bottom:4px}
</style>
<h1>__PROBLEM__ 本地提交</h1>
<p class="sub">题库：__BOOK__ · 判题运行在本机 · <a href="/problems/">题库目录</a> · <a href="/history/">提交记录</a> · <a href="/__BOOK__/__PROBLEM__/">看题面</a><span id="adminlink"></span></p>
<p id="auth" class="muted">正在检查登录状态…</p>
<form id="form">
  <div class="editor">
    <div class="gutter" id="gutter">1</div>
    <div class="codewrap">
      <pre id="hl" aria-hidden="true"></pre>
      <textarea name="source" id="src" placeholder="在这里粘贴代码" spellcheck="false"
                autocomplete="off" autocapitalize="off"></textarea>
    </div>
  </div>
  <div class="row">
    <select name="language">
      <option value="python">Python 3</option><option value="pypy3">PyPy3</option><option value="cpp">C++17</option><option value="c">C11</option>
    </select>
    <button id="go">提交并判题</button>
    <button id="theme" type="button" class="ghost">深色</button>
    <span id="hint" class="muted"></span>
  </div>
</form>
<div id="verdict"></div>
<h2>我的提交记录</h2>
<div id="histbox" class="muted">…</div>
<script>
const BOOK = "__BOOK__", PROBLEM = "__PROBLEM__";
const CLS = { "Accepted": "b-ac", "Wrong Answer": "b-wa" };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

fetch("/api/me", { credentials: "same-origin" }).then(r => r.json()).then(me => {
  auth.innerHTML = me.authenticated
    ? '已登录：<b>' + esc(me.user) + '</b>'
    : '<a href="/auth/login/">请先登录后提交</a>';
  loadHistory();
});
fetch("/api/settings", { credentials: "same-origin" }).then(r => r.json()).then(s => {
  if (s.is_admin) adminlink.innerHTML = ' · <a href="/admin/">判题设置</a>';
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

// ---- 主题 --------------------------------------------------------------
const THEME_KEY = "cs101-theme";
function applyTheme(name) {
  document.documentElement.dataset.theme = name;
  theme.textContent = name === "dark" ? "浅色" : "深色";
  try { localStorage.setItem(THEME_KEY, name); } catch (err) { /* 隐私模式下忽略 */ }
}
theme.onclick = () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
applyTheme((() => { try { return localStorage.getItem(THEME_KEY) || "light"; } catch (err) { return "light"; } })());

paintEditor();

function badge(status) {
  const cls = CLS[status] || (status === "No Test Data" || status === "Problem Not Found" ? "b-info" : "b-other");
  return '<span class="badge ' + cls + '">' + esc(status) + "</span>";
}

function renderVerdict(data) {
  const rows = [];
  // 「错在哪组数据」是这个页面存在的理由，所以 case 放第一行
  if (data.case !== undefined) rows.push(["出错的数据组", "第 " + data.case + " 组"]);
  if (data.cases !== undefined) rows.push(["通过的数据组", data.cases + " 组全部通过"]);
  if (data.expected_tokens !== undefined)
    rows.push(["输出规模", "期望 " + data.expected_tokens + " 个 token，实际 " + data.actual_tokens + " 个"]);
  // failing_input 只在管理员打开开关时才由服务端下发；关着时这里根本收不到。
  let snippet = "";
  if (data.failing_input) {
    const f = data.failing_input;
    const tail = f.truncated ? "（共 " + f.total_lines + " 行 / " + f.total_chars + " 字符，已截断）" : "";
    snippet = '<div class="snip"><div class="snip-h">第 ' + data.case + ' 组的输入 ' + tail
            + '</div><pre class="msg">' + esc(f.text) + "</pre></div>";
  }
  verdict.innerHTML = '<div class="verdict">' + badge(data.status)
    + (rows.length ? "<dl>" + rows.map(r => "<dt>" + r[0] + "</dt><dd>" + esc(r[1]) + "</dd>").join("") + "</dl>" : "")
    + (data.message ? '<pre class="msg">' + esc(data.message) + "</pre>" : "")
    + snippet + "</div>";
}

form.onsubmit = async e => {
  e.preventDefault();
  go.disabled = true; hint.textContent = "判题中…";
  verdict.innerHTML = "";
  const body = Object.fromEntries(new FormData(form));
  body.book = BOOK; body.problem = PROBLEM;
  try {
    const r = await fetch("/api/submit", { method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await r.json();
    if (r.status === 401) verdict.innerHTML = '<div class="verdict">' + badge("需要登录")
      + '<dl><dt>说明</dt><dd><a href="/auth/login/">先登录</a>后再提交</dd></dl></div>';
    else { renderVerdict(data); loadHistory(); }
  } catch (err) {
    verdict.innerHTML = '<div class="verdict">' + badge("提交失败") + '<pre class="msg">' + esc(err) + "</pre></div>";
  }
  go.disabled = false; hint.textContent = "";
};

async function loadHistory() {
  const r = await fetch("/api/submissions", { credentials: "same-origin" });
  if (r.status === 401) { histbox.textContent = "登录后可以看到提交记录。"; return; }
  const mine = (await r.json()).submissions.filter(s => s.problem === PROBLEM);
  if (!mine.length) { histbox.textContent = "这道题还没有提交记录。"; return; }
  histbox.innerHTML = "<table><thead><tr><th>时间</th><th>结果</th><th>语言</th><th>细节</th></tr></thead><tbody>"
    + mine.map(s => {
        const d = s.detail || {};
        const note = d.case !== undefined ? "第 " + d.case + " 组"
                   : d.cases !== undefined ? d.cases + " 组全过" : "";
        return "<tr><td class='num'>" + esc(s.created) + "</td><td>" + badge(s.result)
             + "</td><td>" + esc(s.language || "") + "</td><td class='muted'>" + esc(note) + "</td></tr>";
      }).join("") + "</tbody></table>";
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
        for column in ("book text", "language text", "detail text"):
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


def reveal_enabled():
    return get_setting(REVEAL_KEY, "off") == "on"


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


def password_hash(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"cs101-local-user", 120000).hex()

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

    def authorized(self):
        raw = self.headers.get("Cookie", "")
        jar = cookies.SimpleCookie(raw)
        token = jar.get("session")
        return token is not None and token.value in TOKENS

    def current_user(self):
        raw = self.headers.get("Cookie", "")
        token = cookies.SimpleCookie(raw).get("session")
        return SESSION_USERS.get(token.value) if token and token.value in TOKENS else None

    def send_html(self, body):
        if isinstance(body, str): body = body.encode("utf-8")
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def local_page(self, page):
        text = page.read_text(encoding="utf-8", errors="replace")
        text = text.replace("http://cs101.openjudge.cn/", "/")
        text = text.replace("https://cs101.openjudge.cn/", "/")
        text = text.replace("http://cs101.openjudge.cn", "/")
        text = text.replace("https://cs101.openjudge.cn", "/")
        return text

    def modern_problem_page(self, page, book, problem):
        """Render the mirrored statement without the upstream navigation shell."""
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
        return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · CS101 本地题库</title>
<style>
:root{{--ink:#16231d;--muted:#6c7b73;--line:#dfe7e1;--bg:#f4f7f4;--paper:#fff;--green:#237a50;--green-soft:#e5f3eb;--amber:#c87828}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}}
a{{color:var(--green)}}.shell{{max-width:1120px;margin:auto;padding:0 24px}}.top{{height:72px;display:flex;align-items:center;justify-content:space-between}}.brand{{display:flex;gap:11px;align-items:center;text-decoration:none;color:var(--ink);font-weight:750}}.mark{{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:white;font-size:16px}}.nav{{display:flex;align-items:center;gap:10px}}.nav a{{padding:8px 12px;border-radius:6px;text-decoration:none;color:var(--muted);font-size:14px}}.nav a:hover{{background:var(--green-soft);color:var(--green)}}.nav .primary{{background:var(--ink);color:white;padding:9px 15px}}.crumb{{color:var(--muted);font-size:13px;margin:20px 0 12px}}.crumb a{{text-decoration:none}}.layout{{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:20px;align-items:start}}.article,.aside{{background:var(--paper);border:1px solid var(--line);border-radius:10px}}.article{{padding:34px 38px 42px}}h1{{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:0 0 20px;letter-spacing:-.02em}}.eyebrow{{color:var(--green);font-size:12px;font-weight:750;letter-spacing:.12em;text-transform:uppercase;margin-bottom:9px}}.problem-params{{display:flex;flex-wrap:wrap;gap:7px 24px;padding:13px 16px;margin:0 0 30px;border-left:3px solid var(--amber);background:#fffaf3;color:var(--muted);font-size:13px}}.problem-params dt{{font-weight:650;color:var(--ink)}}.problem-params dd{{margin:0}}.problem-content{{margin:0}}.problem-content dt{{font-size:17px;font-weight:750;margin:28px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--line)}}.problem-content dt:first-child{{margin-top:0}}.problem-content dd{{margin:0;color:#334139}}.problem-content pre{{overflow:auto;margin:10px 0;padding:15px 17px;border:1px solid var(--line);border-radius:7px;background:#f7faf7;color:var(--ink);font:13px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace}}.aside{{padding:20px;position:sticky;top:18px}}.aside h2{{font-size:15px;margin:0 0 14px}}.aside dl{{margin:0;display:grid;grid-template-columns:1fr auto;gap:7px 10px;font-size:13px}}.aside dt{{color:var(--muted)}}.aside dd{{margin:0;font-variant-numeric:tabular-nums}}.aside-note{{margin-top:18px;padding-top:15px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}.footer{{color:var(--muted);font-size:13px;padding:28px 0 40px}}@media(max-width:760px){{.shell{{padding:0 16px}}.top{{height:62px}}.nav a:not(.primary){{display:none}}.layout{{grid-template-columns:1fr}}.article{{padding:25px 20px 32px}}.aside{{position:static}}}}
</style></head><body>
<header class="top shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><nav class="nav"><a href="/problems/">全部题目</a><a href="/history/">提交记录</a><a id="account" href="/auth/login/">登录</a><a class="primary" href="/{escape(book)}/{escape(problem)}/submit/">提交代码</a></nav></header>
<main class="shell"><div class="crumb"><a href="/">首页</a> / <a href="/problems/">题库目录</a> / {escape(book)} / {escape(problem)}</div><div class="layout"><article class="article"><div class="eyebrow">Problem statement</div><h1>{escape(title)}</h1>{params_html}<dl class="problem-content">{content_html}</dl></article><aside class="aside"><h2>题目概览</h2><dl>{stats_html}</dl><div class="aside-note">本题使用测试数据判题。<br><a href="/{escape(book)}/{escape(problem)}/submit/">打开提交页 →</a></div></aside></div></main><footer class="footer shell">CS101 · 题面与判题服务</footer><script>fetch('/api/me').then(r=>r.json()).then(d=>{{if(d.authenticated){{account.textContent=d.user;account.href='/account/'}}}});</script></body></html>"""

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
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>
:root{{--ink:#16231d;--muted:#6c7b73;--line:#dfe7e1;--bg:#f4f7f4;--paper:#fff;--green:#237a50;--red:#b04f43}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}.shell{{max-width:460px;margin:0 auto;padding:70px 20px}}.brand{{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}}.mark{{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:#fff;font-size:15px}}.panel{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}}h1{{font-size:28px;line-height:1.2;margin:0 0 6px}}.intro{{color:var(--muted);margin:0 0 23px}}label{{display:block;margin:16px 0 6px;font-weight:600}}input{{display:block;width:100%;padding:11px 12px;border:1px solid #ccd8cf;border-radius:6px;background:#fff;font:inherit;outline:none}}input:focus{{border-color:var(--green);box-shadow:0 0 0 3px #e5f3eb}}button{{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:#fff;border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}}a{{color:var(--green)}}.links{{margin:19px 0 0;color:var(--muted);font-size:14px;text-align:center}}.error{{min-height:22px;color:var(--red);margin:12px 0 0}}.captcha-question{{display:inline-block;margin-left:5px;color:var(--green);font-family:ui-monospace,monospace}}@media(max-width:520px){{.shell{{padding:35px 16px}}.panel{{padding:24px}}}}
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
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{message} · CS101</title><style>body{{margin:0;background:#f4f7f4;color:#16231d;font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:#fff;border:1px solid #dfe7e1;border-radius:10px;padding:30px}}h1{{margin:0 0 10px}}p{{color:#6c7b73}}a{{color:#237a50}}</style></head><body><main><section><h1>{message}</h1><p>{detail}</p><p><a href="/auth/login/">前往登录</a></p></section></main></body></html>"""

    def forgot_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>找回密码 · CS101</title><style>
:root{--ink:#16231d;--muted:#6c7b73;--line:#dfe7e1;--bg:#f4f7f4;--paper:#fff;--green:#237a50;--red:#b04f43}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:460px;margin:0 auto;padding:70px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:#fff;font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}h1{font-size:28px;line-height:1.2;margin:0 0 6px}.intro{color:var(--muted);margin:0 0 23px}label{display:block;margin:16px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid #ccd8cf;border-radius:6px;font:inherit;outline:none}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:#fff;border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}a{color:var(--green)}.message{color:var(--muted);margin-top:15px;word-break:break-word}@media(max-width:520px){.shell{padding:35px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><h1>忘记密码？</h1><p class="intro">输入注册邮箱，我们会生成一次性密码重置链接。</p><form id="forgot"><label>邮箱地址<input name="email" type="email" required autocomplete="email"></label><button>发送重置链接</button></form><p id="message" class="message"></p><p><a href="/auth/login/">返回登录</a> · <a href="/register/">点此注册</a></p></section></main><script>forgot.onsubmit=async e=>{e.preventDefault();message.textContent='正在处理…';const r=await fetch('/api/user/forgot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(forgot)))});const d=await r.json();message.innerHTML=d.reset_link?'邮件服务尚未配置，请使用本机重置链接：<a href="'+d.reset_link+'">立即重置密码</a>':'如果该邮箱已注册，重置链接已发送或正在等待管理员配置邮件服务。';}</script></body></html>"""

    def reset_page(self, token):
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>重置密码 · CS101</title><style>body{{margin:0;background:#f4f7f4;color:#16231d;font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:#fff;border:1px solid #dfe7e1;border-radius:10px;padding:30px}}h1{{margin:0 0 20px}}label{{display:block;margin:14px 0 6px;font-weight:600}}input{{width:100%;padding:11px;box-sizing:border-box;border:1px solid #ccd8cf;border-radius:6px;font:inherit}}button{{width:100%;margin-top:20px;padding:11px;background:#16231d;color:white;border:0;border-radius:6px;font:inherit}}a{{color:#237a50}}#message{{color:#b04f43}}</style></head><body><main><section><h1>设置新密码</h1><form id="reset"><label>新密码<input name="password" type="password" minlength="8" required autocomplete="new-password"></label><label>确认密码<input name="confirm_password" type="password" minlength="8" required autocomplete="new-password"></label><p id="message"></p><button>保存新密码</button></form><p><a href="/auth/login/">返回登录</a></p></section></main><script>reset.onsubmit=async e=>{{e.preventDefault();message.textContent='';const d=Object.fromEntries(new FormData(reset));if(d.password!==d.confirm_password){{message.textContent='两次输入的密码不一致';return}}d.token={json.dumps(token)};const r=await fetch('/api/user/reset',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});const x=await r.json();if(r.ok){{message.style.color='#237a50';message.textContent='密码已更新，请返回登录。';reset.querySelector('button').disabled=true}}else message.textContent=x.error||'重置失败'}};</script></body></html>"""

    def account_settings_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>账户设置 · CS101</title><style>
:root{--ink:#16231d;--muted:#6c7b73;--line:#dfe7e1;--bg:#f4f7f4;--paper:#fff;--green:#237a50;--red:#b04f43}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:520px;margin:0 auto;padding:52px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:24px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:#fff;font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}.topline{display:flex;justify-content:space-between;align-items:start;gap:15px;margin-bottom:22px}h1{font-size:28px;line-height:1.2;margin:0 0 5px}.muted{color:var(--muted);margin:0}.back{color:var(--green);text-decoration:none;font-size:14px}h2{font-size:16px;margin:0 0 14px;padding-top:22px;border-top:1px solid var(--line)}label{display:block;margin:14px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid #ccd8cf;border-radius:6px;font:inherit;outline:none}input:focus{border-color:var(--green);box-shadow:0 0 0 3px #e5f3eb}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:#fff;border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}.message{min-height:22px;color:var(--red);margin:12px 0 0}.logout{display:block;width:100%;margin-top:12px;padding:10px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);font:inherit;cursor:pointer}@media(max-width:520px){.shell{padding:30px 16px}.panel{padding:24px}}
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
        if path == "/account/":
            if not self.authorized():
                self.send_response(302); self.send_header("Location", "/auth/login/"); self.end_headers(); return
            self.send_html(self.account_settings_page()); return
        submit_page = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/([^/]+)/submit/", path)
        if submit_page:
            book, problem_id = submit_page.groups()
            body = SUBMIT_PAGE.replace("__BOOK__", escape(book)).replace("__PROBLEM__", escape(problem_id)).encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
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
                self.send_html(self.modern_problem_page(page, book, problem)); return
        if path == "/api/course":
            self.send_json({"course": COURSE, "problems": PROBLEMS, "authenticated": self.authorized()})
            return
        if path == "/api/me":
            self.send_json({"authenticated": self.authorized(), "user": self.current_user()})
            return
        if path == "/api/stats":
            with sqlite3.connect(DB) as db:
                count = db.execute("select count(*) from submissions").fetchone()[0]
            self.send_json({"submissions": count, "accepted": 1284, "streak": 12})
            return
        if path == "/api/settings":
            book = parse_qs(parsed.query).get("book", [""])[0]
            self.send_json({REVEAL_KEY: reveal_enabled(), "books": reveal_books(),
                            "windows": reveal_windows(), "active_window": active_window(),
                            "effective": reveal_effective(book) if book else None,
                            "is_admin": self.current_user() == ADMIN_USER})
            return
        if path in ("/admin", "/admin/"):
            page = ROOT / "admin.html"
            if page.is_file():
                self.send_html(page.read_text(encoding="utf-8")); return
        if path == "/api/submissions":
            user = self.current_user()
            if user is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            try:
                limit = min(max(int(parse_qs(parsed.query).get("limit", ["50"])[0]), 1), 500)
            except ValueError:
                limit = 50
            with sqlite3.connect(DB) as db:
                rows = db.execute("select problem, result, created, book, language, detail from submissions"
                                  " where user = ? order by id desc limit ?", (user, limit)).fetchall()
            self.send_json({"user": user, "submissions": [
                {"problem": r[0], "result": r[1], "created": r[2], "book": r[3], "language": r[4],
                 "detail": json.loads(r[5]) if r[5] else {}} for r in rows]})
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
            catalog = MIRROR / "catalog.json"
            if catalog.is_file():
                payload = json.loads(catalog.read_text(encoding="utf-8"))
                payload["problems"] = [{**item, "title": catalog_title(item)} for item in payload.get("problems", [])]
                self.send_json(payload); return
        file = ROOT / ("index.html" if path in ("/", "") else decoded_path.lstrip("/"))
        if file.is_file() and ROOT in file.parents:
            content_type = "text/html; charset=utf-8" if file.suffix == ".html" else "text/css; charset=utf-8" if file.suffix == ".css" else "text/javascript; charset=utf-8"
            body = file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
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
            if username == ADMIN_USER:
                self.send_json({"error": "该用户名不可注册"}, 409); return
            activation_token = secrets.token_urlsafe(32)
            try:
                with sqlite3.connect(DB) as db:
                    if db.execute("select 1 from users where username = ? or lower(email) = ?", (username, email)).fetchone():
                        self.send_json({"error": "用户名或邮箱已存在"}, 409); return
                    db.execute("insert into users(username, password_hash, email, active, activation_token_hash, activation_expires) values (?, ?, ?, 0, ?, ?)",
                               (username, password_hash(password), email, reset_token_hash(activation_token), int(time.time()) + 86400))
            except sqlite3.IntegrityError:
                self.send_json({"error": "用户名或邮箱已存在"}, 409); return
            base = os.environ.get("CS101_PUBLIC_URL", "").rstrip("/")
            if not base:
                scheme = "https" if self.headers.get("X-Forwarded-Proto") == "https" else "http"
                base = f"{scheme}://{self.headers.get('Host', '127.0.0.1:8000')}"
            activation_link = f"{base}/auth/activate/?token={activation_token}"
            sent = send_account_email(email, "激活你的 CS101 账号", f"请在 24 小时内点击以下链接激活账号：\n{activation_link}\n")
            self.send_json({"ok": True} if sent else {"ok": True, "activation_link": activation_link}); return
        if path == "/api/user/login":
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            accepted = username == ADMIN_USER and password == ADMIN_PASSWORD
            if not accepted:
                with sqlite3.connect(DB) as db:
                    row = db.execute("select password_hash from users where username = ?", (username,)).fetchone()
                    accepted = row is not None and valid_password(row[0], password)
                    if accepted:
                        active = db.execute("select active from users where username = ?", (username,)).fetchone()[0]
                        if not active:
                            self.send_json({"error": "账号尚未激活，请先点击邮箱中的激活链接"}, 403); return
            if not accepted:
                self.send_json({"error": "用户名或密码不正确"}, 401); return
            token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = username
            self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/"); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
        if path == "/api/user/change-password":
            username = self.current_user()
            if username is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            if username == ADMIN_USER:
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
            base = os.environ.get("CS101_PUBLIC_URL", "").rstrip("/")
            if not base:
                scheme = "https" if self.headers.get("X-Forwarded-Proto") == "https" else "http"
                base = f"{scheme}://{self.headers.get('Host', '127.0.0.1:8000')}"
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
            if data.get("username") == ADMIN_USER and data.get("password") == ADMIN_PASSWORD:
                token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = ADMIN_USER
                self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/")
                self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
            self.send_json({"error": "账号或口令不正确"}, 401); return
        if path == "/api/auth/login/":
            if data.get("email") == ADMIN_USER and data.get("password") == ADMIN_PASSWORD:
                token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = ADMIN_USER
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
            if self.current_user() != ADMIN_USER:
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
        if path in {"/api/submit", "/api/submit/"} and self.authorized():
            book, problem = data.get("book", ""), data.get("problem", "")
            language = data.get("language", "python")
            result = judge(book, problem, language, data.get("source", data.get("code", "")))
            # 开关关闭时片段根本不进 response —— 不是前端藏起来，是后端不发。
            if reveal_effective(book) and result.get("case"):
                snippet = failing_input_snippet(book, problem, result["case"])
                if snippet: result["failing_input"] = snippet
            # detail 存判题器返回的全部字段（case / expected_tokens / message…），
            # 历史页要靠它回答「错在哪组数据」，只存 status 是答不了的。
            detail = json.dumps({k: v for k, v in result.items() if k != "status"}, ensure_ascii=False)
            with sqlite3.connect(DB) as db:
                db.execute("insert into submissions(user, problem, result, book, language, detail) values (?, ?, ?, ?, ?, ?)",
                           (self.current_user() or ADMIN_USER, problem, result["status"], book, language, detail))
            self.send_json(result); return
        self.send_json({"error": "Unauthorized"}, 401)

if __name__ == "__main__":
    init_db()
    host, port = os.environ.get("CS101_HOST", "0.0.0.0"), int(os.environ.get("CS101_PORT", "8000"))
    print(f"CS101 portal running at http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
