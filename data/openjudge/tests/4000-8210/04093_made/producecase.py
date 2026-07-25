"""4093 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4093
SAMPLE_IN = '3\n3 1 2 3\n1 2\n1 3\n3\n1 1 1\n1 -1 0\n1 -1 -1\n'
SAMPLE_OUT = 'NOT FOUND\n1 3\n1\n'
REFERENCE_SOURCE = 'import sys\ninput = sys.stdin.read\ndata = input().split()\n\nindex = 0\nN = int(data[index])\nindex += 1\n\nword_documents = []\n\n# 读取每个词的倒排索引\nfor _ in range(N):\n    ci = int(data[index])\n    index += 1\n    documents = sorted(map(int, data[index:index + ci]))\n    index += ci\n    word_documents.append(documents)\n\nM = int(data[index])\nindex += 1\n\nresults = []\n\n# 处理每个查询\nfor _ in range(M):\n    query = list(map(int, data[index:index + N]))\n    index += N\n\n    # 集合存储各词的文档集合（使用交集获取所有词都出现的文档）\n    included_docs = []\n    excluded_docs = set()\n\n    # 解析查询条件\n    for i in range(N):\n        if query[i] == 1:\n            included_docs.append(word_documents[i])\n        elif query[i] == -1:\n            excluded_docs.update(word_documents[i])\n\n    # 仅在有包含词时计算交集\n    if included_docs:\n        result_set = set(included_docs[0])\n        for docs in included_docs[1:]:\n            result_set.intersection_update(docs)\n        result_set.difference_update(excluded_docs)\n        final_docs = sorted(result_set)\n        results.append(" ".join(map(str, final_docs)) if final_docs else "NOT FOUND")\n    else:\n        results.append("NOT FOUND")\n\n# 输出所有查询结果\nfor result in results:\n    print(result)\n'

def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"

def g4093(r):
    n = r.randint(1, 5); m = r.randint(1, 8); lines = [str(n)]
    for _ in range(n):
        docs = sorted(r.sample(range(1, 10), r.randint(0, 5)))
        lines.append(" ".join([str(len(docs))] + list(map(str, docs))))
    lines.append(str(m))
    for _ in range(m): lines.append(" ".join(str(r.choice([-1, 0, 1])) for _ in range(n)))
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4093(random.Random(NUMBER + i)) for i in range(1, 20)]

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
