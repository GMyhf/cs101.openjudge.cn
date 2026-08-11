#!/usr/bin/env python3
"""Small local course portal for cs101.openjudge.cn."""
from http import cookies
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import contextlib
import gzip
import socket
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


def parse_sample_sections(text, truncate_explanations=True):
    """把标注式样例切成 [{input, output}, ...]，解析不出就返回空列表。

    truncate_explanations=False 时保留输出段原样。这个开关是给
    `tools/full_sweep.py` 的守门检查用的：它要验的正是「输出段首行会不会是 `#`」，
    而截断本身会把这种输出削成空串 —— 拿截断后的结果去验，它永远看不见自己要防的那件事。
    """
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
        if section["kind"] == "output" and truncate_explanations:
            cut = next((i for i, line in enumerate(body) if SAMPLE_EXPLAIN.match(line)), None)
            if cut is not None:
                body = body[:cut]
        cases.setdefault(section["index"], {})[section["kind"]] = "\n".join(body).strip("\n")
    return [{"input": case.get("input", ""), "output": case.get("output", "")}
            for _, case in sorted(cases.items())
            if case.get("input", "").strip() or case.get("output", "").strip()]


JUDGE_SLOTS = set()
JUDGE_SLOTS_LOCK = threading.Lock()

# 全局同时判题数。判题是 CPU 密集的，并发超过核数**不会提高吞吐** ——
# 只会把墙钟拉长，而 `_run` 的超时（cpu_seconds + 1）量的正是墙钟。
# 于是超售的后果不是「慢一点」，而是**正确代码被判 TLE**，还会作为真实判定
# 写进学生的提交记录。连不上还能重试，判错了是要申诉的。
#
# 32 核实测（每人一份正确解，每组烧 1.5s CPU）：
#   并发 60  → 60 AC，最慢 19s
#   并发 100 → 5 个 TLE 冒出来
#   并发 150 → 44 个 TLE
# 排队等待换来的是「慢但对」，这个交换在判题场景里永远划算。
JUDGE_CONCURRENCY = int(os.environ.get("CS101_JUDGE_CONCURRENCY", os.cpu_count() or 4))
JUDGE_SEMAPHORE = threading.BoundedSemaphore(JUDGE_CONCURRENCY)
# 排太久就明确回「忙」，而不是让浏览器无限等下去。
JUDGE_QUEUE_WAIT_SECONDS = int(os.environ.get("CS101_JUDGE_QUEUE_WAIT", "150"))

RUN_QUOTA_WINDOW_SECONDS = 300
RUN_QUOTA_MAX = 30
# 提交比运行样例重得多：一次要跑完全部测试点（最长 300 秒），还会入库留痕。
# 所以窗口更长、次数更少 —— 2 次/分钟的持续上限，对「改一版交一版」绰绰有余。
SUBMIT_QUOTA_WINDOW_SECONDS = 600
SUBMIT_QUOTA_MAX = 20
QUOTA_HISTORY = {}
QUOTA_LOCK = threading.Lock()


QUOTAS_KEY = "quotas"
# 默认值是拍的（按「改一版跑一版」的调试节奏），没有真实使用数据支撑 ——
# 所以必须能在管理页上改，而不是改常量再重启：真正会撞上额度的是考试当天，
# 那正是最不能重启的时刻。limit 填 0 表示不限（考试时可临时放开）。
QUOTA_DEFAULTS = {
    "run": {"limit": 30, "window": 300},
    "submit": {"limit": 20, "window": 600},
    # 注册按来源地址计数，而一个班常在同一出口 IP 后面：开学第一节课
    # 集中注册就是一次「一个 IP、上百个合法请求」。所以默认给得宽，
    # 只拦批量刷号；真要更紧或更松，管理页上改，不用重启。
    "register": {"limit": 100, "window": 600},
    # 找回密码：两个维度共用这一份额度。按邮箱计数挡的是「盯着某人的信箱狂发重置邮件」，
    # 按来源地址计数挡的是「手里有一份邮箱名单、从一个地方群发」。
    # 正常人一次重置只需要一两封，10 次/10 分钟对真实使用绰绰有余。
    "forgot": {"limit": 10, "window": 600},
}
QUOTA_LIMIT_CAP = 100000
QUOTA_WINDOW_RANGE = (10, 86400)


def quota_config():
    """管理员配置优先，坏值或缺项回落到默认，永远返回三个桶都齐全的表。"""
    try:
        stored = json.loads(get_setting(QUOTAS_KEY, "{}")) or {}
    except (ValueError, TypeError):
        stored = {}
    config = {}
    for bucket, default in QUOTA_DEFAULTS.items():
        entry = stored.get(bucket) if isinstance(stored.get(bucket), dict) else {}
        try:
            limit = int(entry.get("limit", default["limit"]))
        except (TypeError, ValueError):
            limit = default["limit"]
        try:
            window = int(entry.get("window", default["window"]))
        except (TypeError, ValueError):
            window = default["window"]
        limit = max(0, min(limit, QUOTA_LIMIT_CAP))
        window = max(QUOTA_WINDOW_RANGE[0], min(window, QUOTA_WINDOW_RANGE[1]))
        config[bucket] = {"limit": limit, "window": window}
    return config


def quota_retry_after(bucket, user, window=None, limit=None):
    """每用户滑动窗口配额。返回还需等待的秒数；0 表示放行（并已记账）。

    互斥只挡「同时」，挡不住「一直」—— 一个登录用户可以串行地无限次要求我们执行代码。
    计数按用户名而非 IP，与登录限速同一理由：一个班常共用出口 IP，按 IP 会把整班一起限住。

    限的是**请求我们执行**这件事，不是「成功执行」：题号不存在、编译失败一样计数，
    否则拿无效请求刷同样能把机器占满。

    不传 window/limit 时读管理员配置；limit 为 0 表示不限。
    """
    if window is None or limit is None:
        conf = quota_config()[bucket]
        window, limit = conf["window"], conf["limit"]
    if limit <= 0:
        return 0
    key = (bucket, (user or "").lower())
    now = time.time()
    with QUOTA_LOCK:
        stamps = [t for t in QUOTA_HISTORY.get(key, []) if now - t < window]
        if len(stamps) >= limit:
            QUOTA_HISTORY[key] = stamps
            return max(1, round(window - (now - stamps[0])))
        stamps.append(now)
        QUOTA_HISTORY[key] = stamps
        return 0


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
    # 先占住这个用户的位置，再排全局队：顺序反过来的话，
    # 一个用户连点两次会占掉两个全局名额。
    got_slot = JUDGE_SEMAPHORE.acquire(timeout=JUDGE_QUEUE_WAIT_SECONDS)
    try:
        yield got_slot
    finally:
        if got_slot:
            JUDGE_SEMAPHORE.release()
        with JUDGE_SLOTS_LOCK:
            JUDGE_SLOTS.discard(key)


# 图标 + 样式表 + 主题引导。改动前这三行在 `server.py` 里逐字复制了 9 份、
# 5 个 `.html` 各一份 —— 一份写错就是某个页面在深色下闪白，而十几份里挑错的
# 那一份只能靠肉眼。`send_html()` 统一把 `__THEME_HEAD__` 换成它，
# 所以每个模板的 <head> 里只留这个占位符。
THEME_HEAD = (
    '<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">'
    '<link rel="stylesheet" href="/static/theme.css">'
    # 引导脚本必须在首屏绘制前跑完，否则深色用户会先看到一帧白。
    # 也因为这里总会写上 data-theme，theme.css 里的深色才只需要一个块。
    "<script>(function(){try{var t=localStorage.getItem('cs101-theme');"
    "if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)')"
    ".matches?'dark':'light';document.documentElement.dataset.theme=t;}"
    "catch(e){document.documentElement.dataset.theme='light';}})();</script>"
)
THEME_HEAD_SLOT = "__THEME_HEAD__"

STATIC_DIR = (ROOT / "static").resolve()
STATIC_TYPES = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg", ".gif": "image/gif", ".bmp": "image/bmp",
                ".webp": "image/webp", ".ico": "image/x-icon",
                ".woff2": "font/woff2"}
# 值得压的只有文本。JPEG/PNG/GIF/WOFF2 本身已是压缩格式，再压一遍是纯 CPU 浪费；
# SVG 是文本，压缩比很高，所以它在名单里。1KB 以下不压：小响应压完常常更大，
# 而且省下的字节还不够一个包。级别 6 是 zlib 默认，4.25MB 压一次 30ms、
# 收口后的 395KB 只要几毫秒。
GZIP_TYPES = ("text/", "application/json", "image/svg+xml")
GZIP_MIN_BYTES = 1024
GZIP_LEVEL = 6


def gzip_if_worthwhile(body, content_type, accepts_gzip):
    """压得动就返回压好的正文，否则返回 None（照发原文）。

    单独抽出来是为了能直接验：走 HTTP 那条路验不到阈值 —— 小到能触发阈值的响应
    通常也压不动，两条规则的效果重合，删掉阈值用例照样绿。
    """
    if not accepts_gzip or len(body) < GZIP_MIN_BYTES:
        return None
    if not content_type.startswith(GZIP_TYPES):
        return None
    encoded = gzip.compress(body, GZIP_LEVEL)
    # 压不动就别压：省下客户端的解压，也避免 Content-Length 反而变大。
    return encoded if len(encoded) < len(body) else None


