#!/usr/bin/env python3
"""Small local course portal for cs101.openjudge.cn."""
from http import cookies
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
from urllib.parse import parse_qs, urlparse
from judge import judge

ROOT = Path(__file__).parent
DB = ROOT / "data" / "course.db"
MIRROR = ROOT / "data" / "openjudge"
ADMIN_USER = os.environ.get("CS101_ADMIN_USER", "GMyhf")
ADMIN_PASSWORD = os.environ.get("CS101_ADMIN_PASSWORD", "legend200909")
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

def init_db():
    DB.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as db:
        db.execute("create table if not exists submissions (id integer primary key, user text, problem text, result text, created text default current_timestamp)")
        db.execute("create table if not exists users (username text primary key, password_hash text not null, created text default current_timestamp)")

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
        if path == "/auth/login/":
            self.send_html(self.account_page()); return
        if path == "/register/":
            self.send_html(self.account_page(register=True)); return
        submit_page = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/([^/]+)/submit/", path)
        if submit_page:
            book, problem_id = submit_page.groups()
            body = (f"<!doctype html><html lang='zh-CN'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                    f"<title>本地提交 - {escape(problem_id)}</title><style>body{{font:15px system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#17221d}}textarea{{width:100%;min-height:360px;font:14px monospace;padding:12px}}select,button{{padding:10px 14px;margin:10px 8px 10px 0}}#result{{white-space:pre-wrap;padding:14px;background:#f2f5f1}}</style>"
                    f"<h1>{escape(problem_id)} 本地提交</h1><p>题库：{escape(book)} · 判题运行在本机</p><p id='auth'>正在检查登录状态...</p><form id='form'><select name='language'><option value='python'>Python 3</option><option value='cpp'>C++17</option><option value='c'>C11</option></select><textarea name='source' placeholder='在这里粘贴代码'></textarea><br><button>提交并判题</button></form><pre id='result'>等待提交</pre>"
                    "<script>(async()=>{let me=await fetch('/api/me',{credentials:'same-origin'}).then(r=>r.json());if(!me.authenticated){auth.innerHTML='<a href=\"/auth/login/\">请先登录后提交</a>';}})();form.onsubmit=async e=>{e.preventDefault();result.textContent='判题中...';const body=Object.fromEntries(new FormData(form));body.book='" + escape(book) + "';body.problem='" + escape(problem_id) + "';const r=await fetch('/api/submit',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();result.textContent=r.status===401?'请先登录后再提交：'+data.error:JSON.stringify(data,null,2)}</script></html>").encode()
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
        if path == "/api/catalog":
            catalog = MIRROR / "catalog.json"
            if catalog.is_file():
                payload = json.loads(catalog.read_text(encoding="utf-8"))
                self.send_json(payload); return
        file = ROOT / ("index.html" if path in ("/", "") else path.lstrip("/"))
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
        if path in {"/api/submit", "/api/submit/"} and self.authorized():
            result = judge(data.get("book", ""), data.get("problem", ""), data.get("language", "python"), data.get("source", data.get("code", "")))
            with sqlite3.connect(DB) as db: db.execute("insert into submissions(user, problem, result) values (?, ?, ?)", (self.current_user() or ADMIN_USER, data.get("problem", ""), result["status"]))
            self.send_json(result); return
        self.send_json({"error": "Unauthorized"}, 401)

if __name__ == "__main__":
    init_db()
    host, port = os.environ.get("CS101_HOST", "0.0.0.0"), int(os.environ.get("CS101_PORT", "8000"))
    print(f"CS101 portal running at http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
