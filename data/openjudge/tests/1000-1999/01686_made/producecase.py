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

# ---- 题面契约与 1686 专用生成器 ----
# 题面写“所有运算符的优先级相同，运算次序从左至右”，而原数据（及外部 AC 代码）按常规优先级，
# 二者在 a+b*2 这类写法上结论相反。新数据只生成“两种理解结果一致”的表达式（gen_file 里逐条断言），
# 不论按哪种理解都能得到同一答案。
_ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()+-* \t")
LIM16 = 32767

def _padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0: del r[k]
    return r

def _pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            e = dict(k1)
            for var, ex in k2: e[var] = e.get(var, 0) + ex
            k = tuple(sorted(e.items()))
            r[k] = r.get(k, 0) + v1 * v2
            if r[k] == 0: del r[k]
    return r

def _poly(expr, usual=False):
    """把表达式展开成多项式 {单项式: 系数}；usual=False 按题面（同级、从左至右），True 按常规优先级。语法错抛异常。"""
    toks = [c for c in expr if c not in ' \t']
    pos = [0]
    def peek(): return toks[pos[0]] if pos[0] < len(toks) else None
    def atom():
        c = peek()
        if c is None: raise ValueError
        pos[0] += 1
        if c == '(':
            v = seq()
            if peek() != ')': raise ValueError
            pos[0] += 1; return v
        if c.isdigit(): return {(): int(c)} if c != '0' else {}
        if c.isalpha(): return {((c, 1),): 1}
        raise ValueError
    def apply(op, a, b):
        return _padd(a, b) if op == '+' else _padd(a, b, -1) if op == '-' else _pmul(a, b)
    def term():
        v = atom()
        while peek() == '*':
            pos[0] += 1; v = _pmul(v, atom())
        return v
    def seq():
        if usual:
            v = term()
            while peek() in ('+', '-'):
                op = peek(); pos[0] += 1; v = apply(op, v, term())
            return v
        v = atom()
        while peek() in ('+', '-', '*'):
            op = peek(); pos[0] += 1; v = apply(op, v, atom())
        return v
    v = seq()
    if pos[0] != len(toks): raise ValueError
    return v

def valid(text):
    try:
        if not text.endswith('\n') or '\r' in text: return False
        lines = text[:-1].split('\n')
        if not lines[0].isdigit(): return False
        n = int(lines[0])
        if not 1 <= n <= 20 or len(lines) != 2 * n + 1: return False
        for ln in lines[1:]:
            if not ln.strip() or len(ln) > 80 or set(ln) - _ALLOWED: return False   # 无空行、≤80 字符、字符集
            p = _poly(ln)                                                          # 语法正确（按题面的同级从左至右）
            if any(abs(c) > LIM16 for c in p.values()): return False             # 系数不超过 16 位整数
            if any(ex > LIM16 for k in p for _, ex in k): return False           # 指数不超过 16 位整数
        return True
    except Exception:
        return False

def _solve_text(text):
    lines = text[:-1].split('\n'); out = []
    for i in range(int(lines[0])):
        out.append("YES" if _poly(lines[2 * i + 1]) == _poly(lines[2 * i + 2]) else "NO")
    return "\n".join(out) + "\n"

# AST：叶子为字符串，内部节点为 (op, l, r)
def _show(t, r, ws):
    def sp():
        if ws and r.random() < ws: return r.choice([' ', '\t', '  ', ' \t'])
        return ''
    def go(t, need):
        if isinstance(t, str): s = t
        else:
            op, a, b = t
            la = go(a, op == '*' and not isinstance(a, str) and a[0] in '+-')
            rb = go(b, not isinstance(b, str))
            s = la + sp() + op + sp() + rb
        if need or (not isinstance(t, str) and r.random() < .08) or (isinstance(t, str) and r.random() < .03):
            s = '(' + sp() + s + sp() + ')'
        return s
    return go(t, False)

