import random,subprocess,sys,tempfile
from pathlib import Path
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

REFERENCE='# 参考解：原先引用的提交（50936084）只枚举上边界 j<i 的行段 j+1..i，漏掉了从第 0 行开始的子矩形，\n# N=1 时输出 -inf；旧生成器靠「第一行全负」把这个缺陷藏住了。这里换成 O(N^3) 的列压缩 + Kadane。\nimport sys\ndata = sys.stdin.buffer.read().split()\nn = int(data[0])\na = list(map(int, data[1:1 + n * n]))\nrows = [a[i * n:(i + 1) * n] for i in range(n)]\nbest = -10 ** 18\nfor top in range(n):\n    col = [0] * n\n    for bot in range(top, n):\n        col = [c + v for c, v in zip(col, rows[bot])]\n        cur = 0\n        m = -10 ** 18\n        for c in col:\n            cur = c if cur < 0 else cur + c\n            if cur > m:\n                m = cur\n        if m > best:\n            best = m\nprint(best)\n'
LANGUAGE='Python3'
NUMBER=1050
SAMPLE='4\n0 -2 -7 0 9 2 -6 2\n-4 1 -4  1 -1\n\n8  0 -2\n'
def valid(text):
    """题面：首行单独一个正整数 N（N 最大 500），随后 N^2 个 [-127,127] 内的整数，以空白（空格、换行）分隔。"""
    lines = text.split("\n")
    first = lines[0].split()
    if len(first) != 1 or not first[0].isdigit():
        return False
    n = int(first[0])
    if not (1 <= n <= 500) or first[0] != str(n):
        return False
    toks = "\n".join(lines[1:]).split()
    if len(toks) != n * n:
        return False
    for t in toks:
        try:
            v = int(t)
        except ValueError:
            return False
        if str(v) != t or not (-127 <= v <= 127):
            return False
    return True

def gen1050(seed):
    """N 取到 400：参考解（纯 Python O(N^3)）在 N=500 约 12s，超过 Python 单组 20s 的一半，故规模组定在 400（约 5s）。"""
    r = random.Random(1050_000 + seed)
    def fmt(n, g, layout):
        if layout == 0:
            body = "\n".join(" ".join(map(str, row)) for row in g)
        else:
            flat = [v for row in g for v in row]; out = []; i = 0
            while i < len(flat):
                k = r.randint(1, 2 * n); out.append(" ".join(map(str, flat[i:i + k]))); i += k
            body = "\n".join(out)
        return f"{n}\n{body}\n"
    def rand_grid(n, lo=-127, hi=127):
        return [[r.randint(lo, hi) for _ in range(n)] for _ in range(n)]
    def plant(n, bias):
        # 背景偏负，种一块偏正的矩形，位置随机（含贴第 0 行、第 0 列、最后一行/列）
        g = [[r.randint(-127, 127 - bias) for _ in range(n)] for _ in range(n)]
        h, w = r.randint(1, n), r.randint(1, n)
        y = r.choice([0, n - h, r.randint(0, n - h)]); x = r.choice([0, n - w, r.randint(0, n - w)])
        for i in range(y, y + h):
            for j in range(x, x + w):
                g[i][j] = r.randint(-127 + bias, 127)
        return g
    fixed = {
        1: (1, [[r.randint(1, 127)]]),
        2: (1, [[-127]]),
        3: (1, [[0]]),
        4: (2, [[-5, -3], [-7, -1]]),
        5: (3, [[127] * 3 for _ in range(3)]),
        6: (2, [[127, -127], [-127, 127]]),
        7: (3, [[5, -1, -1], [-1, -1, -1], [-1, -1, -1]]),   # 最优解只在第 0 行
        8: (4, [[0] * 4 for _ in range(4)]),
    }
    if seed in fixed:
        n, g = fixed[seed]
    elif seed <= 16:
        n = r.randint(2, 10); g = plant(n, r.randint(0, 120)) if seed % 2 else rand_grid(n)
    elif seed <= 20:
        n = r.randint(2, 12); g = rand_grid(n, -127, -1)       # 全负：答案是最大元素
    elif seed <= 24:
        n = r.randint(20, 60); g = plant(n, r.randint(10, 80))
    elif seed <= 28:
        n = r.randint(100, 200); g = plant(n, r.randint(5, 40)) if seed % 2 else rand_grid(n)
    elif seed <= 31:
        n = r.randint(280, 320); g = plant(n, r.randint(5, 30))
    elif seed <= 35:
        n = 400; g = plant(n, r.randint(3, 20)) if seed % 2 else rand_grid(n)
    elif seed == 36:
        n = 400; g = [[127] * n for _ in range(n)]           # 答案 20320000
    elif seed == 37:
        n = 400; g = rand_grid(n, -127, -1); g[0][0] = -1     # 全负，最大元素在左上角
    elif seed == 38:
        n = 400; g = rand_grid(n, -127, -60)
        for j in range(n): g[0][j] = r.randint(50, 127)      # 最优解是整个第 0 行
    else:
        n = 400; g = rand_grid(n, -127, -1); g[n - 1][n - 1] = 127
    return fmt(n, g, seed % 3 == 0)

def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[gen1050(s) for s in range(1, 40)]
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);clean='\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n';(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(clean)
if __name__=='__main__':main()