IMAGE_MANIFEST = STATIC_DIR / "openjudge" / "images" / "manifest.json"
if IMAGE_MANIFEST.is_file():
    _image_assets = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8")).get("assets", {})
else:
    _image_assets = {}
MIRRORED_IMAGE_URLS = {
    source: entry["path"] for source, entry in _image_assets.items()
    if isinstance(entry, dict) and isinstance(entry.get("path"), str)
}
MIRRORED_IMAGE_PATTERN = (
    re.compile("|".join(re.escape(source) for source in sorted(MIRRORED_IMAGE_URLS, key=len,
                                                               reverse=True)))
    if MIRRORED_IMAGE_URLS else None
)
BOOK_META = {
    "practice": {"name": "题库（包括计概、数算题目）", "count": 986},
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

# 提交页在 `submit.html`。判题结果不再直接 dump JSON —— 项目的立意是
# 「反馈错在哪组数据」，所以 WA 要把 case 编号、期望/实际 token 数摆出来，
# TLE/RE 要把判题器的 message 摆出来。
#
# 它曾经是这个文件里一段 800 行的字符串常量，占了 server.py 的三分之一。
# 搬成独立文件有三个好处：`server.py` 回到能整体读完的长度；页面 JS 里的
# `\b` 不再需要 raw 字符串保护（HTML 文件里没有 Python 转义这回事）；
# 改页面不用重启服务 —— 下面按 mtime 失效。
SUBMIT_TEMPLATE = ROOT / "submit.html"
_SUBMIT_PAGE_CACHE = {}


def submit_page_template():
    """读一次缓存一次，文件变了自动重读。"""
    mtime = SUBMIT_TEMPLATE.stat().st_mtime_ns
    if _SUBMIT_PAGE_CACHE.get("mtime") != mtime:
        _SUBMIT_PAGE_CACHE["text"] = SUBMIT_TEMPLATE.read_text(encoding="utf-8")
        _SUBMIT_PAGE_CACHE["mtime"] = mtime
    return _SUBMIT_PAGE_CACHE["text"]


# 默认 busy timeout 是 5 秒。一个班同时交时写会互相排队，超时抛的是
# `database is locked` —— 学生看到的是「提交失败」，而那次判题其实已经跑完了。
DB_BUSY_TIMEOUT_SECONDS = 15

# 每行提交都带着整份源码（`source` 列），所以全表扫描扫的是代码正文，不是几个整数。
# 索引列按各处 where/group by 的实际前缀选：
#   (book, problem, id)  → 目录页的 group by book,problem；题库页的 where book=? group by problem；
#                          提交记录按题过滤后 order by id desc
#   (book, lower(user))  → 题库页的每人一行（where book=? and lower(user)=lower(?)、group by lower(user)）
#   (lower(user), id)    → /api/submissions?mine=1 的 order by id desc limit
#   (result, problem)    → /api/stats 的两条 where result='Accepted'（首页每 60 秒轮一次）
SUBMISSION_INDEXES = (
    ("submissions_book_problem_id", "submissions(book, problem, id desc)"),
    ("submissions_book_user", "submissions(book, lower(user))"),
    ("submissions_user_id", "submissions(lower(user), id desc)"),
    ("submissions_result_problem", "submissions(result, problem)"),
)


def connect_db():
    """统一的库连接。

    只加 busy timeout：WAL 是写进库文件的持久设置，`init_db()` 开一次就够。
    """
    return sqlite3.connect(DB, timeout=DB_BUSY_TIMEOUT_SECONDS)


def init_db():
    DB.parent.mkdir(exist_ok=True)
    with connect_db() as db:
        # 默认的 rollback journal 下写者会挡住读者：判题写一条记录的工夫，
        # 别人翻题库页就得等。WAL 让读写并行，代价是库旁边多两个 `-wal`/`-shm`
        # 文件（已加进 .gitignore —— `data/*.db` 匹配不到它们）。
        # 备份走 `Connection.backup()` 在线接口，WAL 下同样拿得到一致快照。
        db.execute("pragma journal_mode=WAL")
        db.execute("create table if not exists submissions (id integer primary key, user text, problem text, result text, created text default current_timestamp)")
        db.execute("create table if not exists users (username text primary key, password_hash text not null, created text default current_timestamp)")
        db.execute("create table if not exists settings (key text primary key, value text not null)")
        # 历史库里没有这几列；用 ALTER 补，已存在则跳过（create table if not exists 加不了列）。
        existing = {row[1] for row in db.execute("pragma table_info(submissions)")}
        for column in ("book text", "language text", "detail text", "source text"):
            if column.split()[0] not in existing:
                db.execute(f"alter table submissions add column {column}")
        user_columns = {row[1] for row in db.execute("pragma table_info(users)")}
        for column in ("email text", "nickname text", "active integer default 1", "activation_token_hash text", "activation_expires integer", "reset_token_hash text", "reset_expires integer"):
            if column.split()[0] not in user_columns:
                db.execute(f"alter table users add column {column}")
        db.execute("update users set active = 1 where activation_token_hash is null")
        db.execute("update users set nickname = username where nickname is null or trim(nickname) = ''")
        # 索引建在补完列之后：`book` 是 ALTER 加上来的，提前建会 no such column。
        for name, target in SUBMISSION_INDEXES:
            db.execute(f"create index if not exists {name} on {target}")

# 「出错那组的输入片段」开关。默认**关**：管理员忘了考前关掉是泄题，
# 忘了课后打开只是少点帮助——两种疏忽的代价不对称，所以默认取保守的一侧。
REVEAL_KEY = "reveal_failing_input"
SNIPPET_CHARS = 400
SNIPPET_LINES = 12


def get_setting(key, default=""):
    with connect_db() as db:
        row = db.execute("select value from settings where key = ?", (key,)).fetchone()
    return row[0] if row else default


def set_setting(key, value):
    with connect_db() as db:
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
    with connect_db() as db:
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


def failing_case_file(book, problem_id, case_index, kind):
    """出错那组的数据文件路径。`kind` 取 "input" / "output"。

    改动前这两个取片段的函数各自 `json.loads` 整份 5.6MB 的 catalog（各 40ms），
    而隔壁 `catalog_raw()` 就是带 mtime 失效的缓存 —— 一次 WA 反馈白解析两遍。
    """
    catalog = catalog_raw()
    item = next((p for p in catalog.get("problems", [])
                 if p.get("book") == book and p.get("id") == problem_id), None)
    cases = (item or {}).get("test_cases") or []
    if not 1 <= case_index <= len(cases):
        return None
    path = MIRROR / cases[case_index - 1][kind]
    return path if path.is_file() else None


def failing_input_snippet(book, problem_id, case_index):
    """取出错那组的输入片段。只给输入，绝不给期望输出——那是答案。"""
    path = failing_case_file(book, problem_id, case_index, "input")
    if path is None:
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    clipped = "\n".join(lines[:SNIPPET_LINES])
    truncated = len(lines) > SNIPPET_LINES or len(clipped) > SNIPPET_CHARS
    return {"text": clipped[:SNIPPET_CHARS], "truncated": truncated,
            "total_lines": len(lines), "total_chars": len(text)}

def failing_output_snippet(book, problem_id, case_index):
    """Read the expected .out for the failing case and cap only the UI payload."""
    path = failing_case_file(book, problem_id, case_index, "output")
    if path is None:
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


# `catalog.json` 的 `test_cases` 是每题逐组的数据文件路径清单，占整份目录的 90%
# （实测：整个响应 4.25MB，其中 3.9MB 是它）。**页面一个字段都没用到** ——
# `problems.html` 与 `admin.html` 只读 book/id/path/title/test_count/pass_rate/
# accepted_count/attempt_count。判题取数据走 `catalog_raw()`，不经这个响应。
# 顺带也不再把 `_made/` 与归档目录的内部布局透给任何访客。
CATALOG_INTERNAL_FIELDS = ("test_cases",)


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
            "problems": [{**{k: v for k, v in item.items() if k not in CATALOG_INTERNAL_FIELDS},
                          "title": catalog_title(item)} for item in problems],
            "unique_total": len(all_keys),
            "unique_tested_count": len(tested_keys),
            "book_meta": BOOK_META,
        }
    with connect_db() as db:
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


BOOK_STATUS_LIMIT = 100


def load_detail(raw):
    """判题详情存的是 JSON 文本。**坏数据不该让整页打不开** —— 返回空 dict。"""
    try:
        detail = json.loads(raw) if raw else {}
    except ValueError:
        return {}
    return detail if isinstance(detail, dict) else {}


def nickname_map(db):
    names = {
        row[0].casefold(): row[1]
        for row in db.execute(
            "select username, coalesce(nullif(trim(nickname), ''), username) from users")
    }
    names.update({
        row[0][len("profile_nickname:"):]: row[1]
        for row in db.execute(
            "select key, value from settings where key like 'profile_nickname:%'")
    })
    return names


