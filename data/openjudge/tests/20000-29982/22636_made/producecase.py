import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 23n2300011075(才疏学浅)\ndef dfs(i,j):\n    if dp[i][j]>0:\n        return dp[i][j]\n    else:\n        for k in range(4):\n            if 0<=i+d[k][0]<r and 0<=j+d[k][1]<c and maze[i][j]>maze[i+d[k][0]][j+d[k][1]]:\n                dp[i][j]=max(dp[i][j],dfs(i+d[k][0],j+d[k][1])+1)\n    return dp[i][j]\n\nr,c=map(int,input().split())\nmaze=[]\nfor i in range(r):\n    l=list(map(int,input().split()))\n    maze.append(l)\ndp=[[0]*c for _ in range(r)]\nd=[[-1,0],[1,0],[0,1],[0,-1]]\nans=0\nfor i in range(r):\n    for j in range(c):\n        ans=max(ans,dfs(i,j))\nprint(ans+1)\n'
SAMPLE_IN = '5 5\n1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n'
SAMPLE_OUT = '25\n'
def generate_case(r):
    m, n = r.randint(2, 10), r.randint(2, 10); return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0, 100000000)) for _ in range(n)) for _ in range(m)) + "\n"

assert SAMPLE_IN == '5 5\n1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22636 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
