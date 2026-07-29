import random, subprocess, sys, tempfile
from pathlib import Path
def g1321(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(1, 8); k = r.randint(1, n)
        board = ["".join(r.choice("##.") for _ in range(n)) for _ in range(n)]
        blocks.append(f"{n} {k}\n" + "\n".join(board))
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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
