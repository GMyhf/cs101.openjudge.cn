"""4105 拯救公主 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计：
- 原数据全是无墙、无传送门的小空地图（R≤8、C≤9、K≤3、T=1），从未出现 oop!；
- 原内嵌参考解用普通 BFS 处理 0 代价的传送，队列失序，答案可能偏大
  （反例：1 / 6 5 2 / E1.#. / 01##0 / ..$01 / 00..# / 0$.S. / $1#.# 应为 6，原解给 7）；
  另外它把「集齐 K 种」理解成「集齐图上出现过的、编号 <K 的那几种」，
  K=1 而图上没有宝石 0 时也能救出公主（原第 1、20 组即如此，答案 9、10）。
现参考解改为分层 BFS（同层内做传送门 0 代价闭包），状态为（格子, 已得宝石集合），
目标为宝石集合 = (1<<K)-1；与堆优化 Dijkstra 对拍。生成的地图只放编号 <K 的宝石，
避免「K 种」是指 0..K-1 还是任意 K 种的歧义。
复核补充：题面「公主所在的地方被设下了结界」也可理解为宝石不齐时不能踏入 E。
原生成的随机图里有 13 组答案依赖「E 可中途经过」这一理解，现每张图生成后都用两种理解各解一次，
答案不同就重抽，使数据与这一歧义无关（main() 写盘前逐张再 assert 一遍）。
"""
import random
import subprocess
import sys
import tempfile
from pathlib import Path

SAMPLE_IN = '1\n7 8 2\n........\n..S..#0.\n.##..1..\n.0#.....\n...1#...\n...##E..\n...1....\n'
SAMPLE_OUT = '11\n'
REFERENCE = 'import sys\n\n\ndef solve(R, C, K, g):\n    cells = "".join(g)\n    n = R * C\n    full = (1 << K) - 1\n    gem = [0] * n\n    for i, ch in enumerate(cells):\n        if "0" <= ch <= "4" and int(ch) < K:\n            gem[i] = 1 << int(ch)\n    portals = [i for i, ch in enumerate(cells) if ch == "$"]\n    isp = [ch == "$" for ch in cells]\n    nb = []\n    for i in range(n):\n        r, c = divmod(i, C)\n        lst = []\n        if cells[i] != "#":\n            if r > 0 and cells[i - C] != "#": lst.append(i - C)\n            if r < R - 1 and cells[i + C] != "#": lst.append(i + C)\n            if c > 0 and cells[i - 1] != "#": lst.append(i - 1)\n            if c < C - 1 and cells[i + 1] != "#": lst.append(i + 1)\n        nb.append(lst)\n    s = cells.index("S"); e = cells.index("E")\n    target = (e << 5) | full\n    seen = bytearray(n << 5)\n    start = s << 5\n    seen[start] = 1\n    frontier = [start]\n    d = 0\n    while frontier:\n        k = 0\n        while k < len(frontier):  # 同层内传送门 0 代价闭包\n            st = frontier[k]; k += 1\n            if st == target:\n                return str(d)\n            cell = st >> 5\n            if isp[cell]:\n                m = st & 31\n                for p in portals:\n                    t = (p << 5) | m\n                    if not seen[t]:\n                        seen[t] = 1; frontier.append(t)\n        nxt = []\n        for st in frontier:\n            m = st & 31\n            for j in nb[st >> 5]:\n                t = (j << 5) | (m | gem[j])\n                if not seen[t]:\n                    seen[t] = 1; nxt.append(t)\n        frontier = nxt\n        d += 1\n    return "oop!"\n\n\ndef main():\n    a = sys.stdin.read().split()\n    t = int(a[0]); i = 1; out = []\n    for _ in range(t):\n        R, C, K = int(a[i]), int(a[i + 1]), int(a[i + 2]); i += 3\n        g = a[i:i + R]; i += R\n        out.append(solve(R, C, K, g))\n    print("\\n".join(out))\n\n\nmain()\n'


