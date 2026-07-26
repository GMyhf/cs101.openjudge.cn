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

# 认证提交这条链路要真的走进判题器，所以题号必须选数据已入库的（`*_made/`）；
# `data/openjudge/tests/**` 下抓取的数据不入库，用它会让新克隆的仓库跑不通。
SUBMIT_BOOK = "pctbook"
SUBMIT_PROBLEM = "E03406"


def request(port, method, path, body=None, cookie=None):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=8)
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
        environment["CS101_LOAD_DOTENV"] = "0"
        cls.process = subprocess.Popen(
            [sys.executable, "server.py"], cwd=ROOT, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        # 先登记清理再等待：即使服务端起不来、setUpClass 抛异常，
        # addClassCleanup 也会跑，不会漏下孤儿进程和临时库文件。
        cls.addClassCleanup(cls._stop_server)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            try:
                status, _, _ = request(cls.port, "GET", "/api/me")
                if status == 200:
                    return
            except (ConnectionRefusedError, OSError):
                time.sleep(0.05)
        cls._stop_server()
        raise RuntimeError("server did not start: " + (cls.process.stderr.read() or "<no stderr>"))

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
            "username": username, "password": "T001-password",
        })
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
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

    def test_submit_page_renders_without_placeholders(self):
        status, _, body = request(self.port, "GET", f"/{SUBMIT_BOOK}/{SUBMIT_PROBLEM}/submit/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8", errors="replace")
        self.assertIn(SUBMIT_PROBLEM, text)
        self.assertIn("我的提交记录", text)
        self.assertIn("height:520px", text)
        self.assertIn("查看代码", text)
        for placeholder in ("__BOOK__", "__PROBLEM__"):
            self.assertNotIn(placeholder, text)      # 模板占位符必须已被替换

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
        self.assertEqual(latest["detail"]["language_version"], "Python3(3.9)")
        admin = self._admin_cookie()
        status, _, body = request(self.port, "GET", "/api/submissions", cookie=admin)
        self.assertEqual(status, 200)
        admin_latest = json.loads(body)["submissions"][0]
        self.assertEqual(admin_latest["source"], "print('wrong')")

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

    def test_reveal_switch_defaults_to_off(self):
        """必须在**没有任何设置记录**的全新库上验，否则测的是上一个用例写进去的值。

        本类的用例按字母序执行，`test_failing_input_...` 排在前面并会把开关显式写成 off；
        若在共享库上读 `/api/settings`，读到的是那行记录，默认值这条分支根本走不到
        （改默认为 on 也照样通过）。所以这里另开一个干净的库直接问 `reveal_enabled()`。
        """
        import server
        with tempfile.TemporaryDirectory() as folder:
            fresh = Path(folder) / "fresh.db"
            saved = server.DB
            server.DB = fresh
            try:
                server.init_db()
                with sqlite3.connect(fresh) as db:
                    self.assertEqual(db.execute("select count(*) from settings").fetchone()[0], 0)
                self.assertIs(server.reveal_enabled(), False)
            finally:
                server.DB = saved

    def test_reveal_switch_rejects_non_admin(self):
        username = "t006_switch_student"
        cookie = self.register_and_login(username, "T006-password")
        status, _, _ = request(self.port, "POST", "/api/settings",
                               {"reveal_failing_input": True}, cookie=cookie)
        self.assertEqual(status, 403)
        _, _, body = request(self.port, "GET", "/api/settings")
        self.assertIs(json.loads(body)["reveal_failing_input"], False)

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
                self.assertFalse(server.reveal_effective("practice", now))     # 默认关

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
        # 判题器 2026-07-26 起支持 PyPy3（人拍板），提交页要给得出这个选项。
        import server
        self.assertIn('value="pypy3"', server.SUBMIT_PAGE)

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
        self.assertEqual(count("?limit=2"), 2)
        self.assertEqual(count("?limit=abc"), total)      # 非法值回落默认，不是 500
        self.assertEqual(count("?limit=99999"), total)    # 夹到上界，不是拒绝

    def test_static_path_cannot_traverse(self):
        for path in ("/../server.py", "/%2e%2e/server.py", "/data/../server.py"):
            status, _, body = request(self.port, "GET", path)
            self.assertEqual(status, 404, path)
            self.assertNotIn(b"ThreadingHTTPServer", body, path)


if __name__ == "__main__":
    unittest.main()
