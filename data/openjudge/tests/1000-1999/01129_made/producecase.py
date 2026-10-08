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
def _is_planar(n,adj):
    """DMP 路径添加法判定平面性（逐个双连通分量）。adj: list of set。"""
    import sys
    E=sum(len(a) for a in adj)//2
    if n>=3 and E>3*n-6:return False
    # 双连通分量（边集）
    sys.setrecursionlimit(10000)
    disc=[-1]*n;low=[0]*n;t=[0];st=[];blocks=[]
    def dfs(u,p):
        disc[u]=low[u]=t[0];t[0]+=1
        for v in adj[u]:
            if v==p:continue
            if disc[v]<0:
                st.append((u,v));dfs(v,u)
                low[u]=min(low[u],low[v])
                if low[v]>=disc[u]:
                    b=[]
                    while True:
                        e=st.pop();b.append(e)
                        if e==(u,v):break
                    blocks.append(b)
            elif disc[v]<disc[u]:
                st.append((u,v));low[u]=min(low[u],disc[v])
    for s in range(n):
        if disc[s]<0:dfs(s,-1)
    for b in blocks:
        if len(b)<9:continue  # 边数 < 9 的块必为平面（K5 有 10 边，K3,3 有 9 边）
        if not _dmp(b):return False
    return True

def _dmp(edges):
    g={}
    for u,v in edges:
        g.setdefault(u,set()).add(v);g.setdefault(v,set()).add(u)
    V=list(g)
    if len(V)>=3 and len(edges)>3*len(V)-6:return False
    # 找一个环
    par={};start=V[0];stack=[(start,None)];seen=set();cyc=None
    order=[]
    def find_cycle():
        par={start:None};depth={start:0};stk=[start]
        while stk:
            u=stk.pop()
            for v in g[u]:
                if v==par[u]:continue
                if v in par:
                    # 回边 u-v，构造环
                    a,b=u,v;pa=[a];pb=[b]
                    sa={a:0}
                    x=a
                    while par[x] is not None:x=par[x];pa.append(x)
                    sa={x:i for i,x in enumerate(pa)}
                    y=b;pb=[b]
                    while y not in sa:y=par[y];pb.append(y)
                    return pa[:sa[y]+1]+pb[-2::-1]
                par[v]=u;stk.append(v)
        return None
    cyc=find_cycle()
    Hv=set(cyc);He=set()
    for i in range(len(cyc)):
        a,b=cyc[i],cyc[(i+1)%len(cyc)];He.add(frozenset((a,b)))
    faces=[list(cyc),list(cyc)]
    total=len(edges)
    while len(He)<total:
        frags=[]
        for u,v in edges:
            if frozenset((u,v)) not in He and u in Hv and v in Hv:
                frags.append(({u,v},('e',u,v)))
        seenc=set()
        for s in V:
            if s in Hv or s in seenc:continue
            comp={s};stk=[s];att=set()
            while stk:
                x=stk.pop()
                for y in g[x]:
                    if y in Hv:att.add(y)
                    elif y not in comp:comp.add(y);stk.append(y)
            seenc|=comp
            frags.append((att,('c',comp)))
        best=None
        for att,info in frags:
            adm=[i for i,f in enumerate(faces) if att<=set(f)]
            if not adm:return False
            if best is None or len(adm)<len(best[2]):best=(att,info,adm)
            if len(adm)==1:break
        att,info,adm=best;fi=adm[0]
        if info[0]=='e':path=[info[1],info[2]]
        else:
            comp=info[1];a=next(iter(att))
            # BFS 从 a 经 comp 内部到另一个附着点
            prev={a:None};q=[a];end=None
            for x in q:
                for y in g[x]:
                    if x==a and y not in comp:continue
                    if y in comp and y not in prev:prev[y]=x;q.append(y)
                    elif y in Hv and y!=a and x!=a and x in comp:
                        end=(y,x);break
                if end:break
            y,x=end;path=[y]
            while x is not None:path.append(x);x=prev[x]
            path=path[::-1]
        f=faces[fi];u,v=path[0],path[-1]
        i,j=f.index(u),f.index(v);L=len(f)
        def walk(i,j):
            r=[f[i]]
            while i!=j:i=(i+1)%L;r.append(f[i])
            return r
        inner=path[1:-1]
        f1=walk(i,j)+inner[::-1];f2=walk(j,i)+inner
        faces[fi]=f1;faces.append(f2)
        for k in range(len(path)-1):He.add(frozenset((path[k],path[k+1])))
        Hv|=set(path)
    return True

