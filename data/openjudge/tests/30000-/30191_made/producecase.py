import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "N,K=map(int,input().split())\ndef num(a):\n\t# 状态a中的国王数\n    return bin(a).count('1')\n# 存储所有单行合法的状态\nstate=[]\nfor a in range(1<<N):\n    if a&(a<<1):\n        continue\n    k=num(a)\n    if k>K:\n        continue\n    state.append(a)\nM=len(state)\n# 存储相邻两行合法的状态\nconflict=[[False]*M for _ in range(M)]\nfor i in range(M):\n    for j in range(M):\n        a=state[i]\n        b=state[j]\n        if a&b==0 and a&(b<<1)==0 and a&(b>>1)==0:\n            conflict[i][j]=True\ndp=[[0]*M for _ in range(K+1)]\nfor i in range(M):\n    a=state[i]\n    dp[num(a)][i]=1\nfor _ in range(N-1):\n    dp1=[[0]*M for _ in range(K+1)]\n    for i in range(M):\n        a=state[i]\n        k=num(a)\n        for m in range(K+1-k):\n            for j in range(M):\n                if conflict[i][j]:\n                    dp1[k+m][i]+=dp[m][j]\n    dp=dp1\nprint(sum(dp[-1]))\n"
SAMPLE_IN = '3 2\n'
def valid(text):
    # 题面：一行两个数 N K，1<=N<=9，0<=K<=N*N
    if not text.endswith('\n') or text.count('\n') != 1: return False
    t = text[:-1].split(' ')
    if len(t) != 2: return False
    try: n, k = int(t[0]), int(t[1])
    except ValueError: return False
    return 1 <= n <= 9 and 0 <= k <= n * n

def generate_case(r):
    n = r.randint(1, 5); k = r.randint(0, n * n)
    return f"{n} {k}\n"

def all_cases():
    # 原数据 N 只到 5；补上 N=1 最小、N=9 满规模（答案超 32 位）、K 超过最多可放 25 个国王时答案为 0 等
    pairs = [(1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (2, 4), (3, 0), (3, 4), (3, 5), (4, 4), (4, 5),
             (5, 9), (5, 10), (6, 5), (7, 8), (7, 16), (7, 17), (8, 10), (8, 16), (8, 17)]
    pairs += [(9, k) for k in range(27)] + [(9, 40), (9, 81)]
    return [SAMPLE_IN] + [f"{n} {k}\n" for n, k in pairs]

def main():
    cases = all_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
