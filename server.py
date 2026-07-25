#!/usr/bin/env python3
"""Small local course portal for cs101.openjudge.cn."""
from http import cookies
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import hashlib
import os
import secrets
import sqlite3
import urllib.error
import urllib.request
import re
from html import escape
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

COURSE = {
    "title": "计算机科学导论",
    "term": "2026 春季学期",
    "teacher": "GMyhf",
    "notice": "第 8 周作业已发布，截止时间为周日 23:59。",
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
<p class="sub">题库：__BOOK__ · 判题运行在本机 · <a href="/problems/">题库目录</a> · <a href="/__BOOK__/__PROBLEM__/">看题面</a><span id="adminlink"></span></p>
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
      <option value="python">Python 3</option><option value="cpp">C++17</option><option value="c">C11</option>
    </select>
    <button id="go">提交并判题</button>
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

// ---- 语法高亮 ----------------------------------------------------------
// 不引外部库：粘性正则按位置扫一遍，命中就包 span，没命中的连续片段整段转义。
// 顺序要紧：注释和字符串必须排在关键字前面，否则 "# def" 里的 def 会被当关键字。
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

function highlight(code, lang) {
  const specs = SPECS[lang] || SPECS.python;
  let out = "", i = 0, plain = 0;
  const flush = () => { if (plain) { out += esc(code.slice(i - plain, i)); plain = 0; } };
  while (i < code.length) {
    let hit = null;
    for (const spec of specs) {
      spec[1].lastIndex = i;
      const m = spec[1].exec(code);
      if (m && m.index === i && m[0]) { hit = [spec[0], m[0]]; break; }
    }
    if (hit) { flush(); out += '<span class="t-' + hit[0] + '">' + esc(hit[1]) + "</span>"; i += hit[1].length; }
    else { i++; plain++; }
  }
  flush();
  return out;
}

function paintEditor() {
  const code = src.value;
  // 末尾补一个换行：最后一行为空时，高亮层会比 textarea 少一行高度，滚动就对不齐
  hl.innerHTML = highlight(code + "\n", form.language.value);
  gutter.textContent = Array.from({ length: code.split("\n").length }, (_, k) => k + 1).join("\n");
  hl.scrollTop = src.scrollTop; hl.scrollLeft = src.scrollLeft;
}

src.addEventListener("input", paintEditor);
src.addEventListener("scroll", () => { hl.scrollTop = src.scrollTop; hl.scrollLeft = src.scrollLeft; });
form.language.addEventListener("change", paintEditor);
src.addEventListener("keydown", e => {
  if (e.key !== "Tab") return;
  e.preventDefault();
  src.setRangeText("    ", src.selectionStart, src.selectionEnd, "end");
  paintEditor();
});
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


def password_hash(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"cs101-local-user", 120000).hex()

def valid_password(stored, password):
    return stored == password_hash(password)

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

    def account_page(self, register=False):
        title = "注册 CS101 账号" if register else "登录 CS101"
        endpoint = "/api/user/register" if register else "/api/user/login"
        switch = "已有账号？登录" if register else "还没有账号？注册"
        switch_url = "/auth/login/" if register else "/register/"
        return f"""<!doctype html><html lang='zh-CN'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>body{{font:15px system-ui;max-width:430px;margin:70px auto;padding:0 20px;color:#17221d}}h1{{font-size:28px}}label{{display:block;margin:18px 0 6px}}input{{width:100%;padding:12px;box-sizing:border-box;border:1px solid #ccd5cc;border-radius:4px}}button{{margin-top:22px;padding:12px 18px;background:#17221d;color:white;border:0;border-radius:4px;cursor:pointer}}a{{color:#3d8b68}}#error{{color:#b04f43;min-height:20px}}</style><h1>{title}</h1><p>本地 CS101 账户系统</p><form id='account'><label>用户名<input name='username' required minlength='2' maxlength='32' autocomplete='username'></label><label>密码<input name='password' type='password' required minlength='6' autocomplete='current-password'></label><p id='error'></p><button>提交</button></form><p><a href='{switch_url}'>{switch}</a> · <a href='/'>返回 CS101 首页</a></p><script>account.onsubmit=async e=>{{e.preventDefault();error.textContent='';let r=await fetch('{endpoint}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(new FormData(account)))}});let d=await r.json();if(r.ok)location.href='/';else error.textContent=d.error||'操作失败'}}</script></html>"""

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
            page = MIRROR / "pages" / f"{local_problem.group(1)}__{local_problem.group(2)}.html"
            if page.is_file():
                self.send_html(self.local_page(page)); return
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
            with sqlite3.connect(DB) as db:
                rows = db.execute("select problem, result, created, book, language, detail from submissions"
                                  " where user = ? order by id desc limit 50", (user,)).fetchall()
            self.send_json({"user": user, "submissions": [
                {"problem": r[0], "result": r[1], "created": r[2], "book": r[3], "language": r[4],
                 "detail": json.loads(r[5]) if r[5] else {}} for r in rows]})
            return
        if path in ("/problems", "/problems/"):
            page = ROOT / "problems.html"
            if page.is_file():
                self.send_html(page.read_text(encoding="utf-8")); return
        if path == "/api/catalog":
            catalog = MIRROR / "catalog.json"
            if catalog.is_file():
                payload = json.loads(catalog.read_text(encoding="utf-8"))
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
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            if len(username) < 2 or len(username) > 32 or not re.fullmatch(r"[\w\u4e00-\u9fff-]+", username):
                self.send_json({"error": "用户名需为 2-32 个字母、数字、下划线、中文或短横线"}, 400); return
            if len(password) < 6:
                self.send_json({"error": "密码至少需要 6 位"}, 400); return
            if username == ADMIN_USER:
                self.send_json({"error": "该用户名不可注册"}, 409); return
            try:
                with sqlite3.connect(DB) as db: db.execute("insert into users(username, password_hash) values (?, ?)", (username, password_hash(password)))
            except sqlite3.IntegrityError:
                self.send_json({"error": "用户名已存在"}, 409); return
            token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = username
            self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/"); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
        if path == "/api/user/login":
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            accepted = username == ADMIN_USER and password == ADMIN_PASSWORD
            if not accepted:
                with sqlite3.connect(DB) as db:
                    row = db.execute("select password_hash from users where username = ?", (username,)).fetchone()
                accepted = row is not None and valid_password(row[0], password)
            if not accepted:
                self.send_json({"error": "用户名或密码不正确"}, 401); return
            token = secrets.token_urlsafe(24); TOKENS.add(token); SESSION_USERS[token] = username
            self.send_response(200); self.send_header("Set-Cookie", f"session={token}; HttpOnly; SameSite=Lax; Path=/"); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
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