def valid(text):
    """题面契约：多组地图，每组首行中继站数 N（1<=N<=26），随后 N 行，第 i 行形如 X:YZ...，
    X 为第 i 个大写字母，冒号后为前 N 个字母中的相邻站（不含自身、不重复）；相邻关系对称；
    图是平面图；以单独一行 0 结束。"""
    import re
    if not text.endswith('\n'):return False
    lines=text[:-1].split('\n');i=0;maps=0
    while True:
        if i>=len(lines) or not re.fullmatch(r'\d+',lines[i]):return False
        N=int(lines[i]);i+=1
        if N==0:break
        if not 1<=N<=26 or i+N>len(lines):return False
        adj=[set() for _ in range(N)]
        for k in range(N):
            s=lines[i+k]
            if len(s)<2 or s[0]!=chr(65+k) or s[1]!=':':return False
            rest=s[2:]
            if len(set(rest))!=len(rest):return False
            for ch in rest:
                if not('A'<=ch<=chr(64+N)) or ch==s[0]:return False
                adj[k].add(ord(ch)-65)
        i+=N
        if any((k in adj[j])!=(j in adj[k]) for k in range(N) for j in range(N)):return False
        if not _is_planar(N,adj):return False
        maps+=1
    return i==len(lines) and maps>=1

def _fmt1129(n,E):
    adj=[set() for _ in range(n)]
    for u,v in E:adj[u].add(v);adj[v].add(u)
    return f'{n}\n'+''.join(chr(65+i)+':'+''.join(chr(65+j) for j in sorted(adj[i]))+'\n' for i in range(n))

