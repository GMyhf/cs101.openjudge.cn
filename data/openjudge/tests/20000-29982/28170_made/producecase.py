import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def dfs(x,y):\n    graph[x][y] = "-"\n    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:\n        if 0<=x+dx<10 and 0<=y+dy<10 and graph[x+dx][y+dy] == ".":\n            dfs(x+dx,y+dy)\ngraph = []\nresult = 0\nfor i in range(10):\n    graph.append(list(input()))\nfor i in range(10):\n    for j in range(10):\n        if graph[i][j] == ".":\n            result += 1\n            dfs(i,j)\nprint(result)\n'
SAMPLE_IN = '---.--.-..\n-..-.-....\n...--....-\n----......\n--.---....\n-.-..-.---\n....-.-..-\n-..-----..\n-.......-.\n.....--.--\n'
SAMPLE_OUT = '8\n'
def valid(text):
    """题面：10x10 字符棋盘，'-' 为空位，'.' 为己方落子；10 行各 10 个字符。"""
    if not text.endswith('\n') or '\r' in text:
        return False
    rows = text[:-1].split('\n')
    return len(rows) == 10 and all(len(row) == 10 and set(row) <= set('.-') for row in rows)

def generate_case(r, p=0.5):
    rows = ["".join('.' if r.random() < p else '-' for _ in range(10)) for _ in range(10)]
    return "\n".join(rows) + "\n"

def fixed_cases():
    g = lambda f: "\n".join("".join(f(i, j) for j in range(10)) for i in range(10)) + "\n"
    return [
        g(lambda i, j: '-'),                                   # 0 个鹰
        g(lambda i, j: '.'),                                   # 整盘一个鹰
        g(lambda i, j: '.' if (i + j) % 2 == 0 else '-'),      # 棋盘格：50 个孤子（斜向不连通）
        g(lambda i, j: '.' if i % 2 == 0 or (j == 9 if i % 4 == 1 else j == 0) else '-'),  # 蛇形长链：1 个
        g(lambda i, j: '.' if (i, j) in ((0, 0), (9, 9), (0, 9), (9, 0)) else '-'),        # 四角孤子
        g(lambda i, j: '.' if j % 2 == 0 else '-'),            # 5 条竖线
        g(lambda i, j: '-' if (i, j) == (4, 4) else '.'),      # 只有一个空位
    ]

def cases():
    out = [SAMPLE_IN] + fixed_cases()
    r = random.Random(28170)
    for p in [0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 0.5]:
        while True:
            c = generate_case(r, p)
            if c not in out: break
        out.append(c)
    assert len(out) == 20 and len(set(out)) == 20 and all(valid(c) for c in out)
    return out

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases()):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
