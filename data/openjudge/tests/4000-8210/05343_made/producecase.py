"""5343 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5343
SAMPLE_IN = '8\nD8 A6 C3 B8 C5 A1 B5 D3\n'
SAMPLE_OUT = 'Queue1:A1\nQueue2:\nQueue3:C3 D3\nQueue4:\nQueue5:C5 B5\nQueue6:A6\nQueue7:\nQueue8:D8 B8\nQueue9:\nQueueA:A1 A6\nQueueB:B5 B8\nQueueC:C3 C5\nQueueD:D3 D8\nA1 A6 B5 B8 C3 C5 D3 D8\n'
REFERENCE_SOURCE = "from collections import deque\n\n\nn = int(input())\nqueues = [deque() for _ in range(9)]\ncards = deque(list(input().split()))\n\nwhile cards:\n    card = cards.popleft()\n    queues[int(card[1])-1].append(card)\n\nqs = {'A': deque(), 'B': deque(), 'C': deque(), 'D': deque()}\nfor i in range(9):\n    tmp = []\n    while queues[i]:\n        card = queues[i].popleft()\n        qs[card[0]].append(card)\n        tmp.append(card)\n    print(f'Queue{i+1}:'+' '.join(tmp))\n\nresult = []\nfor char in qs.keys():\n    tmp = []\n    while qs[char]:\n        card = qs[char].popleft()\n        result.append(card)\n        tmp.append(card)\n    print(f'Queue{char}:' + ' '.join(tmp))\nprint(*result)\n"

def valid(text):
    """题面契约：两行；第一行 n（1<=n<=100）；第二行 n 张牌，每张形如 XY，X 为 A～D，Y 为 1～9。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    if len(lines) != 2:
        return False
    h = lines[0].split()
    if len(h) != 1 or not h[0].isdigit():
        return False
    n = int(h[0])
    cards = lines[1].split()
    if not 1 <= n <= 100 or len(cards) != n:
        return False
    return all(len(c) == 2 and c[0] in "ABCD" and c[1] in "123456789" for c in cards)


DECK = [s + str(v) for s in "ABCD" for v in range(1, 10)]


def g5343(r, plan):
    n, kind = plan
    if isinstance(n, tuple):
        n = r.randint(*n)
    if kind == "distinct":        # 不重复抽牌
        values = r.sample(DECK, n)
    elif kind == "deck":          # 整副 36 张打乱
        values = DECK[:]; r.shuffle(values)
    elif kind == "same":          # 同一张牌重复
        values = [r.choice(DECK)] * n
    elif kind == "suit":          # 同一花色
        s = r.choice("ABCD"); values = [s + str(r.randint(1, 9)) for _ in range(n)]
    elif kind == "rank":          # 同一点数
        v = str(r.randint(1, 9)); values = [r.choice("ABCD") + v for _ in range(n)]
    elif kind == "sorted":        # 已经有序
        values = sorted(r.choice(DECK) for _ in range(n))
    elif kind == "rsorted":       # 逆序
        values = sorted((r.choice(DECK) for _ in range(n)), reverse=True)
    elif kind == "few":           # 只用少数几张，很多空队列
        pool = r.sample(DECK, 3); values = [r.choice(pool) for _ in range(n)]
    else:                         # 有放回随机，含重复牌
        values = [r.choice(DECK) for _ in range(n)]
    return str(len(values)) + "\n" + " ".join(values) + "\n"


PLAN = [
    (1, "rand"), (2, "rand"), (2, "same"), ((3, 10), "distinct"), ((5, 15), "suit"),
    ((5, 15), "rank"), ((10, 30), "rand"), ((10, 30), "few"), (36, "deck"), ((37, 60), "rand"),
    ((60, 99), "rand"), (100, "rand"), (100, "same"), (100, "suit"), (100, "rank"),
    (100, "sorted"), (100, "rsorted"), (100, "few"), (100, "rand"),
]


def build_cases():
    return [SAMPLE_IN] + [g5343(random.Random(NUMBER + i), PLAN[i - 1]) for i in range(1, 20)]


def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    assert all(valid(c) for c in cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
