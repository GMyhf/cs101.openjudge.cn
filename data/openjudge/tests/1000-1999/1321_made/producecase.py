import random, subprocess, sys, tempfile
from pathlib import Path
def g1321(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(1, 8); k = r.randint(1, n)
        board = ["".join(r.choice("##.") for _ in range(n)) for _ in range(n)]
        blocks.append(f"{n} {k}\n" + "\n".join(board))
    return "\n".join(blocks) + "\n-1 -1\n"


def valid(text):
    """题面契约：多组，每组首行两个正整数 n k（n<=8，k<=n），随后 n 行、每行 n 个 # 或 . ；
    以 -1 -1 结束。“数据保证不出现多余的空白行或者空白列”按严格读法核：棋盘每行、每列至少一个 #。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    i, blocks = 0, 0
    while True:
        if i >= len(lines):
            return False
        head = lines[i].split(); i += 1
        if len(head) != 2:
            return False
        try:
            n, k = map(int, head)
        except ValueError:
            return False
        if (n, k) == (-1, -1):
            return i == len(lines) and blocks >= 1
        if not (1 <= n <= 8 and 1 <= k <= n):
            return False
        if i + n > len(lines):
            return False
        board = lines[i:i + n]; i += n
        if any(len(row) != n or set(row) - set("#.") for row in board):
            return False
        if any("#" not in row for row in board) or any(all(row[j] == "." for row in board) for j in range(n)):
            return False
        blocks += 1


def _board1321(r, n, dens):
    """随机棋盘，保证每行每列至少一个 #。"""
    while True:
        b = [["#" if r.random() < dens else "." for _ in range(n)] for _ in range(n)]
        for y in range(n):
            if "#" not in b[y]: b[y][r.randrange(n)] = "#"
        for x in range(n):
            if all(b[y][x] == "." for y in range(n)): b[r.randrange(n)][x] = "#"
        return ["".join(row) for row in b]


def _deficient1321(r, n):
    """每行每列都有 #，但最大匹配 < n：前 t 行的 # 只落在同一批 t-1 列里。"""
    t = r.randint(2, n - 1)
    cols = r.sample(range(n), t - 1)
    b = [["." for _ in range(n)] for _ in range(n)]
    for y in range(t):
        for x in cols:
            if r.random() < .7: b[y][x] = "#"
        if all(b[y][x] == "." for x in cols): b[y][r.choice(cols)] = "#"
    for y in range(t, n):
        for x in range(n):
            if r.random() < .5: b[y][x] = "#"
        if "#" not in b[y]: b[y][r.randrange(n)] = "#"
    for x in range(n):
        if all(b[y][x] == "." for y in range(n)): b[r.randrange(t, n)][x] = "#"
    rows = list(range(n)); r.shuffle(rows)
    return ["".join(b[y]) for y in rows]


def g1321_v2(r, seed):
    blocks = []
    def add(n, k, board): blocks.append(f"{n} {k}\n" + "\n".join(board))
    if seed == 1:          # 最小与边界：1x1、k=n 对角唯一解、全 # 的 k=1 / k=n
        add(1, 1, ["#"]); add(8, 8, ["".join("#" if x == y else "." for x in range(8)) for y in range(8)])
        add(8, 1, ["#" * 8] * 8); add(8, 8, ["#" * 8] * 8); add(2, 2, ["##", "#."])
    elif seed <= 3:        # 答案最大：全 # 棋盘逐个 k（8x8 时 k=6 达 564480）
        m = 8 if seed == 2 else 7
        for k in range(1, m + 1):
            add(m, k, ["#" * m] * m)
    elif seed <= 8:        # 答案为 0：k 超过最大匹配
        for _ in range(r.randint(2, 5)):
            n = r.randint(3, 8); add(n, n, _deficient1321(r, n))
    elif seed <= 30:       # 随机形状、随机 k
        for _ in range(r.randint(1, 6)):
            n = r.randint(1, 8); add(n, r.randint(1, n), _board1321(r, n, r.choice([.3, .5, .7, .9])))
    else:                  # 多组满规模（卡指数级暴力枚举格子子集）
        for _ in range(15):
            n = 8; add(n, r.randint(3, 6), _board1321(r, n, r.choice([.7, .85, 1.0])))
    return "\n".join(blocks) + "\n-1 -1\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1321: 棋盘问题\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01321/\n# License: not declared in source collection; no license is inferred.\ndef place_pieces(n, k, row, board, cols, count):\n    # 如果已经放置了k个棋子，计数加一\n    if k == 0:\n        count[0] += 1\n        return\n\n    # 从当前行row开始尝试\n    for i in range(row, n):\n        # 遍历该行所有列\n        for j in range(n):\n            # 如果当前位置是可放棋子的地方，并且没有放置在该列，且该行还没被用过\n            if board[i][j] == \'#\' and not cols[j]:\n                # 放置棋子，标记该行和该列\n                cols[j] = 1\n                place_pieces(n, k - 1, i + 1, board, cols, count)\n                # 回溯，撤销棋子的放置\n                cols[j] = 0\n\ndef main():\n    while True:\n        # 读取 n 和 k\n        n, k = map(int, input().split())\n        if n == -1 and k == -1:\n            break\n\n        # 读取棋盘形状\n        board = [input().strip() for _ in range(n)]\n\n        # 用来记录列的状态，0 表示该列没有放棋子，1 表示该列已放置棋子\n        cols = [0] * n\n        count = [0]  # 计数器，存储可行的方案数\n\n        place_pieces(n, k, 0, board, cols, count)\n\n        print(count[0])\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='2 1\n#.\n.#\n4 4\n...#\n..#.\n.#..\n#...\n-1 -1\n'
GENERATOR='g1321'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[g1321_v2(random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
