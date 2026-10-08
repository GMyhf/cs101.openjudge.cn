"""6640 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 29 组数据（原 20 组 + 9 组追加）。

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

def valid(text):
    """题面：1<=N<=1000 篇文档，每行 c_i（1<=c_i<=100）后跟 c_i 个单词；1<=M<=1000 个查询，每行一个单词；
    单词全部由小写字母组成，长度不超过 256。"""
    try:
        lines = text.split("\n")
        if lines[-1] != "": return False
        lines = lines[:-1]
        def word_ok(w):
            return 1 <= len(w) <= 256 and all("a" <= ch <= "z" for ch in w)
        if lines[0] != str(int(lines[0])): return False
        n = int(lines[0])
        if not 1 <= n <= 1000: return False
        for ln in lines[1:n + 1]:
            t = ln.split(" ")
            if t[0] != str(int(t[0])): return False
            c = int(t[0])
            if not 1 <= c <= 100 or len(t) != c + 1: return False
            if not all(word_ok(w) for w in t[1:]): return False
        if lines[n + 1] != str(int(lines[n + 1])): return False
        m = int(lines[n + 1])
        if not 1 <= m <= 1000 or len(lines) != n + 2 + m: return False
        return all(word_ok(q) for q in lines[n + 2:])
    except Exception:
        return False

LOW = "abcdefghijklmnopqrstuvwxyz"
def rword(r, lo=1, hi=10):
    return "".join(r.choice(LOW) for _ in range(r.randint(lo, hi)))

def make(r, n, cmax, vocab, m, dup=0.0, miss=0.2, rare_q=False, long_words=0):
    voc = set()
    while len(voc) < vocab:
        voc.add(rword(r))
    voc = sorted(voc)
    for _ in range(long_words):
        voc.append(rword(r, 250, 256))
    docs = []
    for _ in range(n):
        c = r.randint(1, cmax)
        ws = [r.choice(voc) for _ in range(c)]
        if dup and r.random() < dup and c >= 2:
            ws[-1] = ws[0]  # 同一文档里重复出现的单词，只能输出一次文档号
        r.shuffle(ws)
        docs.append(f"{c} " + " ".join(ws))
    used = sorted({w for d in docs for w in d.split(" ")[1:]})
    qs = []
    for _ in range(m):
        if r.random() < miss:
            w = rword(r)
            while w in used: w = rword(r)
            qs.append(w)
        else:
            qs.append(r.choice(used))
    return f"{n}\n" + "\n".join(docs) + f"\n{m}\n" + "\n".join(qs) + "\n"

def g6640(r):
    n = r.randint(2, 20)
    return make(r, n, 8, r.randint(5, 20), r.randint(3, 10), dup=0.3)

EXTRA = [
    lambda r: "1\n1 a\n1\na\n",
    lambda r: "1\n3 zz zz zz\n3\nzz\nz\nzzz\n",
    lambda r: "2\n1 abc\n1 abd\n2\nab\nabcd\n",
    lambda r: make(r, 5, 4, 10, 6, miss=1.0),
    lambda r: make(r, 30, 10, 15, 20, dup=0.8, long_words=3),
    lambda r: make(r, 1000, 100, 20000, 1000, dup=0.2, miss=0.3),
    lambda r: make(r, 1000, 100, 60000, 1000, dup=0.3, miss=0.1, long_words=50),
    lambda r: make(r, 1000, 100, 300, 200, dup=0.5, miss=0.05),
    lambda r: make(r, 1000, 3, 50, 1000, dup=0.5, miss=0.2),
]

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
    for i, f in enumerate(EXTRA):
        cases.append(f(random.Random(NUMBER * 10 + i)))
    assert all(valid(c) for c in cases)
    assert len(set(cases)) == len(cases)
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
