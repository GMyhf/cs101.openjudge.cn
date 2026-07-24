import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '4 4 1\n#@##\n**##\n###+\n****\n'
SAMPLE_OUT = '6\n'
CASES = ['4 4 1\n#@##\n**##\n###+\n****\n', '5 5 0\n@****\n*#***\n*****\n*#***\n****+\n', '10 9 3\n@*#******\n***####**\n***#*#*##\n**##*****\n*********\n**#*#****\n*#**#**#*\n****#*#*#\n*****#***\n********+\n', '9 10 5\n@*#*******\n**********\n*#*#*##***\n****#*****\n*###***#**\n*********#\n**********\n******#*#*\n*********+\n', '4 6 4\n@*****\n***#**\n*****#\n*****+\n', '5 6 9\n@*#***\n**#*#*\n******\n*#****\n*****+\n', '9 5 1\n@****\n*****\n***#*\n*#***\n*****\n*****\n*****\n*#***\n****+\n', '4 8 5\n@*******\n**#*#***\n***##***\n*******+\n', '10 4 9\n@***\n*#**\n****\n***#\n**#*\n****\n****\n****\n****\n***+\n', '8 5 7\n@****\n**#**\n**#**\n****#\n*****\n****#\n***#*\n****+\n', '10 5 9\n@#*#*\n*****\n***#*\n*****\n*****\n*****\n**#*#\n*****\n*****\n****+\n', '9 7 5\n@*#**#*\n*#*#***\n*#**#**\n***###*\n******#\n*******\n*##*#**\n******#\n******+\n', '10 8 7\n@*****#*\n********\n***##**#\n*#******\n********\n**#*****\n****#***\n******#*\n*##****#\n*******+\n', '8 9 8\n@********\n****#****\n*******#*\n*********\n*****##**\n*******#*\n**##**#**\n********+\n', '6 6 6\n@**#*#\n***##*\n**#***\n**#***\n*##*##\n*****+\n', '9 4 3\n@***\n****\n*#**\n****\n***#\n****\n**#*\n**#*\n***+\n', '4 4 4\n@#**\n**#*\n****\n***+\n', '6 8 3\n@*#**#*#\n********\n***#****\n**#**#**\n*****#**\n*******+\n', '6 9 7\n@###***##\n*#******#\n****##**#\n*********\n*****##**\n********+\n', '6 7 5\n@**#*#*\n**##***\n***#***\n*******\n*******\n******+\n']
REFERENCE_SOURCE = "# 夏天明 元培学院\n\nfrom collections import deque\n\nM, N, T = map(int, input().split())\ngraph = [list(input()) for i in range(M)]\ndirec = [(0,1), (1,0), (-1,0), (0,-1)]\nstart, end = None, None\nfor i in range(M):\n    for j in range(N):\n        if graph[i][j] == '@':\n            start = (i, j)\ndef bfs():\n    q = deque([start + (T, 0)])\n    visited = [[-1]*N for i in range(M)]\n    visited[start[0]][start[1]] = T\n    while q:\n        x, y, t, time = q.popleft()\n        time += 1\n        for dx, dy in direc:\n            if 0<=x+dx<M and 0<=y+dy<N:\n                if (elem := graph[x+dx][y+dy]) == '*' and t > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t\n                    q.append((x+dx, y+dy, t, time))\n                elif elem == '#' and t > 0 and t-1 > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t-1\n                    q.append((x+dx, y+dy, t-1, time))\n                elif elem == '+':\n                    return time\n    return -1\nprint(bfs())\n"
assert CASES[0] == SAMPLE_IN
random.seed(4115)
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
