"""6640 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 6640
SAMPLE_IN = '3\n2 hello world\n4 the world is great\n2 great news\n4\nhello\nworld\ngreat\npku\n'
SAMPLE_OUT = '1\n1 2\n2 3\nNOT FOUND\n'
REFERENCE_SOURCE = 'from collections import defaultdict\ndef main():\n    n = int(input())\n    index = 1\n    inverted_index = defaultdict(set)   # 构建倒排索引\n    for i in range(1, n + 1):\n        parts = input().split()\n        doc_id = i\n        num_words = int(parts[0])\n        words = parts[1:num_words + 1]\n        for word in words:\n            inverted_index[word].add(doc_id)\n\n    m = int(input())\n    results = []\n\n    # 查询倒排索引\n    for _ in range(m):\n        query = input()\n        if query in inverted_index:\n            results.append(" ".join(map(str, sorted(list(inverted_index[query])))))\n        else:\n            results.append("NOT FOUND")\n\n    # 输出查询结果\n    for result in results:\n        print(result)\n\nif __name__ == "__main__":\n    main()\n'

def g6640(r):
    n = r.randint(2, 20); vocabulary = [f"w{i}" for i in range(r.randint(5, 20))]
    docs = []
    for _ in range(n):
        words = r.sample(vocabulary, r.randint(1, min(8, len(vocabulary))))
        docs.append(f"{len(words)} " + " ".join(words))
    queries = r.sample(vocabulary + ["missing"], r.randint(3, min(10, len(vocabulary) + 1)))
    return f"{n}\n" + "\n".join(docs) + f"\n{len(queries)}\n" + "\n".join(queries) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g6640(random.Random(NUMBER + i + attempt * 1000))
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
