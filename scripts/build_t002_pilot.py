#!/usr/bin/env python3
"""Generate the T-002 pilot batch and its deterministic test files."""
import inspect
import random
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "data" / "openjudge" / "tests"


def bucket(n):
    if n < 2000: return "1000-1999"
    if n < 3000: return "2000-2999"
    if n <= 3682: return "3000-3682"
    if n <= 8210: return "4000-8210"
    if n <= 19963: return "10000-19963"
    if n <= 29982: return "20000-29982"
    return "30000-"


def q03468(text):
    it = iter(text.split()); out = []
    while True:
        try: n = int(next(it))
        except StopIteration: break
        v = [int(next(it)) for _ in range(n)]
        total, largest = sum(v), max(v)
        out.append(f"{min(total / 2, total - largest):.1f}")
    return "\n".join(out) + ("\n" if out else "")


def q04117(text):
    out = []
    for token in text.split():
        n = int(token); dp = [0] * (n + 1); dp[0] = 1
        for part in range(1, n + 1):
            for total in range(part, n + 1):
                dp[total] += dp[total - part]
        out.append(str(dp[n]))
    return "\n".join(out) + ("\n" if out else "")


def q04118(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        n, k = int(next(it)), int(next(it))
        pos = [int(next(it)) for _ in range(n)]
        profit = [int(next(it)) for _ in range(n)]
        dp = [0] * n
        for i in range(n):
            dp[i] = profit[i] + max(
                [dp[j] for j in range(i) if pos[i] - pos[j] > k] or [0]
            )
        out.append(str(max(dp)))
    return "\n".join(out) + "\n"


def q04137(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        number, remove = next(it), int(next(it)); stack = []
        for ch in number:
            while stack and remove and stack[-1] > ch:
                stack.pop(); remove -= 1
            stack.append(ch)
        if remove: stack = stack[:-remove]
        out.append("".join(stack).lstrip("0") or "0")
    return "\n".join(out) + "\n"


def q04138(text):
    s = int(text.split()[0]); prime = [True] * (s + 1)
    if s >= 0: prime[0] = False
    if s >= 1: prime[1] = False
    for i in range(2, int(s ** 0.5) + 1):
        if prime[i]:
            for j in range(i * i, s + 1, i): prime[j] = False
    ans = max((p * (s - p) for p in range(2, s)
               if prime[p] and prime[s - p]), default=0)
    return str(ans) + "\n"


def q04146(text):
    n = int(text.split()[0]); ans = 0
    for a in range(n + 1):
        for b in range(n + 1):
            for c in range(n + 1):
                if (a + b) % 2 == 0 and (b + c) % 3 == 0 and (a + b + c) % 5 == 0:
                    ans = max(ans, a + b + c)
    return str(ans) + "\n"


def q04148(text):
    out = []; case = 1
    for line in text.splitlines():
        p, e, i, d = map(int, line.split())
        if (p, e, i, d) == (-1, -1, -1, -1): break
        day = d + 1
        while (day - p) % 23 or (day - e) % 28 or (day - i) % 33:
            day += 1
        out.append(f"Case {case}: the next triple peak occurs in {day - d} days.")
        case += 1
    return "\n".join(out) + ("\n" if out else "")


def q05345(text):
    it = iter(text.split()); n, m = int(next(it)), int(next(it))
    values = [int(next(it)) for _ in range(n)]; out = []
    for _ in range(m):
        op, x = next(it), int(next(it))
        if op == "C": values = [(v + x) % 65536 for v in values]
        else: out.append(str(sum((v >> x) & 1 for v in values)))
    return "\n".join(out) + ("\n" if out else "")


def q05455(text):
    values = list(dict.fromkeys(map(int, text.split())))
    if not values: return ""
    left, right = {}, {}
    for value in values[1:]:
        cur = values[0]
        while True:
            if value < cur:
                if cur not in left: left[cur] = value; break
                cur = left[cur]
            elif value > cur:
                if cur not in right: right[cur] = value; break
                cur = right[cur]
            else: break
    queue = [values[0]]; out = []
    while queue:
        cur = queue.pop(0); out.append(str(cur))
        if cur in left: queue.append(left[cur])
        if cur in right: queue.append(right[cur])
    return " ".join(out) + "\n"


def q06646(text):
    it = iter(text.split()); n = int(next(it))
    children = [(int(next(it)), int(next(it))) for _ in range(n)]
    def depth(node):
        if node == -1: return 0
        left, right = children[node - 1]
        return 1 + max(depth(left), depth(right))
    return str(depth(1)) + "\n"


def q07622(text):
    values = list(map(int, text.split())); n, permutation = values[0], values[1:]
    bit = [0] * (n + 2); answer = 0
    for value in reversed(permutation):
        x = value - 1
        while x:
            answer += bit[x]; x -= x & -x
        x = value
        while x <= n:
            bit[x] += 1; x += x & -x
    return str(answer) + "\n"


def q07810(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        value = next(it)
        out.append("Yes" if int(value) % 19 == 0 or "19" in value else "No")
    return "\n".join(out) + "\n"


def q08581(text):
    preorder = text.strip(); pos = 0; inorder = []; postorder = []
    def visit():
        nonlocal pos
        char = preorder[pos]; pos += 1
        if char == ".": return
        visit(); inorder.append(char); visit(); postorder.append(char)
    visit()
    return "".join(inorder) + "\n" + "".join(postorder) + "\n"


def q09267(text):
    n, m = map(int, text.split()); states = [0] * m; states[0] = 1
    for _ in range(n):
        next_states = [0] * m
        for run, count in enumerate(states):
            next_states[0] += count
            if run + 1 < m: next_states[run + 1] += count
        states = next_states
    return str(sum(states)) + "\n"


def q19757(text):
    it = iter(text.split()); out = []
    while True:
        radius, n = int(next(it)), int(next(it))
        if radius == n == -1: break
        troops = sorted(int(next(it)) for _ in range(n)); index = 0; answer = 0
        while index < n:
            left = troops[index]
            while index < n and troops[index] <= left + radius: index += 1
            marker = troops[index - 1]
            while index < n and troops[index] <= marker + radius: index += 1
            answer += 1
        out.append(str(answer))
    return "\n".join(out) + "\n"


def q22275(text):
    values = list(map(int, text.split())); preorder = values[1:]; postorder = []
    def visit(sequence):
        if not sequence: return
        root = sequence[0]; cut = 1
        while cut < len(sequence) and sequence[cut] < root: cut += 1
        visit(sequence[1:cut]); visit(sequence[cut:]); postorder.append(str(root))
    visit(preorder)
    return " ".join(postorder) + "\n"


def q24637(text):
    values = list(map(int, text.split())); n, treasure = values[0], values[1:]
    dp = [[0, 0] for _ in range(n)]
    for node in range(n - 1, -1, -1):
        left, right = 2 * node + 1, 2 * node + 2
        skip = (max(dp[left]) if left < n else 0) + (max(dp[right]) if right < n else 0)
        take = treasure[node] + (dp[left][0] if left < n else 0) + (dp[right][0] if right < n else 0)
        dp[node] = [skip, take]
    return str(max(dp[0])) + "\n"


def q27217(text):
    n = int(text.split()[0]); catalan = [0] * (n + 1); catalan[0] = 1
    for size in range(1, n + 1):
        catalan[size] = sum(catalan[left] * catalan[size - 1 - left] for left in range(size))
    return str(catalan[n]) + "\n"


def q27880(text):
    values = list(map(int, text.split())); n = values[0]
    edges = [tuple(values[i:i + 3]) for i in range(2, len(values), 3)]
    parent = list(range(n + 1))
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]; node = parent[node]
        return node
    count = largest = 0
    for u, v, cost in sorted(edges, key=lambda edge: edge[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; count += 1; largest = max(largest, cost)
    return f"{count} {largest}\n"


def q19943(text):
    values = list(map(int, text.split())); n = values[0]; matrix = [[0] * n for _ in range(n)]
    for i in range(2, len(values), 2):
        u, v = values[i], values[i + 1]
        matrix[u][u] += 1; matrix[v][v] += 1
        matrix[u][v] -= 1; matrix[v][u] -= 1
    return "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"


def gen_batteries(rng):
    cases = [[3, 5], [3, 3, 5], [2, 2], [1, 9, 9, 9, 9]]
    cases += [[rng.randint(1, 30) for _ in range(rng.randint(2, 8))] for _ in range(8)]
    return "\n".join(str(len(v)) + "\n" + " ".join(map(str, v)) for v in cases) + "\n"


def gen_partitions(rng): return "\n".join(map(str, [1, 2, 3, 4, 5, 10, 20, 50] + [rng.randint(1, 50) for _ in range(12)])) + "\n"


def gen_restaurants(rng):
    cases = [(3, 11, [1, 2, 10], [15, 2, 30]), (4, 2, [1, 4, 7, 10], [5, 8, 4, 10])]
    for _ in range(8):
        n = rng.randint(1, 12); cases.append((n, rng.randint(1, 8), sorted(rng.sample(range(1, 80), n)), [rng.randint(1, 100) for _ in range(n)]))
    lines = [str(len(cases))]
    for n, k, positions, profits in cases:
        lines += [f"{n} {k}", " ".join(map(str, positions)), " ".join(map(str, profits))]
    return "\n".join(lines) + "\n"


def gen_remove(rng):
    cases = [("9128456", 2), ("1444", 3), ("987654321", 4), ("100000001", 2)]
    for _ in range(12):
        size = rng.randint(2, 9)
        cases.append((str(rng.randint(1, 9)) + "".join(str(rng.randint(1, 9)) for _ in range(size - 1)), rng.randint(1, size - 1)))
    return str(len(cases)) + "\n" + "\n".join(f"{n} {k}" for n, k in cases) + "\n"


def gen_prime_sum(rng):
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    p, q = rng.choice(primes), rng.choice(primes)
    return f"{p + q}\n"


def gen_square(rng): return f"{rng.choice([0, 1, 2, 3, 5, 10, 25, 50, 100])}\n"


def gen_peaks(rng):
    lines = []
    for _ in range(10):
        d = rng.randint(0, 365); base = rng.randint(0, 21252)
        lines.append(f"{(base + rng.randint(0, 22)) % 23} {(base + rng.randint(0, 27)) % 28} {(base + rng.randint(0, 32)) % 33} {d}")
    return "\n".join(lines) + "\n-1 -1 -1 -1\n"


def gen_bits(rng):
    n, m = rng.randint(1, 20), rng.randint(20, 60)
    values = [rng.randrange(65536) for _ in range(n)]
    ops = [(rng.choice(["C", "C", "Q"]), rng.randrange(16)) for _ in range(m)]
    return f"{n} {m}\n" + " ".join(map(str, values)) + "\n" + "\n".join(f"{op} {x}" for op, x in ops) + "\n"


def gen_bst_level(rng): return " ".join(map(str, rng.sample(range(1, 200), rng.randint(3, 30)) + [1, 1, 2])) + "\n"


def gen_tree_depth(rng):
    n = rng.randint(1, 10); children = []
    for i in range(1, n + 1):
        options = list(range(i + 1, n + 1)) + [-1]
        children.append((rng.choice(options), rng.choice(options)))
    return str(n) + "\n" + "\n".join(f"{l} {r}" for l, r in children) + "\n"


def gen_permutation(rng):
    n = rng.randint(1, 100); values = list(range(1, n + 1)); rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def gen_prices(rng):
    values = [19, 38, 119, 190, 191, 918, 100, 200, 1000000000] + [rng.randint(1, 2000000000) for _ in range(12)]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def gen_extended_tree(rng):
    def make(depth):
        if depth == 0 or rng.random() < .25: return "."
        return rng.choice("ABCDEFGH") + make(depth - 1) + make(depth - 1)
    return make(5) + "\n"


def gen_nuclear(rng): return f"{rng.randint(2, 49)} {rng.randint(2, 5)}\n"


def gen_saruman(rng):
    lines = []
    for _ in range(8):
        n = rng.randint(1, 30); lines += [f"{rng.randint(0, 20)} {n}", " ".join(map(str, [rng.randint(0, 100) for _ in range(n)]))]
    return "\n".join(lines) + "\n-1 -1\n"


def gen_bst_post(rng):
    n = rng.randint(1, 80); values = list(range(1, n + 1)); rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def gen_treasure(rng):
    n = rng.randint(1, 100); values = [rng.randint(0, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def gen_catalan(rng): return f"{rng.randint(1, 1000)}\n"


def gen_mst(rng):
    n = rng.randint(2, 30); edges = [(i, i + 1, rng.randint(1, 10000)) for i in range(1, n)]
    for _ in range(rng.randint(n, n * 3)):
        u, v = rng.sample(range(1, n + 1), 2); edges.append((u, v, rng.randint(1, 10000)))
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {c}" for u, v, c in edges) + "\n"


def gen_laplacian(rng):
    n = rng.randint(2, 15); edges = [(i, i + 1) for i in range(n - 1)]
    for _ in range(rng.randint(0, n * 2)):
        u, v = rng.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges: edges.append((u, v))
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"


CASES = {
    3468: (q03468, gen_batteries, "2\n3 5\n3\n3 3 5\n", "3.0\n5.5\n"),
    4117: (q04117, gen_partitions, "5\n", "7\n"),
    4118: (q04118, gen_restaurants, "2\n3 11\n1 2 15\n10 2 30\n3 16\n1 2 15\n10 2 30\n", "40\n30\n"),
    4137: (q04137, gen_remove, "2\n9128456 2\n1444 3\n", "12456\n1\n"),
    4138: (q04138, gen_prime_sum, "50\n", "589\n"),
    4146: (q04146, gen_square, "3\n", "5\n"),
    4148: (q04148, gen_peaks, "0 0 0 0\n0 0 0 100\n5 20 34 325\n4 5 6 7\n283 102 23 320\n203 301 203 40\n-1 -1 -1 -1\n", "Case 1: the next triple peak occurs in 21252 days.\nCase 2: the next triple peak occurs in 21152 days.\nCase 3: the next triple peak occurs in 19575 days.\nCase 4: the next triple peak occurs in 16994 days.\nCase 5: the next triple peak occurs in 8910 days.\nCase 6: the next triple peak occurs in 10789 days.\n"),
    5345: (q05345, gen_bits, "3 5\n1 2 4\nQ 1\nQ 2\nC 1\nQ 1\nQ 2\n", "1\n1\n2\n1\n"),
    5455: (q05455, gen_bst_level, "51 45 59 86 45 4 15 76 60 20 61 77 62 30 2 37 13 82 19 74 2 79 79 97 33 90 11 7 29 14 50 1 96 59 91 39 34 6 72 7\n", "51 45 59 4 50 86 2 15 76 97 1 13 20 60 77 90 11 14 19 30 61 82 96 7 29 37 62 79 91 6 33 39 74 34 72\n"),
    6646: (q06646, gen_tree_depth, "3\n2 3\n-1 -1\n-1 -1\n", "2\n"),
    7622: (q07622, gen_permutation, "6\n2 6 3 4 5 1\n", "8\n"),
    7810: (q07810, gen_prices, "4\n95\n100\n3192\n2913\n", "Yes\nNo\nYes\nNo\n"),
    8581: (q08581, gen_extended_tree, "ABD..EF..G..C..\n", "DBFEGAC\nDFGEBCA\n"),
    9267: (q09267, gen_nuclear, "4 3\n", "13\n"),
    19757: (q19757, gen_saruman, "0 3\n10 20 20\n10 7\n70 30 1 7 15 20 50\n-1 -1\n", "2\n4\n"),
    22275: (q22275, gen_bst_post, "5\n4 2 1 3 5\n", "1 3 2 5 4\n"),
    24637: (q24637, gen_treasure, "6\n3 4 5 1 3 1\n", "9\n"),
    27217: (q27217, gen_catalan, "3\n", "5\n"),
    27880: (q27880, gen_mst, "4 5\n1 2 3\n1 4 5\n2 4 7\n2 3 6\n3 4 8\n", "3 6\n"),
    19943: (q19943, gen_laplacian, "4 5\n2 1\n1 3\n2 3\n0 1\n0 2\n", "2 -1 -1 0\n-1 3 -1 -1\n-1 -1 3 -1\n0 -1 -1 2\n"),
}


def write_case(number, solve, generate, sample_in, sample_out):
    assert solve(sample_in).strip() == sample_out.strip(), number
    solve_source = textwrap.dedent(inspect.getsource(solve))
    generate_source = textwrap.dedent(inspect.getsource(generate))
    directory = TESTS / bucket(number) / f"{number:05d}_made"
    data = directory / "data"
    data.mkdir(parents=True, exist_ok=True)
    samplecode = solve_source + "\n\nif __name__ == '__main__':\n    import sys\n    sys.stdout.write(q" + f"{number:05d}" + "(sys.stdin.read()))\n"
    # Keep the production copy self-contained and identical to samplecode's solve.
    producecase = solve_source + "\n\n" + generate_source
    producecase += f'''
import random
from pathlib import Path
SAMPLE_IN = {sample_in!r}
SAMPLE_OUT = {sample_out!r}
assert q{number:05d}(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random({number})
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [gen_{number:05d}(rng) for _ in range(19)]):
    (root / f"{{index}}.in").write_text(content, encoding="utf-8")
    (root / f"{{index}}.out").write_text(q{number:05d}(content), encoding="utf-8")
print("generated 20 cases for {number:05d}")
'''
    # The function names in the source are renamed to avoid collisions in standalone files.
    samplecode = samplecode.replace(f"def q{number:05d}", f"def solve")
    producecase = producecase.replace(f"def q{number:05d}", f"def solve_text")
    producecase = producecase.replace(f"def {generate.__name__}", "def generate_case")
    producecase = producecase.replace(f"q{number:05d}(", "solve_text(")
    producecase = producecase.replace(f"gen_{number:05d}(", "generate_case(")
    samplecode = samplecode.replace("q" + f"{number:05d}" + "(", "solve(")
    (directory / "samplecode.py").write_text(samplecode, encoding="utf-8")
    (directory / "producecase.py").write_text(producecase, encoding="utf-8")
    for old in data.glob("*"): old.unlink()
    rng = random.Random(number)
    for index, content in enumerate([sample_in] + [generate(rng) for _ in range(19)]):
        (data / f"{index}.in").write_text(content, encoding="utf-8")
        (data / f"{index}.out").write_text(solve(content), encoding="utf-8")


def main():
    for number, values in CASES.items():
        write_case(number, *values)
    print(f"built {len(CASES)} pilot packages")


if __name__ == "__main__":
    main()
