"""19942 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 19942
SAMPLE_IN = '5 5 3 3\n3 3 2 1 0\n0 0 1 3 1\n3 1 2 2 3\n2 0 0 2 2\n2 0 0 0 1\n0 1 2\n2 2 0\n0 1 2\n'
SAMPLE_OUT = '12 12 17\n10 17 19\n9 6 14\n'
REFERENCE_SOURCE = "m,n,p,q = map(int, input().split())\nyuan=[[int(x) for x in input().split()] for _ in range(m)]\njuan=[[int(x) for x in input().split()] for _ in range(p)]\nanswer=[[None]*(n-q+1)  for _ in range(m-p+1)]\ndef j(x,y):\n    s=0\n    for i in range(p):\n        for j in range(q):\n            s += juan[i][j]*yuan[i+x][j+y]\n    return s\n\nfor a in range(m-p+1):\n    for b in  range(n-q+1):\n        answer[a][b] = str(j(a,b))\n        \nfor i in range(m-p+1):\n    print(' '.join(answer[i]))\n"

def g19942(r):
    m,n=r.randint(2,7),r.randint(2,7); p,q=r.randint(1,m),r.randint(1,n); rows=[" ".join(str(r.randint(-5,5)) for _ in range(n)) for _ in range(m)]; ker=[" ".join(str(r.randint(-5,5)) for _ in range(q)) for _ in range(p)]; return f"{m} {n} {p} {q}\n"+"\n".join(rows+ker)+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g19942(random.Random(NUMBER + i + attempt * 1000))
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
