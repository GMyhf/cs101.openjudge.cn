import http.client
import json
import os
import re
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "static"

# 认证提交这条链路要真的走进判题器，所以题号必须选数据已入库的（`*_made/`）；
# `data/openjudge/tests/**` 下抓取的数据不入库，用它会让新克隆的仓库跑不通。
SUBMIT_BOOK = "pctbook"
SUBMIT_PROBLEM = "E03406"


def request(port, method, path, body=None, cookie=None):
    # 8 秒对判题类请求太紧：一次提交要真的跑完全部测试点，编译型语言还要先编译，
    # 而闸门是全量跑（`full_sweep` 之后机器正忙）。2026-07-28 就这么假红过一次。
    # 服务端启动等待早已因同样的原因从 8 秒放宽到 30 秒，这里一直没跟上。
    # **一个偶尔发红的闸门，正是让真红被忽略的机制** —— 宁可等久一点。
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
    headers = {"Content-Type": "application/json"}
    if cookie:
        headers["Cookie"] = cookie
    payload = json.dumps(body).encode() if body is not None else None
    connection.request(method, path, payload, headers)
    response = connection.getresponse()
    raw = response.read()
    response_headers = dict(response.getheaders())
    connection.close()
    return response.status, response_headers, raw


class ServerApiTests(unittest.TestCase):
    def registration_payload(self, username, password):
        _, _, page = request(self.port, "GET", "/register/")
        html = page.decode("utf-8")
        token = re.search(r'name="captcha_token" value="([^"]+)"', html).group(1)
        left, right = map(int, re.search(r'class="captcha-question">(\d+) \+ (\d+)', html).groups())
        return {"email": username + "@example.com", "username": username,
                "password": password, "confirm_password": password,
                "captcha_token": token, "captcha_answer": str(left + right)}

    def register_and_login(self, username, password):
        status, _, body = request(self.port, "POST", "/api/user/register",
                                  self.registration_payload(username, password))
        self.assertEqual(status, 200)
        result = json.loads(body)
        if "activation_link" in result:
            query = result["activation_link"].split("?", 1)[1]
            status, _, _ = request(self.port, "GET", "/auth/activate/?" + query)
            self.assertEqual(status, 200)
        status, headers, _ = request(self.port, "POST", "/api/user/login",
                                     {"username": username, "password": password})
        self.assertEqual(status, 200)
        return headers["Set-Cookie"].split(";", 1)[0]

    @classmethod
    def setUpClass(cls):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            cls.port = sock.getsockname()[1]
        cls.db_file = tempfile.NamedTemporaryFile(prefix="cs101-t001-", suffix=".db", delete=False)
        cls.db_file.close()
        cls.addClassCleanup(os.unlink, cls.db_file.name)
        environment = os.environ.copy()
        environment.update({
            "CS101_HOST": "127.0.0.1",
            "CS101_PORT": str(cls.port),
            "CS101_DB": cls.db_file.name,
            "CS101_ADMIN_PASSWORD": "T001-admin-only",
        })
        for key in ("CS101_SMTP_HOST", "CS101_SMTP_PORT", "CS101_SMTP_USER",
                    "CS101_SMTP_PASSWORD", "CS101_SMTP_FROM", "CS101_PUBLIC_URL"):
            environment.pop(key, None)
        environment["CS101_PUBLIC_URL"] = "http://10.129.81.235:8000"
        environment["CS101_LOAD_DOTENV"] = "0"
        cls.process = subprocess.Popen(
            [sys.executable, "server.py"], cwd=ROOT, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        # 先登记清理再等待：即使服务端起不来、setUpClass 抛异常，
        # addClassCleanup 也会跑，不会漏下孤儿进程和临时库文件。
        cls.addClassCleanup(cls._stop_server)
        # 8 秒在单跑这个文件时够用，但闸门是 `unittest discover` 全量跑（64 项），
        # 机器有负载时服务端启动会慢过去 —— 2026-07-27 就这么假红过一次。
        # **一个偶尔发红的闸门，正是让真红被忽略的机制**：swiftc 那次红了四个提交
        # 没人管，靠的就是「反正它有时会抽风」这种心理。宁可等久一点。
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                status, _, _ = request(cls.port, "GET", "/api/me")
                if status == 200:
                    cls._unthrottle_registration()
                    return
            except (ConnectionRefusedError, OSError):
                time.sleep(0.05)
        cls._stop_server()
        raise RuntimeError("server did not start: " + (cls.process.stderr.read() or "<no stderr>"))

    @classmethod
    def _unthrottle_registration(cls):
        """整个套件都从 127.0.0.1 注册，会撞上注册限频（默认按来源地址计数）。

        所以这里显式把它关掉，让套件不依赖默认额度是多少；
        专门测限频的那条用例自己再把额度调回小值。
        """
        status, headers, _ = request(cls.port, "POST", "/api/login",
                                     {"username": "GMyhf", "password": "T001-admin-only"})
        if status != 200:
            return
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        request(cls.port, "POST", "/api/settings",
                {"quotas": {"register": {"limit": 0, "window": 600}}}, cookie=cookie)

    @classmethod
    def _stop_server(cls):
        if cls.process.poll() is None:
            cls.process.terminate()
            try:
                cls.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                cls.process.kill()
                cls.process.wait()

    def test_submit_requires_authentication(self):
        status, _, body = request(self.port, "POST", "/api/submit", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python", "source": "print(1)",
        })
        self.assertEqual(status, 401)
        self.assertIn(b"Unauthorized", body)

    def test_activation_link_uses_configured_public_url(self):
        result = self.registration_payload("LanLinkUser", "T001-password")
        status, _, body = request(self.port, "POST", "/api/user/register", result)
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertTrue(payload["activation_link"].startswith("http://10.129.81.235:8000/auth/activate/"))

    def test_home_navigation_has_submission_user_link_and_account_menu(self):
        status, _, body = request(self.port, "GET", "/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        # 2026-07-26：导航重构后容器 id 是 account-control（原 user-menu），
        # 登录后 #account 的 href 由前端脚本改成 /history/?mine=1。断言跟着改成
        # **功能仍在**的证据，而不是旧的 DOM 名字。
        self.assertIn('id="account-control"', text)
        self.assertIn('id="account"', text)
        self.assertIn('href="/account/">账户设置</a>', text)
        self.assertIn('id="logout"', text)

    def test_register_login_session_and_authenticated_submit(self):
        username = "t001_user"
        cookie = self.register_and_login(username, "T001-password")

        status, _, body = request(self.port, "GET", "/api/me", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"authenticated": True, "user": username})

        status, _, _ = request(self.port, "POST", "/api/logout", cookie=cookie)
        self.assertEqual(status, 200)
        status, _, body = request(self.port, "GET", "/api/me", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["authenticated"], False)

        status, headers, _ = request(self.port, "POST", "/api/user/login", {
            "username": username.upper(), "password": "T001-password",
        })
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        status, _, body = request(self.port, "GET", "/api/me", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"authenticated": True, "user": username})
        duplicate = self.registration_payload("T001_USER", "T001-other-password")
        status, _, _ = request(self.port, "POST", "/api/user/register", duplicate)
        self.assertEqual(status, 409)
        status, _, body = request(self.port, "POST", "/api/submit", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print('wrong')",
        }, cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "Wrong Answer")

    def test_account_settings_changes_password(self):
        username = "t006_account"
        old_password = "T006-password"
        new_password = "T006-new-password"
        cookie = self.register_and_login(username, old_password)
        status, _, _ = request(self.port, "GET", "/account/", cookie=cookie)
        self.assertEqual(status, 200)
        status, _, _ = request(self.port, "POST", "/api/user/change-password", {
            "current_password": "wrong", "new_password": new_password,
            "confirm_password": new_password,
        }, cookie=cookie)
        self.assertEqual(status, 400)
        status, _, _ = request(self.port, "POST", "/api/user/change-password", {
            "current_password": old_password, "new_password": new_password,
            "confirm_password": new_password,
        }, cookie=cookie)
        self.assertEqual(status, 200)
        status, headers, _ = request(self.port, "POST", "/api/user/login", {
            "username": username, "password": new_password,
        })
        self.assertEqual(status, 200)

    def test_problem_catalog_page_is_served(self):
        status, _, body = request(self.port, "GET", "/problems/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn("题库目录", text)
        self.assertIn("/api/catalog", text)          # 目录页的数据来源

    def test_catalog_exposes_display_book_names(self):
        status, _, body = request(self.port, "GET", "/api/catalog")
        self.assertEqual(status, 200)
        meta = json.loads(body)["book_meta"]
        self.assertEqual(meta["practice"]["name"], "题库（包括计概、数算题目）")
        self.assertEqual(meta["practice"]["count"], 985)
        self.assertEqual(meta["pctbook"]["name"], "计算思维算法实践")

    def test_catalog_summary_is_small_and_contains_judgeable_titles(self):
        status, headers, body = request(self.port, "GET", "/api/catalog?summary=1")
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertGreater(payload["tested_count"], 0)
        self.assertTrue(payload["problems"])
        self.assertTrue(all(item["test_count"] >= 5 for item in payload["problems"]))
        self.assertTrue(any(item["title"] for item in payload["problems"]))
        self.assertLess(int(headers["Content-Length"]), 500_000)

    def test_submit_page_renders_without_placeholders(self):
        status, _, body = request(self.port, "GET", f"/{SUBMIT_BOOK}/{SUBMIT_PROBLEM}/submit/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn(SUBMIT_PROBLEM, text)
        self.assertIn("我的提交记录", text)
        # T-010 起编辑器不再定高：整页 100dvh 不滚动，编辑器随视口伸缩，
        # 滚动只发生在 .pane-body 内。原来这里断言的是 `height:520px`——
        # 那正是本次要去掉的东西，所以断言跟着设计意图一起改。
        self.assertIn("100dvh", text)
        self.assertIn("pane-editor", text)
        self.assertNotIn("height:520px", text)
        self.assertIn("查看代码", text)
        self.assertIn("G++(", text)
        self.assertIn("Python3(", text)
        self.assertIn("PyPy3(", text)
        self.assertIn("查看判题详情", text)

        self.assertIn('value="csharp">C# (.NET SDK 10)', text)
        self.assertIn('value="fsharp">F# (.NET SDK 10)', text)
        self.assertIn('value="vbnet">VB.NET (.NET SDK 10)', text)
        self.assertIn('value="swift">Swift(', text)
        self.assertIn('value="objc">Objective-C(', text)
        self.assertIn("workspace-layout", text)
        self.assertNotIn("Python ×10", text)
        for placeholder in ("__BOOK__", "__PROBLEM__"):
            self.assertNotIn(placeholder, text)      # 模板占位符必须已被替换

    def test_help_page_exposes_runtime_rules(self):
        status, _, body = request(self.port, "GET", "/help/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn("Python ×10", text)
        self.assertIn("C#/F#/VB.NET 内存 ×2", text)

    def test_history_page_exposes_error_details(self):
        status, _, body = request(self.port, "GET", "/history/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn("查看判题详情", text)
        self.assertIn("result-message", text)

    def test_submissions_require_authentication(self):
        status, _, body = request(self.port, "GET", "/api/submissions")
        self.assertEqual(status, 401)
        self.assertIn(b"Unauthorized", body)

    def test_submission_history_records_book_language_and_detail(self):
        """历史记录要能回答「错在哪组数据」——只存 status 是答不了的。"""
        username = "t006_history"
        cookie = self.register_and_login(username, "T006-password")
        status, _, body = request(self.port, "POST", "/api/submit", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print('wrong')",
        }, cookie=cookie)
        self.assertEqual(status, 200)
        verdict = json.loads(body)

        status, _, body = request(self.port, "GET", "/api/submissions", cookie=cookie)
        self.assertEqual(status, 200)
        entries = json.loads(body)["submissions"]
        self.assertTrue(entries)
        latest = entries[0]
        self.assertEqual(latest["user"], username)
        self.assertEqual(latest["problem"], SUBMIT_PROBLEM)
        self.assertEqual(latest["result"], "Wrong Answer")
        self.assertEqual(latest["book"], SUBMIT_BOOK)
        self.assertEqual(latest["language"], "python")
        self.assertEqual(latest["detail"]["case"], verdict["case"])
        self.assertEqual(latest["source"], "print('wrong')")
        self.assertTrue(latest["detail"]["expected_output"]["text"])
        self.assertGreaterEqual(latest["detail"]["time_ms"], 0)
        self.assertGreater(latest["detail"]["memory_kb"], 0)
        self.assertEqual(latest["detail"]["source_bytes"], len("print('wrong')".encode()))
        # 不能把版本号写死：这台机器是 3.12、别的机器可能是 3.9，
        # 写死就等于让闸门依赖运行环境（T-001 立的「闸门必须在全新克隆上成立」）。
        # 断言改成「形状对且与运行时一致」。
        from judge import language_version
        self.assertEqual(latest["detail"]["language_version"], language_version("python"))
        self.assertRegex(latest["detail"]["language_version"], r"^Python3\(\d+\.\d+\)$")
        other_entries = [entry for entry in entries if entry["user"] != username]
        if other_entries:
            self.assertTrue(all(entry["source"] == "" and entry["detail"] == {} for entry in other_entries))
        admin = self._admin_cookie()
        status, _, body = request(self.port, "GET", "/api/submissions", cookie=admin)
        self.assertEqual(status, 200)
        admin_latest = json.loads(body)["submissions"][0]
        self.assertEqual(admin_latest["user"], username)
        self.assertEqual(admin_latest["source"], "print('wrong')")

    def test_stats_are_all_computed_from_data(self):
        """站点统计里不能有写死的数。

        `/api/stats` 原来返回 `"accepted": 1284, "streak": 12` —— 两个凭空编的数字。
        当时没有页面调用它，所以没人看见；但假数字不会因为暂时没人看就变得无害，
        接上去的那天它就在对学生撒谎。`streak` 已删（没有任何数据能算出它）。
        """
        _, _, body = request(self.port, "GET", "/api/stats")
        stats = json.loads(body)
        self.assertNotIn("streak", stats)
        for key in ("submissions", "accepted", "solved_problems", "users", "online"):
            self.assertIn(key, stats)
            self.assertIsInstance(stats[key], int)

        # 提交一发错的，通过数不该动、提交数该 +1 —— 这两个数必须真的跟着数据走。
        cookie = self.register_and_login("t010_stats_user", "T010-password")
        before = json.loads(request(self.port, "GET", "/api/stats")[2])
        request(self.port, "POST", "/api/submit",
                {"book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM,
                 "language": "python", "source": "print('wrong')"}, cookie=cookie)
        after = json.loads(request(self.port, "GET", "/api/stats")[2])
        self.assertEqual(after["submissions"], before["submissions"] + 1)

        # 和库里的真实计数交叉核对。只断言「提交错解后通过数不变」是不够的 ——
        # 写死成 1284 时它也不变（我第一版就漏在这儿，变异自检才发现）。
        with sqlite3.connect(self.db_file.name) as db:
            real_submissions = db.execute("select count(*) from submissions").fetchone()[0]
            real_accepted = db.execute(
                "select count(*) from submissions where result = 'Accepted'").fetchone()[0]
            real_users = db.execute("select count(*) from users").fetchone()[0]
        self.assertEqual(after["submissions"], real_submissions)
        self.assertEqual(after["accepted"], real_accepted)
        self.assertEqual(after["users"], real_users)

    def test_online_count_follows_activity_not_login_history(self):
        """在线人数要有时效，且按人去重。

        会话表只在登出时才缩小，拿它的大小当在线数，会把「三天前登录过、浏览器一直
        没关」也算进去 —— 那不是在线，是从没登出。
        """
        import server
        cookie = self.register_and_login("t010_online_a", "T010-password")
        request(self.port, "GET", "/api/me", cookie=cookie)
        self.assertGreaterEqual(json.loads(request(self.port, "GET", "/api/stats")[2])["online"], 1)

        # 同一个人再开一个会话，人数不该翻倍
        first = json.loads(request(self.port, "GET", "/api/stats")[2])["online"]
        again = self.register_and_login("t010_online_a2", "T010-password")
        request(self.port, "GET", "/api/me", cookie=again)
        self.assertEqual(json.loads(request(self.port, "GET", "/api/stats")[2])["online"], first + 1)

    def test_online_count_expires_and_dedupes(self):
        """时间窗与去重逻辑直接对函数验。

        **不能借 HTTP 那条路验这个**：服务端跑在子进程里，测试进程里的
        `server.SESSION_SEEN` 始终是空的，`online_users()` 不管怎样都返回 0 ——
        那是个恒真断言。（我第一版就是这么写的。）
        """
        import server
        saved = (dict(server.SESSION_SEEN), set(server.TOKENS), dict(server.SESSION_USERS))
        try:
            server.SESSION_SEEN.clear(); server.TOKENS.clear(); server.SESSION_USERS.clear()
            now = 1_000_000.0
            for token, user in (("t1", "amy"), ("t2", "amy"), ("t3", "bob")):
                server.TOKENS.add(token); server.SESSION_USERS[token] = user
                server.SESSION_SEEN[token] = now
            # 三个会话、两个人 -> 2
            self.assertEqual(server.online_users(now), 2)
            # bob 的打点拨到窗外 -> 只剩 amy
            server.SESSION_SEEN["t3"] = now - server.ONLINE_WINDOW_SECONDS - 1
            self.assertEqual(server.online_users(now), 1)
            # 已登出的会话（不在 TOKENS 里）即使打点很新也不算
            server.SESSION_SEEN["t1"] = now; server.SESSION_SEEN["t2"] = now
            server.TOKENS.discard("t1"); server.TOKENS.discard("t2")
            self.assertEqual(server.online_users(now), 0)
            # 过期的打点要被清掉，字典不能无限长
            self.assertEqual(server.SESSION_SEEN, {})
        finally:
            server.SESSION_SEEN.clear(); server.SESSION_SEEN.update(saved[0])
            server.TOKENS.clear(); server.TOKENS.update(saved[1])
            server.SESSION_USERS.clear(); server.SESSION_USERS.update(saved[2])

    def _admin_cookie(self):
        status, headers, _ = request(self.port, "POST", "/api/login", {
            "username": "GMyhf", "password": "T001-admin-only",
        })
        self.assertEqual(status, 200)
        return headers["Set-Cookie"].split(";", 1)[0]

    def _set_reveal(self, cookie, enabled):
        status, _, body = request(self.port, "POST", "/api/settings",
                                  {"reveal_failing_input": enabled}, cookie=cookie)
        self.assertEqual(status, 200)
        return json.loads(body)["reveal_failing_input"]

    def test_reveal_switch_defaults_to_on(self):
        """全局默认是**开**（人拍板 2026-07-27）——但考试时段必须仍然一票否决。

        必须在**没有任何设置记录**的全新库上验，否则测的是上一个用例写进去的值：
        本类的用例按字母序执行，`test_failing_input_...` 排在前面并会把开关显式写成 off；
        若在共享库上读 `/api/settings`，读到的是那行记录，默认值这条分支根本走不到。

        两条一起断言才有意义：只钉「默认开」，等于把「考试时段一票否决」这条防线让出去；
        只钉「考试时段关」，又管不住默认值被人悄悄改回 off。
        """
        import server
        from datetime import datetime, timedelta
        with tempfile.TemporaryDirectory() as folder:
            fresh = Path(folder) / "fresh.db"
            saved = server.DB
            server.DB = fresh
            try:
                server.init_db()
                with sqlite3.connect(fresh) as db:
                    self.assertEqual(db.execute("select count(*) from settings").fetchone()[0], 0)
                self.assertIs(server.reveal_enabled(), True)
                self.assertIs(server.reveal_effective(SUBMIT_BOOK), True)

                # 考试时段内：无论全局默认是什么，都必须关。
                now = datetime.now()
                window = {"start": (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"),
                          "end": (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"),
                          "note": "单元测试用"}
                server.set_setting(server.WINDOWS_KEY, json.dumps([window]))
                self.assertIsNotNone(server.active_window())
                self.assertIs(server.reveal_effective(SUBMIT_BOOK), False)
            finally:
                server.DB = saved

    def test_reveal_switch_rejects_non_admin(self):
        username = "t006_switch_student"
        cookie = self.register_and_login(username, "T006-password")
        _, _, before = request(self.port, "GET", "/api/settings")
        was = json.loads(before)["reveal_failing_input"]
        status, _, _ = request(self.port, "POST", "/api/settings",
                               {"reveal_failing_input": not was}, cookie=cookie)
        self.assertEqual(status, 403)
        _, _, after = request(self.port, "GET", "/api/settings")
        # 断言的是「非管理员改不动」，不是某个具体值 —— 默认值一改，写死的值就成了假断言。
        self.assertIs(json.loads(after)["reveal_failing_input"], was)

    def test_failing_input_snippet_follows_the_switch(self):
        """开关关着时片段不能出现在接口返回里——是服务端不下发，不是前端隐藏。"""
        admin = self._admin_cookie()
        self.addCleanup(self._set_reveal, admin, False)
        username = "t006_switch_user"
        cookie = self.register_and_login(username, "T006-password")
        payload = {"book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM,
                   "language": "python", "source": "print('wrong')"}

        self._set_reveal(admin, False)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        verdict = json.loads(body)
        self.assertNotIn("failing_input", verdict)
        self.assertTrue(verdict["expected_output"]["text"])

        self.assertIs(self._set_reveal(admin, True), True)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        verdict = json.loads(body)
        snippet = verdict.get("failing_input")
        self.assertIsNotNone(snippet)
        self.assertTrue(snippet["text"])
        # 输入仍受泄题开关控制，期望 .out 用于解释错误结果。
        self.assertEqual(set(snippet), {"text", "truncated", "total_lines", "total_chars"})

        self._set_reveal(admin, False)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        self.assertNotIn("failing_input", json.loads(body))

    def test_book_override_accepts_on_off_strings(self):
        """管理页下拉框发的是 "on"/"off" 字符串。

        `"off"` 是非空字符串，按真值判会被存成 `"on"`——即「选关变成开」，
        而且这条路径只有走 HTTP 才会经过（直接 `set_setting` 写的是已归一化的值）。
        """
        admin = self._admin_cookie()
        self.addCleanup(request, self.port, "POST", "/api/settings", {"books": {}}, admin)
        status, _, body = request(self.port, "POST", "/api/settings",
                                  {"books": {SUBMIT_BOOK: "off"}}, cookie=admin)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["books"].get(SUBMIT_BOOK), "off")

        status, _, body = request(self.port, "POST", "/api/settings",
                                  {"books": {SUBMIT_BOOK: "on"}}, cookie=admin)
        self.assertEqual(json.loads(body)["books"].get(SUBMIT_BOOK), "on")

        # 空值表示「跟随全局」，不该留在覆盖表里
        status, _, body = request(self.port, "POST", "/api/settings",
                                  {"books": {SUBMIT_BOOK: ""}}, cookie=admin)
        self.assertNotIn(SUBMIT_BOOK, json.loads(body)["books"])

    def test_reveal_policy_layers(self):
        """考试时段一票否决 → 题库覆盖 → 全局默认；坏时段必须 fail closed。"""
        import server
        from datetime import datetime
        with tempfile.TemporaryDirectory() as folder:
            saved, server.DB = server.DB, Path(folder) / "policy.db"
            try:
                server.init_db()
                now = datetime(2026, 7, 26, 10, 0)
                # 这条验的是**层次**，所以两个方向的全局默认都要走一遍；
                # 只验一个方向的话，默认值一改这条就会跟着倒（2026-07-27 改成 on 时就是这样）。
                server.set_setting(server.REVEAL_KEY, "off")
                self.assertFalse(server.reveal_effective("practice", now))

                server.set_setting(server.REVEAL_KEY, "on")
                self.assertTrue(server.reveal_effective("practice", now))

                server.set_setting(server.BOOKS_KEY, json.dumps({"practice": "off"}))
                self.assertFalse(server.reveal_effective("practice", now))     # 题库覆盖全局
                self.assertTrue(server.reveal_effective("dsapre", now))        # 未覆盖的跟随全局

                server.set_setting(server.WINDOWS_KEY, json.dumps(
                    [{"start": "2026-07-26T09:00", "end": "2026-07-26T11:00", "note": "期末考"}]))
                self.assertFalse(server.reveal_effective("dsapre", now))       # 时段内一票否决
                self.assertTrue(server.reveal_effective("dsapre", datetime(2026, 7, 26, 12, 0)))

                # 坏配置宁可误关：若按「不命中」处理，一条手改坏的时段会静默失去考试保护
                server.set_setting(server.WINDOWS_KEY, json.dumps([{"start": "x", "end": "y"}]))
                self.assertFalse(server.reveal_effective("dsapre", now))
                self.assertTrue(server.active_window(now)["malformed"])
            finally:
                server.DB = saved

    @unittest.skipUnless(shutil.which("node"), "需要 node 才能真跑页面里的高亮代码")
    def test_submit_page_highlighter_runs(self):
        """在 node 里真跑一遍页面发出的高亮函数。

        光看 `--check` 语法是不够的：`SUBMIT_PAGE` 若不是 raw 字符串，
        JS 里的 `\\\\b` 会被 Python 吃成退格符，关键字正则**静默失效**——
        页面照样能加载、语法照样合法，只是高亮不对。只有真跑才看得出来。
        """
        import server
        page = server.SUBMIT_PAGE
        script = page[page.index("<script>") + 8: page.rindex("</script>")]
        core = script[script.index("const PY_KW"): script.index("function paintEditor")]
        harness = (
            'const esc = s => String(s).replace(/[&<>"]/g,'
            ' c => ({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;"}[c]));\n'
            + core + "\n"
            'const out = highlight("def f(): # c\\n  return \'a\' + 1", "python");\n'
            'const checks = ["t-kw", "t-com", "t-str", "t-num"].every(c => out.includes(\'class="\' + c + \'"\'));\n'
            'const boundary = !highlight("classic = 1", "python").includes(\'class="t-kw"\');\n'
            'const escaped = !highlight("x = \'<b>\'", "python").includes("<b>");\n'
            # 括号匹配必须跳过字符串/注释里的括号；自动缩进要沿用本行缩进并在 : / { 后加一级
            'const pair = JSON.stringify(bracketMatch("a[b(c)]", 1, "python")) === "[1,6]";\n'
            # 这个用例必须能区分守卫的有无：串里的 "(" 若不跳过，会跟后面真实的 ")" 错配成 [5,12]
            'const skip = bracketMatch(\'x = "(" + f()\', 5, "python") === null;\n'
            'const marks = (highlight("f(x)", "python", [1, 3]).match(/t-match/g) || []).length === 2;\n'
            'const ind = indentFor("    if x:", 9, "python") === "        "\n'
            '         && indentFor("  if (x) {", 10, "cpp") === "      ";\n'
            # 括号补全：行尾补全、右括号跳过、退格删空对、右侧是字母则不插手
            'const p1 = JSON.stringify(pairAction("f", 1, 1, "(")) === \'{"from":1,"to":1,"insert":"()","caret":2}\';\n'
            'const p2 = pairAction("f()", 2, 2, ")").caret === 3;\n'
            'const p3 = pairAction("f()", 2, 2, "Backspace").insert === "";\n'
            'const p4 = pairAction("foo", 1, 1, "(") === null;\n'
            'process.exit(checks && boundary && escaped && pair && skip && marks && ind'
            ' && p1 && p2 && p3 && p4 ? 0 : 1);\n')
        with tempfile.NamedTemporaryFile("w", suffix=".mjs", encoding="utf-8", delete=False) as handle:
            handle.write(harness)
            path = handle.name
        self.addCleanup(os.unlink, path)
        result = subprocess.run(["node", path], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0,
                         "高亮未按预期工作（关键字/注释/字符串/数字、词边界、HTML 转义）："
                         + (result.stderr or result.stdout)[:400])

    def test_submit_page_offers_pypy3(self):
        """判题器 2026-07-26 起支持 PyPy3（人拍板），提交页要给得出这个选项。

        2026-07-26 修：语言选项后来改成渲染时注入（模板里只剩 `__LANGUAGE_OPTIONS__`），
        原来断言模板字面量含 `value="pypy3"` 就永远失败了 —— 而功能其实一直好好的。
        断言改成**请求真实页面**，这样以后无论模板怎么改都盯得住同一件事。
        """
        status, _, body = request(self.port, "GET", "/practice/04103/submit/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn('value="pypy3"', text)
        self.assertIn('value="python"', text)
        self.assertNotIn("__LANGUAGE_OPTIONS__", text)      # 占位符必须被替换掉

    @unittest.skipUnless(shutil.which("node"), "需要 node 才能真跑页面里的编辑器代码")
    def test_editor_treats_pypy3_as_python(self):
        """PyPy3 是 Python 语法：高亮表和自动缩进都必须走 python 那套。

        这条防的是「加了下拉选项但编辑器不认」——`SPECS[lang]` 取不到就回退到 python，
        看着像是对的；真正会露馅的是 `indentFor`，它写的是 `lang === "python"`，
        漏掉 pypy3 就会按 C 系规则去看行尾的 `{`，冒号后不再缩进。
        """
        import server
        page = server.SUBMIT_PAGE
        script = page[page.index("<script>") + 8: page.rindex("</script>")]
        core = script[script.index("const PY_KW"): script.index("function paintEditor")]
        harness = (
            'const esc = s => String(s).replace(/[&<>"]/g,'
            ' c => ({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;"}[c]));\n'
            + core + "\n"
            # 高亮：pypy3 必须拿到 python 的规则表，而不是靠回退撞对
            'const specOK = SPECS.pypy3 === SPECS.python;\n'
            'const kw = highlight("def f(): pass", "pypy3").includes(\'class="t-kw"\');\n'
            # 缩进：冒号后要多缩一级；漏掉 pypy3 的话这里只会返回原缩进
            'const ind = indentFor("    if x:", 9, "pypy3") === "        ";\n'
            # 反面：C 系的花括号规则不该套到 pypy3 上
            'const notC = indentFor("  if (x) {", 10, "pypy3") === "  ";\n'
            'process.exit(specOK && kw && ind && notC ? 0 : 1);\n')
        with tempfile.NamedTemporaryFile("w", suffix=".mjs", encoding="utf-8", delete=False) as handle:
            handle.write(harness)
            path = handle.name
        self.addCleanup(os.unlink, path)
        result = subprocess.run(["node", path], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0,
                         "编辑器没把 pypy3 当成 Python 处理："
                         + (result.stderr or result.stdout)[:400])

    def test_history_page_and_limit(self):
        status, _, body = request(self.port, "GET", "/history/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn("提交记录", text)
        self.assertIn("/api/submissions", text)

        username = "t006_hist_page"
        cookie = self.register_and_login(username, "T006-password")
        for source in ("print(1)", "print(2)", "print(3)"):
            request(self.port, "POST", "/api/submit", {
                "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM,
                "language": "python", "source": source,
            }, cookie=cookie)

        def count(query):
            _, _, raw = request(self.port, "GET", "/api/submissions" + query, cookie=cookie)
            return len(json.loads(raw)["submissions"])

        total = count("")
        self.assertGreaterEqual(total, 3)
        mine_status, _, mine_raw = request(self.port, "GET", "/api/submissions?mine=1", cookie=cookie)
        self.assertEqual(mine_status, 200)
        mine_entries = json.loads(mine_raw)["submissions"]
        self.assertGreaterEqual(len(mine_entries), 3)
        self.assertTrue(all(entry["user"] == username for entry in mine_entries))
        self.assertEqual(count("?limit=2"), 2)
        self.assertEqual(count("?limit=abc"), total)      # 非法值回落默认，不是 500
        self.assertEqual(count("?limit=99999"), total)    # 夹到上界，不是拒绝

    def test_submit_page_embeds_sample_io(self):
        """样例由服务端解析后注入，前端不刮 DOM。"""
        status, _, body = request(self.port, "GET", f"/{SUBMIT_BOOK}/{SUBMIT_PROBLEM}/submit/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertNotIn("__SAMPLE_JSON__", text)
        payload = json.loads(re.search(r"const SAMPLES = (\{.*?\});", text).group(1))
        self.assertIn("input", payload)
        self.assertIn("output", payload)
        self.assertTrue(payload["output"].strip(), "样例输出不该是空的")
        self.assertNotIn("<pre>", payload["input"])     # 标签要剥干净

    def test_submit_page_splits_annotated_multi_samples(self):
        """T27237 这类题面：样例 1 的输入和输出一起塞在「样例输入」里，样例 2 整组在「样例输出」里。"""
        status, _, body = request(self.port, "GET", "/pctbook/T27237/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        payload = json.loads(re.search(r"const SAMPLES = (\{.*?\});", text).group(1))
        self.assertEqual(len(payload["cases"]), 2, payload)
        self.assertEqual(payload["cases"][0], {"input": "1 6\n0 0", "output": "5\nHHHOO"})
        self.assertEqual(payload["cases"][1], {"input": "2 4\n0 0", "output": "4\nHHOO"})
        self.assertEqual(payload["input"], "1 6\n0 0")      # 默认给第一组
        # 分隔行和 # 讲解都不该留在样例里
        self.assertNotIn("sample", payload["input"].lower())
        self.assertNotIn("#", payload["cases"][0]["output"])

    def test_static_sample_parser_handles_the_variants_found_in_the_library(self):
        """分隔行的写法在题库里散得很开，这些都是从 1849 个页面里实际扫出来的形状。"""
        import server

        def one(text):
            return server.parse_sample_sections(text)

        # 编号在关键词后 + 全角冒号
        self.assertEqual(one("Sample Input1：\n1\nSample Output1：\n2"),
                         [{"input": "1", "output": "2"}])
        # 编号在关键词前 + 无冒号
        self.assertEqual(one("Sample1 Input\n1\nSample1 Output\n2"),
                         [{"input": "1", "output": "2"}])
        # 上游把 Input 打成了 Iutput（routine__16530）
        self.assertEqual(one("Sample Iutput2:\n7\nSample Output2:\n8"),
                         [{"input": "7", "output": "8"}])
        # 罗马数字编号（practice__20163）
        self.assertEqual(one("Sample Input II:\na\nSample Output II:\nb"),
                         [{"input": "a", "output": "b"}])
        # 编号与关键词拆成两行（practice__20125）
        self.assertEqual(one("Sample1\ninput：\n2\noutput:\n101"),
                         [{"input": "2", "output": "101"}])
        # 输出段的 # 讲解要截断，且讲解常常续到不带 # 的下一行（pctbook__M16531）
        self.assertEqual(one("sample1 in:\n1\nsample1 out:\n6 0\n#讲解\n续行也是讲解"),
                         [{"input": "1", "output": "6 0"}])
        # 但输入段的 # 是真数据，不能动（practice__19949 的 ###John###）
        self.assertEqual(one("Sample1 Input:\n###John### .\nSample1 Output:\n2"),
                         [{"input": "###John### .", "output": "2"}])
        # 没有标记就交回空列表，由调用方回落到「输入 dd / 输出 dd」的老行为
        self.assertEqual(one("1 6\n0 0"), [])

    def test_sample_parser_can_be_asked_not_to_truncate(self):
        """守门检查要验的是「输出段首行会不会是 #」，必须看得到截断前的样子。

        截断会把这种输出削成空串。`tools/full_sweep.py` 的检查一旦拿截断后的结果去验，
        就永远看不见自己要防的那件事 —— 一个永远不会红的检查，等于没有检查。
        """
        import server
        grid = "sample1 in:\n3\nsample1 out:\n#####\n#...#"
        # 默认截断：输出被削空，首行是空的，守门检查看不到任何异常
        self.assertEqual(server.parse_sample_sections(grid)[0]["output"], "")
        # 关掉截断：原样保留，守门检查才能发现首行是 #
        raw = server.parse_sample_sections(grid, truncate_explanations=False)
        self.assertEqual(raw[0]["output"], "#####\n#...#")

    def test_run_endpoint_requires_authentication(self):
        status, _, _ = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM,
            "language": "python", "source": "print(1)", "stdin": "",
        })
        self.assertEqual(status, 401)

    def test_run_endpoint_executes_without_recording_a_submission(self):
        """「运行样例」不该进 submissions 表，否则会污染判题记录与统计。"""
        cookie = self.register_and_login("t010_runner", "T010-password")

        def submission_count():
            _, _, raw = request(self.port, "GET", "/api/submissions?mine=1", cookie=cookie)
            return len(json.loads(raw)["submissions"])

        before = submission_count()
        status, _, raw = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print(int(input()) * 2)", "stdin": "21\n",
        }, cookie=cookie)
        self.assertEqual(status, 200)
        result = json.loads(raw)
        self.assertEqual(result["status"], "OK", result)
        self.assertEqual(result["stdout"].strip(), "42")
        self.assertEqual(submission_count(), before, "运行样例不该产生提交记录")

    def test_run_endpoint_reports_runtime_error_without_crashing(self):
        cookie = self.register_and_login("t010_runner_err", "T010-password")
        status, _, raw = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "raise SystemExit(3)", "stdin": "",
        }, cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(raw)["status"], "Runtime Error")

    def test_run_endpoint_rejects_unknown_problem(self):
        cookie = self.register_and_login("t010_unknown_run", "T010-password")
        status, _, raw = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": "NOT-IN-CATALOG", "language": "python",
            "source": "print('should not execute')", "stdin": "",
        }, cookie=cookie)
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(raw)["status"], "Problem Not Found")

    def test_run_endpoint_enforces_a_per_user_quota(self):
        """互斥只挡「同时」，挡不住「一直」：一个登录用户可以串行地无限次跑任意代码。

        用不存在的题号把额度耗完 —— 配额在题号校验之前记账，所以这 30 次不会真的
        执行代码，测试跑得快；随后对**合法**题号也必须被挡下，才说明限的是运行本身。
        """
        import server
        cookie = self.register_and_login("t013_quota", "T013-password")
        bogus = {"book": SUBMIT_BOOK, "problem": "NOT-IN-CATALOG", "language": "python",
                 "source": "print(1)", "stdin": ""}
        codes = [request(self.port, "POST", "/api/run", bogus, cookie=cookie)[0]
                 for _ in range(server.RUN_QUOTA_MAX)]
        self.assertEqual(set(codes), {404}, "额度用完之前应当只是题号不存在")

        status, _, raw = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print(1)", "stdin": "",
        }, cookie=cookie)
        self.assertEqual(status, 429)
        payload = json.loads(raw)
        self.assertEqual(payload["status"], "Rate Limited")
        self.assertGreater(payload["retry_after"], 0)

        # 配额是按用户算的：另一个人不受影响
        other = self.register_and_login("t013_quota_other", "T013-password")
        status, _, _ = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print(1)", "stdin": "",
        }, cookie=other)
        self.assertEqual(status, 200)

    def test_run_quota_window_actually_expires(self):
        """滑动窗口必须真的滑动 —— 不清旧记录的话，用满一次就被永久挡住。

        上一条测不到这件事（它跑不了 5 分钟），所以直接对纯函数验，
        临时把窗口缩到 1 秒。变异自检里「窗口永不过期」正是靠这条才会红。
        """
        import server
        original = server.RUN_QUOTA_WINDOW_SECONDS
        server.QUOTA_HISTORY.clear()
        server.RUN_QUOTA_WINDOW_SECONDS = 1
        try:
            for _ in range(server.RUN_QUOTA_MAX):
                self.assertEqual(server.quota_retry_after("run", "window_user", 1, server.RUN_QUOTA_MAX), 0)
            self.assertGreater(server.quota_retry_after("run", "window_user", 1, server.RUN_QUOTA_MAX), 0, "额度应已用尽")
            time.sleep(1.2)
            self.assertEqual(server.quota_retry_after("run", "window_user", 1, server.RUN_QUOTA_MAX), 0,
                             "窗口过去之后额度必须恢复")
        finally:
            server.RUN_QUOTA_WINDOW_SECONDS = original
            server.QUOTA_HISTORY.clear()

    def test_submit_endpoint_enforces_a_per_user_quota(self):
        """提交也要有配额：互斥只挡「同时」，一个人串行刷提交照样能把判题机占满。

        额度比运行样例更紧（提交要跑完全部测试点、最长 300 秒，还会入库）。
        为了不真的判 20 次，先把窗口和额度临时调小 —— 改的是服务端进程里的模块常量，
        所以这里直接对纯函数验额度语义，再用一次真实请求确认端点确实接了这个闸。
        """
        import server
        server.QUOTA_HISTORY.clear()
        try:
            for _ in range(server.SUBMIT_QUOTA_MAX):
                self.assertEqual(server.quota_retry_after(
                    "submit", "quota_user", server.SUBMIT_QUOTA_WINDOW_SECONDS,
                    server.SUBMIT_QUOTA_MAX), 0)
            self.assertGreater(server.quota_retry_after(
                "submit", "quota_user", server.SUBMIT_QUOTA_WINDOW_SECONDS,
                server.SUBMIT_QUOTA_MAX), 0, "提交额度用尽后必须开始拒绝")
            # run 与 submit 是两个独立的桶，不该互相消耗。
            # 要把整整一份 run 额度用满才验得出来：只试一次的话，共用一个桶时
            # 剩余空间仍然够那一次，测试照样绿 —— 变异自检就是这么发现这条太松的。
            for attempt in range(server.RUN_QUOTA_MAX):
                self.assertEqual(server.quota_retry_after(
                    "run", "quota_user", server.RUN_QUOTA_WINDOW_SECONDS,
                    server.RUN_QUOTA_MAX), 0,
                    f"运行样例的额度不该被提交吃掉（第 {attempt + 1} 次就被挡了）")
        finally:
            server.QUOTA_HISTORY.clear()

        # 端点真的接上了这个闸：额度耗尽后连合法提交也被挡下
        cookie = self.register_and_login("t014_submit_quota", "T014-password")
        codes = []
        for _ in range(server.SUBMIT_QUOTA_MAX + 1):
            status, _, raw = request(self.port, "POST", "/api/submit", {
                "book": SUBMIT_BOOK, "problem": "NOT-IN-CATALOG",
                "language": "python", "source": "print(1)",
            }, cookie=cookie)
            codes.append(status)
            if status == 429:
                self.assertEqual(json.loads(raw)["status"], "Rate Limited")
                break
        self.assertIn(429, codes, f"提交应在第 {server.SUBMIT_QUOTA_MAX + 1} 次被挡下，实际 {codes}")

    def test_admin_can_change_quotas_without_a_restart(self):
        """额度是拍的，撞上它的时刻（考试当天）恰恰最不能重启 —— 所以必须能在线改。"""
        admin = self._admin_cookie()
        status, _, raw = request(self.port, "GET", "/api/settings")
        self.assertEqual(status, 200)
        payload = json.loads(raw)
        self.assertIn("quotas", payload)
        self.assertIn("quota_defaults", payload)
        original = payload["quotas"]

        try:
            status, _, raw = request(self.port, "POST", "/api/settings", {
                "quotas": {"submit": {"limit": 3, "window": 600}},
            }, cookie=admin)
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(raw)["quotas"]["submit"], {"limit": 3, "window": 600})

            cookie = self.register_and_login("t015_conf_quota", "T015-password")
            codes = [request(self.port, "POST", "/api/submit", {
                "book": SUBMIT_BOOK, "problem": "NOT-IN-CATALOG",
                "language": "python", "source": "print(1)",
            }, cookie=cookie)[0] for _ in range(4)]
            self.assertEqual(codes[-1], 429, f"改小额度后第 4 次应被挡下，实际 {codes}")

            # 0 表示不限：考试当天要能一键放开
            status, _, _ = request(self.port, "POST", "/api/settings", {
                "quotas": {"submit": {"limit": 0, "window": 600}},
            }, cookie=admin)
            self.assertEqual(status, 200)
            status, _, raw = request(self.port, "POST", "/api/submit", {
                "book": SUBMIT_BOOK, "problem": "NOT-IN-CATALOG",
                "language": "python", "source": "print(1)",
            }, cookie=cookie)
            # /api/submit 对未知题号是 200 + status="Problem Not Found"（只有 /api/run 才是 404）
            self.assertEqual(status, 200, "额度填 0 之后不该再被限频")
            self.assertEqual(json.loads(raw)["status"], "Problem Not Found")

            # 坏值要被拒绝，而不是悄悄存进去
            for bad in ({"limit": -1, "window": 600}, {"limit": 5, "window": 1},
                        {"limit": "abc", "window": 600}):
                status, _, _ = request(self.port, "POST", "/api/settings",
                                       {"quotas": {"submit": bad}}, cookie=admin)
                self.assertEqual(status, 400, bad)
        finally:
            request(self.port, "POST", "/api/settings", {"quotas": original}, cookie=admin)

    def test_quota_changes_require_admin(self):
        cookie = self.register_and_login("t015_not_admin", "T015-password")
        status, _, _ = request(self.port, "POST", "/api/settings",
                               {"quotas": {"submit": {"limit": 9999, "window": 600}}}, cookie=cookie)
        self.assertEqual(status, 403)

    def test_registration_is_rate_limited(self):
        """未登录端点，验证码挡得住脚本、挡不住慢速刷号。"""
        admin = self._admin_cookie()
        original = json.loads(request(self.port, "GET", "/api/settings")[2])["quotas"]
        try:
            request(self.port, "POST", "/api/settings",
                    {"quotas": {"register": {"limit": 2, "window": 600}}}, cookie=admin)
            codes = []
            for i in range(4):
                status, _, _ = request(self.port, "POST", "/api/user/register",
                                       self.registration_payload(f"t015_reg_{i}", "T015-password"))
                codes.append(status)
            self.assertIn(429, codes, f"注册应被限频，实际 {codes}")
        finally:
            request(self.port, "POST", "/api/settings", {"quotas": original}, cookie=admin)

    def test_password_reset_requests_are_rate_limited(self):
        """发信端点：可被用来对着某人的信箱反复刷重置邮件。"""
        admin = self._admin_cookie()
        original = json.loads(request(self.port, "GET", "/api/settings")[2])["quotas"]
        try:
            request(self.port, "POST", "/api/settings",
                    {"quotas": {"forgot": {"limit": 3, "window": 600}}}, cookie=admin)
            codes = [request(self.port, "POST", "/api/user/forgot",
                             {"email": "someone@example.com"})[0] for _ in range(5)]
            self.assertIn(429, codes, f"找回密码应被限频，实际 {codes}")
        finally:
            request(self.port, "POST", "/api/settings", {"quotas": original}, cookie=admin)

    def test_password_reset_limit_does_not_leak_which_emails_exist(self):
        """限频不能变成「这个邮箱注册过」的信号。

        这个端点无论邮箱存不存在都回同一个 {"ok": true}，就是为了不泄露注册情况。
        如果限频写在查库之后、只对真实邮箱生效，那 429 本身就把这层保护拆穿了。
        """
        admin = self._admin_cookie()
        original = json.loads(request(self.port, "GET", "/api/settings")[2])["quotas"]
        username = "t016_reset_probe"
        self.register_and_login(username, "T016-password")
        real, fake = username + "@example.com", "definitely-not-registered@example.com"
        try:
            # 先确认两者的正常响应本来就一模一样（这是端点原有的防泄露设计）
            request(self.port, "POST", "/api/settings",
                    {"quotas": {"forgot": {"limit": 0, "window": 600}}}, cookie=admin)
            real_status, _, real_body = request(self.port, "POST", "/api/user/forgot", {"email": real})
            fake_status, _, fake_body = request(self.port, "POST", "/api/user/forgot", {"email": fake})
            self.assertEqual(real_status, fake_status)
            # 改动前这里是不相等的：没配邮件服务时真实邮箱会**把重置链接直接回给调用者**，
            # 既泄露了「该邮箱已注册」，更等于任意账号接管。现在要显式开
            # CS101_SHOW_RESET_LINK=1 才给，默认两者完全一致。
            self.assertEqual(json.loads(real_body), json.loads(fake_body))
            self.assertNotIn("reset_link", json.loads(real_body))

            # 关键判据：**不存在的邮箱同样消耗额度**。
            # 如果限频写在查库之后、只对真实邮箱生效，这里永远不会出现 429，
            # 而 429 与否也就成了「这个邮箱注册过」的旁路信号。
            request(self.port, "POST", "/api/settings",
                    {"quotas": {"forgot": {"limit": 2, "window": 600}}}, cookie=admin)
            codes = [request(self.port, "POST", "/api/user/forgot", {"email": fake})[0]
                     for _ in range(4)]
            self.assertIn(429, codes, f"不存在的邮箱也必须计入额度，实际 {codes}")
        finally:
            request(self.port, "POST", "/api/settings", {"quotas": original}, cookie=admin)

    def test_run_endpoint_rejects_oversized_stdin(self):
        cookie = self.register_and_login("t010_runner_big", "T010-password")
        status, _, raw = request(self.port, "POST", "/api/run", {
            "book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM, "language": "python",
            "source": "print(1)", "stdin": "x" * (64 * 1024 + 1),
        }, cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(raw)["status"], "Input Too Large")

    def test_password_hashes_use_a_per_user_salt(self):
        """改动前全库共用源码里的常量盐，同口令 → 同哈希，一张彩虹表通吃。"""
        import server
        first, second = server.password_hash("CorrectHorse1"), server.password_hash("CorrectHorse1")
        self.assertNotEqual(first, second, "同一口令两次应得到不同哈希（盐不同）")
        self.assertTrue(first.startswith("pbkdf2$"))
        self.assertTrue(server.valid_password(first, "CorrectHorse1"))
        self.assertFalse(server.valid_password(first, "CorrectHorse2"))
        # 老格式必须继续认，否则升级会把现有学生账号全锁在门外
        legacy = server.legacy_password_hash("CorrectHorse1")
        self.assertTrue(server.valid_password(legacy, "CorrectHorse1"))
        self.assertFalse(server.valid_password(legacy, "CorrectHorse2"))
        self.assertTrue(server.needs_rehash(legacy))
        self.assertFalse(server.needs_rehash(first))

    def test_existing_legacy_hash_still_logs_in_and_is_upgraded(self):
        """线上已有学生账号存的是老格式哈希。升级不能把他们锁在门外。

        直接往库里塞一条老格式记录（就是改动前 `password_hash` 的产物），
        然后走真实登录链路，并确认这次登录顺手把它换成了带随机盐的新格式。
        """
        import server
        username = "t012_legacy"
        with sqlite3.connect(self.db_file.name) as db:
            db.execute("insert into users(username, password_hash, email, active) values (?, ?, ?, 1)",
                       (username, server.legacy_password_hash("LegacyPass-1"),
                        "legacy@example.com"))

        status, headers, _ = request(self.port, "POST", "/api/user/login",
                                     {"username": username, "password": "LegacyPass-1"})
        self.assertEqual(status, 200, "老格式账号必须还能登录")
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        self.assertTrue(json.loads(request(self.port, "GET", "/api/me", cookie=cookie)[2])["authenticated"])

        with sqlite3.connect(self.db_file.name) as db:
            stored = db.execute("select password_hash from users where username = ?",
                                (username,)).fetchone()[0]
        self.assertTrue(stored.startswith("pbkdf2$"), "登录后应已升级成每用户随机盐")
        self.assertTrue(server.valid_password(stored, "LegacyPass-1"))

    def test_changing_password_revokes_other_sessions(self):
        """改密是「号被盗了」的标准补救；补救必须真的把别人踢下线。"""
        username = "t012_revoke"
        stolen = self.register_and_login(username, "OldPass-123")   # 模拟盗号者手上的 cookie
        _, headers, _ = request(self.port, "POST", "/api/user/login",
                                {"username": username, "password": "OldPass-123"})
        keeper = headers["Set-Cookie"].split(";", 1)[0]             # 本人当前这条会话
        self.assertTrue(json.loads(request(self.port, "GET", "/api/me", cookie=stolen)[2])["authenticated"])

        status, _, _ = request(self.port, "POST", "/api/user/change-password", {
            "current_password": "OldPass-123", "new_password": "BrandNew-456",
            "confirm_password": "BrandNew-456",
        }, cookie=keeper)
        self.assertEqual(status, 200)

        after = json.loads(request(self.port, "GET", "/api/me", cookie=stolen)[2])
        self.assertFalse(after["authenticated"], "改密后旧会话必须失效")
        # 发起改密的那条会话应当保留，否则用户会被自己踢出去
        self.assertTrue(json.loads(request(self.port, "GET", "/api/me", cookie=keeper)[2])["authenticated"])

    def test_login_throttles_repeated_failures(self):
        username = "t012_throttle"
        self.register_and_login(username, "GoodPass-123")
        codes = [request(self.port, "POST", "/api/user/login",
                         {"username": username, "password": f"wrong-{i}"})[0] for i in range(14)]
        self.assertIn(429, codes, f"连续错误口令应触发冷却，实际全是 {sorted(set(codes))}")
        # 冷却期间即使给对口令也不放行
        status, _, _ = request(self.port, "POST", "/api/user/login",
                               {"username": username, "password": "GoodPass-123"})
        self.assertEqual(status, 429)

    def test_static_path_cannot_traverse(self):
        for path in ("/../server.py", "/%2e%2e/server.py", "/data/../server.py"):
            status, _, body = request(self.port, "GET", path)
            self.assertEqual(status, 404, path)
            self.assertNotIn(b"ThreadingHTTPServer", body, path)

    def test_static_serves_only_whitelisted_assets(self):
        # 上一条防的是「逃出 ROOT」；这条防的是「ROOT 里的东西不该全公开」。
        # 改动前 GET /data/course.db 能下到整个 SQLite 库（口令哈希 + 全部提交），
        # data/.admin_password 走的是同一条代码路径。断言查内容而不是状态码，
        # 因为未命中会落到上游代理，代理通不通网决定了状态码、决定不了内容。
        leaks = {
            "/server.py": b"ThreadingHTTPServer",
            "/judge.py": b"TOTAL_HARD_CAP_S",
            "/data/course.db": b"SQLite format 3",
            "/collab/PLAN.md": b"Decision Log",
            "/data/openjudge/catalog.json": b"test_cases",
        }
        for path, fingerprint in leaks.items():
            _, _, body = request(self.port, "GET", path)
            self.assertNotIn(fingerprint, body, path)

        canary = ROOT / "data" / ".probe-canary"
        canary.write_text("CANARY-NOT-A-REAL-SECRET\n", encoding="utf-8")
        try:
            # 与 data/.admin_password 同目录同形态，但不动真的口令文件
            _, _, body = request(self.port, "GET", "/data/.probe-canary")
            self.assertNotIn(b"CANARY-NOT-A-REAL-SECRET", body)
        finally:
            canary.unlink()

        status, headers, body = request(self.port, "GET", "/static/theme.css")
        self.assertEqual(status, 200)
        self.assertIn("text/css", headers.get("Content-Type", ""))
        self.assertIn(b"--accent", body)

        # 白名单是按后缀发的：static/ 下放一个非白名单后缀也不该发出去
        blocked = STATIC_DIR / "probe-canary.md"
        blocked.write_text("CANARY-NOT-A-REAL-SECRET\n", encoding="utf-8")
        try:
            _, _, body = request(self.port, "GET", "/static/probe-canary.md")
            self.assertNotIn(b"CANARY-NOT-A-REAL-SECRET", body)
        finally:
            blocked.unlink()


if __name__ == "__main__":
    unittest.main()
