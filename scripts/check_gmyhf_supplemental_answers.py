#!/usr/bin/env python3
"""独立复核四题答案及数织唯一解；只读已入库数据，不修改答案或索引。"""
from __future__ import annotations

import hashlib
import itertools
import json
from bisect import bisect_left, bisect_right
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def simple_orthogonal(points):
    """扫描线排除正交多边形的重叠边、非相邻接触和自相交，O(n log n)。"""
    n = len(points)
    groups = defaultdict(list)
    events = []
    ys = set()
    directions = []
    for i, ((x, y), (xx, yy)) in enumerate(zip(points, points[1:] + points[:1])):
        horizontal = y == yy
        directions.append(horizontal)
        lo, hi = sorted((x, xx) if horizontal else (y, yy))
        groups[horizontal, y if horizontal else x].append((lo, hi, i))
        if horizontal:
            ys.add(y)
            events.extend(((lo, 0, y, y), (hi, 2, y, y)))
        else:
            events.append((x, 1, lo, hi))
    for segments in groups.values():
        segments.sort()
        for (_, end, i), (start, _, j) in zip(segments, segments[1:]):
            if start < end or (start == end and (i-j) % n not in (1, n-1)):
                return False
    ys = sorted(ys)
    tree = [0] * (len(ys) + 1)

    def prefix(i):
        total = 0
        while i:
            total += tree[i]
            i -= i & -i
        return total

    intersections = 0
    for _, kind, lo, hi in sorted(events):
        if kind == 1:
            intersections += prefix(bisect_right(ys, hi)) - prefix(bisect_left(ys, lo))
        else:
            i = bisect_left(ys, lo) + 1
            while i < len(tree):
                tree[i] += 1 if kind == 0 else -1
                i += i & -i
    # 相邻且垂直的边必有一个交点；除此之外的交点都不合法。
    corners = sum(a != b for a, b in zip(directions, directions[1:] + directions[:1]))
    return intersections == corners


def lights(text):
    values = list(map(int, text.split()))
    n, m, q = values[:3]
    assert 1 <= n <= 1000 and 1 <= m <= 1000 and n*m <= 10**6
    assert 0 <= q <= 100000 and len(values) == 3 + 2*q
    odd = set()
    for i, j in zip(values[3::2], values[4::2]):
        assert 1 <= i <= n and 1 <= j <= m
        key = (i, j)
        if key in odd:
            odd.remove(key)
        else:
            odd.add(key)
    return str(n*m - len(odd))


def kernel(text):
    """顺时针正交简单多边形的核是各边右半平面的交，允许退化成线段或点。"""
    values = list(map(int, text.split()))
    pos, total = 0, 0
    answers = []
    while pos < len(values):
        n = values[pos]
        pos += 1
        if n == 0:
            assert pos == len(values) and total <= 320000
            return "\n".join(answers)
        assert 4 <= n <= 320000 and pos + 2*n <= len(values)
        points = list(zip(values[pos:pos+2*n:2], values[pos+1:pos+2*n:2]))
        pos += 2*n
        total += n
        assert all(-10**9 <= v <= 10**9 for p in points for v in p)
        assert len(set(points)) == n
        lo_x = lo_y = -10**20
        hi_x = hi_y = 10**20
        area = 0
        for (x, y), (xx, yy) in zip(points, points[1:] + points[:1]):
            assert (x == xx) != (y == yy)
            area += x*yy - xx*y
            if xx > x:
                hi_y = min(hi_y, y)
            elif xx < x:
                lo_y = max(lo_y, y)
            elif yy > y:
                lo_x = max(lo_x, x)
            else:
                hi_x = min(hi_x, x)
        assert area < 0
        assert simple_orthogonal(points), "多边形自相交、重叠或非相邻接触"
        answers.append("Yes" if lo_x <= hi_x and lo_y <= hi_y else "No")
    raise AssertionError("缺少终止标记 0")


def absent(text, *, large=False):
    values = list(map(int, text.split()))
    n, m = values[:2]
    assert 1 <= n <= (100000 if large else 16)
    assert 1 <= m <= (10000 if large else 8)
    assert len(values) == n + 2 and all(1 <= v <= m for v in values[2:])
    # 每个完整字母表块都能提供任意一个字符；最后的不完整块贡献最短缺失长度的 1。
    seen = set()
    length = 1
    for v in values[2:]:
        seen.add(v)
        if len(seen) == m:
            length += 1
            seen.clear()
    return str(length)


