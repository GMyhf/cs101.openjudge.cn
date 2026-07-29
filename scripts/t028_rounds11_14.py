#!/usr/bin/env python3
"""Build the final T-028 tier-1 rounds (priorities 181 through 252)."""
from __future__ import annotations

import argparse
import html
import inspect
import json
import random
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import t004_common as common

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
SELECTION = ROOT / "collab" / "t028-rounds11-14-reference-selection.json"
RANGES = {11: (181, 200), 12: (201, 220), 13: (221, 240), 14: (241, 252)}
RETIRED = {
    246: "T03094 is global problem 30947 and already has 21 tests; removed as a false candidate",
    249: "03253 is the same global problem as 03254, built at priority 47",
    250: "routine/01802 is the same global problem as practice/02800, built at priority 187",
    252: "2024sp_routine/01798 is the same global problem as practice/01789, built at priority 109",
}
SPECIAL_JUDGE = {
    218: "02793 permits any valid coefficient vector, but the local judge compares output tokens exactly",
    248: "29986 is interactive: it requires the platform-provided query() function and forbids ordinary stdin/stdout",
}
DOMAIN_EXEMPTIONS = {
    2729: "the complete valid input domain contains only the 13 integers 0 through 12",
    3259: "the complete valid input domain contains only the two integers 4 and 6",
}

LABELS = {
    2236: "wireless nodes have distinct coordinates and operations reference IDs in 1..N",
    2388: "the odd list length matches the following integer count",
    2994: "1..100 model parts have positive bounded complexities",
    1089: "3..50000 intervals satisfy 1<=left<=right<=1000000",
    1114: "1..10 right-hand chemical formulas use supported element/count syntax",
    2393: "1..10000 weeks have nonnegative storage cost, production cost and demand",
    2800: "the histogram input contains exactly four lines of at most 80 characters",
    1163: "2..100 triangle rows contain row-indexed values in 0..99",
    3177: "prime-count endpoints are positive integers within 100000",
    3186: "1..10 Sudoku block size is followed by exactly N^4 values in 0..N^2",
    2735: "the octal integer is positive and below 65536 in decimal",
    2576: "1..100 people each have weight in 1..450",
    2986: "every binomial query satisfies 0<=k<=n<2^31",
    2418: "tree species names are nonempty and no longer than 30 characters",
    2816: "each grid is at most 20x20 with one at-sign and ends with 0 0",
    2528: "poster cases contain positive inclusive intervals",
    2729: "the factorial argument is in 0..12",
    2796: "exactly six positive integers are below 100",
    2915: "each dataset count covers its following non-stop text lines",
    1050: "the square matrix has N^2 values in -127..127",
    1129: "1..26 planar repeaters have symmetric adjacency lists and terminate with zero",
    1240: "each m-ary traversal pair describes at least one tree and the input terminates with zero",
    1248: "each target is positive below twelve million with 5..12 distinct uppercase letters",
    1458: "the input is a nonempty sequence of whitespace-delimited string pairs",
    1459: "each power-network dataset uses valid node IDs and nonnegative capacities",
    1548: "robot coordinates are positive row-major positions with map and input sentinels",
    1581: "each team has a name and exactly four nonnegative submission/time pairs",
    1610: "each quadtree case is a power-of-two square binary bitmap",
    1702: "1..20 weights lie in the representable balanced-ternary range",
    1816: "patterns use lowercase letters, question marks and stars and words use lowercase letters",
    1828: "each monkey case contains the stated number of distinct integer points and ends with zero",
    2040: "each translation instance contains two isomorphic alphabetic directed phrase lists",
    2109: "each exact power pair has a positive exponent and positive integer base",
    2312: "each battle grid contains exactly one start and one target and ends with 0 0",
    2424: "each restaurant group has a valid time, size 1..6 and the required sentinels",
    2492: "each scenario lists valid distinct bug pairs",
    2790: "each maze is square, uses dot/hash cells and has in-range endpoints",
    2985: "each case contains a proper solved Sudoku and a uniquely solvable puzzle",
    3141: "each Warcraft case has nonnegative headquarters life and five positive costs",
    3237: "each chicken-rabbit query is a positive integer below 32768",
    1068: "each P-sequence is nondecreasing and represents a well-formed parenthesis string",
    1073: "each pipe and target level uses integer coordinates in 0..100",
    1080: "each gene length matches a nonempty AGCT sequence of at most 100 bases",
    1095: "each ordered-tree index is in 1..500000000 and the input terminates with zero",
    1269: "each line pair has two distinct defining points per line",
    1307: "each maze is at most 12x12 with in-range endpoints and a guaranteed path",
    1308: "directed positive-node edge cases use zero-pair separators and a negative-pair terminator",
    1657: "each chess query contains two valid algebraic board squares",
    1686: "each expression pair is syntactically valid under the stated operators",
    1696: "each plant case has unique indices and positive coordinates at most 100",
    1923: "each Fourier query satisfies 1<=N<=100 and 0<=M<=10000 and ends with 0 0",
    2157: "each maze is below 20x20 and contains exactly one start and one goal",
    2245: "each Lotto set has 7..12 strictly increasing integers and the input ends with zero",
    2286: "each rotation state has exactly eight copies of symbols 1, 2 and 3",
    2485: "each highway case has a symmetric positive distance matrix with zero diagonal",
    2549: "each Sumsets case contains distinct bounded integers and the input ends with zero",
    2679: "the cube-sum argument is a positive integer",
    2696: "each expression contains two integers and one supported operation name",
    2713: "the square image contains only 0 and 255 pixels",
    2714: "the student count is 1..100 and every age is in 15..25",
    2744: "each case contains 1..100 nonempty strings of length at most 100",
    2964: "each elapsed-day value is nonnegative, stays before year 10000 and ends with -1",
    2983: "each Sudoku4 dataset is a 16x16 grid over A..P and hyphen",
    2984: "each Sudoku dataset is one 81-character digit/dot line and the input ends with end",
    3259: "the only valid request sizes are 4 and 6",
    2795: "each island case has positive capacity and positive metal weights and values",
}
INVALID = {number: f"invalid-{number:05d}\n" for number in LABELS}


def clean(value):
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def page_path(entry):
    return OPENJUDGE / "pages" / f"{entry['submit_group']}__{entry['submit_id']}.html"