def book_user_payload(book, username):
    """兼容旧链接：汇总某个用户在一个题库里做过哪些题。

    只出「结果 / 次数 / 时间」这类记分板字段，**不出代码，也不出判题详情** ——
    这一页是给别人看的，别人的代码只有本人和管理员看得到（`/api/submissions`
    定的规矩），换个 URL 不该换个规矩。
    """
    catalog = {item.get("id", ""): item
               for item in catalog_raw().get("problems", []) if item.get("book") == book}
    with connect_db() as db:
        rows = db.execute(
            """select problem, count(*), max(created),
                      count(case when result = 'Accepted' then 1 end),
                      min(case when result = 'Accepted' then created end)
                 from submissions where book = ? and lower(user) = lower(?)
                group by problem""", (book, username)).fetchall()
        # 每题的「最新一次结果」单独查。**不要靠 max(id) 带出裸列** —— SQLite 只在
        # 查询里恰好有一个 min/max 聚合时才保证裸列来自那一行，这里聚合有好几个。
        latest = dict(db.execute(
            """select s.problem, s.result from submissions s
                 join (select problem, max(id) as top from submissions
                        where book = ? and lower(user) = lower(?) group by problem) m
                   on s.id = m.top""", (book, username)).fetchall())
        canonical = db.execute(
            """select user from submissions where book = ? and lower(user) = lower(?)
                order by id desc limit 1""", (book, username)).fetchone()
    if canonical is None:
        return None
    problems = []
    for problem, attempts, last_submit, accepted, first_accepted in rows:
        item = catalog.get(problem, {})
        problems.append({
            "id": problem,
            "title": catalog_title({"book": book, "id": problem}),
            "path": item.get("path", ""),
            "result": "Accepted" if accepted else latest.get(problem, ""),
            "attempts": attempts,
            "accepted_at": first_accepted,
            "last_submit": last_submit,
        })
    problems.sort(key=lambda entry: entry["id"])
    return {
        "book": book,
        "name": BOOK_META.get(book, {}).get("name", book),
        "user": canonical[0],
        "solved": sum(1 for entry in problems if entry["result"] == "Accepted"),
        "attempted": len(problems),
        "submissions": sum(entry["attempts"] for entry in problems),
        "problems": problems,
    }


def book_solution_payload(book, submission_id, viewer):
    """一次提交的详情。状态页点结果进来的就是这一页。

    分成两半：**记分板那半人人可见**（谁、哪道题、什么结果、用时内存代码长度），
    **代码与判题详情只有本人和管理员**。这跟 `/api/submissions` 是同一条判断，
    照抄而不是另写一份 —— 权限判断有两份，迟早只改一份。
    """
    with connect_db() as db:
        row = db.execute(
            """select id, user, problem, result, created, language, detail, source
                 from submissions where id = ? and book = ?""", (submission_id, book)).fetchone()
    if row is None:
        return None
    detail = load_detail(row[6])
    owner = same_username(row[1] or "", viewer) or same_username(viewer, ADMIN_USER)
    item = next((entry for entry in catalog_raw().get("problems", [])
                 if entry.get("book") == book and entry.get("id") == row[2]), {})
    return {
        "id": row[0],
        "book": book,
        "name": BOOK_META.get(book, {}).get("name", book),
        "user": row[1],
        "problem": row[2],
        "title": catalog_title({"book": book, "id": row[2]}),
        "path": item.get("path", ""),
        "result": row[3],
        "created": row[4],
        "language": row[5],
        "language_version": detail.get("language_version"),
        "time_ms": detail.get("time_ms"),
        "memory_kb": detail.get("memory_kb"),
        "source_bytes": detail.get("source_bytes"),
        "mine": owner,
        "detail": detail if owner else {},
        "source": (row[7] or "") if owner else "",
    }


def book_page_payload(book, authenticated, status_problem="", status_name=""):
    """题库页要的三份数据：题目表、排名、最近状态。

    排名和状态**只在登录后返回**。理由不是洁癖：站点已经通过 Tailscale Funnel
    对公网开着（见 docs/管理员手册.md），「谁在几点交了哪道题」连起来就是作息，
    没有理由对匿名访客敞开。题目表本来就在 `/api/catalog` 里公开，这里维持不变。

    这里只从 detail 里取 time_ms / memory_kb 两个数。**不要顺手把 detail 整个
    发出去** —— 它含 `failing_input` / `expected_output`，那是出错那组的测试数据，
    公开等于泄题（同一个理由让 `/api/submissions` 把 detail 限死在本人和管理员）。
    """
    problems = [item for item in catalog_raw().get("problems", []) if item.get("book") == book]
    ranking, status = [], []
    with connect_db() as db:
        stats = {
            row[0]: {
                "attempt_count": row[1],
                "accepted_count": row[2],
                "pass_rate": f"{row[2] / row[1] * 100:.0f}%" if row[1] else "",
            }
            for row in db.execute(
                """select problem, count(distinct lower(user)),
                          count(distinct case when result = 'Accepted' then lower(user) end)
                     from submissions where book = ? group by problem""", (book,))
        }
        if authenticated:
            nicknames = nickname_map(db)
            ranking = [
                {"user": row[0] or "",
                 "name": nicknames.get(str(row[0] or "").casefold(), row[0] or ""),
                 "solved": row[1], "submissions": row[2], "last_submit": row[3]}
                for row in db.execute(
                    """select min(user),
                              count(distinct case when result = 'Accepted' then problem end),
                              count(*), max(created)
                         from submissions where book = ?
                         group by lower(user)
                         order by 2 desc, 3 asc, 4 asc, lower(min(user)) asc""", (book,))
            ]
            status_sql = """select id, created, user, problem, result, language, detail, source
                              from submissions where book = ?"""
            status_params = [book]
            if status_problem:
                status_sql += " and lower(problem) = lower(?)"
                status_params.append(status_problem)
            if status_name:
                term = status_name.casefold()
                matching_users = [
                    str(row[0] or "").casefold()
                    for row in db.execute(
                        "select distinct user from submissions where book = ?", (book,))
                    if term in str(nicknames.get(str(row[0] or "").casefold(), row[0] or "")).casefold()
                ]
                if matching_users:
                    status_sql += " and lower(user) in (" + ",".join(["?"] * len(matching_users)) + ")"
                    status_params.extend(matching_users)
                else:
                    status_sql += " and 0"
            status_sql += " order by id desc limit ?"
            status_params.append(BOOK_STATUS_LIMIT)
            for row in db.execute(status_sql, status_params):
                detail = load_detail(row[6])
                status.append({"id": row[0], "created": row[1], "user": row[2],
                               "name": nicknames.get(str(row[2] or "").casefold(), row[2] or ""),
                               "problem": row[3],
                               "title": catalog_title({"book": book, "id": row[3]}),
                               "result": row[4], "language": row[5], "time_ms": detail.get("time_ms"),
                               "memory_kb": detail.get("memory_kb"),
                               "source_bytes": detail.get(
                                   "source_bytes", len((row[7] or "").encode("utf-8")))})
    return {
        "book": book,
        "name": BOOK_META.get(book, {}).get("name", book),
        "problem_count": len(problems),
        "tested_count": sum(1 for item in problems if (item.get("test_count") or 0) > 0),
        "authenticated": authenticated,
        "filters": {"problem": status_problem, "name": status_name},
        "problems": [
            {
                "id": item.get("id", ""),
                "path": item.get("path", ""),
                "title": catalog_title(item),
                "test_count": item.get("test_count", 0),
                **stats.get(item.get("id", ""),
                            {"attempt_count": 0, "accepted_count": 0, "pass_rate": ""}),
            }
            for item in problems
        ],
        "ranking": ranking,
        "status": status,
    }


PBKDF2_ROUNDS = 120000
LEGACY_SALT = b"cs101-local-user"          # 改动前全库共用这一个盐，且它就写在源码里


def password_hash(password, salt=None):
    """每个用户一份随机盐，存成 `pbkdf2$轮数$盐$哈希`。

    改动前所有用户共用源码里的常量盐 `cs101-local-user`。后果不是理论上的：
    同一个口令在库里就是同一串哈希（口令谁和谁一样，看一眼就知道），
    而且盐公开、全库只有一份 —— 一张彩虹表就能同时打所有账号。
    在这个洞之上，`/data/course.db` 还一度可以直接下载（见 T-010）。
    """
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ROUNDS).hex()
    return f"pbkdf2${PBKDF2_ROUNDS}${salt.hex()}${digest}"


def legacy_password_hash(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), LEGACY_SALT, PBKDF2_ROUNDS).hex()


def same_username(left, right):
    return str(left).strip().casefold() == str(right).strip().casefold()

def valid_password(stored, password):
    """新旧两种格式都认；比较一律走 compare_digest，不用 `==`。"""
    stored = str(stored or "")
    if stored.startswith("pbkdf2$"):
        try:
            _, rounds, salt_hex, digest = stored.split("$", 3)
            candidate = hashlib.pbkdf2_hmac("sha256", password.encode(),
                                            bytes.fromhex(salt_hex), int(rounds)).hex()
        except (ValueError, TypeError):
            return False
        return hmac.compare_digest(candidate, digest)
    return hmac.compare_digest(stored, legacy_password_hash(password))


def needs_rehash(stored):
    """老格式（固定盐）在下一次成功登录时顺手升级，不用要求用户改密。"""
    return not str(stored or "").startswith("pbkdf2$")

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

