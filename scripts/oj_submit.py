"""向 cs101.openjudge.cn 提交并轮询判题结果。

**为什么需要它**（2026-07-26 人拍板，见 PLAN 的 Decision Log）：
本地对拍只能证明两个实现**彼此一致**，证明不了它们**解对了题**。
round4 的 3725 是两个实现一致地跑偏了 400 次；round5 的 3750/4012/4076/3377
在本地全部通过（对拍、字节复现、逐组复算），平台却判 WA/PE ——
**它们生成的数据是错的**。平台提交是目前唯一能捅破这一层的手段。

**口令绝不入库（红线 2）**：只从环境变量 `OJ_USER` / `OJ_PASS` 读，
本模块不写任何凭据到磁盘、不打印口令、也不接受把口令当参数传进来。

**提交前要按题拆成单题独立程序**：整份 `solve()` / `alt()` 分派器交上去会被平台的
pylint 判 `E0102 function-redefined`（不同分支里重名的嵌套函数）算 Compile Error。
round4 的 19 份 oracle 第一次提交就是整批栽在这上面。

**三档顺序**：`Python3` → 若 TLE 则 `PyPy3` → 若仍 TLE 则写 `C++`。
实证：3728/4009 的 Python 实现在 Python3 档 TLE、PyPy3 档 Accepted，
算法本身是够的；而纯暴力实现换 PyPy3 一份都救不回来。
"""
from __future__ import annotations

import base64
import http.cookiejar
import json
import os
import re
import time
import urllib.parse
import urllib.request

HOST = os.environ.get("OJ_BASE_URL", "http://cs101.openjudge.cn")
HOST_HEADER = os.environ.get("OJ_HOST_HEADER")
LANGUAGES = ("Python3", "PyPy3", "G++", "GCC", "Java", "Pascal")
FINAL_VERDICTS = ("Accepted", "Wrong Answer", "Time Limit Exceeded", "Runtime Error",
                  "Compile Error", "Presentation Error", "Memory Limit Exceeded",
                  "Output Limit Exceeded")


class Session:
    def __init__(self, retries=4):
        self._jar = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self._jar))
        self._opener.addheaders = [("User-Agent", "Mozilla/5.0")]
        self._retries = retries

    def _request(self, url, data=None):
        request = urllib.request.Request(url, data=data)
        if HOST_HEADER:
            request.add_header("Host", HOST_HEADER)
        return request

    def _get(self, url):
        for attempt in range(self._retries):
            try:
                with self._opener.open(self._request(url), timeout=60) as response:
                    return response.read().decode("utf-8", "replace")
            except Exception:
                if attempt == self._retries - 1:
                    raise
                time.sleep(5 * (attempt + 1))          # 平台会偶发 connection reset

    def _post(self, url, fields):
        data = urllib.parse.urlencode(fields).encode()
        with self._opener.open(self._request(url, data), timeout=60) as response:
            return response.read().decode("utf-8", "replace")

    def login(self):
        """口令只从环境变量读；缺失时直接报错，不去猜、也不落盘。"""
        user, password = os.environ.get("OJ_USER"), os.environ.get("OJ_PASS")
        if not user or not password:
            raise RuntimeError("需要环境变量 OJ_USER / OJ_PASS；口令不入库（红线 2）")
        body = self._post(f"{HOST}/api/auth/login/", {"email": user, "password": password})
        if json.loads(body).get("result") != "SUCCESS":
            raise RuntimeError("登录失败")           # 不回显返回体，避免带出账号信息
        return self

    def submit(self, number, source, language, group="practice"):
        if language not in LANGUAGES:
            raise ValueError(f"语言必须是 {LANGUAGES} 之一，收到 {language!r}")
        page = self._get(f"{HOST}/{group}/{number}/submit/")
        contest = re.search(r'name="contestId" value="(\d+)"', page)
        if not contest:
            raise RuntimeError(f"{number}: 拿不到 contestId（是不是没登录或题号不对）")
        body = self._post(f"{HOST}/api/solution/submitv2/", {
            "contestId": contest.group(1), "problemNumber": number,
            "sourceEncode": "base64", "language": language,
            "source": base64.b64encode(source.encode()).decode()})
        doc = json.loads(body)
        if doc.get("result") != "SUCCESS":
            raise RuntimeError(f"{number}: 提交被拒 {str(doc)[:120]}")
        return doc["redirect"].rstrip("/").rsplit("/", 1)[-1]

    def poll(self, solution_id, attempts=90, interval=3):
        url = f"{HOST}/practice/solution/{solution_id}/"
        for _ in range(attempts):
            page = self._get(url)
            for verdict in FINAL_VERDICTS:
                if verdict in page:
                    spent = re.search(r"(\d+)\s*kB.*?(\d+)\s*ms", page, re.S)
                    return {"verdict": verdict, "ms": int(spent.group(2)) if spent else None,
                            "solution_id": solution_id}
            time.sleep(interval)
        return {"verdict": "TIMEOUT_POLLING", "ms": None, "solution_id": solution_id}

    def run(self, number, source, language, group="practice"):
        return self.poll(self.submit(number, source, language, group))


def escalate(session, number, source, tiers=("Python3", "PyPy3"), group="practice"):
    """三档里的前两档：Python3 超时就换 PyPy3。仍超时的返回最后一档结果，交人决定写不写 C++。"""
    attempts = []
    for language in tiers:
        result = session.run(number, source, language, group)
        attempts.append({"language": language, **result})
        if result["verdict"] != "Time Limit Exceeded":
            break
    return {"final": attempts[-1]["verdict"], "attempts": attempts}
