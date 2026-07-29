import random, subprocess, sys, tempfile
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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