def valid(text):
    """题面契约：T（1..10）组；每组 R C K（2≤R,C≤200，K 为正整数且不超过 5 种），R 行各 C 个字符，
    字符取自 S E # $ . 0-4；S、E 恰各一个；$ 不超过 10 个。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or not lines[0].isdigit() or not 1 <= int(lines[0]) <= 10:
        return False
    pos = 1
    for _ in range(int(lines[0])):
        if pos >= len(lines):
            return False
        head = lines[pos].split(" "); pos += 1
        if len(head) != 3 or not all(x.isdigit() for x in head):
            return False
        R, C, K = map(int, head)
        if not (2 <= R <= 200 and 2 <= C <= 200 and 1 <= K <= 5) or pos + R > len(lines):
            return False
        rows = lines[pos:pos + R]; pos += R
        if any(len(x) != C or any(ch not in "SE#$.01234" for ch in x) for x in rows):
            return False
        allc = "".join(rows)
        if allc.count("S") != 1 or allc.count("E") != 1 or allc.count("$") > 10:
            return False
    return pos == len(lines)


def make_map(r, R, C, K, wall=0.25, portals=None, gems=None, maze=False):
    """随机地图：只放编号 <K 的宝石（每种至少一个）；maze=True 时先挖迷宫式长走廊，再按 wall 概率打通墙。"""
    if maze:
        cells = ["#"] * (R * C)
        stack = [(0, 0)]
        cells[0] = "."
        while stack:
            y, x = stack[-1]
            nbrs = [(y + dy, x + dx, y + dy // 2, x + dx // 2) for dy, dx in ((2, 0), (-2, 0), (0, 2), (0, -2))
                    if 0 <= y + dy < R and 0 <= x + dx < C and cells[(y + dy) * C + x + dx] == "#"]
            if not nbrs:
                stack.pop()
                continue
            ny, nx, my, mx = r.choice(nbrs)
            cells[my * C + mx] = "."
            cells[ny * C + nx] = "."
            stack.append((ny, nx))
        for i in range(R * C):
            if cells[i] == "#" and r.random() < wall * 0.3:
                cells[i] = "."
    else:
        cells = ["#" if r.random() < wall else "." for _ in range(R * C)]
    if portals is None:
        portals = r.randint(0, 10)
    if gems is None:
        gems = r.randint(K, max(K, min(3 * K, R * C // 4)))
    pick = r.sample(range(R * C), 2 + portals + gems)
    cells[pick[0]] = "S"
    cells[pick[1]] = "E"
    for p in pick[2:2 + portals]:
        cells[p] = "$"
    for j, p in enumerate(pick[2 + portals:]):
        cells[p] = str(j if j < K else r.randrange(K))
    return ["".join(cells[i * C:(i + 1) * C]) for i in range(R)]


_NS = {}
exec(REFERENCE.replace("\n\nmain()\n", "\n"), _NS)


def solve_e_blocked(R, C, K, g):
    """另一种理解：宝石不齐时不能踏入 E。分层 BFS，同层做传送门 0 代价闭包。"""
    cells = "".join(g)
    full = (1 << K) - 1
    s, e = cells.index("S"), cells.index("E")
    portals = [i for i, ch in enumerate(cells) if ch == "$"]
    start = (s, 0)
    seen = {start}
    frontier = [start]
    d = 0
    while frontier:
        k = 0
        while k < len(frontier):
            cell, m = frontier[k]; k += 1
            if cell == e:
                return str(d)
            if cells[cell] == "$":
                for p in portals:
                    if (p, m) not in seen:
                        seen.add((p, m)); frontier.append((p, m))
        nxt = []
        for cell, m in frontier:
            r, c = divmod(cell, C)
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                j = nr * C + nc
                ch = cells[j]
                if ch == "#":
                    continue
                mm = m | (1 << int(ch)) if ch.isdigit() and int(ch) < K else m
                if j == e and mm != full:
                    continue
                if (j, mm) not in seen:
                    seen.add((j, mm)); nxt.append((j, mm))
        frontier = nxt
        d += 1
    return "oop!"


def unambiguous(K, g):
    return _NS["solve"](len(g), len(g[0]), K, g) == solve_e_blocked(len(g), len(g[0]), K, g)


def make_map_safe(r, R, C, K, **kw):
    """make_map 的包装：答案与「E 能否中途经过」无关才收下。"""
    while True:
        g = make_map(r, R, C, K, **kw)
        if unambiguous(K, g):
            return g


def maps_of(content):
    a = content.split()
    i = 1
    for _ in range(int(a[0])):
        R, C, K = int(a[i]), int(a[i + 1]), int(a[i + 2]); i += 3
        yield K, a[i:i + R]
        i += R


def render(sets):
    out = [str(len(sets))]
    for K, g in sets:
        out.append(f"{len(g)} {len(g[0])} {K}")
        out += g
    return "\n".join(out) + "\n"


def handmade():
    cases = []
    # 1 最小地图与 oop!：2x2、被墙隔开、宝石被围住、K 种不全（K=1 却没有宝石 0）
    cases.append(render([(1, ["S0", ".E"]), (1, ["S#", "#E"]), (1, ["S.", "0E"]),
                         (2, ["S..#0", "...##", "1...E"]), (1, ["S...", "....", "...E"])]))
    # 2 传送门：原参考解给错答案的反例；隔墙两侧的传送门；只有 1 个传送门（不能传送）
    cases.append(render([(2, ["E1.#.", "01##0", "..$01", "00..#", "0$.S.", "$1#.#"]),
                         (1, ["S$#....", "..#....", "..#....", "..#..0$", "..#...E"]),
                         (1, ["S$#...", "..#.0E", "..####", "......"]),
                         (3, ["S.$#$.2", "...#...", "0..#..1", "...#..E"])]))
    # 3 宝石在 E 的另一侧、需绕开 E 去拿（E 能否中途经过两种理解答案一致）；传送门落点旁就是宝石
    cases.append(render([(1, ["S...0", ".###.", "..E.."]), (2, ["S.$....", "#######", "1..E..$", "0......"])]))
    return cases


def build_cases():
    r = random.Random(4105)
    cases = [SAMPLE_IN] + handmade()
    # 4-15 小地图，T=10，混合墙密度 / 传送门 / 宝石种类
    for i in range(4, 16):
        sets = []
        for _ in range(10):
            R, C, K = r.randint(2, 10), r.randint(2, 10), r.randint(1, 5)
            K = min(K, max(1, (R * C - 2) // 3))
            sets.append((K, make_map_safe(r, R, C, K, wall=r.choice([0.0, 0.2, 0.35, 0.5]),
                                     portals=r.randint(0, min(10, (R * C - 2 - K) // 3)),
                                     gems=r.randint(K, max(K, (R * C - 2) // 3)))))
        cases.append(render(sets))
    # 16-27 中等地图（20~80），T=3..10
    for i in range(16, 28):
        sets = []
        for _ in range(r.randint(3, 10)):
            R, C, K = r.randint(20, 80), r.randint(20, 80), r.randint(1, 5)
            sets.append((K, make_map_safe(r, R, C, K, wall=r.choice([0.1, 0.3, 0.45]), maze=r.random() < 0.4)))
        cases.append(render(sets))
    # 28-39 满尺寸 200x200：K=5 时状态 128 万个，Python 参考解每张约 0.7s，
    # 一组只放 2 张；K 小时多放几张（T 不超过 10）。
    for i in range(28, 40):
        K = [5, 5, 4, 3, 2, 1][(i - 28) % 6]
        T = {5: 2, 4: 3, 3: 5, 2: 8, 1: 10}[K]
        sets = []
        for j in range(T):
            R = 200 if j == 0 else r.randint(150, 200)
            C = 200 if j == 0 else r.randint(150, 200)
            sets.append((K, make_map_safe(r, R, C, K, wall=r.choice([0.2, 0.3, 0.4]), maze=(i + j) % 3 == 0,
                                     portals=r.choice([0, 2, 10]), gems=r.choice([K, 3 * K, 20]))))
        cases.append(render(sets))
    return cases


def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as fh:
        fh.write(REFERENCE)
        fh.flush()
        return subprocess.run([sys.executable, fh.name], input=content, text=True,
                              capture_output=True, timeout=120, check=True).stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN) == SAMPLE_OUT, "参考解跑不出样例输出"
    d = Path(__file__).parent / "data"
    d.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        assert all(unambiguous(K, g) for K, g in maps_of(c)), f"第 {i} 组答案依赖「E 能否中途经过」"
        (d / f"{i}.in").write_text(c)
        (d / f"{i}.out").write_text(solve_reference(c))


if __name__ == "__main__":
    main()