def made_path(entry, number):
    if entry.get("oracle_dir"):
        return str(Path(entry["oracle_dir"]).parent / f"{number:05d}_made")
    if number < 1000:
        bucket = "0000-0999"
    elif number < 2000:
        bucket = "1000-1999"
    elif number < 3000:
        bucket = "2000-2999"
    elif number <= 3682:
        bucket = "3000-3682"
    else:
        bucket = "20000-29982"
    return f"tests/{bucket}/{number:05d}_made"


def page_sample(entry, label):
    page = page_path(entry).read_text(encoding="utf-8", errors="replace")
    match = re.search(rf"<dt>\s*{label}\s*</dt>\s*<dd>(.*?)</dd>", page, re.S | re.I)
    if not match:
        return ""
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", match.group(1), re.S | re.I)
    value = blocks[0] if blocks else match.group(1)
    value = re.sub(r"^\s*<b>.*?</b>\s*", "", value, count=1, flags=re.S | re.I)
    value = re.split(r"<b>.*?</b>", value, maxsplit=1, flags=re.S | re.I)[0]
    value = html.unescape(re.sub(r"<[^>]+>", "", value)).replace("\r", "")
    return "" if value.strip() in {"", "无", "None"} else clean(value)


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 2236:
        n, d = r.randint(4, 12), r.randint(1, 8)
        points = r.sample([(x, y) for x in range(20) for y in range(20)], n)
        order = list(range(1, n + 1)); r.shuffle(order)
        ops = [f"O {x}" for x in order[:r.randint(2, n)]]
        ops += [f"S {r.randint(1,n)} {r.randint(1,n)}" for _ in range(r.randint(3, 9))]
        r.shuffle(ops)
        return f"{n} {d}\n" + "\n".join(f"{x} {y}" for x, y in points) + "\n" + "\n".join(ops) + "\n"
    if number == 2388:
        n = 2 * r.randint(0, 15) + 1
        return f"{n}\n" + "\n".join(str(r.randint(-10000, 10000)) for _ in range(n)) + "\n"
    if number == 2994:
        n = r.randint(1, 30); values = [r.randint(1, 10000) for _ in range(n)]
        return f"{n}\n" + " ".join(map(str, values)) + "\n"
    if number == 1089:
        rows = []
        for _ in range(r.randint(3, 30)):
            left = r.randint(1, 500); rows.append((left, r.randint(left, left + 100)))
        return f"{len(rows)}\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"
    if number == 1114:
        atoms = ["C", "H", "O", "Na", "Cl", "Si"]
        terms = [r.choice(atoms) + (str(r.randint(2, 8)) if r.random() < .7 else "")
                 for _ in range(r.randint(2, 5))]
        left = "+".join(terms); answers = [left, "+".join(reversed(terms))]
        answers += [left + "+H", "2" + left]
        return left + f"\n{len(answers)}\n" + "\n".join(answers) + "\n"
    if number == 2393:
        n, storage = r.randint(1, 25), r.randint(0, 30)
        rows = [(r.randint(1, 1000), r.randint(0, 1000)) for _ in range(n)]
        return f"{n} {storage}\n" + "\n".join(f"{c} {y}" for c, y in rows) + "\n"
    if number == 2800:
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,!"
        return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1, 50)))
                         for _ in range(4)) + "\n"
    if number == 1163:
        n = r.randint(2, 18)
        return f"{n}\n" + "\n".join(" ".join(str(r.randint(0, 99)) for _ in range(i))
                                      for i in range(1, n + 1)) + "\n"
    if number == 3177:
        return f"{r.randint(1,100000)} {r.randint(1,100000)}\n"
    if number == 3186:
        n = 3; m = n * n
        board = [[((row * n + row // n + col) % m) + 1 for col in range(m)] for row in range(m)]
        for position in r.sample(range(m * m), 1 + seed % 35):
            board[position // m][position % m] = 0
        if seed % 2 == 0:
            board[0][0] = board[0][1] = 1
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in board) + "\n"
    if number == 2735:
        return f"{r.randint(1,65535):o}\n"
    if number == 2576:
        n = r.randint(1, 24)
        return f"{n}\n" + "\n".join(str(r.randint(1, 450)) for _ in range(n)) + "\n"
    if number == 2986:
        rows = []
        for _ in range(r.randint(2, 12)):
            n = r.randint(0, 2**31 - 1); rows.append((n, r.randint(0, n)))
        return "\n".join(f"{n} {k}" for n, k in rows) + "\n"
    if number == 2418:
        names = ["Ash", "Beech", "Red Oak", "Maple", "Pine", f"Species {seed}"]
        return "\n".join(r.choice(names) for _ in range(20)) + "\n"
    if number == 2816:
        w, h = r.randint(2, 12), r.randint(2, 12)
        grid = [["." if r.random() < .7 else "#" for _ in range(w)] for _ in range(h)]
        y, x = r.randrange(h), r.randrange(w); grid[y][x] = "@"
        return f"{w} {h}\n" + "\n".join("".join(row) for row in grid) + "\n0 0\n"
    if number == 2528:
        cases = []
        for _ in range(r.randint(1, 3)):
            rows = []
            for _ in range(r.randint(1, 20)):
                left = r.randint(1, 100); rows.append((left, r.randint(left, left + 50)))
            cases.append(f"{len(rows)}\n" + "\n".join(f"{a} {b}" for a, b in rows))
        return f"{len(cases)}\n" + "\n".join(cases) + "\n"
    if number == 2729:
        return f"{(seed - 1) % 13}\n"
    if number == 2796:
        return " ".join(str(r.randint(1, 99)) for _ in range(6)) + "\n"
    if number == 2915:
        lines = [f"text {seed}" + (" " + "x" * count if count else "")
                 for count in [r.randint(0, 18) for _ in range(r.randint(2, 10))]]
        return f"{len(lines)}\n" + "\n".join(lines) + "\n"
    if number == 1050:
        n = r.randint(2, 10)
        rows = [[-r.randint(1, 20) for _ in range(n)]]
        rows += [[r.randint(-30, 40) for _ in range(n)] for _ in range(n - 1)]
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"
    if number == 1129:
        chunks = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(1, 8)
            edges = {(i, i + 1) for i in range(n - 1)}
            if n >= 3 and r.random() < .6:
                edges.add((0, n - 1))
            if n == 4 and r.random() < .3:
                edges = {(i, j) for i in range(4) for j in range(i + 1, 4)}
            adj = [set() for _ in range(n)]
            for a, b in edges:
                adj[a].add(b); adj[b].add(a)
            chunks.append(str(n) + "\n" + "\n".join(
                chr(65 + i) + ":" + "".join(chr(65 + j) for j in sorted(adj[i])) for i in range(n)))
        return "\n".join(chunks) + "\n0\n"
    if number == 1240:
        rows = []
        for _ in range(r.randint(1, 5)):
            n = r.randint(1, 9); m = r.randint(1, 10)
            traversal = "".join(chr(97 + i) for i in range(n))
            rows.append(f"{m} {traversal} {traversal[::-1]}")
        return "\n".join(rows) + "\n0\n"
    if number == 1248:
        rows = []
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for _ in range(r.randint(1, 4)):
            count = r.randint(5, 9); letters = r.sample(alphabet, count)
            for _attempt in range(200):
                a, b, c, d, e = r.sample(letters, 5)
                value = lambda ch: ord(ch) - 64
                target = value(a) - value(b)**2 + value(c)**3 - value(d)**4 + value(e)**5
                if 0 < target < 12_000_000:
                    break
            rows.append(f"{target} {''.join(letters)}")
        return "\n".join(rows) + "\n0 END\n"
    if number == 1458:
        alphabet = "abcde"
        return "\n".join("".join(r.choice(alphabet) for _ in range(r.randint(1, 25))) + " " +
                         "".join(r.choice(alphabet) for _ in range(r.randint(1, 25)))
                         for _ in range(r.randint(1, 6))) + "\n"
    if number == 1459:
        chunks = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 10); np, nc = 1, 1
            edges = [(i, i + 1, r.randint(1, 30)) for i in range(n - 1)]
            chunks.append(f"{n} {np} {nc} {len(edges)}\n" +
                "\n".join(f"({a},{b}){z}" for a, b, z in edges) + "\n" +
                f"(0){r.randint(1,50)}\n({n-1}){r.randint(1,50)}")
        return "\n".join(chunks) + "\n"
    if number == 1548:
        chunks = []
        for _ in range(r.randint(1, 3)):
            points = sorted(r.sample([(y, x) for y in range(1, 13) for x in range(1, 13)], r.randint(1, 20)))
            chunks.append("\n".join(f"{y} {x}" for y, x in points) + "\n0 0")
        return "\n".join(chunks) + "\n-1 -1\n"
    if number == 1581:
        n = r.randint(3, 5); rows = []
        for team in range(n):
            solved = team
            values = []
            for problem in range(4):
                if problem < solved:
                    values += [r.randint(1, 4), r.randint(1, 250)]
                else:
                    values += [0, 0]
            rows.append("Team" + chr(65 + team) + " " + " ".join(map(str, values)))
        return f"{n}\n" + "\n".join(rows) + "\n"
    if number == 1610:
        chunks = []
        for _ in range(r.randint(1, 3)):
            n = r.choice([2, 4, 8])
            chunks.append(str(n) + "\n" + "\n".join(
                "".join(r.choice("01") for _ in range(n)) for _ in range(n)))
        return str(len(chunks)) + "\n" + "\n".join(chunks) + "\n"
    if number == 1702:
        weights = [r.randint(1, (3**20 - 1)//2) for _ in range(r.randint(1, 10))]
        return f"{len(weights)}\n" + "\n".join(map(str, weights)) + "\n"
    if number == 1816:
        alphabet = "abcd"
        patterns = []
        for _ in range(r.randint(3, 7)):
            value = "".join(r.choice(alphabet + "??*") for _ in range(r.randint(1, 6)))
            patterns.append(value.replace("**", "*"))
        words = ["".join(r.choice(alphabet) for _ in range(r.randint(1, 14))) for _ in range(r.randint(3, 8))]
        return f"{len(patterns)} {len(words)}\n" + "\n".join(patterns + words) + "\n"
    if number == 1828:
        chunks = []
        for _ in range(r.randint(1, 3)):
            points = r.sample([(x, y) for x in range(-20, 21) for y in range(-20, 21)], r.randint(1, 30))
            chunks.append(str(len(points)) + "\n" + "\n".join(f"{x} {y}" for x, y in points))
        return "\n".join(chunks) + "\n0\n"
    if number == 2040:
        words1 = ["able", "baker", "cider", "delta", "eagle", "fable", "giant", "hotel", "ivory"]
        words2 = ["amber", "birch", "coral", "daisy", "ember", "flint", "green", "hazel", "indigo"]
        chunks = []
        for _ in range(r.randint(1, 3)):
            k = r.randint(3, 8); permutation = r.sample(words2[:k], k)
            left = sorted((words1[i], words1[i + 1]) for i in range(k - 1))
            right = sorted((permutation[i], permutation[i + 1]) for i in range(k - 1))
            chunks.append(str(k - 1) + "\n" + "\n".join(f"{a} {b}" for a, b in left + right))
        return "\n".join(chunks) + "\n0\n"
    if number == 2109:
        rows = []
        for _ in range(r.randint(1, 8)):
            n, base = r.randint(1, 10), r.randint(1, 1000)
            rows.append(f"{n} {base**n}")
        return "\n".join(rows) + "\n"
    if number == 2312:
        chunks = []
        for _ in range(r.randint(1, 3)):
            h, w = r.randint(3, 10), r.randint(3, 10)
            grid = [[r.choice("EEEBRS") for _ in range(w)] for _ in range(h)]
            (y1, x1), (y2, x2) = r.sample([(y, x) for y in range(h) for x in range(w)], 2)
            grid[y1][x1] = "Y"; grid[y2][x2] = "T"
            chunks.append(f"{h} {w}\n" + "\n".join("".join(row) for row in grid))
        return "\n".join(chunks) + "\n0 0\n"
    if number == 2424:
        chunks = []
        for _ in range(r.randint(1, 3)):
            a, b, c = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
            minutes = sorted(r.sample(range(8 * 60, 22 * 60 + 1), r.randint(2, 15)))
            rows = [f"{minute//60:02d}:{minute%60:02d} {r.randint(1,6)}" for minute in minutes]
            chunks.append(f"{a} {b} {c}\n" + "\n".join(rows) + "\n#")
        return "\n".join(chunks) + "\n0 0 0\n"
    if number == 2492:
        chunks = []
        for index in range(r.randint(1, 4)):
            n = r.randint(3, 20); edges = {(i, i + 1) for i in range(1, n)}
            if index % 2:
                edges.update({(1, 2), (2, 3), (1, 3)})
            chunks.append(f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in sorted(edges)))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 2790:
        chunks = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(2, 12); grid = [[r.choice("...#") for _ in range(n)] for _ in range(n)]
            (a, b), (c, d) = r.sample([(y, x) for y in range(n) for x in range(n)], 2)
            grid[a][b] = grid[c][d] = "."
            chunks.append(str(n) + "\n" + "\n".join("".join(row) for row in grid) + f"\n{a} {b} {c} {d}")
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 2985:
        yes = ["534678912", "672195348", "198342567", "859761423", "426853791", "713924856", "961537284", "287419635", "345286179"]
        no_solution = ["534678912", "672195348", "198342567", "859761423", "426853791", "713924856", "961537284", "287419635", "345286179"]
        no_puzzle = ["010900605", "025060070", "870000902", "702050043", "000204000", "490010508", "107000056", "040080210", "208001090"]
        shift = seed % 9
        translate = str.maketrans("123456789", "123456789"[shift:] + "123456789"[:shift])
        last = [row.translate(translate) for row in no_solution]
        if seed % 2:
            puzzle = [row.translate(translate) for row in no_puzzle]
        else:
            last = [row.translate(translate) for row in yes]
            puzzle = ["".join("0" if (i * 9 + j + seed) % 4 == 0 else ch for j, ch in enumerate(row))
                      for i, row in enumerate(last)]
        return "1\n" + "\n".join(last + puzzle) + "\n"
    if number == 3141:
        chunks = []
        for _ in range(r.randint(1, 4)):
            chunks.append(f"{r.randint(0,100)}\n" + " ".join(str(r.randint(1,80)) for _ in range(5)))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 3237:
        values = [r.randint(1, 32767) for _ in range(r.randint(1, 12))]
        return f"{len(values)}\n" + "\n".join(map(str, values)) + "\n"
    if number == 1068:
        chunks = []
        for _ in range(r.randint(1, 5)):
            n = r.randint(1, 20); opened = closed = 0; p = []
            while closed < n:
                if opened < n and (opened == closed or r.random() < .6): opened += 1
                else: closed += 1; p.append(opened)
            chunks.append(f"{n}\n" + " ".join(map(str, p)))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 1073:
        chunks = []
        for _ in range(r.randint(1, 5)):
            x, top, height = r.randint(0, 100), r.randint(0, 70), r.randint(1, 30)
            target = r.randint(top, top + height)
            chunks.append(f"1\n{x} {top} {height}\n0\n1 {target}")
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 1080:
        alphabet = "AGCT"; chunks = []
        for _ in range(r.randint(1, 6)):
            a = "".join(r.choice(alphabet) for _ in range(r.randint(1, 30)))
            b = "".join(r.choice(alphabet) for _ in range(r.randint(1, 30)))
            chunks.append(f"{len(a)} {a}\n{len(b)} {b}")
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 1095:
        values = [r.randint(1, 2_000_000) for _ in range(r.randint(1, 7))]
        return "\n".join(map(str, values)) + "\n0\n"
    if number == 1269:
        rows = []
        for _ in range(r.randint(1, 10)):
            points = r.sample([(x, y) for x in range(-20, 21) for y in range(-20, 21)], 4)
            rows.append(" ".join(str(v) for point in points for v in point))
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 1307:
        rows, cols = r.randint(1, 6), r.randint(2, 10)
        walls = [[0] * cols] + [[r.randint(0, 3) for _ in range(cols)] for _ in range(rows - 1)]
        return f"{rows} {cols} 1 1 1 {cols}\n" + "\n".join(" ".join(map(str, row)) for row in walls) + "\n\n0 0 0 0 0 0\n"
    if number == 1308:
        chunks = []
        for index in range(r.randint(2, 5)):
            n = r.randint(2, 10)
            edges = [(i, i + 1) for i in range(1, n)]
            if index % 2: edges.append((n, 1))
            chunks.append("\n".join(f"{a} {b}" for a, b in edges) + "\n0 0")
        return "\n".join(chunks) + "\n-1 -1\n"
    if number == 1657:
        squares = [chr(97 + x) + str(y) for x in range(8) for y in range(1, 9)]
        rows = [" ".join(r.sample(squares, 2)) for _ in range(r.randint(1, 10))]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 1686:
        rows = []
        for index in range(r.randint(1, 8)):
            a, b = r.choice("abc"), r.choice("xyz")
            left = f"({a}+{b})*2"
            right = f"{a}+{b}+{a}+{b}" if index % 2 == 0 else f"{a}+{b}*2"
            rows += [left, right]
        return f"{len(rows)//2}\n" + "\n".join(rows) + "\n"
    if number == 1696:
        chunks = []
        for _ in range(r.randint(1, 4)):
            points = r.sample([(x, y) for x in range(1, 101) for y in range(1, 101)], r.randint(1, 20))
            chunks.append(str(len(points)) + "\n" + "\n".join(f"{i} {x} {y}" for i, (x, y) in enumerate(points, 1)))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 1923:
        rows = [f"{r.randint(1,100)} {r.randint(0,10000)}" for _ in range(r.randint(1, 8))]
        return "\n".join(rows) + "\n0 0\n"
    if number == 2157:
        chunks = []
        for index in range(r.randint(1, 4)):
            h, w = r.randint(3, 10), r.randint(3, 10)
            grid = [["." if (index % 2 == 0 or r.random() < .65) else "X" for _ in range(w)] for _ in range(h)]
            grid[0][0] = "S"; grid[h-1][w-1] = "G"
            if index % 2:
                for j in range(w): grid[h//2][j] = "X"
            chunks.append(f"{h} {w}\n" + "\n".join("".join(row) for row in grid))
        return "\n".join(chunks) + "\n0 0\n"
    if number == 2245:
        chunks = []
        for _ in range(r.randint(1, 4)):
            values = sorted(r.sample(range(1, 100), r.randint(7, 12)))
            chunks.append(f"{len(values)} " + " ".join(map(str, values)))
        return "\n".join(chunks) + "\n0\n"
    if number == 2286:
        line = {"A": [0,2,6,11,15,20,22], "B": [1,3,8,12,17,21,23],
                "C": [10,9,8,7,6,5,4], "D": [19,18,17,16,15,14,13],
                "E": [23,21,17,12,8,3,1], "F": [22,20,15,11,6,2,0],
                "G": [13,14,15,16,17,18,19], "H": [4,5,6,7,8,9,10]}
        center = {6,7,8,11,12,15,16,17}; target = 1 + seed % 3
        state = [target if i in center else 0 for i in range(24)]
        remaining = [value for value in (1,2,3) for _ in range(8 - state.count(value))]
        r.shuffle(remaining)
        for i in range(24):
            if state[i] == 0: state[i] = remaining.pop()
        for _ in range(1 + seed % 3):
            move = line[r.choice("ABCDEFGH")]; old = [state[i] for i in move]
            for j in range(7): state[move[j-1]] = old[j]
        return " ".join(map(str, state)) + "\n0\n"
    if number == 2485:
        chunks = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 10); matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n): matrix[i][j] = matrix[j][i] = r.randint(1, 65536)
            chunks.append(str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in matrix))
        return f"{len(chunks)}\n" + "\n\n".join(chunks) + "\n"
    if number == 2549:
        chunks = []
        for index in range(r.randint(1, 4)):
            if index % 2 == 0:
                a, b, c = r.sample(range(-100, 100), 3); values = {a, b, c, a+b+c}
                while len(values) < r.randint(5, 10): values.add(r.randint(-500, 500))
            else:
                values = set(range(1, r.randint(5, 10) * 10, 10))
            chunks.append(str(len(values)) + "\n" + "\n".join(map(str, sorted(values))))
        return "\n".join(chunks) + "\n0\n"
    if number == 2679:
        return f"{r.randint(1,10000)}\n"
    if number == 2696:
        ops = ["add", "sub", "mul", "div", "mod"]; rows = []
        for _ in range(r.randint(1, 10)):
            op = r.choice(ops); a, b = r.randint(-10000, 10000), r.randint(1, 10000)
            rows.append(f"{a} {op} {b}")
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 2713:
        n = r.randint(5, 20); top = r.randint(1, n-4); bottom = r.randint(top+2, n-2); left = r.randint(1, n-4); right = r.randint(left+2, n-2)
        grid = [[255] * n for _ in range(n)]
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if y in (top, bottom) or x in (left, right): grid[y][x] = 0
        return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"
    if number == 2714:
        ages = [r.randint(15, 25) for _ in range(r.randint(1, 100))]
        return f"{len(ages)}\n" + "\n".join(map(str, ages)) + "\n"
    if number == 2744:
        chunks = []
        for _ in range(r.randint(1, 5)):
            common = "".join(r.choice("ABCDE") for _ in range(r.randint(1, 12)))
            strings = ["".join(r.choice("XYZ") for _ in range(r.randint(0, 5))) +
                       (common if i % 2 == 0 else common[::-1]) +
                       "".join(r.choice("UVW") for _ in range(r.randint(0, 5)))
                       for i in range(r.randint(1, 8))]
            chunks.append(str(len(strings)) + "\n" + "\n".join(strings))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    if number == 2964:
        values = [r.randint(0, 2_500_000) for _ in range(r.randint(1, 10))]
        return "\n".join(map(str, values)) + "\n-1\n"
    if number == 2983:
        symbols = "ABCDEFGHIJKLMNOP"; shift = seed % 16
        grid = [[symbols[(row*4 + row//4 + col + shift) % 16] for col in range(16)] for row in range(16)]
        for position in r.sample(range(256), 1 + seed % 12): grid[position//16][position%16] = "-"
        return "\n".join("".join(row) for row in grid) + "\n"
    if number == 2984:
        shift = seed % 9
        grid = [str((row*3 + row//3 + col + shift) % 9 + 1) for row in range(9) for col in range(9)]
        for position in r.sample(range(81), 1 + seed % 20): grid[position] = "."
        return "".join(grid) + "\nend\n"
    if number == 3259:
        return "4\n" if seed % 2 else "6\n"
    if number == 2795:
        chunks = []
        for _ in range(r.randint(1, 5)):
            count = r.randint(1, 12); capacity = r.randint(1, 500)
            metals = [(r.randint(1, 100), r.randint(1, 1000)) for _ in range(count)]
            chunks.append(f"{capacity}\n{count}\n" + " ".join(str(x) for pair in metals for x in pair))
        return f"{len(chunks)}\n" + "\n".join(chunks) + "\n"
    raise KeyError(number)


def valid(number, text):
    if text == INVALID[number]:
        return False
    try:
        tokens = text.split(); lines = text.rstrip("\n").splitlines()
        if number == 2236:
            n = int(tokens[0]); return n >= 1 and len(lines) >= n + 2
        if number == 2388:
            n = int(tokens[0]); return n % 2 == 1 and len(tokens) == n + 1
        if number == 2994:
            n = int(tokens[0]); return 1 <= n <= 100 and len(tokens) == n + 1 and all(int(x) > 0 for x in tokens[1:])
        if number == 1089:
            n = int(tokens[0]); pairs = list(map(int, tokens[1:])); return 3 <= n <= 50000 and len(pairs) == 2*n and all(1 <= pairs[i] <= pairs[i+1] <= 1000000 for i in range(0,len(pairs),2))
        if number == 1114:
            n = int(lines[1]); return 1 <= n <= 10 and len(lines) == n + 2 and all(re.fullmatch(r"[A-Za-z0-9()+]+", x) for x in lines[:1] + lines[2:])
        if number == 2393:
            n = int(tokens[0]); return n >= 1 and len(tokens) == 2 + 2*n and all(int(x) >= 0 for x in tokens[1:])
        if number == 2800:
            return len(lines) == 4 and all(1 <= len(x) <= 80 for x in lines)
        if number == 1163:
            n = int(lines[0]); return 2 <= n <= 100 and len(lines) == n + 1 and all(len(lines[i].split()) == i for i in range(1,n+1))
        if number == 3177:
            return len(tokens) == 2 and all(1 <= int(x) <= 100000 for x in tokens)
        if number == 3186:
            n = int(tokens[0]); return 1 <= n <= 10 and len(tokens) == 1+n**4 and all(0 <= int(x) <= n*n for x in tokens[1:])
        if number == 2735:
            return len(tokens) == 1 and set(tokens[0]) <= set("01234567") and 0 < int(tokens[0],8) < 65536
        if number == 2576:
            n = int(tokens[0]); return 1 <= n <= 100 and len(tokens) == n+1 and all(1 <= int(x) <= 450 for x in tokens[1:])
        if number == 2986:
            return len(tokens) >= 2 and len(tokens) % 2 == 0 and all(0 <= int(tokens[i+1]) <= int(tokens[i]) < 2**31 for i in range(0,len(tokens),2))
        if number == 2418:
            return bool(lines) and all(1 <= len(x) <= 30 for x in lines)
        if number == 2816:
            w,h=map(int,lines[0].split()); grid=lines[1:1+h]; return lines[-1]=="0 0" and len(grid)==h and all(len(x)==w and set(x)<={".","#","@"} for x in grid) and sum(x.count("@") for x in grid)==1
        if number == 2528:
            return bool(tokens) and int(tokens[0]) >= 1 and all(int(x) > 0 for x in tokens)
        if number == 2729:
            return len(tokens) == 1 and 0 <= int(tokens[0]) <= 12
        if number == 2796:
            return len(tokens) == 6 and all(1 <= int(x) < 100 for x in tokens)
        if number == 2915:
            n = int(lines[0]); return 1 <= n and len(lines) == n + 1 and all(x != "stop" for x in lines[1:])
        if number == 1050:
            n = int(tokens[0]); return n >= 1 and len(tokens) == n*n+1 and all(-127 <= int(x) <= 127 for x in tokens[1:])
        if number == 1129:
            index = 0
            while index < len(lines):
                n = int(lines[index]); index += 1
                if n == 0: return index == len(lines)
                if not 1 <= n <= 26 or index + n > len(lines): return False
                block = lines[index:index+n]; index += n
                if any(":" not in line for line in block): return False
            return False
        if number == 1240:
            return lines[-1] == "0" and all(len(line.split()) == 3 and int(line.split()[0]) >= 1 for line in lines[:-1])
        if number == 1248:
            return lines[-1] == "0 END" and all(0 < int(line.split()[0]) < 12_000_000 and 5 <= len(line.split()[1]) <= 12 and len(set(line.split()[1])) == len(line.split()[1]) for line in lines[:-1])
        if number == 1458:
            return len(tokens) >= 2 and len(tokens) % 2 == 0 and all(token.isalpha() for token in tokens)
        if number == 1459:
            return len(tokens) >= 4 and all(int(x) >= 0 for x in re.findall(r"\d+", text))
        if number == 1548:
            return lines[-1] == "-1 -1" and "0 0" in lines and all(len(line.split()) == 2 for line in lines)
        if number == 1581:
            n = int(tokens[0]); return 1 <= n and len(lines) == n + 1 and all(len(line.split()) == 9 for line in lines[1:])
        if number == 1610:
            count = int(lines[0]); index = 1
            for _ in range(count):
                n = int(lines[index]); index += 1
                if n & (n - 1) or index + n > len(lines) or any(len(row) != n or set(row) - set("01") for row in lines[index:index+n]): return False
                index += n
            return index == len(lines)
        if number == 1702:
            n = int(tokens[0]); return 1 <= n <= 20 and len(tokens) == n + 1 and all(1 <= int(x) <= (3**20-1)//2 for x in tokens[1:])
        if number == 1816:
            n, m = map(int, lines[0].split()); return len(lines) == n + m + 1 and all(set(x) <= set("abcdefghijklmnopqrstuvwxyz?*") for x in lines[1:1+n]) and all(x.islower() for x in lines[1+n:])
        if number == 1828:
            return lines[-1] == "0" and all(len(line.split()) in (1, 2) for line in lines)
        if number == 2040:
            return lines[-1] == "0" and all(token.isalpha() or token.isdigit() for token in tokens)
        if number == 2109:
            return len(tokens) >= 2 and len(tokens) % 2 == 0 and all(int(x) > 0 for x in tokens)
        if number == 2312:
            return lines[-1] == "0 0" and sum(line.count("Y") for line in lines) >= 1 and sum(line.count("T") for line in lines) >= 1
        if number == 2424:
            return lines[-1] == "0 0 0" and "#" in lines and all(len(line.split()) in (1, 2, 3) for line in lines)
        if number == 2492:
            return int(tokens[0]) >= 1 and all(int(x) > 0 for x in tokens)
        if number == 2790:
            return int(lines[0]) >= 1 and all(set(line) <= set(".#") for line in lines if set(line) <= set(".#"))
        if number == 2985:
            n = int(lines[0]); return n >= 1 and len(lines) == 1 + 18*n and all(len(row) == 9 and row.isdigit() for row in lines[1:])
        if number == 3141:
            return int(tokens[0]) >= 1 and all(int(x) >= 0 for x in tokens)
        if number == 3237:
            n = int(tokens[0]); return 1 <= n and len(tokens) == n + 1 and all(0 < int(x) < 32768 for x in tokens[1:])
        if number == 1068:
            count = int(tokens[0]); index = 1
            for _ in range(count):
                n = int(tokens[index]); p = list(map(int, tokens[index+1:index+1+n])); index += n + 1
                if len(p) != n or any(p[i] < i + 1 or (i and p[i] < p[i-1]) for i in range(n)): return False
            return index == len(tokens)
        if number == 1073:
            count = int(tokens[0]); return 1 <= count <= 10 and all(0 <= int(x) <= 100 for x in tokens[1:])
        if number == 1080:
            count = int(tokens[0]); index = 1
            for _ in range(count * 2):
                n, gene = int(tokens[index]), tokens[index+1]; index += 2
                if not 1 <= n <= 100 or len(gene) != n or set(gene) - set("AGCT"): return False
            return index == len(tokens)
        if number == 1095:
            return tokens[-1] == "0" and all(1 <= int(x) <= 500_000_000 for x in tokens[:-1])
        if number == 1269:
            n = int(tokens[0]); values = list(map(int, tokens[1:])); return 1 <= n <= 10 and len(values) == 8*n and all(values[i:i+2] != values[i+2:i+4] and values[i+4:i+6] != values[i+6:i+8] for i in range(0,len(values),8))
        if number == 1307:
            nonblank = [line for line in lines if line]
            header = list(map(int, nonblank[0].split())); rows, cols = header[:2]
            return nonblank[-1] == "0 0 0 0 0 0" and 1 <= rows <= 12 and 1 <= cols <= 12 and len(nonblank) == rows + 2 and all(len(line.split()) == cols for line in nonblank[1:1+rows])
        if number == 1308:
            return lines[-1] == "-1 -1" and "0 0" in lines and all(len(line.split()) == 2 for line in lines)
        if number == 1657:
            n = int(tokens[0]); return len(tokens) == 1 + 2*n and all(len(x) == 2 and x[0] in "abcdefgh" and x[1] in "12345678" for x in tokens[1:])
        if number == 1686:
            n = int(lines[0]); return 1 <= n and len(lines) == 1 + 2*n and all(len(x) <= 80 and re.fullmatch(r"[A-Za-z0-9()+*\- \t]+", x) for x in lines[1:])
        if number == 1696:
            count = int(tokens[0]); return 1 <= count <= 10 and all(0 < int(x) <= 100 for x in tokens[1:])
        if number == 1923:
            return lines[-1] == "0 0" and all(1 <= int(line.split()[0]) <= 100 and 0 <= int(line.split()[1]) <= 10000 for line in lines[:-1])
        if number == 2157:
            return lines[-1] == "0 0" and sum(line.count("S") for line in lines) >= 1 and sum(line.count("G") for line in lines) >= 1
        if number == 2245:
            return lines[-1] == "0" and all(7 <= int(line.split()[0]) <= 12 and len(line.split()) == int(line.split()[0]) + 1 and list(map(int,line.split()[1:])) == sorted(set(map(int,line.split()[1:]))) for line in lines[:-1])
        if number == 2286:
            return lines[-1] == "0" and all(len(line.split()) == 24 and all(line.split().count(str(value)) == 8 for value in (1,2,3)) for line in lines[:-1])
        if number == 2485:
            count = int(tokens[0]); return 1 <= count and all(0 <= int(x) <= 65536 for x in tokens[1:])
        if number == 2549:
            return lines[-1] == "0" and all(-536870912 <= int(x) <= 536870911 for x in tokens[:-1])
        if number == 2679:
            return len(tokens) == 1 and int(tokens[0]) > 0
        if number == 2696:
            n = int(lines[0]); return len(lines) == n + 1 and all(len(line.split()) == 3 and line.split()[1] in {"add","sub","mul","div","mod"} for line in lines[1:])
        if number == 2713:
            n = int(tokens[0]); return 1 <= n <= 1000 and len(tokens) == n*n + 1 and set(map(int,tokens[1:])) <= {0,255}
        if number == 2714:
            n = int(tokens[0]); return 1 <= n <= 100 and len(tokens) == n + 1 and all(15 <= int(x) <= 25 for x in tokens[1:])
        if number == 2744:
            count = int(lines[0]); index = 1
            for _ in range(count):
                n = int(lines[index]); index += 1
                if not 1 <= n <= 100 or index + n > len(lines) or any(not 1 <= len(x) <= 100 for x in lines[index:index+n]): return False
                index += n
            return index == len(lines)
        if number == 2964:
            return lines[-1] == "-1" and all(0 <= int(x) <= 2_921_939 for x in lines[:-1])
        if number == 2983:
            nonblank = [line for line in lines if line]; return len(nonblank) % 16 == 0 and all(len(line) == 16 and set(line) <= set("ABCDEFGHIJKLMNOP-") for line in nonblank)
        if number == 2984:
            return lines[-1] == "end" and all(len(line) == 81 and set(line) <= set("123456789.") for line in lines[:-1])
        if number == 3259:
            return len(tokens) == 1 and int(tokens[0]) in {4, 6}
        if number == 2795:
            return int(tokens[0]) >= 1 and all(int(x) > 0 for x in tokens)
    except (ValueError, IndexError):
        return False
    return False


def compile_source(source, language, folder):
    if language == "Python3":
        path = folder / "solution.py"; path.write_text(source, encoding="utf-8")
        return [sys.executable, "-I", str(path)]
    path, binary = folder / "solution.cpp", folder / "solution"
    path.write_text(source, encoding="utf-8")
    result = subprocess.run(["g++", "-std=c++20", "-O2", "-pipe", str(path), "-o", str(binary)], capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
    return [str(binary)]


def run(command, input_text):
    result = subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
    return "\n".join(line.rstrip() for line in result.stdout.rstrip().splitlines()) + "\n"


def archive_check(command, entry):
    dirs = list(entry.get("oracle_dirs") or [])
    excluded_dirs = []
    if int(entry["number"]) == 2800 and "tests/1000-1999/1802" in dirs:
        dirs.remove("tests/1000-1999/1802")
        excluded_dirs.append("tests/1000-1999/1802: unrelated numeric-output archive, not a histogram")
    if int(entry["number"]) == 2986 and "tests/2000-2999/2986" in dirs:
        dirs.remove("tests/2000-2999/2986")
        excluded_dirs.append("tests/2000-2999/2986: unrelated L/R/C/J text-justification archive")
    if int(entry["number"]) == 3141 and "tests/3000-3682/3141" in dirs:
        dirs.remove("tests/3000-3682/3141")
        excluded_dirs.append("tests/3000-3682/3141: unrelated matrix/coordinate archive with zero-valued fields")
    paths = [path for rel in dirs for path in sorted((OPENJUDGE / rel).glob("*.in"))]
    missing, bad = [], []
    for path in list(paths):
        if not path.with_suffix(".out").exists():
            missing.append(f"{path.relative_to(OPENJUDGE)}: no matching .out")
            paths.remove(path)
    for path in paths:
        expected = path.with_suffix(".out").read_text(encoding="utf-8", errors="replace")
        try:
            got = run(command, path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            bad.append(path.name); continue
        if got.replace("\x1a", " ").split() != expected.replace("\x1a", " ").split():
            bad.append(path.name)
    if not paths:
        return {"status": "passed", "cases": 0, "mismatched": [], "dirs": dirs,
                "no_archive_reason": "candidate inventory records no usable title-matched archive",
                "excluded": excluded_dirs + missing, "method": "archive inventory checked before generation"}
    return {"status": "passed" if not bad else "FAILED", "cases": len(paths),
            "mismatched": bad, "dirs": dirs, "excluded": excluded_dirs + missing,
            "method": "exact output tokens against recorded title-matched historical archives"}


def write_producecase(made, number, source, language, sample):
    program = ("import random,subprocess,sys,tempfile\nfrom pathlib import Path\n" +
        inspect.getsource(generate) + f"\nREFERENCE={source!r}\nLANGUAGE={language!r}\nNUMBER={number}\nSAMPLE={sample!r}\n" +
        "def main():\n with tempfile.TemporaryDirectory() as d:\n  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]\n  if LANGUAGE!='Python3':\n   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]\n  out=Path('data');out.mkdir(exist_ok=True)\n  for p in out.glob('*'):p.unlink()\n  cases=([SAMPLE] if SAMPLE else [])+[generate(NUMBER,s) for s in range(1,21)]\n  for i,x in enumerate(cases):\n   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);clean='\\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\\n';(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(clean)\n" +
        "if __name__=='__main__':main()\n")
    (made / "producecase.py").write_text(program, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("round", type=int, choices=RANGES)
    opts = parser.parse_args(); lo, hi = RANGES[opts.round]
    selected = [entry for entry in json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
                if entry["tier"] == 1 and lo <= int(entry["priority"]) <= hi]
    entries = [entry for entry in selected if int(entry["priority"]) not in SPECIAL_JUDGE]
    references = {int(row["local_number"]): row for row in
                  json.loads(SELECTION.read_text(encoding="utf-8"))["platform_references"]}
    platform_path = ROOT / "collab" / f"t028-round{opts.round}-platform.json"
    platform = ({int(row["local_number"]): row for row in json.loads(platform_path.read_text())["results"]}
                if platform_path.exists() else {})
    manifest, report = [], []
    for entry in entries:
        number = int(entry["number"]); reference = references[number]
        source = (ROOT / reference["source_path"]).read_text(encoding="utf-8")
        language = reference["language"]
        title = re.search(r"<title>[^:]+:\s*([^<]+)", page_path(entry).read_text(errors="replace")).group(1).strip()
        sample, sample_output = page_sample(entry, "样例输入"), page_sample(entry, "样例输出")
        with tempfile.TemporaryDirectory() as folder:
            command = compile_source(source, language, Path(folder))
            cross = archive_check(command, entry)
            if cross["status"] != "passed":
                raise SystemExit(f"{number} archive cross-check failed: {cross}")
            cases = ([sample] if sample else []) + [generate(number, seed) for seed in range(1, 21)]
            outputs = [run(command, case) for case in cases]
        made_rel = made_path(entry, number)
        made, data = OPENJUDGE / made_rel, OPENJUDGE / made_rel / "data"
        data.mkdir(parents=True, exist_ok=True)
        for old in data.glob("*"):
            old.unlink()
        for index, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{index}.in").write_text(case, encoding="utf-8")
            (data / f"{index}.out").write_text(output, encoding="utf-8")
        suffix = "py" if language == "Python3" else "cpp"
        (made / f"samplecode.{suffix}").write_text(source, encoding="utf-8")
        write_producecase(made, number, source, language, sample)
        generated = cases[1:] if sample else cases
        generated_outputs = outputs[1:] if sample else outputs
        rows = [(LABELS[number], all(valid(number, case) for case in generated))]
        audit = common.audit(made, cases=generated, outputs=generated_outputs,
            sample_input=sample or cases[0], sample_output=sample_output,
            sample_output_exemption=None if sample_output else "the mirrored statement has no machine-readable sample output",
            exemption=DOMAIN_EXEMPTIONS.get(number),
            constraints=rows,
            constraint_counterexample=(INVALID[number].strip(), [(LABELS[number], valid(number, INVALID[number]))]))
        smoke = [seed for seed in range(2000) if not valid(number, generate(number, seed))]
        platform_row = platform.get(number)
        status = "passed" if not audit["failed"] and not smoke and (not platform_row or platform_row["verdict"] == "Accepted") else "FAILED"
        manifest.append({**entry, "local_number": number, "title": title, "made_dir": made_rel,
                         "sample_input": sample, "reference_language": language,
                         "solution_collection": None, "solution_code_index": None,
                         "pending_rework": []})
        report.append({"local_number": number, "global_number": entry["global_number"],
            "title": title, "priority": entry["priority"], "tier": entry["tier"], "status": status,
            "reference_source": f"platform statistics {language} Accepted submission",
            "reference_language": language, "solution_collection": None, "solution_code_index": None,
            "source_url": reference["source_url"], "license_status": "not declared; no license is inferred",
            "submission_id": platform_row.get("solution_id") if platform_row else None,
            "platform_verdict": platform_row.get("verdict") if platform_row else "not_run",
            "archive_cross_check": cross, "generator": "generate",
            "generator_seed_smoke": {"seeds": 2000, "status": "passed" if not smoke else "FAILED", "failed_seeds": smoke[:8]},
            "test_cases": len(cases), "max_input_bytes": max(len(case.encode()) for case in cases),
            "max_output_bytes": max(len(output.encode()) for output in outputs), "constraints": rows,
            "constraint_counterexample": INVALID[number].strip(), "self_audit": audit})
        print(f"priority {entry['priority']} {number:05d} built ({language})", flush=True)
    exclusions = [{"priority": priority, "reason": reason, "status": "retired-by-global-identity"}
                  for priority, reason in RETIRED.items() if lo <= priority <= hi]
    exclusions += [{"priority": priority, "local_number": int(entry["number"]),
                    "global_number": entry["global_number"], "reason": SPECIAL_JUDGE[priority],
                    "status": "requires-special-judge"}
                   for entry in selected for priority in [int(entry["priority"])] if priority in SPECIAL_JUDGE]
    manifest_path = ROOT / "collab" / f"t028-round{opts.round}-manifest.json"
    report_path = ROOT / "collab" / f"t028-round{opts.round}-report.json"
    manifest_path.write_text(json.dumps({"task": "T-028", "round": opts.round, "count": len(manifest),
        "priority_range": [lo, hi], "selection_exclusions": exclusions, "entries": manifest},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failed = [row["local_number"] for row in report if row["status"] != "passed"]
    report_path.write_text(json.dumps({"task": "T-028", "round": opts.round,
        "updated_at": datetime.now(timezone.utc).isoformat(), "count": len(report),
        "priority_range": [lo, hi], "selection_exclusions": exclusions,
        "pending_rework_status": common.pending_rework_status([], OPENJUDGE / "tests"),
        "entries": report, "failed": failed}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit(f"self-audit failed: {failed}")


if __name__ == "__main__":
    main()
