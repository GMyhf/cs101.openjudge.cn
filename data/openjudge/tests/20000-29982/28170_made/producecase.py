import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def dfs(x,y):\n    graph[x][y] = "-"\n    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:\n        if 0<=x+dx<10 and 0<=y+dy<10 and graph[x+dx][y+dy] == ".":\n            dfs(x+dx,y+dy)\ngraph = []\nresult = 0\nfor i in range(10):\n    graph.append(list(input()))\nfor i in range(10):\n    for j in range(10):\n        if graph[i][j] == ".":\n            result += 1\n            dfs(i,j)\nprint(result)\n'
SAMPLE_IN = '---.--.-..\n-..-.-....\n...--....-\n----......\n--.---....\n-.-..-.---\n....-.-..-\n-..-----..\n-.......-.\n.....--.--\n'
SAMPLE_OUT = '8\n'
def generate_case(r):
    rows = ["".join(r.choice(".-") for _ in range(10)) for _ in range(10)]
    assert all(len(row) == 10 and set(row) <= set(".-") for row in rows)
    return "\n".join(rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28170 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
