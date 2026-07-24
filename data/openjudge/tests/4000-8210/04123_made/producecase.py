import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '1\n5 4 0 0\n'
SAMPLE_OUT = '32\n'
CASES = ['1\n5 4 0 0\n', '1\n4 3 1 2\n', '1\n5 4 1 0\n', '1\n4 4 3 2\n', '1\n5 4 4 3\n', '1\n4 3 0 1\n', '1\n3 3 1 1\n', '1\n4 4 0 1\n', '1\n1 2 0 1\n', '1\n3 3 2 0\n', '1\n3 3 2 1\n', '1\n3 3 1 1\n', '1\n3 3 2 2\n', '1\n4 4 0 1\n', '1\n5 4 0 2\n', '1\n4 3 1 0\n', '1\n1 2 0 0\n', '1\n1 2 0 1\n', '1\n2 3 0 1\n', '1\n1 2 0 1\n']
REFERENCE_SOURCE = 'maxn = 10;\nsx = [-2,-1,1,2, 2, 1,-1,-2] # 马的横向移动\nsy = [ 1, 2,2,1,-1,-2,-2,-1] # 马的纵向移动\n\nans = 0;\n \ndef Dfs(dep: int, x: int, y: int):\n    #是否已经全部走完\n    if n*m == dep:\n        global ans\n        ans += 1\n        return\n    \n    #对于每个可以走的点\n    for r in range(8):\n        s = x + sx[r]\n        t = y + sy[r]\n        if chess[s][t]==False and 0<=s<n and 0<=t<m :\n            chess[s][t]=True\n            Dfs(dep+1, s, t)\n            chess[s][t] = False; #回溯\n \n\nfor _ in range(int(input())):\n    n,m,x,y = map(int, input().split())\n    chess = [[False]*maxn for _ in range(maxn)]  #False表示没有走过\n    ans = 0\n    chess[x][y] = True\n    Dfs(1, x, y)\n    print(ans)\n'
assert CASES[0] == SAMPLE_IN
random.seed(4123)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
