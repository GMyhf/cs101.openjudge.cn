"""6901 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 6901
SAMPLE_IN = '5\n1 2 3 4\n1 0\n90 3 1 2 4\n4 2 3 2\n2 1 3\n'
SAMPLE_OUT = '3\n1 2 4\n'
REFERENCE_SOURCE = "def find_topic_center_and_mentioners():\n    n = int(input())\n    mention_count = {}  # 记录每个人被提及的次数\n    mention_relations = {}  # 记录提及关系，key为提及的人，value为提及的人的集合\n    \n    for _ in range(n):\n        tweet = input().split()\n        sender, k = int(tweet[0]), int(tweet[1])\n        if k > 0:\n            mentioned = list(map(int, tweet[2:]))\n            for person in mentioned:\n                if person not in mention_count:\n                    mention_count[person] = 1\n                    mention_relations[person] = set([sender])\n                else:\n                    mention_count[person] += 1\n                    mention_relations[person].add(sender)\n    \n    # 找到被提及最多的人\n    topic_center = max(mention_count, key=mention_count.get)\n    \n    # 输出结果\n    print(topic_center)\n    print(' '.join(map(str, sorted(mention_relations[topic_center]))))\n\n# 调用函数处理输入数据\nfind_topic_center_and_mentioners()\n"

def g6901(r):
    n = r.randint(3, 30); rows = []
    for _ in range(n):
        sender = r.randint(1, 100); mentioned = r.sample(range(1, 101), r.randint(0, 6))
        rows.append(" ".join(map(str, [sender, len(mentioned)] + mentioned)))
    return str(n) + "\n" + "\n".join(rows) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g6901(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

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
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