def _rand_tree(r, size, vars_, digits='123456789'):
    if size <= 1:
        return r.choice(vars_) if vars_ and r.random() < .7 else r.choice(digits)
    k = r.randint(1, size - 1)
    op = r.choice('++--**' if size < 6 else '++--*')
    return (op, _rand_tree(r, k, vars_, digits), _rand_tree(r, size - k, vars_, digits))

def _rewrite(r, t):
    """保持等价的随机变形。"""
    if isinstance(t, str):
        c = r.random()
        if t.isdigit() and t != '0' and int(t) >= 2 and c < .3:
            a = r.randint(1, int(t) - 1); return ('+', str(a), str(int(t) - a))
        if c < .1: return ('*', t, '1') if r.random() < .5 else ('*', '1', t)
        if c < .15: return ('+', t, '0') if r.random() < .5 else ('-', t, '0')
        return t
    op, a, b = t
    if r.random() < .5:
        a = _rewrite(r, a); b = _rewrite(r, b)
    c = r.random()
    if op in '+*' and c < .35: return (op, b, a)
    if op == '*' and c < .55 and not isinstance(b, str) and b[0] in '+-':
        return (b[0], ('*', a, b[1]), ('*', a, b[2]))
    if op == '*' and c < .55 and not isinstance(a, str) and a[0] in '+-':
        return (a[0], ('*', a[1], b), ('*', a[2], b))
    if op == '-' and c < .7 and not isinstance(b, str) and b[0] in '+-':
        return ('-' if b[0] == '+' else '+', ('-', a, b[1]), b[2])
    if op == '+' and c < .7 and not isinstance(b, str) and b[0] in '+-':
        return (b[0], ('+', a, b[1]), b[2])
    if op == '+' and c < .8 and a == b: return ('*', '2', a)
    return (op, a, b)

def _perturb(r, t, vars_):
    if isinstance(t, str):
        c = r.random()
        if t.isalpha() and c < .4: return t.swapcase()
        if t.isdigit() and c < .7: return str((int(t) + r.choice([1, 8])) % 10)
        return r.choice(vars_ + ['1', '2'])
    op, a, b = t
    c = r.random()
    if c < .25: return (r.choice([o for o in '+-*' if o != op]), a, b)
    if c < .35 and op == '-': return (op, b, a)
    if c < .7: return (op, _perturb(r, a, vars_), b)
    return (op, a, _perturb(r, b, vars_))

def _ok(s):
    if len(s) > 80: return False
    p = _poly(s)
    if p != _poly(s, usual=True): return False
    return not (any(abs(c) > LIM16 for c in p.values()) or any(ex > LIM16 for k in p for _, ex in k))

def _pair(r, style):
    while True:
        if style == 'case':
            vars_ = list('aAbB')
        elif style == 'many':
            vars_ = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        else:
            vars_ = r.sample(list('abcdexyzXYZ'), r.randint(1, 4))
        ws = r.choice([0, 0, .15, .5]) if style != 'ws' else .7
        if style == 'power':
            # 高次幂：x 的 k 次方 vs k±1 次方，卡掉随机代 [0,1) 小数再比差值的写法
            v = r.choice('abcxyzAB'); k = r.randint(14, 36)
            e1 = '*'.join([v] * k)
            k2 = k if r.random() < .4 else k + r.choice([-1, 1])
            parts = [v] * k2; e2 = ''
            while parts:
                g = r.randint(1, min(4, len(parts))); grp = '*'.join(parts[:g]); parts = parts[g:]
                e2 = (e2 + '*' if e2 else '') + ('(' + grp + ')' if g > 1 else grp)
            if r.random() < .5: e1, e2 = e2, e1
        elif style == 'const':
            t1 = _rand_tree(r, r.randint(2, 9), [], '0123456789')
            t2 = _rand_tree(r, r.randint(1, 5), [], '0123456789')
            e1, e2 = _show(t1, r, ws), _show(t2, r, ws)
            if r.random() < .5:
                # 找一个数值相同的 t2
                val = _poly(e1).get((), 0)
                if 0 <= val <= 9: e2 = str(val)
                elif -9 <= val < 0: e2 = '0-' + str(-val)
        else:
            t1 = _rand_tree(r, r.randint(1, 12 if style != 'big' else 20), vars_)
            t2 = t1
            for _ in range(r.randint(1, 6)): t2 = _rewrite(r, t2)
            if r.random() < .5:
                t2 = _perturb(r, t2, vars_)
            e1, e2 = _show(t1, r, ws), _show(t2, r, ws)
            if r.random() < .5: e1, e2 = e2, e1
        if e1 and e2 and _ok(e1) and _ok(e2):
            return e1, e2

