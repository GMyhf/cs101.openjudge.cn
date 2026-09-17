#!/usr/bin/env python3
"""30193 哈密顿激活层 —— 生成器、输入契约、special judge 验证与数据构建。

2026-09-17 重写。旧版（T-028 phase-2 round 21 的多题共用生成器）因为「可行路径不唯一、
没法逐字比对」只产了不连通的无解实例：21 组全是 -1，`print(-1)` 全过。现在有了 checker，
判法是同目录的 `checker.py`（任一合法路径都对；参考答案 -1 时必须输出 -1）。
旧 `samplecode.py` 是平台上一份 AC 提交（未声明许可证），一并换成为本仓库写的参考解。
平台原数据 `../30193/`（5 组，8×8/7×9、K=8、全部有解，.out 是 spj 用的占位 `0`）只当外部事实读。

题面契约：`N M K B`（N、M ≤ 10），K 行 `r c t`，B 行 `r c`；含 t=1 的一行；1 ≤ t ≤ N×M−B；
障碍与关键神经元不重叠。题面没说 t 互不相同、关键格互不相同，这里生成的都互不相同，
障碍也互不相同（`valid()` 按这个更严的契约查）。

`SHAPES`（seed → 形状）按「这题会怎么错」排，★ 为无解（-1）：
  1 `single`         1×1，路径就是起点。
  2 `line`           1×M / N×1，起点在一端，唯一路径。
  3 `line_mid` ★     单行、起点在中间：两头都是死胡同。
  4 `open_free`      10×10、无障碍、只锁起点：路径极多，逐字比对必冤判。
  5 `open_few`       10×10、零星障碍、K=2..3。
  6 `platform_like`  8×8 / 7×9、B=2..3、K=8（仿平台原数据）。
  7 `dense_locks`    10×10、K=25..40：时间戳剪枝为主。
  8 `end_locked`     终点（t=总长）被锁定，K=4。
  9 `color_count` ★  9×9、起点在少数色：黑白格数对不上。
 10 `lock_parity` ★  有解实例把一个锁的 t 挪 ±1：锁定格颜色与 t 奇偶不符。
 11 `disconnected` ★ 障碍墙把网格切成两块（两块各自颜色平衡）。
 12 `dead_ends` ★    连通、颜色平衡，但有三个度数为 1 的格子。
 13 `thin`           2×M / 3×M / N×2，带锁。
 14 `tail_blob`      障碍是一整块（随机哈密顿路径的尾巴），K=5。
 15 `subtle_none` ★  锁挪 ±2 或同奇偶互换：静态检查（颜色、奇偶、曼哈顿、连通）全过，
                     只有搜索才能证明无解。「print(-1) 碰运气」与「只做静态检查」都在这挂。
 16 `scattered`      10×10、8..15 个散落障碍、K=6。
 17 `small_multi`    4×5 / 5×5、只锁起点，小而解多。
 18 `shifted_ok`     锁挪 ±2 后原路径失效、但仍有别的解：只会「输出生成时那条路径」的错解挂。
 19 `all_locked`     K = 总格数：每一步都锁定，路径被完全钉死。
 20 `subtle_none_big` ★ 同 15，但网格更大（8×8..10×10）。
有解的路径由随机哈密顿路径（backbite 随机游走）采样，锁定点取自该路径。
每个候选实例都要参考解在搜索结点上限内做完，且换两种同分候选次序也做完（`robust()`；
与平台「DFS+剪枝」提示同量级，不挑只对某一种搜索次序友好的实例）；
★ 组由 `static_reasons()`（颜色计数、锁的奇偶、曼哈顿、连通、死胡同，独立于参考解）
恰好给出设计的那一条无解证明；15/20 两组静态检查全过，改用 `_oracle_exists()`（与参考解独立：按 (当前格, 已访问集合) 记忆化的穷举 +
集合 BFS 连通性 + 曼哈顿时限）复核无解；有解组由 checker 验证参考路径。
第 0 组是题面样例，断言参考输出与题面样例输出（-1）相同。
"""
from __future__ import annotations

import importlib.util
import random
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

NUMBER = 30193
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = ("HAL 是一个 N × M 的神经元矩阵（最多10x10）。第一行包含四个整数 N, M, K, B ... "
                "输入保证包含起点信息（即存在一行满足 t=1）。1 ≤ t ≤ N × M − B。... 保证障碍物坐标与关键神经元坐标不重叠。")