# 未配邮件服务时是否把激活/重置链接直接回给调用者。**只为本机开发存在**：
# 打开它等于「知道邮箱就能拿到该邮箱的账号链接」。
ACCOUNT_LINKS_ENV = "CS101_SHOW_ACCOUNT_LINKS"
SESSION_ISSUED = {}
SESSION_TTL_SECONDS = 14 * 24 * 3600
LOGIN_FAILURES = {}
LOGIN_MAX_FAILURES = 10
LOGIN_LOCKOUT_SECONDS = 900


def start_session(username):
    token = secrets.token_urlsafe(24)
    TOKENS.add(token); SESSION_USERS[token] = username
    SESSION_SEEN[token] = SESSION_ISSUED[token] = time.time()
    return token


def drop_session(token):
    TOKENS.discard(token)
    SESSION_USERS.pop(token, None)
    SESSION_SEEN.pop(token, None)
    SESSION_ISSUED.pop(token, None)


def revoke_sessions(username, keep=None):
    """改密/重置口令后把该用户的其它会话全部作废。

    改动前不做这件事，于是「我号被盗了，赶紧改密码」这个动作**根本不起作用** ——
    盗号者手上的 cookie 改密之后照样能用（实测过）。改密是补救被盗的标准手段，
    它必须能把别人踢下线，否则等于没补救。
    """
    for token in [t for t, u in SESSION_USERS.items()
                  if same_username(u, username) and t != keep]:
        drop_session(token)


def session_expired(token):
    issued = SESSION_ISSUED.get(token)
    if issued is None:                      # 服务重启前签发的会话，补记一次签发时间
        SESSION_ISSUED[token] = time.time()
        return False
    return time.time() - issued > SESSION_TTL_SECONDS


def login_locked(username):
    """同一用户名连续失败过多就冷却一段时间。

    按用户名而不是按 IP：一个班往往共用出口 IP，按 IP 锁会把整班一起锁掉。
    """
    failures, until = LOGIN_FAILURES.get(str(username).casefold(), (0, 0.0))
    return failures >= LOGIN_MAX_FAILURES and time.time() < until


def note_login_failure(username):
    key = str(username).casefold()
    failures, until = LOGIN_FAILURES.get(key, (0, 0.0))
    if time.time() >= until:
        failures = 0
    LOGIN_FAILURES[key] = (failures + 1, time.time() + LOGIN_LOCKOUT_SECONDS)


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


def safe_return_path(value):
    """Allow login redirects only to an ordinary path on this site.

    `<` 和 `>` 一起挡掉，理由不是「看着不像路径」：这个值会被 `json.dumps` 塞进
    **登录页的内联 `<script>`**，而 `json.dumps` 只转义引号和反斜杠，不转义 `<` 和 `/`。
    于是 `?next=/x</script><script>…</script>` 会提前关掉脚本块，把攻击者的标签
    注入到**用户输入口令的那一页**上。合法的同站路径里这两个字符本来就该是
    百分号编码的，直接拒绝不会误伤。落库处另有 `</` 转义兜底（见 account_page）。
    """
    value = str(value or "")
    if (not value.startswith("/") or value.startswith("//") or "\\" in value
            or "<" in value or ">" in value
            or len(value) > 2048 or any(ord(character) < 32 for character in value)):
        return "/"
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return "/"
    return value

# 反向代理（Tailscale Funnel / Cloudflare / nginx）会把请求转成本机连接，
# 只有来自这里的连接才允许用 X-Forwarded-For 覆盖来源地址 —— 否则任何人
# 直接连上来加一个头就能伪造自己的 IP，限频形同虚设。
TRUSTED_PROXIES = {"127.0.0.1", "::1"}


