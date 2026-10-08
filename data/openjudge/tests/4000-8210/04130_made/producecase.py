"""4130 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4130
SAMPLE_IN = '3 1\nK.S\n##1\n1#T\n3 1\nK#T\n.S#\n1#.\n3 2\nK#T\n.S.\n21.\n0 0\n'
SAMPLE_OUT = '5\nimpossible\n8\n'
REFERENCE_SOURCE = 'import sys\nimport heapq\nfrom collections import deque\n\ndef solve():\n    data = sys.stdin.read().splitlines()\n    if not data:\n        return\n    line_index = 0\n    # 四个方向：上、下、左、右\n    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]\n    results = []\n    \n    while line_index < len(data):\n        if not data[line_index].strip():\n            line_index += 1\n            continue\n        parts = data[line_index].split()\n        line_index += 1\n        n = int(parts[0])\n        m = int(parts[1])\n        if n == 0 and m == 0:\n            break\n        \n        # 读入迷宫\n        g = []\n        xs = ys = xe = ye = None\n        snake_index = {}\n        snake_count = 0\n        for i in range(n):\n            row = list(data[line_index].strip())\n            line_index += 1\n            for j, ch in enumerate(row):\n                if ch == \'K\':\n                    xs, ys = i, j\n                elif ch == \'T\':\n                    xe, ye = i, j\n                elif ch == \'S\':\n                    snake_index[(i, j)] = snake_count\n                    snake_count += 1\n            g.append(row)\n        \n        # 预处理：BFS 判断目标和所有钥匙是否可达（忽略杀蛇额外时间）\n        reachable = [[False]*n for _ in range(n)]\n        # flag[0] 表示唐僧所在房间可达，flag[1..m] 表示钥匙1..m可达\n        flag = [False]*(m+1)\n        q = deque([(xs, ys)])\n        reachable[xs][ys] = True\n        while q:\n            x0, y0 = q.popleft()\n            for dx, dy in directions:\n                x1, y1 = x0 + dx, y0 + dy\n                if not (0 <= x1 < n and 0 <= y1 < n):\n                    continue\n                if g[x1][y1] == \'#\':\n                    continue\n                if not reachable[x1][y1]:\n                    reachable[x1][y1] = True\n                    q.append((x1, y1))\n                    if g[x1][y1].isdigit():\n                        key_val = int(g[x1][y1])\n                        if 1 <= key_val <= m:\n                            flag[key_val] = True\n                    elif x1 == xe and y1 == ye:\n                        flag[0] = True\n        # 如果目标房间或任一必须钥匙不可达，直接输出 "impossible"\n        if not (flag[0] and all(flag[1:])):\n            results.append("impossible")\n            continue\n        \n        # 若预处理通过，则利用 Dijkstra 求最短时间\n        # 状态编码：将 (已取钥匙数, 蛇杀记) 合并为一个整数\n        def encode(keys, smask):\n            return keys * (1 << snake_count) + smask\n        \n        # 在每个格子上用字典记录状态编码对应的最短耗时，降低内存占用\n        visited = [[{} for _ in range(n)] for _ in range(n)]\n        init_state = encode(0, 0)\n        visited[xs][ys][init_state] = 0\n        heap = [(0, xs, ys, 0, 0)]  # (耗时, x, y, keys, snake_mask)\n        ans = -1\n        while heap:\n            t, x, y, keys, smask = heapq.heappop(heap)\n            state_code = encode(keys, smask)\n            if visited[x][y].get(state_code, float(\'inf\')) < t:\n                continue\n            if x == xe and y == ye and keys == m:\n                ans = t\n                break\n            for dx, dy in directions:\n                nx, ny = x + dx, y + dy\n                if not (0 <= nx < n and 0 <= ny < n):\n                    continue\n                if g[nx][ny] == \'#\':\n                    continue\n                nkeys = keys\n                nsmask = smask\n                nt = t + 1  # 每走一步耗时1分钟\n                cell = g[nx][ny]\n                # 若该房间有蛇且尚未杀死，则需额外1分钟，并更新蛇状态\n                if cell == \'S\':\n                    idx = snake_index[(nx, ny)]\n                    if not (smask & (1 << idx)):\n                        nt += 1\n                        nsmask = smask | (1 << idx)\n                # 若该房间有钥匙且正是下一个需要的钥匙，则拾取钥匙\n                if cell.isdigit():\n                    k = int(cell)\n                    if keys < m and k == keys + 1:\n                        nkeys = keys + 1\n                new_state = encode(nkeys, nsmask)\n                if new_state not in visited[nx][ny] or nt < visited[nx][ny][new_state]:\n                    visited[nx][ny][new_state] = nt\n                    heapq.heappush(heap, (nt, nx, ny, nkeys, nsmask))\n        results.append("impossible" if ans == -1 else str(ans))\n    \n    sys.stdout.write("\\n".join(results))\n    \nif __name__ == \'__main__\':\n    solve()\n'

# 题面约束：多组数据，每组首行 N M（0 < N <= 100，0 <= M <= 9），接着 N 行、每行 N 个字符，
# 取自 K T S . # 与数字 1-9；恰有一个 K、一个 T，蛇 S 至多 5 条；以 "0 0" 结束。
def valid(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    i = 0
    while True:
        if i >= len(lines):
            return False
        h = lines[i].split()
        if len(h) != 2 or " ".join(h) != lines[i] or not all(x.isdigit() and x == str(int(x)) for x in h):
            return False
        n, m = map(int, h)
        i += 1
        if n == 0 and m == 0:
            return i == len(lines)
        if not (0 < n <= 100 and 0 <= m <= 9) or i + n > len(lines):
            return False
        g = lines[i:i + n]
        if any(len(row) != n or set(row) - set("KTS.#123456789") for row in g):
            return False
        allc = "".join(g)
        if allc.count("K") != 1 or allc.count("T") != 1 or allc.count("S") > 5:
            return False
        i += n


def palace(r, n, m, snakes, wall, keys_per_kind=2, extra_digits=False, far=False):
    g = [["#" if r.random() < wall else "." for _ in range(n)] for _ in range(n)]
    free = [(a, b) for a in range(n) for b in range(n)]
    r.shuffle(free)
    def put(ch):
        if free:                                     # 格子用完就不再放（只会少放重复的钥匙）
            a, b = free.pop()
            g[a][b] = ch
    if far:
        g[0][0] = "K"; g[n - 1][n - 1] = "T"
        free.remove((0, 0)); free.remove((n - 1, n - 1))
    else:
        put("K"); put("T")
    for _ in range(snakes):
        put("S")
    for k in range(1, m + 1):
        put(str(k))
    for k in range(1, m + 1):
        for _ in range(r.randint(0, keys_per_kind - 1)):
            put(str(k))
    if extra_digits and m < 9:                       # 题目不需要的钥匙种类，只是普通房间
        for _ in range(r.randint(1, 3)):
            put(str(r.randint(m + 1, 9)))
    return f"{n} {m}\n" + "\n".join("".join(row) for row in g)


def corridor(n, m):
    """蛇形走廊：钥匙按 m..1 逆序放在通向 T 的路上，必须走到底再折返；走廊上有 5 条蛇。"""
    g = [["#"] * n for _ in range(n)]
    path = []
    for i in range(0, n, 2):
        cols = range(n) if (i // 2) % 2 == 0 else range(n - 1, -1, -1)
        for j in cols:
            g[i][j] = "."; path.append((i, j))
        if i + 1 < n:
            j = n - 1 if (i // 2) % 2 == 0 else 0
            g[i + 1][j] = "."; path.append((i + 1, j))
    a, b = path[0]; g[a][b] = "K"
    a, b = path[len(path) // 3]; g[a][b] = "T"
    for t, k in enumerate(range(m, 0, -1)):
        a, b = path[len(path) // 2 + t * (len(path) // 2 - 1) // max(m, 1)]
        g[a][b] = str(k)
    for t in range(5):
        a, b = path[1 + t * (len(path) // 6)]
        if g[a][b] == ".":
            g[a][b] = "S"
    return f"{n} {m}\n" + "\n".join("".join(row) for row in g)


SMALL = [
    "2 0\nKT\n..",                     # M=0，一步
    "2 0\nK#\n#T",                     # 到不了
    "3 0\nKST\n...\n...",              # 杀蛇 3 分钟，绕路 4 分钟
    "3 0\nKST\n###\n...",              # 必须杀蛇
    "3 1\nK.T\n###\n...",              # 缺钥匙 1
    "3 2\nK2T\n.#.\n.1.",              # 先 1 后 2：走过 2 不算
    "3 1\nKT1\n...\n...",              # 先路过 T 拿钥匙再回来
    "4 2\nK.S1\n.###\n...2\nT...",
    "3 3\nK13\n2#S\n.ST",
    "5 1\nKSSSS\n.####\n.#1..\n.#.#.\nS..#T",   # 来回走同一条蛇道，只杀一次
    "4 1\nK..T\n.##.\n.##.\n1SS.",
    "3 2\nK31\n.#2\n9.T",              # 题目不需要的 3、9 号钥匙
]


def build_cases():
    r = random.Random(NUMBER)
    fin = lambda parts: "\n".join(parts) + "\n0 0\n"
    cases = [SAMPLE_IN, fin(SMALL)]
    cases.append(fin([palace(r, 100, 0, 0, 0.0, far=True), palace(r, 100, 0, 5, 0.3, far=True)]))
    cases.append(fin([palace(r, 100, 9, 0, 0.15, 3)]))
    # 本题 limits.json 无记录，判题按单组 4s 兜底；参考解（每格一个 dict 的 Dijkstra）在 100x100、M=9、
    # 3~4 条蛇时要 1.8s~3.3s，超过时限一半。满规模 M=9 只配 1~2 条蛇，5 条蛇的放到 45x45。
    cases.append(fin([palace(r, 100, 9, 2, 0.15)]))
    cases.append(fin([palace(r, 45, 9, 5, 0.15)]))
    cases.append(fin([palace(r, 100, 9, 1, 0.25, 1)]))
    cases.append(fin([corridor(100, 9)]))
    cases.append(fin([palace(r, 100, 9, 5, 0.65), palace(r, 100, 9, 5, 0.7), palace(r, 100, 0, 5, 0.6)]))  # 多半 impossible
    cases.append(fin([corridor(n, m) for n, m in ((5, 1), (9, 3), (21, 9), (40, 5))]))
    while len(cases) < 20:
        parts = []
        for _ in range(r.randint(1, 12)):
            n = r.choice([r.randint(2, 6), r.randint(2, 15), r.randint(10, 40)])
            m = r.randint(0, min(9, n * n - 2))
            sn = r.randint(0, min(5, n * n - 2 - m))
            parts.append(palace(r, n, m, sn, r.choice([0.0, 0.15, 0.3, 0.45]), r.randint(1, 3), r.random() < 0.3))
        cases.append(fin(parts))
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
