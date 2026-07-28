#!/usr/bin/env python3
"""并发压测：一份**正确**的代码，在多少并发下开始被误判？

要回答的具体问题不是「机器会不会卡」，而是一件会冤枉学生的事：
判题每组的超时是 `cpu_seconds + 1`，而**这个 +1 是墙钟**。机器繁忙时墙钟被拉长，
一份本来跑得进限时的正确代码就可能被判 TLE —— 代码没问题，是服务器忙。
平时几个人永远测不出来，偏偏会在开学第一节课和考试当天发生。

所以这里提交的一律是**能 AC 的代码**（只是刻意消耗一些 CPU），
任何非 Accepted 的结果都是误判，正是要测的东西。

必须用不同账号：判题对同一用户有互斥（同时只跑一个），
用一个账号并发只会串行，测不出并发。

强烈建议**跑在独立实例上**（自己的 CS101_DB 和端口），不要打生产库：

    CS101_DB=/tmp/lt.db CS101_PORT=8100 CS101_SHOW_ACCOUNT_LINKS=1 python3 server.py &
    python3 scripts/loadtest_judge.py --base http://127.0.0.1:8100 --levels 1,10,30,60,100
"""
import argparse
import concurrent.futures
import http.cookiejar
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request

# 正确解 + 刻意消耗约 BURN 秒 CPU：模拟「算法对但不轻量」的真实提交。
# 02942 读 n 输出斐波那契第 n 项。
SOURCE = """import time
n = int(input())
end = time.process_time() + {burn}
x = 0
while time.process_time() < end:
    x += 1
a, b = 1, 1
for _ in range(n):
    a, b = b, a + b
print(a)
"""


def call(opener, base, path, payload=None, timeout=400):
    request = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"})
    try:
        response = opener.open(request, timeout=timeout)
        return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        try:
            return error.code, json.loads(error.read() or b"{}")
        except ValueError:
            return error.code, {}


def make_account(base, index):
    """注册 → 激活 → 登录，返回一个已登录的 opener。"""
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    name = f"lt{index}_{int(time.time())}"
    _, page = None, None
    raw = opener.open(base + "/register/", timeout=60).read().decode()
    token = re.search(r'name="captcha_token" value="([^"]+)"', raw).group(1)
    left, right = map(int, re.search(r'class="captcha-question">(\d+) \+ (\d+)', raw).groups())
    status, body = call(opener, base, "/api/user/register", {
        "email": f"{name}@example.com", "username": name,
        "password": "LoadTest-123", "confirm_password": "LoadTest-123",
        "captcha_token": token, "captcha_answer": str(left + right)})
    if status != 200:
        raise RuntimeError(f"注册失败 {status} {body}")
    if "activation_link" in body:
        opener.open(base + "/auth/activate/?" + body["activation_link"].split("?", 1)[1],
                    timeout=60).read()
    status, body = call(opener, base, "/api/user/login",
                        {"username": name, "password": "LoadTest-123"})
    if status != 200:
        raise RuntimeError(f"登录失败 {status} {body}")
    return opener


def submit(opener, base, book, problem, source):
    started = time.perf_counter()
    status, body = call(opener, base, "/api/submit",
                        {"book": book, "problem": problem, "language": "python",
                         "source": source})
    return {"http": status, "status": body.get("status"),
            "judge_ms": body.get("time_ms"), "wall_s": time.perf_counter() - started}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="http://127.0.0.1:8100")
    parser.add_argument("--book", default="practice")
    parser.add_argument("--problem", default="02942")
    parser.add_argument("--levels", default="1,10,30,60,100")
    parser.add_argument("--burn", type=float, default=1.5,
                        help="每组测试点刻意消耗的 CPU 秒数（默认 1.5）")
    options = parser.parse_args()
    levels = [int(x) for x in options.levels.split(",")]
    source = SOURCE.format(burn=options.burn)

    peak = max(levels)
    print(f"准备 {peak} 个账号（判题对同一用户有互斥，必须用不同账号）…")
    openers = []
    for index in range(peak):
        openers.append(make_account(options.base, index))
        if (index + 1) % 20 == 0:
            print(f"  {index + 1}/{peak}")

    print(f"\n每次提交：正确解，每组刻意烧 {options.burn}s CPU")
    print(f"{'并发':>5} {'AC':>5} {'误判':>5} {'墙钟中位':>9} {'墙钟P95':>9} {'最慢':>8}  误判明细")
    print("-" * 78)
    for level in levels:
        with concurrent.futures.ThreadPoolExecutor(max_workers=level) as pool:
            results = list(pool.map(
                lambda o: submit(o, options.base, options.book, options.problem, source),
                openers[:level]))
        walls = sorted(r["wall_s"] for r in results)
        accepted = [r for r in results if r["status"] == "Accepted"]
        wrong = [r for r in results if r["status"] != "Accepted"]
        counts = {}
        for r in wrong:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        p95 = walls[min(len(walls) - 1, int(len(walls) * 0.95))]
        detail = "  ".join(f"{k}×{v}" for k, v in sorted(counts.items())) or "—"
        print(f"{level:>5} {len(accepted):>5} {len(wrong):>5} "
              f"{statistics.median(walls):>8.1f}s {p95:>8.1f}s {walls[-1]:>7.1f}s  {detail}")
        time.sleep(3)
    print("-" * 78)
    print("提交的全部是能 AC 的代码，所以「误判」列里任何非零都是服务器负载造成的冤枉判定。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