class Handler(BaseHTTPRequestHandler):
    def client_ip(self):
        """真实客户端地址；限频与日志都用它。

        **实测（2026-07-28 开 Funnel 后）**：从公网发来的请求，
        `self.client_address[0]` 是 `127.0.0.1` —— 因为 Funnel 在本机做反代。
        照此按来源地址限频，会把**整个互联网算成一个客户端**：
        一个脚本就能耗尽全局额度把所有人挡在门外，而它自己也不会被单独限住。
        注册与找回密码是仅有的两个未登录端点，限频是它们唯一的闸，所以这条必须对。
        """
        peer = self.client_address[0]
        if peer in TRUSTED_PROXIES:
            first = self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            if first:
                return first
        return peer

    def session_cookie(self, token):
        """会话 cookie。经 HTTPS 进来时加 Secure。

        按请求判断而不是全局开关：这台机器同时可以走 tailnet 内的 HTTP 访问，
        一刀切加 Secure 会让那条路径登不上。伪造这个头只会让伪造者自己的 cookie
        变成 Secure，损人不利己，所以采信它是安全的。
        """
        secure = "; Secure" if self.headers.get("X-Forwarded-Proto") == "https" else ""
        return f"session={token}; HttpOnly; SameSite=Lax; Path=/{secure}"

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.client_ip(), fmt % args))

    def accepts_gzip(self):
        return "gzip" in self.headers.get("Accept-Encoding", "").lower()

    def send_body(self, body, content_type, status=200, cache=None, etag=None):
        """统一出口：按需 gzip，带上缓存头。

        压缩只对文本类型、且只在超过 `GZIP_MIN_BYTES` 时做 —— 小响应压完反而更大，
        而图片/字体本身已经是压缩格式，再压一遍是纯 CPU 浪费。
        压过的响应必须带 `Vary: Accept-Encoding`，否则中间缓存会把 gzip 的那份
        发给不支持 gzip 的客户端。
        """
        encoded = gzip_if_worthwhile(body, content_type, self.accepts_gzip())
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        if cache:
            self.send_header("Cache-Control", cache)
        if etag:
            self.send_header("ETag", etag)
        if content_type.startswith(GZIP_TYPES):
            self.send_header("Vary", "Accept-Encoding")
        if encoded is not None:
            self.send_header("Content-Encoding", "gzip")
            body = encoded
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_body(body, "application/json; charset=utf-8", status)

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
        if session_expired(token.value):
            drop_session(token.value); return False
        self._touch(token.value)
        return True

    def current_user(self):
        raw = self.headers.get("Cookie", "")
        token = cookies.SimpleCookie(raw).get("session")
        if not token or token.value not in TOKENS:
            return None
        if session_expired(token.value):
            drop_session(token.value); return None
        self._touch(token.value)
        return SESSION_USERS.get(token.value)

    def send_html(self, body):
        if isinstance(body, str): body = body.encode("utf-8")
        # 所有页面都从这里出去（含读盘的 `.html` 与镜像题面），
        # 所以主题引导只需在这一处注入。
        body = body.replace(THEME_HEAD_SLOT.encode(), THEME_HEAD.encode())
        self.send_body(body, "text/html; charset=utf-8")

    def send_static(self, file, content_type):
        """静态分发。带 ETag 复验；镜像图片按不可变缓存。

        改动前这里一个缓存头都没有：`theme.css` 每翻一页重下，题面里的图片
        每次打开都重取（`static/openjudge/images/` 有 16MB）。
        `mirror/` 下的文件名就是内容哈希，同名文件内容不可能变 —— 抓取脚本
        换内容就换文件名 —— 所以对它用 immutable 是安全的。其余静态文件走
        `no-cache`：每次仍来问一句，但命中 ETag 就只回一个 304，省掉正文。
        """
        stat = file.stat()
        etag = f'W/"{stat.st_size:x}-{stat.st_mtime_ns:x}"'
        immutable = file.parent == STATIC_DIR / "openjudge" / "images" / "mirror"
        cache = "public, max-age=31536000, immutable" if immutable else "no-cache"
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.send_header("Cache-Control", cache)
            self.send_header("ETag", etag)
            self.end_headers(); return
        self.send_body(file.read_bytes(), content_type, cache=cache, etag=etag)

    def local_page(self, page):
        text = page.read_text(encoding="utf-8", errors="replace")
        text = text.replace("http://cs101.openjudge.cn/", "/")
        text = text.replace("https://cs101.openjudge.cn/", "/")
        text = text.replace("http://cs101.openjudge.cn", "/")
        text = text.replace("https://cs101.openjudge.cn", "/")
        # 镜像页的 <head> 里写死了 POJ 的 favicon（static.openjudge.cn），
        # 上面那几条只改 cs101.openjudge.cn，管不到它 —— 于是本地打开镜像页，
        # 标签页上挂的是别人家的图标。换成本站的。
        text = re.sub(r'href="https?://static\.openjudge\.cn/styles/favicon\.ico[^"]*"',
                      'href="/static/favicon.svg"', text)
        # 题面图片统一走本站副本：既避免 HTTP mixed content，也避免外站失效或限流。
        # 清单由抓取脚本生成，运行时改写保证重新抓取 HTML 后仍使用同源资源。
        if MIRRORED_IMAGE_PATTERN:
            text = MIRRORED_IMAGE_PATTERN.sub(
                lambda match: MIRRORED_IMAGE_URLS[match.group(0)], text)
        return text

    def book_page(self, book, view, subject=""):
        template = (ROOT / "book.html").read_text(encoding="utf-8")
        return (template.replace("__BOOK_NAME__", escape(BOOK_META.get(book, {}).get("name", book)))
                .replace("__BOOK_JSON__", json.dumps(book, ensure_ascii=False))
                .replace("__VIEW_JSON__", json.dumps(view))
                .replace("__SUBJECT_JSON__", json.dumps(subject, ensure_ascii=False).replace("</", "<\\/"))
                .replace("__BOOK__", escape(book)))

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
        return (submit_page_template().replace("__BOOK__", escape(book))
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
__THEME_HEAD__<style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:820px;margin:auto;padding:0 24px}.top{height:72px;display:flex;align-items:center;justify-content:space-between}.brand{display:flex;gap:11px;align-items:center;text-decoration:none;color:var(--ink);font-weight:750}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg)}.back{color:var(--green);text-decoration:none}.panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:30px 34px;box-shadow:0 12px 34px rgba(34,63,45,.06)}h1{font-size:30px;margin:0 0 7px}h2{font-size:18px;margin:28px 0 8px;padding-top:20px;border-top:1px solid var(--line)}p{color:var(--muted)}.rule{padding:14px 16px;border-left:3px solid var(--warn);background:var(--soft);color:var(--ink)}code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);padding:2px 5px;border-radius:4px}@media(max-width:600px){.shell{padding:0 16px}.panel{padding:24px 20px}.top{height:62px}}
</style></head><body><header class="top shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><a class="back" href="/">返回首页</a></header><main class="shell"><section class="panel"><h1>帮助/说明</h1><p>这里使用本机测试数据判题，提交页右侧选择语言后即可提交代码并查看每组数据的结果。</p><h2>时间与内存倍率</h2><div class="rule">Python ×10 · PyPy3 ×3 · C/C++/Swift/Objective-C ×1 · C#/F#/VB.NET ×2<br>C#/F#/VB.NET 内存 ×2</div><h2>题面限制的含义</h2><p>题面显示的时限按 C/C++ 计算，是全部测试点限时之和。其他语言按照上面的倍率执行；内存限制仅对 C#、F#、VB.NET 按 2 倍计算。</p><h2>提交结果</h2><p>提交记录会保留提交人、结果、语言、运行时间、内存和代码。出现错误时，判题详情会标出出错的数据组，并展示对应的输入、期望输出和实际输出。</p><h2>文档</h2><p><a class="back" href="https://gmyhf.github.io/cs101.openjudge.cn/dev-handbook.html" target="_blank" rel="noopener">CS101 判题系统开发教学手册</a></p><p><a class="back" href="https://github.com/GMyhf/cs101.openjudge.cn/blob/main/docs/%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C.md" target="_blank" rel="noopener">使用手册</a></p><p><a class="back" href="https://github.com/GMyhf/cs101.openjudge.cn/blob/main/docs/%E7%AE%A1%E7%90%86%E5%91%98%E6%89%8B%E5%86%8C.md" target="_blank" rel="noopener">管理员手册</a></p></section></main></body></html>"""

    def account_page(self, register=False, next_path="/"):
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
        after_login_json = json.dumps(next_path).replace("</", "<\\/")
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
__THEME_HEAD__<style>
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}.shell{{max-width:460px;margin:0 auto;padding:70px 20px}}.brand{{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}}.mark{{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}}.panel{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}}h1{{font-size:28px;line-height:1.2;margin:0 0 6px}}.intro{{color:var(--muted);margin:0 0 23px}}label{{display:block;margin:16px 0 6px;font-weight:600}}input{{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;background:var(--panel);font:inherit;outline:none}}input:focus{{border-color:var(--green);box-shadow:0 0 0 3px var(--accent-soft)}}button{{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}}a{{color:var(--green)}}.links{{margin:19px 0 0;color:var(--muted);font-size:14px;text-align:center}}.error{{min-height:22px;color:var(--danger);margin:12px 0 0}}.captcha-question{{display:inline-block;margin-left:5px;color:var(--green);font-family:ui-monospace,monospace}}@media(max-width:520px){{.shell{{padding:35px 16px}}.panel{{padding:24px}}}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><h1>{title}</h1><p class="intro">{'创建账号后即可提交代码并查看判题记录。' if register else '登录后继续使用提交与判题功能。'}</p><form id="account">{fields}<p id="error" class="error"></p><button>提交</button></form><p class="links">{links} · <a href="/">返回首页</a></p></section></main><script>const form=document.querySelector('#account'),error=document.querySelector('#error'),AFTER_LOGIN={after_login_json};form.onsubmit=async e=>{{e.preventDefault();error.textContent='';const data=Object.fromEntries(new FormData(form));if(data.confirm_password!==undefined&&data.password!==data.confirm_password){{error.textContent='两次输入的密码不一致';return}}const r=await fetch('{endpoint}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}});const d=await r.json();if(r.ok){{if(d.activation_link){{error.style.color='var(--accent)';error.innerHTML='注册成功，请点击激活链接：<a href="'+d.activation_link+'">激活账号</a>';form.querySelector('button').disabled=true}}else location.href=AFTER_LOGIN}}else error.textContent=d.error||'操作失败'}};</script></body></html>"""

    def activation_page(self, token):
        with connect_db() as db:
            row = db.execute("select username from users where activation_token_hash = ? and activation_expires > ? and active = 0",
                             (reset_token_hash(token), int(time.time()))).fetchone()
            if row:
                db.execute("update users set active = 1, activation_token_hash = null, activation_expires = null where username = ?", (row[0],))
                message, detail = "账号已激活", "现在可以登录 CS101 题库。"
            else:
                message, detail = "激活链接无效或已过期", "请重新注册或联系管理员。"
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{message} · CS101</title>
__THEME_HEAD__<style>body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:30px}}h1{{margin:0 0 10px}}p{{color:var(--muted)}}a{{color:var(--accent)}}</style></head><body><main><section><h1>{message}</h1><p>{detail}</p><p><a href="/auth/login/">前往登录</a></p></section></main></body></html>"""

    def forgot_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>找回密码 · CS101</title>
__THEME_HEAD__<style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:460px;margin:0 auto;padding:70px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:28px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}h1{font-size:28px;line-height:1.2;margin:0 0 6px}.intro{color:var(--muted);margin:0 0 23px}label{display:block;margin:16px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;font:inherit;outline:none}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}a{color:var(--green)}.message{color:var(--muted);margin-top:15px;word-break:break-word}@media(max-width:520px){.shell{padding:35px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><h1>忘记密码？</h1><p class="intro">输入注册邮箱，我们会生成一次性密码重置链接。</p><form id="forgot"><label>邮箱地址<input name="email" type="email" required autocomplete="email"></label><button>发送重置链接</button></form><p id="message" class="message"></p><p><a href="/auth/login/">返回登录</a> · <a href="/register/">点此注册</a></p></section></main><script>forgot.onsubmit=async e=>{e.preventDefault();message.textContent='正在处理…';const r=await fetch('/api/user/forgot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(forgot)))});const d=await r.json();message.innerHTML=d.reset_link?'邮件服务尚未配置，请使用本机重置链接：<a href="'+d.reset_link+'">立即重置密码</a>':'如果该邮箱已注册，重置链接已发送或正在等待管理员配置邮件服务。';}</script></body></html>"""

    def reset_page(self, token):
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>重置密码 · CS101</title>
__THEME_HEAD__<style>body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,sans-serif}}main{{max-width:460px;margin:70px auto;padding:0 20px}}section{{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:30px}}h1{{margin:0 0 20px}}label{{display:block;margin:14px 0 6px;font-weight:600}}input{{width:100%;padding:11px;box-sizing:border-box;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);font:inherit}}button{{width:100%;margin-top:20px;padding:11px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit}}a{{color:var(--accent)}}#message{{color:var(--danger)}}</style></head><body><main><section><h1>设置新密码</h1><form id="reset"><label>新密码<input name="password" type="password" minlength="8" required autocomplete="new-password"></label><label>确认密码<input name="confirm_password" type="password" minlength="8" required autocomplete="new-password"></label><p id="message"></p><button>保存新密码</button></form><p><a href="/auth/login/">返回登录</a></p></section></main><script>reset.onsubmit=async e=>{{e.preventDefault();message.textContent='';const d=Object.fromEntries(new FormData(reset));if(d.password!==d.confirm_password){{message.textContent='两次输入的密码不一致';return}}d.token={json.dumps(token)};const r=await fetch('/api/user/reset',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});const x=await r.json();if(r.ok){{message.style.color='var(--accent)';message.textContent='密码已更新，请返回登录。';reset.querySelector('button').disabled=true}}else message.textContent=x.error||'重置失败'}};</script></body></html>"""

    def account_settings_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>账户设置 · CS101</title>
