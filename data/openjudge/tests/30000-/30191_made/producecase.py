import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "N,K=map(int,input().split())\ndef num(a):\n\t# 状态a中的国王数\n    return bin(a).count('1')\n# 存储所有单行合法的状态\nstate=[]\nfor a in range(1<<N):\n    if a&(a<<1):\n        continue\n    k=num(a)\n    if k>K:\n        continue\n    state.append(a)\nM=len(state)\n# 存储相邻两行合法的状态\nconflict=[[False]*M for _ in range(M)]\nfor i in range(M):\n    for j in range(M):\n        a=state[i]\n        b=state[j]\n        if a&b==0 and a&(b<<1)==0 and a&(b>>1)==0:\n            conflict[i][j]=True\ndp=[[0]*M for _ in range(K+1)]\nfor i in range(M):\n    a=state[i]\n    dp[num(a)][i]=1\nfor _ in range(N-1):\n    dp1=[[0]*M for _ in range(K+1)]\n    for i in range(M):\n        a=state[i]\n        k=num(a)\n        for m in range(K+1-k):\n            for j in range(M):\n                if conflict[i][j]:\n                    dp1[k+m][i]+=dp[m][j]\n    dp=dp1\nprint(sum(dp[-1]))\n"
SAMPLE_IN = '3 2\n'
def generate_case(r):
    n = r.randint(1, 5); k = r.randint(0, n * n)
    return f"{n} {k}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30191 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
