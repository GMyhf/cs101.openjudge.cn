import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '3\n3 1 2 3\n1 2\n1 3\n3\n1 1 1\n1 -1 0\n1 -1 -1\n'
SAMPLE_OUT = 'NOT FOUND\n1 3\n1\n'
CASES = ['3\n3 1 2 3\n1 2\n1 3\n3\n1 1 1\n1 -1 0\n1 -1 -1\n', '3\n2 3 5\n0\n3 2 3 7\n7\n1 -1 1\n1 -1 1\n1 -1 0\n0 0 1\n0 0 -1\n1 0 1\n0 1 -1\n', '4\n4 4 5 8 9\n5 4 5 6 8 9\n4 3 4 5 6\n1 5\n3\n0 -1 -1 0\n1 0 1 0\n1 1 -1 1\n', '1\n3 1 3 4\n6\n1\n0\n-1\n0\n-1\n0\n', '2\n1 9\n3 2 8 9\n8\n-1 0\n-1 -1\n1 1\n-1 1\n1 0\n-1 -1\n0 -1\n1 1\n', '4\n0\n4 2 4 5 7\n3 2 3 8\n2 1 8\n3\n1 -1 1 1\n0 -1 0 0\n1 0 -1 -1\n', '4\n0\n2 4 7\n3 2 3 4\n3 1 3 6\n7\n-1 1 0 1\n0 1 0 0\n-1 -1 0 1\n-1 1 -1 -1\n-1 -1 -1 0\n0 0 -1 1\n0 1 0 0\n', '5\n4 3 5 6 9\n1 9\n3 1 6 9\n4 5 6 7 8\n4 3 4 6 7\n5\n1 0 -1 1 1\n1 1 0 -1 1\n1 -1 -1 0 0\n0 1 1 -1 1\n1 -1 0 -1 1\n', '5\n1 6\n0\n1 3\n1 6\n0\n3\n0 -1 0 -1 1\n0 1 1 -1 1\n-1 1 -1 0 0\n', '5\n2 5 9\n0\n0\n2 2 9\n5 2 4 6 7 9\n3\n-1 0 -1 1 1\n-1 0 -1 1 1\n-1 1 -1 0 -1\n', '4\n5 1 3 4 8 9\n2 6 7\n3 2 5 9\n3 2 3 9\n3\n-1 1 1 0\n0 1 -1 -1\n0 1 1 -1\n', '1\n4 2 3 4 6\n8\n1\n-1\n1\n1\n1\n0\n1\n0\n', '5\n1 6\n1 6\n0\n3 2 3 6\n4 2 3 5 9\n2\n1 -1 1 0 1\n1 1 0 0 1\n', '3\n0\n2 5 8\n5 1 3 4 6 7\n8\n0 0 0\n0 -1 0\n0 0 0\n-1 -1 1\n-1 1 -1\n0 1 0\n0 0 0\n-1 0 1\n', '3\n1 2\n2 1 8\n1 9\n1\n1 -1 1\n', '4\n2 2 4\n2 1 7\n5 2 3 4 5 8\n0\n1\n0 1 0 0\n', '3\n2 3 6\n4 1 3 5 6\n3 6 7 9\n3\n-1 0 1\n1 -1 -1\n0 1 -1\n', '4\n1 3\n3 3 4 6\n4 1 2 6 7\n3 4 5 6\n8\n0 -1 0 1\n-1 0 0 1\n-1 -1 -1 1\n1 0 0 0\n1 1 1 1\n1 1 0 -1\n1 0 -1 -1\n-1 -1 0 0\n', '5\n4 4 5 8 9\n0\n3 4 5 7\n2 2 9\n1 4\n8\n0 -1 1 0 0\n-1 -1 -1 -1 0\n1 -1 -1 1 1\n1 -1 1 1 -1\n-1 1 1 1 -1\n0 0 1 0 0\n1 0 -1 1 0\n-1 -1 0 0 1\n', '5\n0\n3 1 2 7\n0\n1 8\n4 1 2 6 7\n6\n-1 -1 0 1 0\n0 1 -1 1 1\n0 0 0 -1 1\n1 1 1 0 -1\n-1 1 1 -1 0\n-1 1 -1 -1 1\n']
REFERENCE_SOURCE = 'import sys\ninput = sys.stdin.read\ndata = input().split()\n\nindex = 0\nN = int(data[index])\nindex += 1\n\nword_documents = []\n\n# 读取每个词的倒排索引\nfor _ in range(N):\n    ci = int(data[index])\n    index += 1\n    documents = sorted(map(int, data[index:index + ci]))\n    index += ci\n    word_documents.append(documents)\n\nM = int(data[index])\nindex += 1\n\nresults = []\n\n# 处理每个查询\nfor _ in range(M):\n    query = list(map(int, data[index:index + N]))\n    index += N\n\n    # 集合存储各词的文档集合（使用交集获取所有词都出现的文档）\n    included_docs = []\n    excluded_docs = set()\n\n    # 解析查询条件\n    for i in range(N):\n        if query[i] == 1:\n            included_docs.append(word_documents[i])\n        elif query[i] == -1:\n            excluded_docs.update(word_documents[i])\n\n    # 仅在有包含词时计算交集\n    if included_docs:\n        result_set = set(included_docs[0])\n        for docs in included_docs[1:]:\n            result_set.intersection_update(docs)\n        result_set.difference_update(excluded_docs)\n        final_docs = sorted(result_set)\n        results.append(" ".join(map(str, final_docs)) if final_docs else "NOT FOUND")\n    else:\n        results.append("NOT FOUND")\n\n# 输出所有查询结果\nfor result in results:\n    print(result)\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4093)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
