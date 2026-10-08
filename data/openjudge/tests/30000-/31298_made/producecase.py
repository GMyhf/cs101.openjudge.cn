#!/usr/bin/env python3
"""31298 警察招募又来了 —— 生成器、输入契约与数据构建。

第 0、1 组是题面的两组样例。形状按错法排：

  · `edge`      —— 犯罪恰好发生在第 t+k-1 分钟（警员最后一分钟还在役）和第 t+k 分钟
                   （刚退役）：把服役区间写成 [t, t+k] 或 [t, t+k-2] 的差一错在这里挂。
  · `fifo`      —— 新老警员同时在役：派最晚入伍的（栈）而不是最早的（队列），老警员会
                   白白过期，多出无法处理的犯罪。
  · `k1`        —— k=1：警员只在招募那一分钟在役，而那一分钟没有犯罪，所有犯罪都处理不了。
  · `no_expire` —— k >= n：没人会退役，忘了处理过期的写法在这里碰巧对，用来和别的形状对照。
  · `crime_first` —— 开头先来一串犯罪（还没有警员）。
  · `random` / `big` —— 随机与题面上界 n=10^5。
"""
import random

NUMBER = 31298
INPUT_DOMAIN = "第一行包含两个整数 n, k（1 <= n, k <= 10^5）；第二行包含 n 个整数 a_i：a_i = -1 表示犯罪，a_i = x（1 <= x <= 10）表示招募 x 名警员"
SAMPLES = [
    ("6 2\n1 1 -1 -1 -1 1\n", "2\n"),
    ("5 1\n5 -1 3 -1 -1\n", "3\n"),
]
MAX_N = 10 ** 5
MAX_K = 10 ** 5
SHAPES = ("edge", "fifo", "random", "k1", "no_expire", "crime_first", "edge", "fifo", "big")


def render(k, events):
    return f"{len(events)} {k}\n" + " ".join(map(str, events)) + "\n"


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "edge":
        # 一段 = 第 t 分钟招 gap 人，接着 gap-1 起犯罪用掉 gap-1 人，第 t+gap 分钟再来一起。
        # gap = k-1 时剩下那人还在役（能处理），gap = k 时他刚退役（处理不了）。
        # 上一段的人在本段开始前都已退役，所以每段末尾那起犯罪只由这条边界决定。
        k = rng.randint(2, 10)            # 一次最多招 10 人，gap <= k <= 10
        limit = rng.randint(200, 20000)
        events = []
        while len(events) + k + 1 <= limit:
            gap = k - 1 if rng.random() < 0.5 else k
            events += [gap] + [-1] * gap
        return render(k, events)
    if shape == "fifo":
        # 老兵快过期、新兵还早：正解先派老兵
        k = rng.randint(5, 200)
        events = []
        limit = rng.randint(500, 30000)
        while len(events) < limit:
            events += [rng.randint(1, 10)] + [-1 if rng.random() < 0.6 else rng.randint(1, 3)
                                               for _ in range(rng.randint(1, k))]
        return render(k, events[:limit])
    if shape == "k1":
        n = rng.randint(2, 20000)
        return render(1, [rng.choice((-1, -1, rng.randint(1, 10))) for _ in range(n)])
    if shape == "no_expire":
        n = rng.randint(10, 30000)
        return render(rng.randint(n, MAX_K), [-1 if rng.random() < 0.85 else rng.randint(1, 10) for _ in range(n)])
    if shape == "crime_first":
        n = rng.randint(10, 20000)
        lead = rng.randint(1, n // 2)
        k = rng.randint(1, 1000)
        return render(k, [-1] * lead + [-1 if rng.random() < 0.7 else rng.randint(1, 10) for _ in range(n - lead)])
    if shape == "big":
        k = rng.randint(1, 100) if seed % 2 else rng.randint(1000, MAX_K)
        return render(k, [-1 if rng.random() < 0.8 else rng.randint(1, 10) for _ in range(MAX_N)])
    n = rng.randint(1, 10000)
    k = rng.randint(1, 10 ** rng.randint(0, 5))
    p = rng.random()
    return render(k, [-1 if rng.random() < p else rng.randint(1, 10) for _ in range(n)])


def valid(text):
    """照题面：第一行 n, k（1..10^5），第二行恰 n 个整数，每个是 -1 或 1..10。"""
    lines = _lines(text)
    if lines is None or len(lines) != 2:
        return "应为 2 行且以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 2:
        return "第一行应为 n k"
    n, k = head
    if not 1 <= n <= MAX_N or not 1 <= k <= MAX_K:
        return f"n={n} 或 k={k} 越界"
    events = _ints(lines[1])
    if events is None or len(events) != n:
        return "第二行个数与 n 不符"
    if not all(a == -1 or 1 <= a <= 10 for a in events):
        return "事件不是 -1 或 1..10"
    return True


def _ints(line):
    parts = line.split(" ")
    for part in parts:
        body = part[1:] if part.startswith("-") else part
        if not body.isdigit() or (len(body) > 1 and body[0] == "0") or part == "-0":
            return None
    return [int(part) for part in parts]


def _lines(text):
    if not text.endswith("\n") or "\r" in text:
        return None
    return text[:-1].split("\n")


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
TOTAL = 40


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [text for text, _answer in SAMPLES]
    cases += [generate(NUMBER, seed) for seed in range(1, TOTAL - len(SAMPLES) + 1)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if valid(case) is not True:
            raise SystemExit(f"case {index} violates the input contract: {valid(case)}")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=120, check=True)
        if index < len(SAMPLES) and result.stdout != SAMPLES[index][1]:
            raise SystemExit(f"第 {index} 组与题面样例输出不符：{result.stdout!r} != {SAMPLES[index][1]!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()
