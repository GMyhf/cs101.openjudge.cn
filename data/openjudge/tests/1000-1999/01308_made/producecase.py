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


def valid(text):
    """题面契约：若干组，每组是若干条边（两个 >0 的整数），以 0 0 结束；
    全部输入以一对负整数结束，之后不再有内容。"""
    try:
        toks = [int(t) for t in text.split()]
    except ValueError:
        return False
    if len(toks) % 2:
        return False
    pairs = list(zip(toks[::2], toks[1::2]))
    if not pairs or not (pairs[-1][0] < 0 and pairs[-1][1] < 0):
        return False
    open_case = False
    for a, b in pairs[:-1]:
        if a == 0 and b == 0:
            open_case = False
        elif a > 0 and b > 0:
            open_case = True
        else:
            return False
    return not open_case


def _tree_edges(r, nodes):
    """随机有根树：nodes[0] 为根，其余随机挂父亲（含长链/星形混合）。"""
    edges = []
    for i in range(1, len(nodes)):
        p = i - 1 if r.random() < .3 else r.randrange(i)
        edges.append((nodes[p], nodes[i]))
    return edges


def _labels(r, n, hi):
    return r.sample(range(1, hi + 1), n)


def _make_case(r, kind, n, hi):
    """kind: tree / forest / twoparent / cycle / rootless / selfloop / island。"""
    if kind == "selfloop":
        if n <= 1:
            return [(v := r.randint(1, hi), v)]
        nodes = _labels(r, n, hi); e = _tree_edges(r, nodes)
        v = r.choice(nodes); e.append((v, v))
    elif kind == "tree":
        nodes = _labels(r, n, hi); e = _tree_edges(r, nodes)
    elif kind == "forest":      # 两棵及以上的树：多根
        nodes = _labels(r, n, hi); k = r.randint(1, n - 1)
        e = _tree_edges(r, nodes[:k]) + _tree_edges(r, nodes[k:])
    elif kind == "twoparent":   # 某非根点入度 2；一半再删掉别的入边，使边数 = 点数-1
        nodes = _labels(r, n, hi); e = _tree_edges(r, nodes)
        have = set(e)
        while True:
            a, b = r.randrange(n), r.randrange(1, n)
            if a != b and (nodes[a], nodes[b]) not in have:
                break
        e.append((nodes[a], nodes[b]))
        if n >= 3 and r.random() < .5:
            e.remove(r.choice([x for x in e if x[1] != nodes[b]]))
    elif kind == "cycle":       # 整体无根：纯环，或环上挂树枝
        nodes = _labels(r, n, hi)
        k = n if n < 4 or r.random() < .5 else r.randint(2, n - 1)
        e = [(nodes[i], nodes[(i + 1) % k]) for i in range(k)]
        e += [(nodes[r.randrange(i)], nodes[i]) for i in range(k, n)]
    else:                       # island：一棵树 + 一个独立环；边数 = 点数-1、恰一个入度 0 点、入度都 <=1
        nodes = _labels(r, n, hi); k = r.randint(2, n - 2)
        e = _tree_edges(r, nodes[:k])
        cyc = nodes[k:]
        e += [(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
    r.shuffle(e)
    return e


def _fmt(cases):
    out = []
    for e in cases:
        out.append("\n".join(f"{a} {b}" for a, b in e) + ("\n" if e else "") + "0 0")
    return "\n".join(out) + "\n-1 -1\n"


def gen1308(seed):
    r = random.Random(1308 * 1_000_003 + seed)
    if seed == 1:     # 手工陷阱：空树（首组）、自环、单边、两根、二父、纯环、树+独立环
        return ("0 0\n1 1 0 0\n1 2 0 0\n1 2 3 4 0 0\n1 3 2 3 0 0\n1 2 2 1 0 0\n"
                "1 2 3 4 4 3 0 0\n1 2 2 3 3 4 0 0\n5 5 5 6 0 0\n0 0\n-1 -1\n")
    if seed == 2:     # 首组即非树（参考解曾在此崩溃），再接空树
        return "3 8 6 8 6 4 5 3 5 6 5 2 0 0\n0 0\n1 2 0 0\n-1 -1\n"
    kinds = ["tree", "forest", "twoparent", "cycle", "selfloop", "island"]
    if seed <= 24:    # 多组随机小中规模
        cases = []
        for _ in range(r.randint(3, 12)):
            kind = r.choice(kinds + ["tree", "tree"])
            n = r.randint(4 if kind == "island" else 2, 30)
            cases.append(_make_case(r, kind, n, r.choice([n, 50, 1000])))
        if r.random() < .3: cases.insert(r.randrange(len(cases) + 1), [])
        return _fmt(cases)
    if seed <= 32:    # 中规模，点号可到 1e5
        return _fmt([_make_case(r, kinds[(seed + i) % 6] if i % 2 else "tree", r.randint(500, 3000), 100000)
                     for i in range(r.randint(2, 5))])
    # 大规模单组：长链树 / 随机树 / 各类非树
    n = 60000
    if seed == 33:
        nodes = _labels(r, n, 100000)
        e = [(nodes[i], nodes[i + 1]) for i in range(n - 1)]; r.shuffle(e)
        return _fmt([e])
    kind = ["tree", "island", "twoparent", "cycle", "forest", "selfloop"][seed - 34]
    return _fmt([_make_case(r, kind, n, 100000)])

REFERENCE='# 修正版参考解（审计时替换）：原 Accepted 提交 52642572 在首组于 BFS 前判否时\n# 引用未定义的 visited 而崩溃，且发现重复访问只跳出内层循环；这里按定义重写：\n# 空集是树；否则入度均 <=1、恰一个入度 0 的根、且从根可达全部点。\nimport sys\nfrom collections import defaultdict\n\n\ndef main():\n    t = list(map(int, sys.stdin.read().split()))\n    out = []\n    case = 0\n    edges = []\n    for i in range(0, len(t) - 1, 2):\n        u, v = t[i], t[i + 1]\n        if u < 0 and v < 0:\n            break\n        if u == 0 and v == 0:\n            case += 1\n            ok = True\n            if edges:\n                indeg = defaultdict(int)\n                adj = defaultdict(list)\n                nodes = set()\n                for a, b in edges:\n                    indeg[b] += 1\n                    adj[a].append(b)\n                    nodes.add(a)\n                    nodes.add(b)\n                roots = [x for x in nodes if indeg[x] == 0]\n                if len(roots) != 1 or any(indeg[x] > 1 for x in nodes):\n                    ok = False\n                else:\n                    seen = {roots[0]}\n                    stack = [roots[0]]\n                    while stack:\n                        x = stack.pop()\n                        for y in adj[x]:\n                            if y not in seen:\n                                seen.add(y)\n                                stack.append(y)\n                    ok = len(seen) == len(nodes)\n            out.append(f"Case {case} is {\'a\' if ok else \'not a\'} tree.")\n            edges = []\n        else:\n            edges.append((u, v))\n    print("\\n".join(out))\n\n\nif __name__ == "__main__":\n    main()\n'
LANGUAGE='Python3'
NUMBER=1308
SAMPLE='6 8  5 3  5 2  6 4\n5 6  0 0\n\n8 1  7 3  6 2  8 9  7 5\n7 4  7 8  7 6  0 0\n\n3 8  6 8  6 4\n5 3  5 6  5 2  0 0\n-1 -1\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[gen1308(s) for s in range(1, 40)]
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);clean='\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n';(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(clean)
if __name__=='__main__':main()
