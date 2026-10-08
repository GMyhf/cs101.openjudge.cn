import random, re, subprocess, sys, tempfile
from pathlib import Path
def g2499(r):
    rows = []
    for _ in range(r.randint(1, 15)):
        a = b = 1
        for _ in range(r.randint(0, 25)):
            if r.random() < .5: a += b
            else: b += a
        rows.append(f"{a} {b}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

import math

def valid(text):
    """题面：首行场景数；每个场景一行两个整数 i j，1 <= i, j <= 2*10^9，且 (i, j) 是树中合法结点（即 gcd(i, j) = 1）。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        return False
    if not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    t = int(lines[0])
    if len(lines) != t + 1:
        return False
    for line in lines[1:]:
        m = re.fullmatch(r"([1-9][0-9]*) ([1-9][0-9]*)", line)
        if not m:
            return False
        i, j = int(m.group(1)), int(m.group(2))
        if not (1 <= i <= 2 * 10**9 and 1 <= j <= 2 * 10**9):
            return False
        if math.gcd(i, j) != 1:
            return False
    return True


LIMIT = 2 * 10**9

def big2499(r, k):
    """满值域组：边界结点、最深的斐波那契链、随机互质大数。逐次减法的写法会超时。"""
    rows = []
    if k == 0:
        rows = [(1, 1), (LIMIT, 1), (1, LIMIT), (LIMIT, LIMIT - 1), (LIMIT - 1, LIMIT), (2, 1), (1, 2), (LIMIT - 1, 1)]
    elif k == 1:
        f = [1, 1]
        while f[-1] + f[-2] <= LIMIT:
            f.append(f[-1] + f[-2])
        for x in range(1, len(f)):
            rows.append((f[x], f[x - 1]))
            rows.append((f[x - 1], f[x]))
    else:
        n = r.randint(200, 1000)
        while len(rows) < n:
            mode = r.random()
            if mode < 0.4:
                i, j = r.randint(1, LIMIT), r.randint(1, LIMIT)
            elif mode < 0.7:
                i, j = r.randint(1, LIMIT), r.randint(1, 50)
            else:
                i, j = r.randint(1, 50), r.randint(1, LIMIT)
            if r.random() < 0.5:
                i, j = j, i
            if math.gcd(i, j) == 1:
                rows.append((i, j))
    return str(len(rows)) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2499: Binary Tree\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02499/\n# License: not declared in source collection; no license is inferred.\ndef count_moves(i, j):\n    left_moves = 0\n    right_moves = 0\n\n    while i != 1 and j != 1:  # 终止条件: (1,1)\n        if i > j:\n            left_moves += i // j  # 计算可以跳跃多少次\n            i %= j  # 直接更新 i，减少迭代次数\n            if i == 0:  # 避免 ZeroDivisionError\n                i = 1\n        else:\n            right_moves += j // i  # 计算可以跳跃多少次\n            j %= i  # 直接更新 j，减少迭代次数\n            if j == 0:  # 避免 ZeroDivisionError\n                j = 1\n\n    # 可能 i != 1 或 j != 1，需要再补一次\n    if i > 1:\n        left_moves += i - 1\n    elif j > 1:\n        right_moves += j - 1\n\n    return left_moves, right_moves\n\n\nn = int(input())  # 读取测试用例数量\nfor case_num in range(1, n + 1):\n    i, j = map(int, input().split())  # 读取 i, j\n    left, right = count_moves(i, j)\n\n    # 输出格式\n    print(f"Scenario #{case_num}:")\n    print(left, right)\n    if case_num != n:\n        print()  # 题目要求每个案例后面空行\n'
SAMPLE='3\n42 1\n3 4\n17 73\n'
GENERATOR='g2499'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 30)]
    cases+=[big2499(random.Random(1000 + k), k) for k in range(10)]
    assert all(valid(c) for c in cases)
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