def gen_file(seed):
    r = random.Random(1686 * 1_000_003 + seed)
    if seed <= 3: styles = ['const']
    elif seed <= 6: styles = ['case']
    elif seed <= 9: styles = ['power']
    elif seed <= 12: styles = ['ws']
    elif seed <= 15: styles = ['many']
    else: styles = ['rand', 'rand', 'big', 'case', 'power', 'ws', 'const', 'many']
    n = 1 if seed in (1, 4) else 20 if seed >= 30 else r.randint(2, 20)
    rows = []
    for _ in range(n): rows += _pair(r, r.choice(styles))
    return f"{n}\n" + "\n".join(rows) + "\n"

REFERENCE='# 参考解（审计时重写）：把两边精确展开成多项式再比较；按题面“同级、从左至右”求值。\n# 生成的数据保证按常规优先级求值结论相同。原外部 AC 代码（samplecode.py）用随机小数代入 eval，\n# 碰上大写变量会 NameError，碰上高次幂会因下溢误判，故不再作为参考解。\nimport sys\ndef padd(p, q, s=1):\n    r = dict(p)\n    for k, v in q.items():\n        r[k] = r.get(k, 0) + s * v\n        if r[k] == 0: del r[k]\n    return r\ndef pmul(p, q):\n    r = {}\n    for k1, v1 in p.items():\n        for k2, v2 in q.items():\n            e = dict(k1)\n            for var, ex in k2: e[var] = e.get(var, 0) + ex\n            k = tuple(sorted(e.items()))\n            r[k] = r.get(k, 0) + v1 * v2\n            if r[k] == 0: del r[k]\n    return r\ndef poly(expr):\n    toks = [c for c in expr if c not in \' \\t\\r\']\n    pos = 0\n    def atom():\n        nonlocal pos\n        c = toks[pos]; pos += 1\n        if c == \'(\':\n            v = seq(); pos += 1; return v\n        if c.isdigit(): return {(): int(c)} if c != \'0\' else {}\n        return {((c, 1),): 1}\n    def seq():\n        nonlocal pos\n        v = atom()\n        while pos < len(toks) and toks[pos] in \'+-*\':\n            op = toks[pos]; pos += 1; w = atom()\n            v = padd(v, w) if op == \'+\' else padd(v, w, -1) if op == \'-\' else pmul(v, w)\n        return v\n    return seq()\nlines = sys.stdin.read().split(\'\\n\')\nn = int(lines[0])\nfor i in range(n):\n    print("YES" if poly(lines[2 * i + 1]) == poly(lines[2 * i + 2]) else "NO")\n'
LANGUAGE='Python3'
NUMBER=1686
SAMPLE='3\n(a+b-c)*2\n(a+a)+(b*2)-(3*c)+c\na*2-(a+c)+((a+c+e)*2)\n3*a+c+(2*e)\n(a-b)*(a-b)\n(a*a)-(2*a*b)-(b*b)\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[gen_file(s) for s in range(1, 40)]
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);clean='\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n';(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(clean)
if __name__=='__main__':main()