def _geo1129(r,n,keep):
    # 平面上随机整点，按随机顺序（或按长度）尝试加线段，不与已有线段交叉 => 直线平面图
    while True:
        P=list({(r.randint(0,60),r.randint(0,60)) for _ in range(n*2)})[:n]
        if len(P)==n:break
    def cr(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def cross(a,b,c,d):
        return cr(a,b,c)*cr(a,b,d)<0 and cr(c,d,a)*cr(c,d,b)<0
    def through(a,b):
        for q in P:
            if q!=a and q!=b and cr(a,b,q)==0 and min(a[0],b[0])<=q[0]<=max(a[0],b[0]) and min(a[1],b[1])<=q[1]<=max(a[1],b[1]):return True
        return False
    cand=[(i,j) for i in range(n) for j in range(i+1,n)]
    if r.random()<.5:cand.sort(key=lambda e:(P[e[0]][0]-P[e[1]][0])**2+(P[e[0]][1]-P[e[1]][1])**2)
    else:r.shuffle(cand)
    E=[]
    for i,j in cand:
        if through(P[i],P[j]):continue
        if any(cross(P[i],P[j],P[a],P[b]) for a,b in E if len({a,b,i,j})==4):continue
        E.append((i,j))
    E=[e for e in E if r.random()<keep]
    perm=list(range(n));r.shuffle(perm)
    return [(perm[a],perm[b]) for a,b in E]

def _special1129(r,kind,n):
    if kind=='empty':return []
    if kind=='path':return [(i,i+1) for i in range(n-1)]
    if kind=='cycle':return [(i,(i+1)%n) for i in range(n)]
    if kind=='tree':return [(i,r.randrange(i)) for i in range(1,n)]
    if kind=='wheel':return [(0,i) for i in range(1,n)]+[(i,i+1 if i<n-1 else 1) for i in range(1,n)]
    if kind=='grid':
        w=r.randint(2,5);h=n//w;E=[]
        for a in range(h):
            for b in range(w):
                if b<w-1:E.append((a*w+b,a*w+b+1))
                if a<h-1:E.append((a*w+b,(a+1)*w+b))
        return E
    if kind=='apollonian':  # 极大平面 3-树，含 K4
        E={(0,1),(1,2),(0,2)};F=[(0,1,2)];m=3
        while m<n:
            a,b,c=F.pop(r.randrange(len(F)));E|={(a,m),(b,m),(c,m)};F+=[(a,b,m),(b,c,m),(a,c,m)];m+=1
        return list(E)
    raise KeyError(kind)

def _relabel(r,n,E):
    perm=list(range(n));r.shuffle(perm)
    return [(perm[a],perm[b]) for a,b in E]

def gen1129(seed):
    r=random.Random(1129*1000+seed)
    maps=[]
    if seed==1:
        maps=[_fmt1129(1,[]),_fmt1129(2,[(0,1)]),_fmt1129(26,[]),_fmt1129(3,[(0,1),(1,2),(0,2)]),_fmt1129(4,[(a,b) for a in range(4) for b in range(a+1,4)]),_fmt1129(26,_special1129(r,'path',26))]
    elif seed==2:
        maps=[_fmt1129(n,_relabel(r,n,_special1129(r,'cycle',n))) for n in (3,4,5,25,26)]+[_fmt1129(n,_relabel(r,n,_special1129(r,'wheel',n))) for n in (4,5,6,7,25,26)]
    elif seed==3:
        maps=[_fmt1129(26,_relabel(r,26,_special1129(r,k,26))) for k in ('tree','grid','apollonian','apollonian')]+[_fmt1129(24,_relabel(r,24,_special1129(r,'grid',24)))]
    else:
        cnt=r.randint(1,4) if seed<30 else 12
        for _ in range(cnt):
            n=26 if seed>=30 or r.random()<.4 else r.randint(1,26)
            t=r.random()
            if t<.6:E=_geo1129(r,n,r.choice([1,1,.97,.9,.7,.5,.3]))
            else:E=_relabel(r,n,_special1129(r,r.choice(['tree','cycle','wheel','grid','apollonian','path']),n if n>=4 else 4)) if n>=4 else []
            maps.append(_fmt1129(n,E))
    return ''.join(maps)+'0\n'

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01129/statistics/\n# Accepted submission: 52288382\n# Source: http://cs101.openjudge.cn/practice/solution/52288382/\n# License: not declared on the submission page; no license is inferred.\n# 注：原提交的回溯只在全部着色后才检查冲突，n=26 时指数爆炸；改为 DSATUR 剪枝回溯。\n\nimport sys\nsys.setrecursionlimit(10000)\ndef min_channels(n, adj):\n    # DSATUR 回溯：每次选饱和度最大的未着色点，只试与邻居不冲突的颜色\n    for k in range(1, 5):\n        col = [-1] * n\n        def bt(cnt):\n            if cnt == n:\n                return True\n            best = -1; bs = -1; bd = -1\n            for v in range(n):\n                if col[v] < 0:\n                    s = len({col[u] for u in adj[v] if col[u] >= 0})\n                    if s > bs or (s == bs and len(adj[v]) > bd):\n                        best, bs, bd = v, s, len(adj[v])\n            used = {col[u] for u in adj[best]}\n            for c in range(k):\n                if c not in used:\n                    col[best] = c\n                    if bt(cnt + 1):\n                        return True\n            col[best] = -1\n            return False\n        if bt(0):\n            return k\n    return 4\ntok = sys.stdin.read().split()\np = 0\nout = []\nwhile True:\n    n = int(tok[p]); p += 1\n    if n == 0:\n        break\n    adj = [set() for _ in range(n)]\n    for i in range(n):\n        s = tok[p]; p += 1\n        for ch in s.split(\':\', 1)[1]:\n            j = ord(ch) - 65\n            adj[i].add(j); adj[j].add(i)\n    k = min_channels(n, adj)\n    out.append(f"{k} channel needed." if k == 1 else f"{k} channels needed.")\nprint(\'\\n\'.join(out))\n'
LANGUAGE='Python3'
NUMBER=1129
SAMPLE='2\nA:\nB:\n4\nA:BC\nB:ACD\nC:ABD\nD:BC\n4\nA:BCD\nB:ACD\nC:ABD\nD:ABC\n0\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[gen1129(s) for s in range(1, 40)]
  for i,x in enumerate(cases):
   assert valid(x),i
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);clean='\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n';(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(clean)
if __name__=='__main__':main()