__THEME_HEAD__<style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:520px;margin:0 auto;padding:52px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:24px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}.topline{display:flex;justify-content:space-between;align-items:start;gap:15px;margin-bottom:22px}h1{font-size:28px;line-height:1.2;margin:0 0 5px}.muted{color:var(--muted);margin:0}.back{color:var(--green);text-decoration:none;font-size:14px}h2{font-size:16px;margin:0 0 14px;padding-top:22px;border-top:1px solid var(--line)}label{display:block;margin:14px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;font:inherit;outline:none}input:focus{border-color:var(--green);box-shadow:0 0 0 3px var(--accent-soft)}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}.message{min-height:22px;color:var(--danger);margin:12px 0 0}.logout{display:block;width:100%;margin-top:12px;padding:10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);font:inherit;cursor:pointer}@media(max-width:520px){.shell{padding:30px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><div class="topline"><div><h1>账户设置</h1><p id="user" class="muted">正在读取账户…</p></div><a class="back" href="/">返回首页</a></div><h2>修改密码</h2><form id="change"><label>当前密码<input name="current_password" type="password" required autocomplete="current-password"></label><label>新密码<input name="new_password" type="password" minlength="8" required autocomplete="new-password"></label><label>确认新密码<input name="confirm_password" type="password" minlength="8" required autocomplete="new-password"></label><p id="message" class="message"></p><button>保存新密码</button></form><button id="logout" class="logout">退出登录</button></section></main><script>
fetch('/api/me').then(r=>r.json()).then(d=>{if(!d.authenticated)location.href='/auth/login/';else user.textContent='用户名：'+d.user}).catch(()=>location.href='/auth/login/');
change.onsubmit=async e=>{e.preventDefault();message.textContent='';const d=Object.fromEntries(new FormData(change));if(d.new_password!==d.confirm_password){message.textContent='两次输入的新密码不一致';return}const r=await fetch('/api/user/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const x=await r.json();if(r.ok){message.style.color='var(--accent)';message.textContent='密码已更新。';change.reset()}else message.textContent=x.error||'修改失败'};
logout.onclick=async()=>{await fetch('/api/logout',{method:'POST'});location.href='/'};
</script></body></html>"""

    def profile_settings_page(self):
        return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>个人信息 · CS101</title>
__THEME_HEAD__<style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:520px;margin:0 auto;padding:52px 20px}.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;margin-bottom:24px}.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--ink);color:var(--bg);font-size:15px}.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:30px;box-shadow:0 18px 45px rgba(34,63,45,.08)}.topline{display:flex;justify-content:space-between;align-items:start;gap:15px;margin-bottom:22px}h1{font-size:28px;line-height:1.2;margin:0 0 5px}.muted{color:var(--muted);margin:0}.back{color:var(--green);text-decoration:none;font-size:14px}label{display:block;margin:14px 0 6px;font-weight:600}input{display:block;width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink);font:inherit;outline:none}input:focus{border-color:var(--green);box-shadow:0 0 0 3px var(--accent-soft)}input[readonly]{background:var(--panel);color:var(--muted)}button{width:100%;margin-top:20px;padding:11px 15px;background:var(--ink);color:var(--bg);border:0;border-radius:6px;font:inherit;font-weight:650;cursor:pointer}.message{min-height:22px;color:var(--danger);margin:12px 0 0}@media(max-width:520px){.shell{padding:30px 16px}.panel{padding:24px}}
</style></head><body><main class="shell"><a class="brand" href="/"><span class="mark">CS</span><span>CS101 题库</span></a><section class="panel"><div class="topline"><div><h1>个人信息</h1><p class="muted">设置排名中显示的名字</p></div><a class="back" href="/">返回首页</a></div><form id="profile"><label>用户名<input id="username" readonly></label><label>昵称<input id="nickname" name="nickname" maxlength="32" required autocomplete="nickname"></label><p id="message" class="message"></p><button>保存个人信息</button></form></section></main><script>
fetch('/api/profile').then(async r=>{if(r.status===401){location.href='/auth/login/';return null}const d=await r.json();if(!r.ok)throw new Error(d.error||'读取失败');return d}).then(d=>{if(d){username.value=d.username;nickname.value=d.nickname}}).catch(e=>message.textContent=e.message);
profile.onsubmit=async e=>{e.preventDefault();message.textContent='';const r=await fetch('/api/profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nickname:nickname.value})});const d=await r.json();if(r.ok){nickname.value=d.nickname;message.style.color='var(--green)';message.textContent='个人信息已保存。'}else{message.style.color='var(--danger)';message.textContent=d.error||'保存失败'}};
</script></body></html>"""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        decoded_path = unquote(path)
        if any(part == ".." for part in decoded_path.split("/")):
            self.send_json({"error": "Not found"}, 404); return
        if path == "/auth/login/":
            requested = parse_qs(parsed.query).get("next", [""])[0]
            self.send_html(self.account_page(next_path=safe_return_path(requested))); return
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
        # 浏览器在页面没声明图标时会隐式请求 /favicon.ico。这条路径以前没人接，
        # 于是落到上游代理 —— 真的从 openjudge 取回了 POJ 的图标（894 字节 ICO），
        # 标签页上就是别人家的标。**没被路由接住的路径不是 404，是「转发给上游」**，
        # 这条兜底规则值得每加一个新路径时想一遍。
        if path == "/favicon.ico":
            self.send_response(302)
            self.send_header("Location", "/static/favicon.svg")
            self.send_header("Cache-Control", "max-age=86400")
            self.end_headers(); return
        if path == "/help/":
            self.send_html(self.help_page()); return
        if path == "/account/":
            if not self.authorized():
                self.send_response(302); self.send_header("Location", "/auth/login/"); self.end_headers(); return
            self.send_html(self.account_settings_page()); return
        if path == "/settings/":
            if not self.authorized():
                self.send_response(302); self.send_header("Location", "/auth/login/"); self.end_headers(); return
            self.send_html(self.profile_settings_page()); return
        submit_page = re.fullmatch(r"/(pctbook|2025sp_routine|25dsapre|2024fallroutine|2024sp_routine|dsapre|routine|practice)/([^/]+)/submit/", path)
        if submit_page:
            book, problem_id = submit_page.groups()
            page = MIRROR / "pages" / f"{book}__{problem_id}.html"
            if page.is_file():
                self.send_html(self.submission_page(page, book, problem_id)); return
        # 题库页。三个标签页共用一份模板，视图名由服务端定，前端不去猜 URL。
        # 走 /book/ 前缀而不是接管 /pctbook/：后者仍然是上游镜像的原页面，
        # 老链接（题面里到处都是）不能因为换了首页入口就打不开。
        book_view = re.fullmatch(r"/book/([^/]+)/(ranking/|status/)?", path)
        if book_view and book_view.group(1) in BOOK_META:
            view = (book_view.group(2) or "").rstrip("/") or "problems"
            self.send_html(self.book_page(book_view.group(1), view)); return
        book_user = re.fullmatch(r"/book/([^/]+)/user/([^/]+)/", decoded_path)
        if book_user and book_user.group(1) in BOOK_META:
            self.send_html(self.book_page(book_user.group(1), "user", book_user.group(2))); return
        book_solution = re.fullmatch(r"/book/([^/]+)/solution/(\d+)/", path)
        if book_solution and book_solution.group(1) in BOOK_META:
            self.send_html(self.book_page(book_solution.group(1), "solution", book_solution.group(2))); return
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
        if path == "/api/profile":
            username = self.current_user()
            if username is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            with connect_db() as db:
                row = db.execute(
                    "select coalesce(nullif(trim(nickname), ''), username) from users where username = ?",
                    (username,),
                ).fetchone()
                if row is None:
                    row = db.execute("select value from settings where key = ?",
                                     ("profile_nickname:" + username.casefold(),)).fetchone()
            self.send_json({"username": username, "nickname": row[0] if row else username})
            return
        if path == "/api/stats":
            self.send_json(site_stats())
            return
        if path == "/api/settings":
            book = parse_qs(parsed.query).get("book", [""])[0]
            self.send_json({REVEAL_KEY: reveal_enabled(), "books": reveal_books(),
                            "windows": reveal_windows(), "active_window": active_window(),
                            "quotas": quota_config(), "quota_defaults": QUOTA_DEFAULTS,
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
            query = parse_qs(parsed.query)
            mine = query.get("mine", [""])[0] == "1"
            query_user = str(query.get("user", [""])[0]).strip()[:64]
            query_book = query.get("book", [""])[0]
            query_problem = query.get("problem", [""])[0]
            try:
                limit = min(max(int(query.get("limit", ["50"])[0]), 1), 500)
            except ValueError:
                limit = 50
            with connect_db() as db:
                filters, values = [], []
                if query_book:
                    filters.append("book = ?"); values.append(query_book)
                if query_problem:
                    filters.append("problem = ?"); values.append(query_problem)
                if mine:
                    filters.append("lower(user) = lower(?)"); values.append(user)
                elif query_user:
                    filters.append("lower(user) = lower(?)"); values.append(query_user)
                where = (" where " + " and ".join(filters)) if filters else ""
                rows = db.execute("select id, user, problem, result, created, book, language, detail, source from submissions"
                                  + where + " order by id desc limit ?", (*values, limit)).fetchall()
                nicknames = nickname_map(db)
            is_admin = same_username(user, ADMIN_USER)
            submissions = []
            for row in rows:
                detail = load_detail(row[7])
                owner = is_admin or same_username(row[1] or "", user)
                submissions.append({
                    "id": row[0], "user": row[1],
                    "name": nicknames.get(str(row[1] or "").casefold(), row[1] or ""),
                    "problem": row[2], "title": catalog_title({"book": row[5], "id": row[2]}),
                    "result": row[3], "created": row[4], "book": row[5],
                    "book_name": BOOK_META.get(row[5], {}).get("name", row[5]),
                    "language": row[6], "language_version": detail.get("language_version"),
                    "time_ms": detail.get("time_ms"),
                    "memory_kb": detail.get("memory_kb"),
                    "source_bytes": detail.get(
                        "source_bytes", len((row[8] or "").encode("utf-8"))),
                    "detail": detail if owner else {},
                    "source": (row[8] or "") if owner else "",
                })
            scope_user = user if mine else query_user
            self.send_json({
                "user": user,
                "scope_user": scope_user,
                "scope_name": nicknames.get(scope_user.casefold(), scope_user) if scope_user else "",
                "submissions": submissions,
            })
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
        book_api = re.fullmatch(r"/api/books/([^/]+)/", path)
        if book_api and book_api.group(1) in BOOK_META:
            query = parse_qs(parsed.query)
            status_problem = str(query.get("problem", [""])[0]).strip()[:64]
            status_name = str(query.get("name", [""])[0]).strip()[:64]
            self.send_json(book_page_payload(book_api.group(1), self.authorized(),
                                             status_problem, status_name)); return
        # 用户页与提交详情页整页都要登录：它们展示的是「谁做了什么」，
        # 不像题目表那样本来就公开。未登录一律 401，页面据此提示去登录。
        user_api = re.fullmatch(r"/api/books/([^/]+)/user/([^/]+)/", unquote(path))
        if user_api and user_api.group(1) in BOOK_META:
            if not self.authorized():
                self.send_json({"error": "Unauthorized"}, 401); return
            payload = book_user_payload(user_api.group(1), user_api.group(2))
            if payload is None:
                self.send_json({"error": "Not Found"}, 404); return
            self.send_json(payload); return
        solution_api = re.fullmatch(r"/api/books/([^/]+)/solution/(\d+)/", path)
        if solution_api and solution_api.group(1) in BOOK_META:
            if not self.authorized():
                self.send_json({"error": "Unauthorized"}, 401); return
            payload = book_solution_payload(solution_api.group(1), int(solution_api.group(2)),
                                            self.current_user() or "")
            if payload is None:
                self.send_json({"error": "Not Found"}, 404); return
            self.send_json(payload); return
        # 静态分发只有两条出口：首页，和 static/ 下的白名单后缀。
        # 改动前这里是 `ROOT / decoded_path`，只要文件在 ROOT 底下就发 ——
        # `ROOT in file.parents` 防的是「逃出 ROOT」，防不住「ROOT 里的东西不该全公开」。
        # 实测 GET /data/course.db 能下到整个 SQLite 库（口令哈希 + 全部提交），
        # GET /data/.admin_password 走的是同一条路径。.gitignore 挡的是 git，不是 HTTP。
        if path in ("/", ""):
            file = ROOT / "index.html"
            if file.is_file():
                # 走 send_html 而不是 send_static：页面里的 `__THEME_HEAD__` 要在这里
                # 被换掉。首页原来是这条路上唯一一个当静态文件发的 HTML，
                # 于是占位符原样印在了页面上（`test_every_page_gets_the_theme_boot_injected`
                # 第一次跑就抓住了这个）。
                self.send_html(file.read_text(encoding="utf-8")); return
        if decoded_path.startswith("/static/"):
            file = (STATIC_DIR / decoded_path[len("/static/"):]).resolve()
            # resolve() 之后再判包含，符号链接就指不出 static/ 了
            if STATIC_DIR in file.parents and file.is_file() and file.suffix in STATIC_TYPES:
                self.send_static(file, STATIC_TYPES[file.suffix]); return
        # Keep the real OpenJudge URL space usable locally: problem, login,
        # statistics, search, and contest pages are fetched through this host.
        try:
            upstream = urllib.request.Request("http://cs101.openjudge.cn" + self.path, headers={"User-Agent": "CS101 local mirror"})
            # 只带 User-Agent：本地会话 cookie 绝不能转发给上游（红线 5）。
            status = 200
            try:
                with urllib.request.urlopen(upstream, timeout=15) as response:
                    body = response.read()
                    content_type = response.headers.get("Content-Type", "text/html; charset=UTF-8")
            except urllib.error.HTTPError as upstream_error:
                # 改动前这里不分状态一律写死 200。但要说清楚：**光改这里并不能让
                # 状态码变得可信** —— 实测上游 cs101.openjudge.cn 对不存在的路径
                # 自己就返回 200（软 404），所以打错的 URL 依然是 200 + 上游页面。
                # 这里只保证「上游真的报错时不再被我们粉饰成 200」。
                # 也因此，T-010 的静态白名单测试必须断言响应内容而不是状态码 ——
                # 那不是我们的实现问题，是上游行为决定的，改不掉。
                status = upstream_error.code
                body = upstream_error.read()
                content_type = upstream_error.headers.get("Content-Type", "text/html; charset=UTF-8")
            if "text/html" in content_type:
                text = body.decode("utf-8", errors="replace")
                text = text.replace("http://cs101.openjudge.cn", "")
                text = text.replace("https://cs101.openjudge.cn", "")
                body = text.encode("utf-8")
            self.send_response(status)
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
            # 未登录端点，没有用户名可依据，只能按来源地址计数。
            # ⚠️ 一个班常在同一出口 IP 后面，开学第一节课集中注册会撞上这个额度 ——
            # 所以默认给得宽，并且**管理页上可以直接调大或填 0 关掉**，不用重启。
            # 验证码挡得住脚本，挡不住慢速刷号；这条挡的是后者。
            retry_after = quota_retry_after("register", self.client_ip())
            if retry_after:
                self.send_json({"error": f"注册太频繁了，请 {retry_after} 秒后再试",
                                "retry_after": retry_after}, 429); return
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
                with connect_db() as db:
                    if db.execute("select 1 from users where lower(username) = lower(?) or lower(email) = ?", (username, email)).fetchone():
                        self.send_json({"error": "用户名或邮箱已存在"}, 409); return
                    db.execute("insert into users(username, password_hash, email, nickname, active, activation_token_hash, activation_expires) values (?, ?, ?, ?, 0, ?, ?)",
                               (username, password_hash(password), email, username,
                                reset_token_hash(activation_token), int(time.time()) + 86400))
            except sqlite3.IntegrityError:
                self.send_json({"error": "用户名或邮箱已存在"}, 409); return
            base = public_base_url()
            activation_link = f"{base}/auth/activate/?token={activation_token}"
            sent = send_account_email(email, "激活你的 CS101 账号", f"请在 24 小时内点击以下链接激活账号：\n{activation_link}\n")
            if sent:
                self.send_json({"ok": True}); return
            # 没发出去时，改动前会把激活链接直接回给调用者。它拿不到别人**既有**的账号
            # （邮箱已注册会 409），但确实放开了一件本来做不到的事：
            # 拿别人的邮箱注册、**无需进对方信箱**就能激活，把这个地址占掉。
            # 邮件正常时占位需要对方信箱里的链接，这条兜底把那道门去掉了。
            # 与重置链接同样处理：要显式开开关才给，否则只写日志。
            if os.environ.get(ACCOUNT_LINKS_ENV) == "1":
                self.send_json({"ok": True, "activation_link": activation_link}); return
            print(f"[activate] {email} -> {activation_link}", flush=True)
            self.send_json({"ok": True}); return
        if path == "/api/user/login":
            username, password = str(data.get("username", "")).strip(), str(data.get("password", ""))
            if login_locked(username):
                self.send_json({"error": "尝试次数过多，请 15 分钟后再试"}, 429); return
            accepted = (same_username(username, ADMIN_USER)
                        and bool(ADMIN_PASSWORD)
                        and hmac.compare_digest(password, ADMIN_PASSWORD))
            session_user = ADMIN_USER if accepted else None
            if not accepted:
                with connect_db() as db:
                    row = db.execute("select username, password_hash, active from users where lower(username) = lower(?)", (username,)).fetchone()
                    accepted = row is not None and valid_password(row[1], password)
                    if accepted:
                        session_user = row[0]
                        active = row[2]
                        if not active:
                            self.send_json({"error": "账号尚未激活，请先点击邮箱中的激活链接"}, 403); return
                        # 老格式（全库共用一个盐）在这里顺手升级，不必打扰用户
                        if needs_rehash(row[1]):
                            db.execute("update users set password_hash = ? where username = ?",
                                       (password_hash(password), row[0]))
            if not accepted:
                note_login_failure(username)
                self.send_json({"error": "用户名或密码不正确"}, 401); return
            LOGIN_FAILURES.pop(str(username).casefold(), None)
            token = start_session(session_user)
            self.send_response(200); self.send_header("Set-Cookie", self.session_cookie(token)); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
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
            with connect_db() as db:
                row = db.execute("select password_hash from users where username = ?", (username,)).fetchone()
                if not row or not valid_password(row[0], current):
                    self.send_json({"error": "当前密码不正确"}, 400); return
                db.execute("update users set password_hash = ? where username = ?", (password_hash(new_password), username))
            current_token = cookies.SimpleCookie(self.headers.get("Cookie", "")).get("session")
            revoke_sessions(username, keep=current_token.value if current_token else None)
            self.send_json({"ok": True}); return
        if path == "/api/profile":
            username = self.current_user()
            if username is None:
                self.send_json({"error": "Unauthorized"}, 401); return
            nickname = str(data.get("nickname", "")).strip()
            if not nickname or len(nickname) > 32 or not nickname.isprintable():
                self.send_json({"error": "昵称需为 1-32 个可见字符"}, 400); return
            with connect_db() as db:
                # 昵称不能是**别人的**用户名。排名页显示的是昵称、链接才是用户名，
                # 不拦这一条，任何人都能把自己在排行榜上显示成别的同学（或管理员）——
                # 一个课程排行榜上的冒名，学生看不出来，看出来了也说不清。
                # 只拦「别人的」：自己的用户名当然可以，那本来就是默认值。
                taken = db.execute(
                    "select 1 from users where lower(username) = lower(?) and lower(username) != lower(?)",
                    (nickname, username)).fetchone()
                if taken or (same_username(nickname, ADMIN_USER)
                             and not same_username(username, ADMIN_USER)):
                    self.send_json({"error": "这个昵称与其他账号的用户名相同，换一个"}, 409); return
                updated = db.execute("update users set nickname = ? where username = ?",
                                     (nickname, username)).rowcount
                if not updated and same_username(username, ADMIN_USER):
                    db.execute("insert into settings(key, value) values (?, ?)"
                               " on conflict(key) do update set value = excluded.value",
                               ("profile_nickname:" + username.casefold(), nickname))
                    updated = 1
            if not updated:
                self.send_json({"error": "账号不存在"}, 404); return
            self.send_json({"ok": True, "nickname": nickname}); return
        if path == "/api/user/forgot":
            email = str(data.get("email", "")).strip().lower()
            # 限频必须在查库**之前**，而且按「请求里写的邮箱」计数，不管它存不存在。
            # 否则只有真实邮箱才会被限住，429 本身就成了「这个邮箱注册过」的信号 ——
            # 那正是下面这个 generic 响应要藏起来的东西。
            retry_after = (quota_retry_after("forgot", "mail:" + email)
                           or quota_retry_after("forgot", "ip:" + self.client_ip()))
            if retry_after:
                self.send_json({"error": f"请求太频繁了，请 {retry_after} 秒后再试",
                                "retry_after": retry_after}, 429); return
            generic = {"ok": True}
            with connect_db() as db:
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
            # 没配邮件服务时，改动前会把重置链接直接回给调用者。那条路径是给本机开发用的，
            # 但它对匿名请求也生效 —— 只要知道某人的邮箱就能拿到他的重置链接，
            # 等于**任意账号接管**。而它是「悄悄降级」触发的：SMTP 没配、变量名打错、
            # 新克隆缺 data/.smtp.env，都会掉进来，没有任何告警。
            # 现在要显式开开关才给（CS101_SHOW_ACCOUNT_LINKS=1），否则只写日志，
            # 对外仍返回与「邮箱不存在」完全一致的响应。
            if os.environ.get(ACCOUNT_LINKS_ENV) == "1":
                self.send_json({"ok": True, "reset_link": link}); return
            print(f"[reset] {email} -> {link}", flush=True)
            self.send_json(generic); return
        if path == "/api/user/reset":
            token = str(data.get("token", ""))
            password, confirmation = str(data.get("password", "")), str(data.get("confirm_password", ""))
            if len(password) < 8:
                self.send_json({"error": "密码至少需要 8 位"}, 400); return
            if password != confirmation:
                self.send_json({"error": "两次输入的密码不一致"}, 400); return
            with connect_db() as db:
                row = db.execute("select username from users where reset_token_hash = ? and reset_expires > ?",
                                 (reset_token_hash(token), int(time.time()))).fetchone()
                if not row:
                    self.send_json({"error": "重置链接无效或已过期"}, 400); return
                db.execute("update users set password_hash = ?, reset_token_hash = null, reset_expires = null where username = ?",
                           (password_hash(password), row[0]))
            revoke_sessions(row[0])
            self.send_json({"ok": True}); return
        if path == "/api/login":
            if same_username(data.get("username", ""), ADMIN_USER) and data.get("password") == ADMIN_PASSWORD:
                token = start_session(ADMIN_USER)
                self.send_response(200); self.send_header("Set-Cookie", self.session_cookie(token))
                self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
            self.send_json({"error": "账号或口令不正确"}, 401); return
        if path == "/api/auth/login/":
            if same_username(data.get("email", ""), ADMIN_USER) and data.get("password") == ADMIN_PASSWORD:
                token = start_session(ADMIN_USER)
                self.send_response(200)
                self.send_header("Set-Cookie", self.session_cookie(token))
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers(); self.wfile.write(b'{"ok":true}'); return
            self.send_json({"error": "账号或口令不正确"}, 401); return
        if path == "/api/logout":
            jar = cookies.SimpleCookie(self.headers.get("Cookie", "")); token = jar.get("session")
            if token: drop_session(token.value)
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
            if "quotas" in data:
                quotas = {}
                for bucket in QUOTA_DEFAULTS:
                    entry = (data["quotas"] or {}).get(bucket)
                    if not isinstance(entry, dict):
                        continue
                    try:
                        limit, window = int(entry.get("limit")), int(entry.get("window"))
                    except (TypeError, ValueError):
                        self.send_json({"error": f"{bucket} 的额度必须是整数"}, 400); return
                    if limit < 0 or limit > QUOTA_LIMIT_CAP:
                        self.send_json({"error": f"{bucket} 的次数需在 0..{QUOTA_LIMIT_CAP}（0 表示不限）"}, 400); return
                    if not QUOTA_WINDOW_RANGE[0] <= window <= QUOTA_WINDOW_RANGE[1]:
                        self.send_json({"error": f"{bucket} 的窗口需在 {QUOTA_WINDOW_RANGE[0]}..{QUOTA_WINDOW_RANGE[1]} 秒"}, 400); return
                    quotas[bucket] = {"limit": limit, "window": window}
                set_setting(QUOTAS_KEY, json.dumps(quotas, ensure_ascii=False))
            self.send_json({REVEAL_KEY: reveal_enabled(), "books": reveal_books(),
                            "windows": reveal_windows(), "active_window": active_window(),
                            "quotas": quota_config(), "quota_defaults": QUOTA_DEFAULTS}); return
        if path in {"/api/run", "/api/run/"} and self.authorized():
            # 「运行样例」：和提交走同一套沙箱，但不写 submissions 表、不计入统计。
            book, problem = data.get("book", ""), data.get("problem", "")
            # 配额放在题号校验之前：超额的请求不该再去解析 4.1MB 的 catalog。
            retry_after = quota_retry_after("run", self.current_user() or ADMIN_USER)
            if retry_after:
                self.send_json({"status": "Rate Limited", "retry_after": retry_after,
                                "message": f"运行样例太频繁了，请 {retry_after} 秒后再试。"}, 429); return
            if not problem_exists(book, problem):
                self.send_json({"status": "Problem Not Found", "message": "本地题库中没有这道题。"}, 404); return
            with judging_slot(self.current_user() or ADMIN_USER) as got_slot:
                if not got_slot:
                    self.send_json({"status": "Busy",
                                    "message": "判题队列忙，稍后再试（或你上一次判题还没结束）。"}, 429); return
                self.send_json(run_sample(book, problem, data.get("language", "python"),
                                          data.get("source", ""), data.get("stdin", "")))
            return
        if path in {"/api/submit", "/api/submit/"} and self.authorized():
            book, problem = data.get("book", ""), data.get("problem", "")
            language = data.get("language", "python")
            retry_after = quota_retry_after("submit", self.current_user() or ADMIN_USER)
            if retry_after:
                self.send_json({"status": "Rate Limited", "retry_after": retry_after,
                                "message": f"提交太频繁了，请 {retry_after} 秒后再试。"}, 429); return
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
                with connect_db() as db:
                    db.execute("insert into submissions(user, problem, result, book, language, detail, source) values (?, ?, ?, ?, ?, ?, ?)",
                               (self.current_user() or ADMIN_USER, problem, result["status"], book, language, detail,
                                submitted_source))
                self.send_json(result); return
        self.send_json({"error": "Unauthorized"}, 401)

class Server(ThreadingHTTPServer):
    """把监听队列从默认的 5 调大。

    `socketserver` 默认 `request_queue_size = 5`：**同时**到达的连接超过 5 个，
    多余的会被内核直接 RST，客户端看到的是 Connection reset by peer ——
    对学生来说就是「点了提交没反应」，而且服务端日志里连一条记录都没有，
    因为那些连接根本没被 accept。

    实测（32 核，独立实例，每人一份正确解）：
        并发 30  → 全部 Accepted
        并发 60  → 8/60  连接重置
        并发 100 → 31/100 连接重置
    一个班同时交，三分之一的人交不上去。判题本身没问题，是排队的门太窄。

    SOMAXCONN 是内核允许的上限（本机 4096）；取它和 512 的较小值，
    足够吸收一个班的瞬时并发，又不至于让积压无限长。
    """
    request_queue_size = min(512, socket.SOMAXCONN)


if __name__ == "__main__":
    init_db()
    host, port = os.environ.get("CS101_HOST", "0.0.0.0"), int(os.environ.get("CS101_PORT", "8000"))
    print(f"CS101 portal running at http://{host}:{port}")
    Server((host, port), Handler).serve_forever()