SAMPLE = "3 3 2 1\n1 1 1\n3 3 8\n2 2\n"
SAMPLE_OUT = "-1\n"
SEARCH_BUDGET = 40_000          # 参考解 dfs 结点上限（约 2 秒）
ORACLE_BUDGET = 400_000
SHAPES = {1: "single", 2: "line", 3: "line_mid", 4: "open_free", 5: "open_few", 6: "platform_like",
          7: "dense_locks", 8: "end_locked", 9: "color_count", 10: "lock_parity", 11: "disconnected",
          12: "dead_ends", 13: "thin", 14: "tail_blob", 15: "subtle_none", 16: "scattered",
          17: "small_multi", 18: "shifted_ok", 19: "all_locked", 20: "subtle_none_big"}
NO_SOLUTION = {"line_mid", "color_count", "lock_parity", "disconnected", "dead_ends", "subtle_none", "subtle_none_big"}
STATIC_OK = {"subtle_none", "subtle_none_big"}
EXPECTED_REASON = {"line_mid": "dead_ends"}


def _load_reference():
    spec = importlib.util.spec_from_file_location("ref30193", REFERENCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REF = _load_reference()
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _neighbors(p, cells):
    for dr, dc in DIRS:
        q = (p[0] + dr, p[1] + dc)
        if q in cells:
            yield q


def backbite(r, cells, path, rounds):
    """在格子集合 cells 上从一条哈密顿路径出发做 backbite 随机游走，返回新路径。"""
    path = list(path)
    if len(path) <= 2:
        return path
    for _ in range(rounds):
        if r.random() < 0.5:
            path.reverse()
        end = path[-1]
        options = sorted(_neighbors(end, cells))
        x = options[r.randrange(len(options))]
        k = path.index(x)
        if k == len(path) - 2:
            continue
        path[k + 1:] = path[k + 1:][::-1]
    return path


def serpentine(n, m):
    return [(i, j if i % 2 == 0 else m - 1 - j) for i in range(n) for j in range(m)]


def random_full_path(r, n, m):
    cells = {(i, j) for i in range(n) for j in range(m)}
    return backbite(r, cells, serpentine(n, m), 30 * n * m)


def locks_from_path(r, path, k, extra=()):
    total = len(path)
    times = {1} | set(extra)
    pool = [t for t in range(2, total + 1) if t not in times]
    times |= set(r.sample(pool, min(max(0, k - len(times)), len(pool))))
    return [(path[t - 1], t) for t in sorted(times)]


def to_text(n, m, locks, blocked, shuffle_rng=None):
    locks = list(locks)
    if shuffle_rng is not None:
        shuffle_rng.shuffle(locks)
    lines = [f"{n} {m} {len(locks)} {len(blocked)}"]
    lines += [f"{p[0] + 1} {p[1] + 1} {t}" for p, t in locks]
    lines += [f"{b[0] + 1} {b[1] + 1}" for b in blocked]
    return "\n".join(lines) + "\n"


def parse(text):
    v = list(map(int, text.split()))
    n, m, k, b = v[:4]
    locks = [(v[4 + 3 * i] - 1, v[5 + 3 * i] - 1, v[6 + 3 * i]) for i in range(k)]
    p = 4 + 3 * k
    blocked = [(v[p + 2 * i] - 1, v[p + 2 * i + 1] - 1) for i in range(b)]
    return n, m, locks, blocked


def solve(text, budget=SEARCH_BUDGET, tiebreak=None):
    n, m, locks, blocked = parse(text)
    return REF.find_path(n, m, locks, {r * m + c for r, c in blocked}, budget, tiebreak)


# 同分候选的另外两种次序：逆序编号、按编号散列打乱。实例必须在三种次序下都能在
# SEARCH_BUDGET 内做完，免得挑出「恰好对参考解的次序友好」、换个次序就指数爆炸的实例。
TIEBREAKS = (lambda v: -v, lambda v: (v * 2654435761) % 1009)


def robust(text):
    """三种次序都在预算内给出同一个可行性结论时返回参考解的路径（或 None）；否则抛 REF.Budget。"""
    path = solve(text)
    for key in TIEBREAKS:
        if (solve(text, tiebreak=key) is None) != (path is None):
            raise SystemExit("不同搜索次序给出了不同的可行性结论")
    return path


def static_reasons(text):
    """只靠静态推理就能判无解的全部理由（空列表 = 静态检查全过）。每条都是无解的充分条件：
    color_count —— 路径黑白交替，起点色格数必须是 ceil(总数/2)；
    lock_parity —— 第 t 步的格子与起点同色当且仅当 t 奇；
    manhattan   —— 相邻两个锁之间曼哈顿距离不能超过时间差；
    disconnected —— 正常格不连通；
    dead_ends   —— 除起点外有两个以上度数 <= 1 的格子（它们都只能当终点）。"""
    n, m, locks, blocked = parse(text)
    cells = {(i, j) for i in range(n) for j in range(m)} - set(blocked)
    at = {t: (r, c) for r, c, t in locks}
    start = at[1]
    reasons = []
    color = lambda p: (p[0] + p[1]) & 1
    same = sum(1 for p in cells if color(p) == color(start))
    if same != (len(cells) + 1) // 2:
        reasons.append("color_count")
    if any((color(p) == color(start)) != (t % 2 == 1) for t, p in at.items()):
        reasons.append("lock_parity")
    times = sorted(at)
    if any(abs(at[a][0] - at[b][0]) + abs(at[a][1] - at[b][1]) > b - a for a, b in zip(times, times[1:])):
        reasons.append("manhattan")
    seen = {start}
    q = deque([start])
    while q:
        p = q.popleft()
        for x in _neighbors(p, cells):
            if x not in seen:
                seen.add(x); q.append(x)
    if len(seen) != len(cells):
        reasons.append("disconnected")
    deg1 = [p for p in cells if sum(1 for _ in _neighbors(p, cells)) <= 1 and p != start]
    if len(deg1) > 1:
        reasons.append("dead_ends")
    return reasons


class OracleBudget(Exception):
    pass


def _oracle_exists(text):
    """独立穷举：记忆化 (当前格, 已访问 frozenset) 的失败状态；集合 BFS 查连通；曼哈顿查锁定时限。"""
    n, m, locks, blocked = parse(text)
    cells = {(i, j) for i in range(n) for j in range(m)} - set(blocked)
    total = len(cells)
    at = {t: (r, c) for r, c, t in locks}
    when = {(r, c): t for r, c, t in locks}
    failed = set()
    count = [0]

    def go(cur, step, visited):
        if step == total:
            return True
        key = (cur, visited)
        if key in failed:
            return False
        count[0] += 1
        if count[0] > ORACLE_BUDGET:
            raise OracleBudget()
        for t, p in at.items():
            if t > step and (p in visited or abs(p[0] - cur[0]) + abs(p[1] - cur[1]) > t - step):
                failed.add(key)
                return False
        seen = {cur}
        q = deque([cur])
        while q:
            p = q.popleft()
            for x in _neighbors(p, cells):
                if x not in visited and x not in seen:
                    seen.add(x); q.append(x)
        if len(seen) != total - step + 1:
            failed.add(key)
            return False
        for x in sorted(_neighbors(cur, cells)):
            if x in visited or (x in when and when[x] != step + 1) or (step + 1 in at and at[step + 1] != x):
                continue
            if go(x, step + 1, visited | {x}):
                return True
        failed.add(key)
        return False

    sys.setrecursionlimit(10000)
    return go(at[1], 1, frozenset([at[1]]))


# ---------------------------------------------------------------- 形状

def _solvable_from(r, n, m, path, k, blocked, extra=()):
    return to_text(n, m, locks_from_path(r, path, k, extra), sorted(blocked), r)


def _path_on(r, n, m, blocked):
    """网格去掉 blocked 后的一条随机哈密顿路径（先让参考解找一条，再 backbite 打乱）。"""
    cells = {(i, j) for i in range(n) for j in range(m)} - set(blocked)
    start = sorted(cells)[r.randrange(len(cells))]
    text = to_text(n, m, [(start, 1)], sorted(blocked))
    try:
        found = solve(text)
    except REF.Budget:
        return None
    if found is None:
        return None
    path = [(x // m, x % m) for x in found]
    return backbite(r, cells, path, 30 * len(cells))


def candidate(r, shape):
    if shape == "single":
        return "1 1 1 0\n1 1 1\n"
    if shape == "line":
        n, m = (1, r.randint(5, 10)) if r.random() < 0.5 else (r.randint(5, 10), 1)
        path = serpentine(n, m)
        if r.random() < 0.5:
            path.reverse()
        return _solvable_from(r, n, m, path, r.randint(1, 4), [])
    if shape == "line_mid":
        m = r.randint(5, 10)
        start = (0, r.randint(1, m - 2))
        return to_text(1, m, [(start, 1)], [])
    if shape == "open_free":
        path = random_full_path(r, 10, 10)
        return _solvable_from(r, 10, 10, path, 1, [])
    if shape == "small_multi":
        n, m = r.choice([(4, 5), (5, 4), (5, 5)])
        path = random_full_path(r, n, m)
        return _solvable_from(r, n, m, path, 1, [])
    if shape == "thin":
        n, m = r.choice([(2, 10), (10, 2), (3, 10), (10, 3), (2, 7)])
        path = random_full_path(r, n, m)
        return _solvable_from(r, n, m, path, r.randint(2, 6), [])
    if shape == "tail_blob":
        n, m = 10, 10
        path = random_full_path(r, n, m)
        cut = r.randint(15, 30)
        blocked = path[len(path) - cut:]
        path = path[:len(path) - cut]
        if r.random() < 0.5:
            path.reverse()
        return _solvable_from(r, n, m, path, 5, blocked)
    if shape in ("open_few", "scattered", "platform_like", "dense_locks", "end_locked", "all_locked",
                 "lock_parity", "shifted_ok", "subtle_none", "subtle_none_big"):
        if shape in ("open_few", "dense_locks", "all_locked"):
            n, m, nb = 10, 10, r.randint(0, 4)
        elif shape == "scattered":
            n, m, nb = 10, 10, r.randint(8, 15)
        elif shape == "platform_like":
            (n, m), nb = r.choice([(8, 8), (7, 9), (9, 7)]), r.randint(2, 3)
        elif shape == "subtle_none":
            n, m, nb = r.randint(5, 7), r.randint(5, 7), r.randint(0, 4)
        elif shape == "subtle_none_big":
            n, m, nb = r.randint(8, 10), r.randint(8, 10), r.randint(0, 6)
        else:
            n, m, nb = r.randint(7, 10), r.randint(7, 10), r.randint(0, 6)
        all_cells = [(i, j) for i in range(n) for j in range(m)]
        blocked = sorted(r.sample(all_cells, nb))
        path = _path_on(r, n, m, blocked)
        if path is None:
            return None
        total = len(path)
        if shape == "open_few":
            return _solvable_from(r, n, m, path, r.randint(2, 3), blocked)
        if shape == "scattered":
            return _solvable_from(r, n, m, path, 6, blocked)
        if shape == "platform_like":
            return _solvable_from(r, n, m, path, 8, blocked)
        if shape == "dense_locks":
            return _solvable_from(r, n, m, path, r.randint(25, 40), blocked)
        if shape == "end_locked":
            return _solvable_from(r, n, m, path, 4, blocked, extra=(total,))
        if shape == "all_locked":
            return _solvable_from(r, n, m, path, total, blocked)
        locks = locks_from_path(r, path, r.randint(4, 10), ())
        if shape == "lock_parity":
            i = r.randrange(1, len(locks))
            p, t = locks[i]
            nt = t + r.choice((-1, 1))
            if not (2 <= nt <= total) or any(tt == nt for _, tt in locks):
                return None
            locks[i] = (p, nt)
        else:  # shifted_ok / subtle_none(_big)：挪 ±2 或同奇偶互换
            if r.random() < 0.5 or len(locks) < 3:
                i = r.randrange(1, len(locks))
                p, t = locks[i]
                nt = t + r.choice((-2, 2))
                if not (2 <= nt <= total) or any(tt == nt for _, tt in locks):
                    return None
                locks[i] = (p, nt)
            else:
                i, j = r.sample(range(1, len(locks)), 2)
                if (locks[i][1] - locks[j][1]) % 2:
                    return None
                locks[i], locks[j] = (locks[i][0], locks[j][1]), (locks[j][0], locks[i][1])
        return to_text(n, m, locks, blocked, r)
    if shape == "color_count":
        n = m = 9
        start = (r.randrange(9), r.randrange(9))
        if (start[0] + start[1]) % 2 == 0:
            start = (start[0], (start[1] + 1) % 9)
        return to_text(n, m, [(start, 1)], [])
    if shape == "disconnected":
        n, m = r.randint(5, 8), r.randint(5, 8)
        col = r.randint(2, m - 3)
        blocked = [(i, col) for i in range(n)]
        path = serpentine(n, col)            # 左半块的一条路径，锁取自它
        return _solvable_from(r, n, m, path, r.randint(1, 3), blocked)
    if shape == "dead_ends":
        n, m = r.randint(5, 8), r.randint(5, 8)
        # 堵住三个角各自的一个邻格，使角变成度数 1
        corners = r.sample([((0, 0), (0, 1)), ((0, m - 1), (1, m - 1)), ((n - 1, 0), (n - 2, 0)),
                            ((n - 1, m - 1), (n - 1, m - 2))], 3)
        blocked = sorted({b for _, b in corners})
        free = [(i, j) for i in range(n) for j in range(m) if (i, j) not in blocked and (i, j) not in {c for c, _ in corners}]
        start = free[r.randrange(len(free))]
        return to_text(n, m, [(start, 1)], blocked)
    raise KeyError(shape)


def generate(number, seed):
    assert number == NUMBER
    shape = SHAPES[seed]
    r = random.Random(number * 1_000_003 + seed)
    for _attempt in range(10_000):
        text = candidate(r, shape)
        if text is None or not valid(number, text):
            continue
        try:
            path = robust(text)
        except REF.Budget:
            continue
        reasons = static_reasons(text)
        if shape in NO_SOLUTION:
            if path is not None:
                continue
            if shape in STATIC_OK:
                # 静态检查全过的无解实例：必须由独立穷举复核
                if reasons:
                    continue
                try:
                    if _oracle_exists(text):
                        raise SystemExit(f"seed {seed}: 参考解判无解，独立穷举却找到了路径")
                except OracleBudget:
                    continue
            elif reasons != [EXPECTED_REASON.get(shape, shape)]:
                # 其余无解形状：static_reasons()（独立于参考解）恰好给出设计的那一条无解证明
                continue
        elif path is None:
            continue
        return text
    raise SystemExit(f"seed {seed}: 找不到合格的 {shape} 实例")


def valid(number, text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text.split("\n")[:-1]
    try:
        head = list(map(int, lines[0].split()))
    except (ValueError, IndexError):
        return False
    if len(head) != 4:
        return False
    n, m, k, b = head
    if not (1 <= n <= 10 and 1 <= m <= 10 and 1 <= k and 0 <= b < n * m) or len(lines) != 1 + k + b:
        return False
    total = n * m - b
    locks, obstacles = [], []
    for line in lines[1:1 + k]:
        v = line.split()
        if len(v) != 3 or not all(x.isdigit() for x in v):
            return False
        r, c, t = map(int, v)
        if not (1 <= r <= n and 1 <= c <= m and 1 <= t <= total):
            return False
        locks.append((r, c, t))
    for line in lines[1 + k:]:
        v = line.split()
        if len(v) != 2 or not all(x.isdigit() for x in v):
            return False
        r, c = map(int, v)
        if not (1 <= r <= n and 1 <= c <= m):
            return False
        obstacles.append((r, c))
    lock_cells = {(r, c) for r, c, _ in locks}
    return (any(t == 1 for *_, t in locks) and len({t for *_, t in locks}) == k and len(lock_cells) == k
            and len(set(obstacles)) == b and not (lock_cells & set(obstacles)))


def check(case, output, answer):
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            p = Path(tmp) / name
            p.write_text(data, encoding="utf-8")
            paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True, timeout=60)
    if res.returncode not in (0, 42):
        raise SystemExit(f"checker 出错（退出码 {res.returncode}）：{res.stdout}{res.stderr[-500:]}")
    return res.returncode == 0, res.stdout.strip()


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    outputs = []
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True)
        if index == 0 and result.stdout != SAMPLE_OUT:
            raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r}")
        shape = SHAPES.get(index)
        if shape is not None and (result.stdout == "-1\n") != (shape in NO_SOLUTION):
            raise SystemExit(f"case {index} ({shape}): 有解/无解与形状设计不符")
        ok, message = check(case, result.stdout, result.stdout)
        if not ok:
            raise SystemExit(f"case {index}: checker 不接受参考解输出：{message}")
        if result.stdout != "-1\n":
            ok, _ = check(case, "-1\n", result.stdout)
            if ok:
                raise SystemExit(f"case {index}: checker 接受了有解实例上的 -1")
        outputs.append(result.stdout)
    for path in out.glob("*"):
        path.unlink()
    for index, (case, answer) in enumerate(zip(cases, outputs)):
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    _build()