def nonogram(text, expected):
    """通过所有可行行列模式的必填格推导唯一性；未完全推出时返回未证明。"""
    lines = [list(map(int, line.split())) for line in text.splitlines()]
    r, c = lines[0]
    assert 1 <= r <= 30 and 1 <= c <= 30 and len(lines) == 1+r+c
    clues = []
    for line in lines[1:]:
        count, *blocks = line
        assert count == len(blocks) and all(v > 0 for v in blocks)
        clues.append(tuple(blocks))

    @lru_cache(None)
    def patterns(size, blocks):
        if not blocks:
            return (0,)
        width = blocks[0]
        rest = sum(blocks[1:]) + len(blocks) - 1
        found = []
        for start in range(size-width-rest+1):
            bits = ((1 << width) - 1) << start
            if len(blocks) == 1:
                found.append(bits)
            else:
                offset = start + width + 1
                found.extend(bits | (tail << offset) for tail in patterns(size-offset, blocks[1:]))
        return tuple(found)

    slots = [[(i, j) for j in range(c)] for i in range(r)]
    slots += [[(i, j) for i in range(r)] for j in range(c)]
    candidates = [patterns(len(line), block) for line, block in zip(slots, clues)]
    grid = [[-1]*c for _ in range(r)]
    changed = True
    while changed:
        changed = False
        for index, cells in enumerate(slots):
            known = sum(1 << j for j, (x, y) in enumerate(cells) if grid[x][y] != -1)
            filled = sum(1 << j for j, (x, y) in enumerate(cells) if grid[x][y] == 1)
            options = [v for v in candidates[index] if v & known == filled]
            assert options, "数织约束无解"
            candidates[index] = options
            must, may = options[0], 0
            for value in options:
                must &= value
                may |= value
            for j, (x, y) in enumerate(cells):
                value = 1 if must & (1 << j) else 0 if not may & (1 << j) else -1
                if value != -1 and grid[x][y] == -1:
                    grid[x][y] = value
                    changed = True
    output = expected.split()
    assert len(output) == r and all(len(line) == c and set(line) <= {'0', '1'} for line in output)
    for cells, block in zip(slots, clues):
        sequence = ''.join(output[x][y] for x, y in cells)
        assert tuple(len(run) for run in sequence.split('0') if run) == block, "答案不满足数织提示"
    unique = all(v != -1 for row in grid for v in row)
    if unique:
        assert all(grid[i][j] == int(output[i][j]) for i in range(r) for j in range(c))
    return unique


def selfcheck():
    # 用枚举所有候选序列的独立算法检查完整字母表分块法。
    def brute(a, m):
        for length in range(1, len(a) + 2):
            for candidate in itertools.product(range(1, m+1), repeat=length):
                it = iter(a)
                if not all(any(x == v for x in it) for v in candidate):
                    return str(length)
        raise AssertionError("不可达")
    for m in range(1, 4):
        for n in range(1, 7):
            for a in itertools.product(range(1, m+1), repeat=n):
                text = f"{n} {m}\n" + " ".join(map(str, a))
                assert absent(text) == brute(a, m)
    assert lights("2 3 3\n1 1\n1 1\n2 3\n") == "5"
    assert kernel("4\n0 0\n0 1\n1 1\n1 0\n0\n") == "Yes"
    assert kernel("8\n0 0\n0 3\n3 3\n3 0\n2 0\n2 2\n1 2\n1 0\n0\n") == "No"
    assert simple_orthogonal([(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)])
    assert not simple_orthogonal([(0, 0), (0, 4), (4, 4), (4, 1),
                                  (-1, 1), (-1, 3), (3, 3), (3, 0)])
    assert nonogram("1 1\n1 1\n1 1\n", "1\n")
    assert not nonogram("2 2\n1 1\n1 1\n1 1\n1 1\n", "10\n01\n")


def review():
    rows = json.loads((ROOT / "collab/gmyhf-download-materialize.json").read_text())["materialized"]
    solvers = {31270: lights, 31420: kernel, 31421: absent,
               31422: lambda text: absent(text, large=True)}
    results = []
    nonograms = []
    for row in rows:
        number = row["global_number"]
        if number not in solvers and number != 30159:
            continue
        directory = ROOT / "data/openjudge/tests" / row["bucket"] / (row["local_id"] + "_GMyhf/data")
        files = []
        for path in sorted(directory.glob("*.in"), key=lambda p: int(p.stem)):
            output = path.with_suffix(".out")
            if number == 30159:
                nonograms.append({"input": str(path.relative_to(ROOT)),
                                  "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                                  "unique_proved": nonogram(path.read_text(), output.read_text())})
                continue
            actual = solvers[number](path.read_text())
            matches = actual.split() == output.read_text().split()
            files.append({"input": str(path.relative_to(ROOT)),
                          "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                          "matches": matches})
        if number in solvers:
            results.append({"global_number": number, "cases": len(files),
                            "status": "答案一致" if all(x["matches"] for x in files) else "答案不一致",
                            "files": files})
    return {"method": "独立算法逐文件比较输出 token；不代表沙箱计时验收。31420 另用扫描线检查简单正交多边形约束。",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "entries": results,
            "nonogram_uniqueness": nonograms}


if __name__ == "__main__":
    selfcheck()
    print(json.dumps(review(), ensure_ascii=False, indent=2))
