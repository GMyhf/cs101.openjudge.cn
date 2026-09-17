"""01729 Jack checker：题面「If several pairs of routes are possible, any one will do.」

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误、3 = 参考答案自身有问题。

每组要求学生输出三个 token：距离、Jack 路线、Jill 路线（空行不计，按空白切分）。
路线模型（与 samplecode.py 一致）：
  · 第 0 分钟 Jack 在 H、Jill 在 h；之后每分钟按路线走一步（N 上、S 下、W 左、E 右）。
  · 不能出界、不能进 '*'；Jack 不能进 h、s；Jill 不能进 H、S。
  · 路线在到达自己学校的那一步结束：中途经过自己学校、或走完没到学校都判错；路线不能为空。
  · 先到校的人停在学校，距离继续按学校位置算，直到两人都到校。
  · 最近距离 = 所有整分钟时刻 (0 .. max(两条路线长度)) 两人欧氏距离的最小值。
判定：这对路线的最近距离（保留两位小数）必须等于参考答案第一行（最优值），
且学生第一行打印的距离与之逐字相同（两位小数，如 6.71）。
不同整数 d² ≤ 2·29² 的 √d² 两两相差 > 0.01，两位小数不会把两个不同的距离写成同一个串。
"""
import sys
from math import sqrt

WA = 42
MAX_BYTES = 32 * 1024 * 1024


def reject(message):
    print(message)
    sys.exit(WA)


def broken(message):
    print("判题数据有误")
    sys.stderr.write(message + "\n")
    sys.exit(3)


def read_cases(path):
    tokens = open(path, encoding="utf-8").read().split()
    cases, p = [], 0
    while True:
        n = int(tokens[p]); p += 1
        if n == 0:
            return cases
        cases.append((n, tokens[p:p + n])); p += n


STEP = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}


def walk(k, who, n, grid, route, start, goal, forbidden):
    if not route:
        reject(f"第 {k} 组：{who} 的路线为空")
    r, c = start
    path = [start]
    last = len(route) - 1
    for i, ch in enumerate(route):
        d = STEP.get(ch)
        if d is None:
            reject(f"第 {k} 组：{who} 的路线只能由 N/S/E/W 组成")
        r += d[0]; c += d[1]
        if not (0 <= r < n and 0 <= c < n):
            reject(f"第 {k} 组：{who} 走出了地图")
        cell = grid[r][c]
        if cell == "*" or cell in forbidden:
            reject(f"第 {k} 组：{who} 走进了不能通行的格子")
        if (r, c) == goal and i != last:
            reject(f"第 {k} 组：{who} 到校后路线还没结束")
        path.append((r, c))
    if (r, c) != goal:
        reject(f"第 {k} 组：{who} 走完路线没有到达学校")
    return path


def main():
    cases = read_cases(sys.argv[1])
    answer = open(sys.argv[3], encoding="utf-8").read().split()
    if len(answer) != 3 * len(cases):
        broken("参考答案 token 数与组数不符")
    with open(sys.argv[2], "rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        reject("输出过长")
    got = raw.decode("utf-8", errors="replace").split()
    if len(got) < 3 * len(cases):
        reject("输出不完整：每组应当有距离、Jack 路线、Jill 路线三行")
    if len(got) > 3 * len(cases):
        reject("输出有多余的内容")
    for index, (n, grid) in enumerate(cases):
        k = index + 1
        best = answer[3 * index]
        printed, jack, jill = got[3 * index:3 * index + 3]
        where = {}
        for r in range(n):
            for c in range(n):
                where[grid[r][c]] = (r, c)
        jack_path = walk(k, "Jack", n, grid, jack, where["H"], where["S"], "hs")
        jill_path = walk(k, "Jill", n, grid, jill, where["h"], where["s"], "HS")
        steps = max(len(jack_path), len(jill_path))
        closest = None
        for t in range(steps):
            a = jack_path[min(t, len(jack_path) - 1)]
            b = jill_path[min(t, len(jill_path) - 1)]
            d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            if closest is None or d2 < closest:
                closest = d2
        achieved = "%.2f" % sqrt(closest)
        if achieved != best:
            if sqrt(closest) < float(best):
                reject(f"第 {k} 组：这对路线两人最近距离不是最大可能值")
            broken(f"第 {k} 组：学生路线最近距离 {achieved} 超过参考最优值 {best}")
        if printed != achieved:
            reject(f"第 {k} 组：第一行的距离与给出路线的实际最近距离（保留两位小数）不符")
    sys.exit(0)


main()
