import http.client
import json
import os
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
        status, headers, _ = request(self.port, "POST", "/api/user/register", {
            "username": username, "password": "T001-password",
        })
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]

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
        for placeholder in ("__BOOK__", "__PROBLEM__"):
            self.assertNotIn(placeholder, text)      # 模板占位符必须已被替换

    def test_submissions_require_authentication(self):
        status, _, body = request(self.port, "GET", "/api/submissions")
        self.assertEqual(status, 401)
        self.assertIn(b"Unauthorized", body)

    def test_submission_history_records_book_language_and_detail(self):
        """历史记录要能回答「错在哪组数据」——只存 status 是答不了的。"""
        username = "t006_history"
        _, headers, _ = request(self.port, "POST", "/api/user/register", {
            "username": username, "password": "T006-password",
        })
        cookie = headers["Set-Cookie"].split(";", 1)[0]
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
        _, headers, _ = request(self.port, "POST", "/api/user/register", {
            "username": username, "password": "T006-password",
        })
        cookie = headers["Set-Cookie"].split(";", 1)[0]
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
        _, headers, _ = request(self.port, "POST", "/api/user/register", {
            "username": username, "password": "T006-password",
        })
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        payload = {"book": SUBMIT_BOOK, "problem": SUBMIT_PROBLEM,
                   "language": "python", "source": "print('wrong')"}

        self._set_reveal(admin, False)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        self.assertNotIn("failing_input", json.loads(body))

        self.assertIs(self._set_reveal(admin, True), True)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        verdict = json.loads(body)
        snippet = verdict.get("failing_input")
        self.assertIsNotNone(snippet)
        self.assertTrue(snippet["text"])
        # 只给输入。期望输出是答案，任何情况下都不能出现在返回里。
        self.assertEqual(set(snippet), {"text", "truncated", "total_lines", "total_chars"})

        self._set_reveal(admin, False)
        _, _, body = request(self.port, "POST", "/api/submit", payload, cookie=cookie)
        self.assertNotIn("failing_input", json.loads(body))

    def test_static_path_cannot_traverse(self):
        for path in ("/../server.py", "/%2e%2e/server.py", "/data/../server.py"):
            status, _, body = request(self.port, "GET", path)
            self.assertEqual(status, 404, path)
            self.assertNotIn(b"ThreadingHTTPServer", body, path)


if __name__ == "__main__":
    unittest.main()
