"""Codeforces 题的独立 oracle 库：**按题面重写一遍，不看生成器**。

`scripts/build_codeforces_basic_data.py` 里每道题是一个函数，同一段代码既造输入又算答案。
它算错了，21 组会自洽地全错 —— 组数、去重、输入契约这些判据一条都不会红。
2026-09-20 就是这样抓到 1749C：生成器算的是一个不相干的贪心，21 组里 20 组答案是错的。

所以每道题在这里另写一份实现，`tests/test_expected_outputs.py` 先拿**官方样例**
（`data/openjudge/statements/<题号>.json`，仓外事实）证明这份实现自己没跑偏，再逐组核 `.out`。

两类函数：
  · `ORACLES[题号](输入文本) -> 期望输出文本`   —— 答案唯一，精确比对（空白按 token 归一）。
  · `VERIFIERS[题号](输入文本, 答案文本) -> None|一句话` —— 答案不唯一（特判题），只验合法性与最优性。
"""
import bisect
import collections
import heapq
import math
import re

ORACLES = {}
VERIFIERS = {}


def oracle(problem_id):
    def register(function):
        ORACLES[problem_id] = function
        return function
    return register


def verifier(problem_id):
    def register(function):
        VERIFIERS[problem_id] = function
        return function
    return register


def ints(text):
    return [int(token) for token in text.split()]


def lines(text):
    return text.splitlines()


def is_tree(count, edges):
    parent = list(range(count + 1))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    if len(edges) != count - 1:
        return False
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return len({find(node) for node in range(1, count + 1)}) == 1


# --------------------------------------------------------------------- 批次 1

@oracle("1A")
def oracle_1a(text):
    n, m, a = ints(text)
    return f"{-(-n // a) * -(-m // a)}\n"


@oracle("1B")
def oracle_1b(text):
    rows = lines(text)
    out = []
    for cell in rows[1:1 + int(rows[0])]:
        cell = cell.strip()
        match = re.fullmatch(r"R(\d+)C(\d+)", cell)
        if match:
            row, column = int(match.group(1)), int(match.group(2))
            name = ""
            while column:
                column, remainder = divmod(column - 1, 26)
                name = chr(ord("A") + remainder) + name
            out.append(f"{name}{row}\n")
        else:
            letters = re.match(r"([A-Z]+)(\d+)", cell)
            column = 0
            for char in letters.group(1):
                column = column * 26 + ord(char) - ord("A") + 1
            out.append(f"R{letters.group(2)}C{column}\n")
    return "".join(out)


@oracle("50A")
def oracle_50a(text):
    m, n = ints(text)
    return f"{m * n // 2}\n"


@oracle("58A")
def oracle_58a(text):
    stream = iter(text.strip())
    return ("YES" if all(char in stream for char in "hello") else "NO") + "\n"


@oracle("69A")
def oracle_69a(text):
    values = ints(text)
    n = values[0]
    rows = [values[1 + 3 * index:4 + 3 * index] for index in range(n)]
    balanced = all(sum(row[column] for row in rows) == 0 for column in range(3))
    return ("YES" if balanced else "NO") + "\n"


@oracle("71A")
def oracle_71a(text):
    rows = lines(text)
    out = []
    for word in rows[1:1 + int(rows[0])]:
        word = word.strip()
        out.append((word if len(word) <= 10
                    else f"{word[0]}{len(word) - 2}{word[-1]}") + "\n")
    return "".join(out)


@oracle("96A")
def oracle_96a(text):
    row = text.strip()
    return ("YES" if "0" * 7 in row or "1" * 7 in row else "NO") + "\n"


@oracle("112A")
def oracle_112a(text):
    first, second = lines(text)[:2]
    first, second = first.strip().lower(), second.strip().lower()
    return f"{(first > second) - (first < second)}\n"


# --------------------------------------------------------------------- 批次 2

@oracle("118A")
def oracle_118a(text):
    out = []
    for char in text.strip().lower():
        if char not in "aoyeui":
            out.append("." + char)
    return "".join(out) + "\n"


@oracle("122A")
def oracle_122a(text):
    n = int(text)
    lucky = [value for value in range(1, 1001)
             if set(str(value)) <= {"4", "7"}]
    return ("YES" if any(n % value == 0 for value in lucky) else "NO") + "\n"


@oracle("131A")
def oracle_131a(text):
    word = text.strip()
    if word[1:].isupper() or (len(word) == 1 and word.isupper()):
        return word.swapcase() + "\n"
    return word + "\n"


@oracle("151A")
def oracle_151a(text):
    # 题面第一行是 8 个数：n k l c d p nl np —— 一杯要 nl 毫升饮料和 np 克盐，两者是分开的。
    n, k, liters, limes, slices, salt, per_drink, per_salt = ints(text)
    return f"{min(k * liters // per_drink, limes * slices, salt // per_salt) // n}\n"


@oracle("158A")
def oracle_158a(text):
    rows = lines(text)
    n, k = ints(rows[0])
    scores = ints(rows[1])
    return f"{sum(1 for score in scores if score >= scores[k - 1] and score > 0)}\n"


@oracle("158B")
def oracle_158b(text):
    counts = collections.Counter(ints(text.splitlines()[1]))
    cars = counts[4] + counts[3] + (counts[2] + 1) // 2
    ones = max(0, counts[1] - counts[3])
    if counts[2] % 2:
        ones = max(0, ones - 2)
    return f"{cars + (ones + 3) // 4}\n"


@oracle("160A")
def oracle_160a(text):
    coins = sorted(ints(text.splitlines()[1]), reverse=True)
    total, taken, count = sum(coins), 0, 0
    for coin in coins:
        taken += coin
        count += 1
        if taken > total - taken:
            break
    return f"{count}\n"


@oracle("189A")
def oracle_189a(text):
    n, a, b, c = ints(text)
    best = [0] + [-1] * n
    for length in range(1, n + 1):
        for piece in (a, b, c):
            if piece <= length and best[length - piece] >= 0:
                best[length] = max(best[length], best[length - piece] + 1)
    return f"{best[n]}\n"


def float_verifier(problem_id, compute, tolerance=1e-4):
    """浮点答案：按题面的绝对/相对误差判，不做精确比对。"""
    def verify(text, answer):
        expected = compute(text)
        got = [float(token) for token in answer.split()]
        if len(got) != len(expected):
            return f"答案有 {len(got)} 个数，应为 {len(expected)} 个"
        for index, (value, target) in enumerate(zip(got, expected)):
            if abs(value - target) > tolerance * max(1.0, abs(target)):
                return f"第 {index + 1} 个数是 {value}，应为 {target}（容差 {tolerance}）"
        return None
    VERIFIERS[problem_id] = verify
    return verify


# --------------------------------------------------------------------- 批次 3

float_verifier("200B", lambda text: [sum(ints(text.splitlines()[1]))
                                     / int(text.splitlines()[0])])


@oracle("230A")
def oracle_230a(text):
    values = ints(text)
    strength, n = values[0], values[1]
    dragons = sorted((values[2 + 2 * index], values[3 + 2 * index]) for index in range(n))
    for power, bonus in dragons:
        if strength <= power:
            return "NO\n"
        strength += bonus
    return "YES\n"


def _is_prime(value):
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True


@oracle("230B")
def oracle_230b(text):
    out = []
    for value in ints(text.splitlines()[1]):
        root = math.isqrt(value)
        out.append(("YES" if root * root == value and _is_prime(root) else "NO") + "\n")
    return "".join(out)


@oracle("231A")
def oracle_231a(text):
    values = ints(text)
    n = values[0]
    rows = [values[1 + 3 * index:4 + 3 * index] for index in range(n)]
    return f"{sum(1 for row in rows if sum(row) >= 2)}\n"


@oracle("236A")
def oracle_236a(text):
    name = text.strip()
    return ("CHAT WITH HER!" if len(set(name)) % 2 == 0 else "IGNORE HIM!") + "\n"


@oracle("263A")
def oracle_263a(text):
    values = ints(text)
    index = values.index(1)
    return f"{abs(index // 5 - 2) + abs(index % 5 - 2)}\n"


@oracle("266A")
def oracle_266a(text):
    row = text.splitlines()[1].strip()
    return f"{sum(1 for index in range(1, len(row)) if row[index] == row[index - 1])}\n"


@oracle("281A")
def oracle_281a(text):
    word = text.strip()
    return word[0].upper() + word[1:] + "\n"


# --------------------------------------------------------------------- 批次 4

@oracle("282A")
def oracle_282a(text):
    rows = lines(text)
    value = 0
    for statement in rows[1:1 + int(rows[0])]:
        value += 1 if "+" in statement else -1
    return f"{value}\n"


@oracle("313B")
def oracle_313b(text):
    rows = lines(text)
    row = rows[0].strip()
    prefix = [0] * len(row)
    for index in range(1, len(row)):
        prefix[index] = prefix[index - 1] + (1 if row[index] == row[index - 1] else 0)
    out = []
    for query in rows[2:2 + int(rows[1])]:
        left, right = ints(query)
        out.append(f"{prefix[right - 1] - prefix[left - 1]}\n")
    return "".join(out)


@oracle("339A")
def oracle_339a(text):
    return "+".join(sorted(text.strip().split("+"))) + "\n"


@oracle("339B")
def oracle_339b(text):
    rows = lines(text)
    n, _m = ints(rows[0])
    time, current = 0, 1
    for house in ints(rows[1]):
        time += (house - current) % n
        current = house
    return f"{time}\n"


@oracle("431C")
def oracle_431c(text):
    n, k, d = ints(text)
    mod = 10 ** 9 + 7

    def count(limit):
        ways = [1] + [0] * n
        for total in range(1, n + 1):
            ways[total] = sum(ways[total - step]
                              for step in range(1, min(limit, total) + 1)) % mod
        return ways[n]

    return f"{(count(k) - count(d - 1)) % mod}\n"


@oracle("433B")
def oracle_433b(text):
    rows = lines(text)
    n = int(rows[0])
    values = ints(rows[1])
    ordered = sorted(values)
    plain, sorted_prefix = [0], [0]
    for index in range(n):
        plain.append(plain[-1] + values[index])
        sorted_prefix.append(sorted_prefix[-1] + ordered[index])
    out = []
    for query in rows[3:3 + int(rows[2])]:
        kind, left, right = ints(query)
        table = plain if kind == 1 else sorted_prefix
        out.append(f"{table[right] - table[left - 1]}\n")
    return "".join(out)


@oracle("455A")
def oracle_455a(text):
    counts = collections.Counter(ints(text.splitlines()[1]))
    best = 0
    previous_value, take, skip = 0, 0, 0
    for value in sorted(counts):
        gain = value * counts[value]
        if value == previous_value + 1:
            take, skip = skip + gain, max(take, skip)
        else:
            take, skip = max(take, skip) + gain, max(take, skip)
        previous_value = value
        best = max(take, skip)
    return f"{best}\n"


@oracle("460A")
def oracle_460a(text):
    n, m = ints(text)
    days, socks = 0, n
    while socks:
        days += 1
        socks -= 1
        if days % m == 0:
            socks += 1
    return f"{days}\n"


# --------------------------------------------------------------------- 批次 5

@oracle("460B")
def oracle_460b(text):
    a, b, c = ints(text)
    found = []
    for digit_sum in range(1, 82):          # 10^9 以内的数字和最多 81
        value = b * digit_sum ** a + c
        if 0 < value < 10 ** 9 and sum(int(char) for char in str(value)) == digit_sum:
            found.append(value)
    found.sort()
    return f"{len(found)}\n" + " ".join(map(str, found)) + "\n"


@oracle("466A")
def oracle_466a(text):
    n, m, a, b = ints(text)
    return f"{min(n * a, -(-n // m) * b, n // m * b + (n % m) * a)}\n"


@oracle("466C")
def oracle_466c(text):
    values = ints(text.splitlines()[1])
    total = sum(values)
    if total % 3:
        return "0\n"
    part = total // 3
    prefix, ways, seen = 0, 0, 0
    for index, value in enumerate(values):
        prefix += value
        if index + 1 < len(values) and prefix == 2 * part:
            ways += seen
        if prefix == part:
            seen += 1
    return f"{ways}\n"


@oracle("474A")
def oracle_474a(text):
    rows = lines(text)
    keyboard = "qwertyuiopasdfghjkl;zxcvbnm,./"
    shift = -1 if rows[0].strip() == "R" else 1
    typed = rows[1].strip()
    return "".join(keyboard[keyboard.index(char) + shift] for char in typed) + "\n"


@oracle("474D")
def oracle_474d(text):
    rows = lines(text)
    t, k = ints(rows[0])
    limit = 10 ** 5
    mod = 10 ** 9 + 7
    ways = [0] * (limit + 1)
    ways[0] = 1
    for length in range(1, limit + 1):
        ways[length] = (ways[length - 1] + (ways[length - k] if length >= k else 0)) % mod
    prefix = [0] * (limit + 1)
    for length in range(1, limit + 1):
        prefix[length] = (prefix[length - 1] + ways[length]) % mod
    out = []
    for query in rows[1:1 + t]:
        a, b = ints(query)
        out.append(f"{(prefix[b] - prefix[a - 1]) % mod}\n")
    return "".join(out)


@oracle("479A")
def oracle_479a(text):
    a, b, c = ints(text)
    return f"{max(a + b + c, a * b * c, (a + b) * c, a * (b + c), a + b * c, a * b + c)}\n"


@oracle("489B")
def oracle_489b(text):
    rows = lines(text)
    boys = sorted(ints(rows[1]))
    girls = sorted(ints(rows[3]))
    pairs = i = j = 0
    while i < len(boys) and j < len(girls):
        if abs(boys[i] - girls[j]) <= 1:
            pairs += 1
            i += 1
            j += 1
        elif boys[i] < girls[j]:
            i += 1
        else:
            j += 1
    return f"{pairs}\n"


def _radius_492b(text):
    rows = lines(text)
    _n, length = ints(rows[0])
    points = sorted(ints(rows[1]))
    best = max(points[0], length - points[-1])
    for index in range(1, len(points)):
        best = max(best, (points[index] - points[index - 1]) / 2)
    return [float(best)]


float_verifier("492B", _radius_492b, tolerance=1e-9)


# --------------------------------------------------------------------- 批次 6

@oracle("508A")
def oracle_508a(text):
    values = ints(text)
    n, m, k = values[0], values[1], values[2]
    grid = [[False] * (m + 2) for _ in range(n + 2)]
    for move in range(k):
        row, column = values[3 + 2 * move], values[4 + 2 * move]
        grid[row][column] = True
        for top in (row - 1, row):
            for left in (column - 1, column):
                if (top >= 1 and left >= 1 and grid[top][left] and grid[top + 1][left]
                        and grid[top][left + 1] and grid[top + 1][left + 1]):
                    return f"{move + 1}\n"
    return "0\n"


@oracle("545C")
def oracle_545c(text):
    values = ints(text)
    n = values[0]
    trees = [(values[1 + 2 * index], values[2 + 2 * index]) for index in range(n)]
    cut, previous = 0, float("-inf")
    for index, (position, height) in enumerate(trees):
        if position - height > previous:
            cut += 1
            previous = position
        elif index + 1 == n or position + height < trees[index + 1][0]:
            cut += 1
            previous = position + height
        else:
            previous = position
    return f"{cut}\n"


@oracle("545D")
def oracle_545d(text):
    served, waited = 0, 0
    for time in sorted(ints(text.splitlines()[1])):
        if waited <= time:
            served += 1
            waited += time
    return f"{served}\n"


@oracle("579A")
def oracle_579a(text):
    return f"{bin(int(text)).count('1')}\n"


@oracle("705A")
def oracle_705a(text):
    n = int(text)
    pieces = ["I hate" if index % 2 == 0 else "I love" for index in range(n)]
    return " that ".join(pieces) + " it\n"


@oracle("706B")
def oracle_706b(text):
    rows = lines(text)
    prices = sorted(ints(rows[1]))
    out = []
    for budget in rows[3:3 + int(rows[2])]:
        out.append(f"{bisect.bisect_right(prices, int(budget))}\n")
    return "".join(out)


@oracle("723A")
def oracle_723a(text):
    points = ints(text)
    return f"{max(points) - min(points)}\n"


@oracle("803A")
def oracle_803a(text):
    n, k = ints(text)
    if k > n * n:
        return "-1\n"
    grid = [[0] * n for _ in range(n)]
    for row in range(n):
        if k <= 0:
            break
        for column in range(row, n):
            if k <= 0:
                break
            if row == column:
                grid[row][column] = 1
                k -= 1
            elif k >= 2:
                grid[row][column] = grid[column][row] = 1
                k -= 2
            else:                      # 只剩 1 个，放到下一行的对角线上才对称
                if row + 1 < n:
                    grid[row + 1][row + 1] = 1
                k -= 1
                break
    return "".join(" ".join(map(str, line)) + "\n" for line in grid)


# --------------------------------------------------------------------- 批次 7

@oracle("893C")
def oracle_893c(text):
    rows = lines(text)
    n, m = ints(rows[0])
    costs = ints(rows[1])
    parent = list(range(n))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for row in rows[2:2 + m]:
        x, y = ints(row)
        a, b = find(x - 1), find(y - 1)
        if a != b:
            parent[a] = b
    cheapest = {}
    for index in range(n):
        root = find(index)
        cheapest[root] = min(cheapest.get(root, costs[index]), costs[index])
    return f"{sum(cheapest.values())}\n"


@oracle("996A")
def oracle_996a(text):
    value, bills = int(text), 0
    for note in (100, 20, 10, 5, 1):
        bills += value // note
        value %= note
    return f"{bills}\n"


@oracle("1000B")
def oracle_1000b(text):
    rows = lines(text)
    n, moment = ints(rows[0])
    bounds = [0] + ints(rows[1]) + [moment]
    segments = [bounds[index + 1] - bounds[index] for index in range(len(bounds) - 1)]
    lit_prefix, dark_suffix = [0], [0] * (len(segments) + 1)
    for index, length in enumerate(segments):
        lit_prefix.append(lit_prefix[-1] + (length if index % 2 == 0 else 0))
    for index in range(len(segments) - 1, -1, -1):
        dark_suffix[index] = dark_suffix[index + 1] + (segments[index] if index % 2 else 0)
    best = lit_prefix[-1]
    for index, length in enumerate(segments):
        if length >= 2:
            best = max(best, lit_prefix[index] + length - 1 + dark_suffix[index + 1])
    return f"{best}\n"


@verifier("1154A")
def verify_1154a(text, answer):
    """题面：a、b、c **任意顺序**都算对 —— 只能验合法性。

    这也意味着这道题在 token 精确比对下会误杀正确程序（见 2026-09-20 的复核记录）。
    """
    board = sorted(ints(text))
    got = ints(answer)
    if len(got) != 3 or any(value <= 0 for value in got):
        return f"应输出三个正整数，实际 {got}"
    a, b, c = got
    produced = sorted([a + b, a + c, b + c, a + b + c])
    if produced != board:
        return f"{got} 造不出黑板上的 {board}（它给出 {produced}）"
    return None


@oracle("1163B2")
def oracle_1163b2(text):
    values = ints(text.splitlines()[1])
    counts = collections.Counter()
    by_count = collections.Counter()
    best = 1
    for day, value in enumerate(values, 1):
        previous = counts[value]
        if previous:
            by_count[previous] -= 1
            if not by_count[previous]:
                del by_count[previous]
        counts[value] = previous + 1
        by_count[previous + 1] += 1
        if len(by_count) == 1:
            only = next(iter(by_count))
            if only == 1 or by_count[only] == 1:
                best = day
        elif len(by_count) == 2:
            low, high = sorted(by_count)
            if (low == 1 and by_count[low] == 1) or (high == low + 1 and by_count[high] == 1):
                best = day
    return f"{best}\n"


@oracle("1195C")
def oracle_1195c(text):
    rows = lines(text)
    top, bottom = ints(rows[1]), ints(rows[2])
    none = first = second = 0
    for a, b in zip(top, bottom):
        none, first, second = (max(none, first, second),
                               max(none, second) + a,
                               max(none, first) + b)
    return f"{max(none, first, second)}\n"


@oracle("1221A")
def oracle_1221a(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        multiset = values[position + 1:position + 1 + n]
        position += 1 + n
        out.append(("YES" if sum(value for value in multiset if value <= 2048) >= 2048
                    else "NO") + "\n")
    return "".join(out)


@oracle("1327A")
def oracle_1327a(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        n, k = values[1 + 2 * index], values[2 + 2 * index]
        out.append(("YES" if n >= k * k and n % 2 == k % 2 else "NO") + "\n")
    return "".join(out)


# 只靠单题流水线自带的暴力 oracle（加上本仓新加的官方样例锚点 `tests/test_rebuilt_anchors.py`）
# 的题。这里不重写一份高效解：这些都是 Div1 量级的构造/计数题，重写的出错概率高于收益，
# 而它们各自的 `producecase.py` 里本来就有一份**算法不同的暴力**在小规模上逐组比过。
# 写下来是为了让「没重写」是一个**记录**，不是一个空白。
PIPELINE_ONLY = {
    "2146D1": "producecase.py 的 `oracle` 用匈牙利算法验证 r*(r+1) 这个上界可达；构造本身走 checker.py。",
    "2167F": "producecase.py 有两份实现：`oracle_exhaustive`（枚举所有 k 元子集求 LCA）与 "
             "`oracle_quadratic`，小规模逐组互核。",
    "2171G": "producecase.py 有 `bfs_oracle` / `k0_oracle` / `dp_x_oracle` 三份，小规模互核。",
    "2192D": "producecase.py 的 `brute` 是 O(n^4) 的字面模拟（枚举 r、u、v 重建父数组），n<=12 的组逐组比。",
    "2194E": "producecase.py 的 `brute` 枚举全部路径与拦截点。",
    "2195E": "producecase.py 的 `simulate` 逐步模拟 Idiot First Search，小树逐组比。",
    "2195H": "producecase.py 的 `brute_valid` 逐三角形验面积与不相交，并跑自带 checker。",
    "2205D": "producecase.py 的 `brute` 枚举删除顺序求最少操作数。",
    "2208D1": "producecase.py 的 `all_tree_matrices` 枚举小树的全部定向，`check_output` 验构造。",
    "2218G": "producecase.py 的 `tally` 按题面定义直接数方案数。",
    "2227F": "producecase.py 的 `oracle_one`/`metric` 按题面重新模拟重力并累加移动距离。",
    "2227H": "producecase.py 的 `brute_one` 枚举小树上的全部情形。",
    "2228D": "producecase.py 的 `brute_one` 枚举所有 (k1,k2) 与染色。",
}

# 没有 oracle 的题，必须在这里写明理由（`tests/test_expected_outputs.py` 的覆盖率用例盯着）。
UNCOVERED = {
    "2109C1": "交互题：判题走 interactor.py，`.out` 不参与比对。",
    "2109C2": "交互题：同上。",
    "2109C3": "交互题：同上。",
    "2173E": "交互题：判题走 interactor.py（自适应对手），`.out` 不参与比对。",
    "2209C": "交互题：判题走 interactor.py，`.out` 不参与比对。",
    "1833B": "题面「若有多解，输出任意一组」，数据里的 .out 是空的 —— 判题走 "
             "`weather_permutation` 特判，只看提交的排列本身。",
    "20C": "题面「若有多解，输出任意一条」，数据里的 .out 是空的 —— 判题走 "
           "`shortest_path` 特判，只看提交的路径本身，期望输出不参与比对。",
}


# --------------------------------------------------------------------- 批次 8

def _roots_20b(text):
    a, b, c = ints(text)
    if a == 0 and b == 0:
        return [-1.0] if c == 0 else [0.0]
    if a == 0:
        return [1.0, -c / b]
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return [0.0]
    if discriminant == 0:
        return [1.0, -b / (2 * a)]
    root = math.sqrt(discriminant)
    values = sorted(((-b - root) / (2 * a), (-b + root) / (2 * a)))
    return [2.0, values[0], values[1]]


float_verifier("20B", _roots_20b, tolerance=1e-6)


@oracle("580A")
def oracle_580a(text):
    values = ints(text.splitlines()[1])
    best = run = 1
    for index in range(1, len(values)):
        run = run + 1 if values[index] >= values[index - 1] else 1
        best = max(best, run)
    return f"{best}\n"


@oracle("1328A")
def oracle_1328a(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        a, b = values[1 + 2 * index], values[2 + 2 * index]
        out.append(f"{(-a) % b}\n")
    return "".join(out)


@oracle("1335A")
def oracle_1335a(text):
    values = ints(text)
    return "".join(f"{(n - 1) // 2}\n" for n in values[1:1 + values[0]])


@oracle("1352C")
def oracle_1352c(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        n, k = values[1 + 2 * index], values[2 + 2 * index]
        out.append(f"{k + (k - 1) // (n - 1)}\n")
    return "".join(out)


@oracle("1364A")
def oracle_1364a(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n, x = values[position], values[position + 1]
        row = values[position + 2:position + 2 + n]
        position += 2 + n
        if sum(row) % x:
            out.append(f"{n}\n")
            continue
        left = next((index for index, value in enumerate(row) if value % x), None)
        if left is None:
            out.append("-1\n")
            continue
        right = next(index for index in range(n - 1, -1, -1) if row[index] % x)
        out.append(f"{max(n - left - 1, right)}\n")
    return "".join(out)


@oracle("2033D")
def oracle_2033d(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        seen, prefix, count = {0}, 0, 0
        for value in row:
            prefix += value
            if prefix in seen:
                count += 1
                seen = {0}
                prefix = 0
            else:
                seen.add(prefix)
        out.append(f"{count}\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 9

@verifier("584A")
def verify_584a(text, answer):
    """n 位、能被 t 整除的正整数，**任意一个都算对**。"""
    n, t = ints(text)
    tokens = answer.split()
    if tokens == ["-1"]:
        return None if (n == 1 and t == 10) else "存在合法答案，不该输出 -1"
    if len(tokens) != 1 or not tokens[0].isdigit():
        return f"应输出一个正整数，实际 {tokens}"
    value = tokens[0]
    if len(value) != n:
        return f"{value} 是 {len(value)} 位，题面要 {n} 位"
    if value[0] == "0":
        return f"{value} 有前导零"
    if int(value) % t:
        return f"{value} 不能被 {t} 整除"
    return None


@verifier("1366D")
def verify_1366d(text, answer):
    """每个 a_i 给两个 >1 的因子，和与 a_i 互质；无解输出 -1 -1。答案不唯一。"""
    rows = lines(text)
    values = ints(rows[1])
    got = answer.split("\n")
    first, second = ints(got[0]), ints(got[1]) if len(got) > 1 else []
    if len(first) != len(values) or len(second) != len(values):
        return f"两行各应有 {len(values)} 个数"
    for value, d1, d2 in zip(values, first, second):
        distinct = set()
        temp, factor = value, 2
        while factor * factor <= temp:
            while temp % factor == 0:
                distinct.add(factor)
                temp //= factor
            factor += 1
        if temp > 1:
            distinct.add(temp)
        if d1 == -1 and d2 == -1:
            if len(distinct) >= 2:
                return f"{value} 有 {len(distinct)} 个不同质因子，存在合法答案"
            continue
        if d1 <= 1 or d2 <= 1 or value % d1 or value % d2:
            return f"{value}: {d1},{d2} 不是大于 1 的因子"
        if math.gcd(d1 + d2, value) != 1:
            return f"{value}: gcd({d1}+{d2}, {value}) != 1"
    return None


@oracle("1398C")
def oracle_1398c(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        digits = rows[index + 1].strip()
        index += 2
        seen = collections.Counter({0: 1})
        prefix, total = 0, 0
        for char in digits:
            prefix += int(char) - 1
            total += seen[prefix]
            seen[prefix] += 1
        out.append(f"{total}\n")
    return "".join(out)


@oracle("1425A")
def oracle_1425a(text):
    values = ints(text)
    out = []
    for coins in values[1:1 + values[0]]:
        mine, turn = 0, 0
        while coins:
            # n/2 为奇数时取一半；n 是 2 或 4 是两个例外（与 n<=2*10^5 的精确 DP 逐个核过）。
            if coins % 2 == 0 and ((coins // 2) % 2 == 1 or coins in (2, 4)):
                take = coins // 2
            else:
                take = 1
            if turn == 0:
                mine += take
            coins -= take
            turn ^= 1
        out.append(f"{mine}\n")
    return "".join(out)


@oracle("1427B")
def oracle_1427b(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        n, k = ints(rows[index])
        games = rows[index + 1].strip()
        index += 2
        wins = games.count("W")
        if wins == 0:
            out.append(f"{0 if k == 0 else 2 * k - 1}\n")
            continue
        if wins + k >= n:
            out.append(f"{2 * n - 1}\n")
            continue
        blocks = [block for block in games.split("L") if block]
        score = 2 * wins - len(blocks)
        gaps = sorted(len(gap) for gap in re.findall(r"(?<=W)L+(?=W)", games))
        for gap in gaps:
            if k >= gap:
                k -= gap
                score += 2 * gap + 1
            else:
                break
        out.append(f"{score + 2 * k}\n")
    return "".join(out)


@oracle("1443C")
def oracle_1443c(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        courier = values[position + 1:position + 1 + n]
        pickup = values[position + 1 + n:position + 1 + 2 * n]
        position += 1 + 2 * n
        low, high = 0, max(courier)
        while low < high:
            middle = (low + high) // 2
            if sum(b for a, b in zip(courier, pickup) if a > middle) <= middle:
                high = middle
            else:
                low = middle + 1
        out.append(f"{low}\n")
    return "".join(out)


@oracle("1526C1")
def oracle_1526c1(text):
    values = ints(text.splitlines()[1])
    health, taken = 0, []
    for value in values:
        heapq.heappush(taken, value)
        health += value
        if health < 0:
            health -= heapq.heappop(taken)
    return f"{len(taken)}\n"


@verifier("1729C")
def verify_1729c(text, answer):
    """最小代价 + 最多经过的瓷砖；路径本身不唯一。"""
    rows = lines(text)
    got = answer.split("\n")
    index, cursor = 1, 0
    for _ in range(int(rows[0])):
        word = rows[index].strip()
        index += 1
        cost, count = ints(got[cursor])
        path = ints(got[cursor + 1])
        cursor += 2
        if cost != abs(ord(word[0]) - ord(word[-1])):
            return f"{word}: 代价应为 {abs(ord(word[0]) - ord(word[-1]))}"
        low, high = sorted((word[0], word[-1]))
        expected = sum(1 for char in word if low <= char <= high)
        if count != expected or len(path) != count:
            return f"{word}: 最多经过 {expected} 块，答案写了 {count}/{len(path)}"
        if len(set(path)) != count or path[0] != 1 or path[-1] != len(word):
            return f"{word}: 路径必须两两不同、从 1 开始、到 {len(word)} 结束"
        letters = [word[position - 1] for position in path]
        if letters != sorted(letters, reverse=word[0] > word[-1]):
            return f"{word}: 路径上的字母必须单调走向终点"
        if sum(abs(ord(letters[i]) - ord(letters[i - 1]))
               for i in range(1, len(letters))) != cost:
            return f"{word}: 路径实际代价与声明的 {cost} 不符"
    return None


# --------------------------------------------------------------------- 批次 10

@oracle("1829E")
def oracle_1829e(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n, m = values[position], values[position + 1]
        position += 2
        grid = [values[position + row * m:position + (row + 1) * m] for row in range(n)]
        position += n * m
        seen = [[False] * m for _ in range(n)]
        best = 0
        for row in range(n):
            for column in range(m):
                if seen[row][column] or grid[row][column] == 0:
                    continue
                stack, total = [(row, column)], 0
                seen[row][column] = True
                while stack:
                    r, c = stack.pop()
                    total += grid[r][c]
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < m and not seen[nr][nc] and grid[nr][nc]:
                            seen[nr][nc] = True
                            stack.append((nr, nc))
                best = max(best, total)
        out.append(f"{best}\n")
    return "".join(out)


@oracle("1843D")
def oracle_1843d(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        position += 1
        graph = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = values[position], values[position + 1]
            position += 2
            graph[u].append(v)
            graph[v].append(u)
        leaves = [0] * (n + 1)
        order, parent, stack = [], [0] * (n + 1), [1]
        seen = {1}
        while stack:
            node = stack.pop()
            order.append(node)
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    parent[nxt] = node
                    stack.append(nxt)
        for node in reversed(order):
            if leaves[node] == 0:
                leaves[node] = 1
            if node != 1:
                leaves[parent[node]] += leaves[node]
        queries = values[position]
        position += 1
        for _ in range(queries):
            x, y = values[position], values[position + 1]
            position += 2
            out.append(f"{leaves[x] * leaves[y]}\n")
    return "".join(out)


@verifier("1868A")
def verify_1868a(text, answer):
    """最大 beauty + 一个达到它的矩阵；矩阵不唯一。"""
    values = ints(text)
    tokens = answer.split()
    position, cursor = 1, 0
    for _ in range(values[0]):
        n, m = values[position], values[position + 1]
        position += 2
        claimed = int(tokens[cursor])
        cursor += 1
        best = 0 if m == 1 else min(n + 1, m)
        if claimed != best:
            return f"n={n} m={m}: 最大 beauty 是 {best}，答案写了 {claimed}"
        matrix = []
        for _row in range(n):
            row = [int(value) for value in tokens[cursor:cursor + m]]
            cursor += m
            if sorted(row) != list(range(m)):
                return f"n={n} m={m}: 每行必须是 0..m-1 的排列"
            matrix.append(row)
        column_mex = []
        for column in range(m):
            present = {matrix[row][column] for row in range(n)}
            mex = 0
            while mex in present:
                mex += 1
            column_mex.append(mex)
        present = set(column_mex)
        beauty = 0
        while beauty in present:
            beauty += 1
        if beauty != claimed:
            return f"n={n} m={m}: 给出的矩阵 beauty 是 {beauty}，不是 {claimed}"
    return None


@oracle("1875D")
def oracle_1875d(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        counts = collections.Counter(row)
        mex = 0
        while counts[mex]:
            mex += 1
        best = [0] * (mex + 1)
        for value in range(1, mex + 1):
            best[value] = min((counts[lower] - 1) * value + lower + best[lower]
                              for lower in range(value))
        out.append(f"{best[mex]}\n")
    return "".join(out)


@oracle("1879B")
def oracle_1879b(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        a = values[position + 1:position + 1 + n]
        b = values[position + 1 + n:position + 1 + 2 * n]
        position += 1 + 2 * n
        out.append(f"{min(min(a) * n + sum(b), min(b) * n + sum(a))}\n")
    return "".join(out)


@oracle("1881C")
def oracle_1881c(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        n = int(rows[index])
        grid = [row.strip() for row in rows[index + 1:index + 1 + n]]
        index += 1 + n
        total = 0
        for row in range(n // 2):
            for column in range(n // 2):
                orbit = [grid[row][column], grid[column][n - 1 - row],
                         grid[n - 1 - row][n - 1 - column], grid[n - 1 - column][row]]
                highest = max(orbit)
                total += sum(ord(highest) - ord(char) for char in orbit)
        out.append(f"{total}\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 11

@oracle("1985H1")
def oracle_1985h1(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        n, m = ints(rows[index])
        grid = [row.strip() for row in rows[index + 1:index + 1 + n]]
        index += 1 + n
        component = [[-1] * m for _ in range(n)]
        sizes = []
        for row in range(n):
            for column in range(m):
                if grid[row][column] != "#" or component[row][column] >= 0:
                    continue
                label, stack, size = len(sizes), [(row, column)], 0
                component[row][column] = label
                while stack:
                    r, c = stack.pop()
                    size += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < n and 0 <= nc < m and grid[nr][nc] == "#"
                                and component[nr][nc] < 0):
                            component[nr][nc] = label
                            stack.append((nr, nc))
                sizes.append(size)
        best = max(sizes) if sizes else 0
        for row in range(n):
            touched = {component[r][c] for r in range(max(0, row - 1), min(n, row + 2))
                       for c in range(m) if component[r][c] >= 0}
            inside = collections.Counter(component[row][c] for c in range(m)
                                         if component[row][c] >= 0)
            best = max(best, m + sum(sizes[label] - inside[label] for label in touched))
        for column in range(m):
            touched = {component[r][c] for r in range(n)
                       for c in range(max(0, column - 1), min(m, column + 2))
                       if component[r][c] >= 0}
            inside = collections.Counter(component[r][column] for r in range(n)
                                         if component[r][column] >= 0)
            best = max(best, n + sum(sizes[label] - inside[label] for label in touched))
        out.append(f"{best}\n")
    return "".join(out)


@oracle("2075C")
def oracle_2075c(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n, m = values[position], values[position + 1]
        limits = sorted(values[position + 2:position + 2 + m])
        position += 2 + m

        def at_least(bound):
            return m - bisect.bisect_left(limits, bound)

        total = 0
        for left in range(1, n):
            right = n - left
            total += at_least(left) * at_least(right) - at_least(max(left, right))
        out.append(f"{total}\n")
    return "".join(out)


@oracle("2131C")
def oracle_2131c(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n, k = values[position], values[position + 1]
        source = values[position + 2:position + 2 + n]
        target = values[position + 2 + n:position + 2 + 2 * n]
        position += 2 + 2 * n
        # x -> x+k 与 x -> |x-k| 保持 min(x mod k, k - x mod k) 不变，也只保持它不变。
        signature = lambda row: sorted(min(value % k, (k - value % k) % k) for value in row)
        out.append(("YES" if signature(source) == signature(target) else "NO") + "\n")
    return "".join(out)


@oracle("2132B")
def oracle_2132b(text):
    values = ints(text)
    out = []
    for n in values[1:1 + values[0]]:
        found = []
        power = 10
        while 1 + power <= n:
            if n % (1 + power) == 0:
                found.append(n // (1 + power))
            power *= 10
        found.sort()
        out.append(f"{len(found)}\n" + (" ".join(map(str, found)) + "\n" if found else ""))
    return "".join(out)


@oracle("2193E")
def oracle_2193e(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = set(values[position + 1:position + 1 + n])
        position += 1 + n
        best = [-1] * (n + 1)
        queue = collections.deque()
        for value in sorted(row):
            if value <= n and best[value] < 0:
                best[value] = 1
                queue.append(value)
        while queue:
            current = queue.popleft()
            for value in row:
                nxt = current * value
                if nxt <= n and best[nxt] < 0:
                    best[nxt] = best[current] + 1
                    queue.append(nxt)
        out.append(" ".join(str(best[index]) for index in range(1, n + 1)) + "\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 12

@oracle("2171D")
def oracle_2171d(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        permutation = values[position + 1:position + 1 + n]
        position += 1 + n
        # 允许的边是「小的在前」的数对。图不连通 <=> 存在长度 L 的前缀恰好装着最大的 L 个值，
        # 那时前 L 个值与其余值之间每一对都是逆序对。
        smallest, split = n + 1, False
        for length in range(1, n):
            smallest = min(smallest, permutation[length - 1])
            if smallest == n - length + 1:
                split = True
                break
        out.append(("No" if split else "Yes") + "\n")
    return "".join(out)


@oracle("2193D")
def oracle_2193d(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        strengths = sorted(values[position + 1:position + 1 + n], reverse=True)
        strikes = values[position + 1 + n:position + 1 + 2 * n]
        position += 1 + 2 * n
        prefix = []
        total = 0
        for need in strikes:
            total += need
            prefix.append(total)
        best = 0
        for index, difficulty in enumerate(strengths):
            usable = index + 1                      # 强度 >= difficulty 的剑
            levels = bisect.bisect_right(prefix, usable)
            best = max(best, difficulty * levels)
        out.append(f"{best}\n")
    return "".join(out)


@oracle("2196A")
def oracle_2196a(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        p, q = values[1 + 2 * index], values[2 + 2 * index]
        # 与 p,q <= 40/60 的博弈暴力逐点核过。
        out.append(("Bob" if p < q <= 3 * p // 2 else "Alice") + "\n")
    return "".join(out)


@oracle("2196B")
def oracle_2196b(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        total = 0
        for left in range(n):
            for right in range(left + 1, n):
                if row[left] * row[right] == right - left:
                    total += 1
        out.append(f"{total}\n")
    return "".join(out)


@oracle("2200G")
def oracle_2200g(text):
    tokens = text.split()
    mod = 10 ** 9 + 7
    cursor, out = 1, []
    for _ in range(int(tokens[0])):
        n, x = int(tokens[cursor]), int(tokens[cursor + 1])
        operations = tokens[cursor + 2:cursor + 2 + n]
        cursor += 2 + n
        factors, added = [], 0
        for operation in operations:
            symbol, value = operation[0], int(operation[1:])
            if symbol == "x":
                factors.append(value % mod)
            elif symbol == "/":
                factors.append(pow(value, mod - 2, mod))
            elif symbol == "+":
                added = (added + value) % mod
            else:
                added = (added - value) % mod
        m = len(factors)
        # 终值 = x * ∏factors + Σ(加数 * 排在它后面的乘法算子之积)。
        # 对固定的一个加法算子，它落在 m 个乘法算子形成的 m+1 个空档里是等概率的，
        # 「后面恰好有 r 个」时那 r 个是均匀随机的 r 元子集 —— 期望是 e_r / C(m, r)。
        elementary = [0] * (m + 1)
        elementary[0] = 1
        for factor in factors:
            for degree in range(m, 0, -1):
                elementary[degree] = (elementary[degree] + elementary[degree - 1] * factor) % mod
        total_product = elementary[m]
        expectation_tail = 0
        choose = 1
        for degree in range(m + 1):
            if degree:
                choose = choose * (m - degree + 1) // degree
            expectation_tail += elementary[degree] * pow(choose % mod, mod - 2, mod) % mod
        expectation_tail = expectation_tail % mod * pow(m + 1, mod - 2, mod) % mod
        out.append(f"{(x % mod * total_product + added * expectation_tail) % mod}\n")
    return "".join(out)


@oracle("2209E")
def oracle_2209e(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        n, q = ints(rows[index])
        word = rows[index + 1].strip()
        queries = [ints(row) for row in rows[index + 2:index + 2 + q]]
        index += 2 + q
        for left, right in queries:
            segment = word[left - 1:right]
            size = len(segment)
            best = [0] * (size + 1)
            for end in range(1, size + 1):
                best[end] = max(
                    (best[end - length] + 1
                     for length in range(1, end + 1)
                     if best[end - length] > 0 or end == length
                     if segment[end - length:end] == segment[:length]),
                    default=0)
            out.append(f"{sum(best[1:])}\n")
    return "".join(out)


@verifier("2218A")
def verify_2218a(text, answer):
    """任意让 min(x,y) 最大的 y 都算对（即 -67<=y<=67 且 y>=x）。"""
    values = ints(text)
    got = ints(answer)
    if len(got) != values[0]:
        return f"应输出 {values[0]} 个数，实际 {len(got)} 个"
    for x, y in zip(values[1:1 + values[0]], got):
        if not -67 <= y <= 67:
            return f"y={y} 越出题面 -67<=y<=67"
        if min(x, y) != x:
            return f"x={x} 时 min(x,y) 的最大值是 {x}，y={y} 只给到 {min(x, y)}"
    return None


@oracle("2218B")
def oracle_2218b(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        row = values[1 + 7 * index:8 + 7 * index]
        out.append(f"{max(2 * value - sum(row) for value in row)}\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 13

@verifier("2218C")
def verify_2218c(text, answer):
    """长度 3n 的排列，按 3 个一块切，中位数之和最大；排列不唯一。

    最大值是 (3n-1) + (3n-3) + … + (3n-(2n-1))：每块用两个大数夹一个更大的数，
    中位数最多能取到 3n-1, 3n-3, …。
    """
    values = ints(text)
    got = ints(answer)
    cursor = 0
    for n in values[1:1 + values[0]]:
        block = got[cursor:cursor + 3 * n]
        cursor += 3 * n
        if sorted(block) != list(range(1, 3 * n + 1)):
            return f"n={n}: 输出不是 1..{3 * n} 的排列"
        total = sum(sorted(block[3 * i:3 * i + 3])[1] for i in range(n))
        best = sum(3 * n - 1 - 2 * i for i in range(n))
        if total != best:
            return f"n={n}: 中位数之和 {total}，最大是 {best}"
    return None


@verifier("2218D")
def verify_2218d(text, answer):
    """相邻两项的 gcd 必须两两不同；序列不唯一。"""
    values = ints(text)
    got = ints(answer)
    cursor = 0
    for n in values[1:1 + values[0]]:
        row = got[cursor:cursor + n]
        cursor += n
        if len(row) != n:
            return f"n={n}: 只给了 {len(row)} 个数"
        if any(not 1 <= value <= 10 ** 18 for value in row):
            return f"n={n}: 有元素越出题面 1<=a_i<=10^18"
        gcds = [math.gcd(row[index], row[index + 1]) for index in range(n - 1)]
        if len(set(gcds)) != len(gcds):
            return f"n={n}: 相邻 gcd 有重复"
    return None


@oracle("2218E")
def oracle_2218e(text):
    """操作后的累计异或恰好等于「第 t 次被选中的元素的原值」，所以终值 = 两个原值的异或。"""
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        best = max(row[i] ^ row[j] for i in range(n) for j in range(i + 1, n))
        out.append(f"{best}\n")
    return "".join(out)


@oracle("2227A")
def oracle_2227a(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        x, y = values[1 + 2 * index], values[2 + 2 * index]
        out.append(("YES" if x % 2 + y % 2 <= 1 else "NO") + "\n")
    return "".join(out)


def _divisible_by_six_count(sequence):
    total = 0
    for left in range(len(sequence)):
        product = 1
        for right in range(left, len(sequence)):
            product *= sequence[right]
            if product % 6 == 0:
                total += 1
    return total


@verifier("2227C")
def verify_2227c(text, answer):
    """重排使「乘积被 6 整除的子数组个数」最少；重排方式不唯一，这里穷举验证最小值。"""
    import itertools
    values = ints(text)
    got = ints(answer)
    position, cursor = 1, 0
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        out = got[cursor:cursor + n]
        cursor += n
        if sorted(out) != sorted(row):
            return f"n={n}: 输出不是原数组的重排"
        if n > 8:
            continue                      # 穷举只对小规模成立；数据里 n<=8
        best = min(_divisible_by_six_count(order) for order in itertools.permutations(row))
        if _divisible_by_six_count(out) != best:
            return (f"n={n}: 给出的排列 f={_divisible_by_six_count(out)}，最小是 {best}")
    return None


@verifier("2218F")
def verify_2218f(text, answer):
    """构造 x+y 个结点的有根树，恰好 x 个子树大小为偶、y 个为奇；树不唯一。

    **题面里藏着一条规则**：`If the number of test cases (t) = 2, I want you to add 1 to x.`
    2026-09-20 之前生成器和 `judge.py` 的 `subtree_parity_tree` 特判都没实现它，
    而数据里 21 组的 t **全是 2** —— 照题面写的正确程序反而全错。
    可行性判据（与 n<=8 的穷举逐点核过）：x <= n//2，且 n 为偶数时 x 不能是 0。
    """
    values = ints(text)
    count = values[0]
    tokens = answer.split()
    cursor = 0
    for index in range(count):
        x, y = values[1 + 2 * index], values[2 + 2 * index]
        if count == 2:
            x += 1                                   # 题面的彩蛋规则
        n = x + y
        possible = x <= n // 2 and not (n % 2 == 0 and x == 0)
        if cursor >= len(tokens):
            return f"第 {index + 1} 组没有答案"
        decision = tokens[cursor].upper()
        cursor += 1
        if decision == "NO":
            if possible:
                return f"x={x} y={y}: 存在合法的树，不该输出 NO"
            continue
        if decision != "YES":
            return f"第 {index + 1} 组的答案既不是 YES 也不是 NO：{decision!r}"
        if not possible:
            return f"x={x} y={y}: 不存在合法的树，却输出了 YES"
        edges = []
        for _ in range(n - 1):
            u, v = int(tokens[cursor]), int(tokens[cursor + 1])
            cursor += 2
            edges.append((u, v))
        if not is_tree(n, edges):
            return f"x={x} y={y}: 给出的 {n - 1} 条边不是一棵树"
        graph = [[] for _ in range(n + 1)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        order, parent, stack, seen = [], [0] * (n + 1), [1], {1}
        while stack:
            node = stack.pop()
            order.append(node)
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    parent[nxt] = node
                    stack.append(nxt)
        size = [1] * (n + 1)
        for node in reversed(order):
            if node != 1:
                size[parent[node]] += size[node]
        even = sum(1 for node in range(1, n + 1) if size[node] % 2 == 0)
        if even != x or n - even != y:
            return f"x={x} y={y}: 这棵树有 {even} 个偶数子树、{n - even} 个奇数子树"
    return None


@verifier("2171E")
def verify_2171e(text, answer):
    """长度 n 的排列，「连续三个两两互质」的下标至多 6 个；排列不唯一。"""
    values = ints(text)
    got = ints(answer)
    cursor = 0
    for n in values[1:1 + values[0]]:
        row = got[cursor:cursor + n]
        cursor += n
        if sorted(row) != list(range(1, n + 1)):
            return f"n={n}: 输出不是 1..{n} 的排列"
        bad = sum(1 for index in range(n - 2)
                  if math.gcd(row[index], row[index + 1]) == 1
                  and math.gcd(row[index], row[index + 2]) == 1
                  and math.gcd(row[index + 1], row[index + 2]) == 1)
        if bad > 6:
            return f"n={n}: 有 {bad} 个 bad 下标，题面要求至多 6 个"
    return None


# ------------------------------------------- 批次 14（rebuilt_tests：单题流水线的题）

@oracle("270A")
def oracle_270a(text):
    values = ints(text)
    out = []
    for angle in values[1:1 + values[0]]:
        # 正 n 边形内角 = 180*(n-2)/n，即 360 % (180 - a) == 0
        out.append(("YES" if 360 % (180 - angle) == 0 else "NO") + "\n")
    return "".join(out)


@oracle("456A")
def oracle_456a(text):
    values = ints(text)
    n = values[0]
    rows = sorted((values[1 + 2 * i], values[2 + 2 * i]) for i in range(n))
    happy = any(rows[i][1] > rows[i + 1][1] for i in range(n - 1))
    return ("Happy Alex" if happy else "Poor Alex") + "\n"


@oracle("546A")
def oracle_546a(text):
    k, n, w = ints(text)
    return f"{max(0, k * w * (w + 1) // 2 - n)}\n"


@oracle("617A")
def oracle_617a(text):
    return f"{-(-int(text) // 5)}\n"


@oracle("698A")
def oracle_698a(text):
    # 状态：0 休息、1 比赛、2 运动。dp 求最少休息天数。
    days = ints(text.splitlines()[1])
    best = [0, float("inf"), float("inf")]
    for day in days:
        rest = min(best) + 1
        contest = min(best[0], best[2]) if day in (1, 3) else float("inf")
        sport = min(best[0], best[1]) if day in (2, 3) else float("inf")
        best = [rest, contest, sport]
    return f"{min(best)}\n"


@oracle("734A")
def oracle_734a(text):
    row = text.splitlines()[1].strip()
    anton, danik = row.count("A"), row.count("D")
    return ("Anton" if anton > danik else "Danik" if danik > anton else "Friendship") + "\n"


@oracle("791A")
def oracle_791a(text):
    a, b = ints(text)
    years = 0
    while a <= b:
        a, b, years = a * 3, b * 2, years + 1
    return f"{years}\n"


@oracle("977A")
def oracle_977a(text):
    n, k = ints(text)
    for _ in range(k):
        n = n // 10 if n % 10 == 0 else n - 1
    return f"{n}\n"


# --------------------------------------------------------------------- 批次 15

@oracle("894E")
def oracle_894e(text):
    values = ints(text)
    n, m = values[0], values[1]
    edges = [(values[2 + 3 * i], values[3 + 3 * i], values[4 + 3 * i]) for i in range(m)]
    start = values[2 + 3 * m]

    def full_collect(weight):
        """一条边在强连通分量里可以反复走：第 i 次收 w - (i-1)i/2，直到非正。

        w 最大 10^8、边最多 10^6，逐次累加会跑到 10^10 量级，所以用闭式：
        走 t 次时总收成 = t*w - Σ_{i=1..t} (i-1)i/2。
        """
        if weight <= 0:
            return 0
        steps = int((1 + math.isqrt(1 + 8 * weight)) // 2)
        while (steps - 1) * steps // 2 >= weight:
            steps -= 1
        while steps * (steps + 1) // 2 < weight:
            steps += 1
        return steps * weight - (steps * (steps + 1) * (2 * steps + 1) // 6
                                 - steps * (steps + 1) // 2) // 2

    graph = [[] for _ in range(n + 1)]
    reverse = [[] for _ in range(n + 1)]
    for x, y, _w in edges:
        graph[x].append(y)
        reverse[y].append(x)
    order, seen = [], [False] * (n + 1)
    for node in range(1, n + 1):                 # 迭代式 Kosaraju
        if seen[node]:
            continue
        stack = [(node, iter(graph[node]))]
        seen[node] = True
        while stack:
            current, children = stack[-1]
            for nxt in children:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:
                order.append(current)
                stack.pop()
    component = [0] * (n + 1)
    label = 0
    seen = [False] * (n + 1)
    for node in reversed(order):
        if seen[node]:
            continue
        label += 1
        stack = [node]
        seen[node] = True
        while stack:
            current = stack.pop()
            component[current] = label
            for nxt in reverse[current]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    inside = [0] * (label + 1)
    condensed = [[] for _ in range(label + 1)]
    for x, y, weight in edges:
        if component[x] == component[y]:
            inside[component[x]] += full_collect(weight)
        else:
            condensed[component[x]].append((component[y], weight))
    # 缩点后的 DAG 上求最长路。用 Kahn 拓扑排序而不是递归 —— 链长可以到 10^5，
    # 递归版在 15.in 上直接 RecursionError。
    indegree = [0] * (label + 1)
    for node in range(1, label + 1):
        for nxt, _weight in condensed[node]:
            indegree[nxt] += 1
    queue = collections.deque(node for node in range(1, label + 1) if indegree[node] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt, _weight in condensed[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    best = [0] * (label + 1)
    for node in reversed(order):
        best[node] = inside[node] + max((weight + best[nxt]
                                         for nxt, weight in condensed[node]), default=0)
    return f"{best[component[start]]}\n"


@oracle("903C")
def oracle_903c(text):
    counts = collections.Counter(ints(text.splitlines()[1]))
    return f"{max(counts.values())}\n"


@oracle("986D")
def oracle_986d(text):
    """最小的代价 S，使得「和为 S 的正整数乘积的最大值」不小于 n。

    和固定为 S 时乘积最大的拆法只用 3，余 1 换成一个 4、余 2 留一个 2。
    n 有上百万位，所以先用 log10 把 S 夹到 ±3 的窗口里，只在窗口内做精确比较；
    精确比较走 `decimal`（libmpdec 的 NTT 乘法），不把整数从十进制字符串转成 int。
    """
    import decimal
    digits = text.strip()
    if digits == "1":
        return "1\n"
    log3, log2, log4 = math.log10(3), math.log10(2), math.log10(4)
    head = digits[:18]
    log_n = math.log10(int(head)) + (len(digits) - len(head))

    def log_best(total):
        if total % 3 == 0:
            return total // 3 * log3
        if total % 3 == 1:
            return log4 + (total - 4) // 3 * log3 if total >= 4 else 0.0
        return log2 + (total - 2) // 3 * log3

    estimate = max(1, int(3 * log_n / log3) - 3)
    while log_best(estimate) > log_n + 1e-9 and estimate > 1:
        estimate -= 1
    context = decimal.Context(prec=len(digits) + 30, Emax=decimal.MAX_EMAX,
                              Emin=decimal.MIN_EMIN)
    with decimal.localcontext(context):
        n = decimal.Decimal(digits)
        three, two, four = decimal.Decimal(3), decimal.Decimal(2), decimal.Decimal(4)

        def best_product(total):
            if total % 3 == 0:
                return three ** (total // 3)
            if total % 3 == 1:
                return four * three ** ((total - 4) // 3) if total >= 4 else decimal.Decimal(1)
            return two * three ** ((total - 2) // 3)

        total = estimate
        while best_product(total) < n:
            total += 1
    return f"{total}\n"


@oracle("1000E")
def oracle_1000e(text):
    values = ints(text)
    n, m = values[0], values[1]
    graph = [[] for _ in range(n + 1)]
    for index in range(m):
        x, y = values[2 + 2 * index], values[3 + 2 * index]
        graph[x].append((y, index))
        graph[y].append((x, index))
    # 先找桥（迭代式 Tarjan），再把 2-边连通分量缩点，答案是桥树的直径。
    discovery = [0] * (n + 1)
    low = [0] * (n + 1)
    timer = 1
    bridges = set()
    stack = [(1, -1, iter(graph[1]))]
    discovery[1] = low[1] = timer
    timer += 1
    while stack:
        node, parent_edge, children = stack[-1]
        for nxt, edge_id in children:
            if edge_id == parent_edge:
                continue
            if discovery[nxt]:
                low[node] = min(low[node], discovery[nxt])
            else:
                discovery[nxt] = low[nxt] = timer
                timer += 1
                stack.append((nxt, edge_id, iter(graph[nxt])))
                break
        else:
            stack.pop()
            if stack:
                up = stack[-1][0]
                low[up] = min(low[up], low[node])
                if low[node] > discovery[up]:
                    bridges.add(parent_edge)
    component = [0] * (n + 1)
    label = 0
    for start in range(1, n + 1):
        if component[start]:
            continue
        label += 1
        queue = [start]
        component[start] = label
        while queue:
            node = queue.pop()
            for nxt, edge_id in graph[node]:
                if edge_id in bridges or component[nxt]:
                    continue
                component[nxt] = label
                queue.append(nxt)
    tree = [[] for _ in range(label + 1)]
    for index in range(m):
        x, y = values[2 + 2 * index], values[3 + 2 * index]
        if index in bridges:
            tree[component[x]].append(component[y])
            tree[component[y]].append(component[x])

    def farthest(source):
        distance = {source: 0}
        queue = collections.deque([source])
        far = source
        while queue:
            node = queue.popleft()
            if distance[node] > distance[far]:
                far = node
            for nxt in tree[node]:
                if nxt not in distance:
                    distance[nxt] = distance[node] + 1
                    queue.append(nxt)
        return far, distance[far]

    first, _ = farthest(1)
    _, diameter = farthest(first)
    return f"{diameter}\n"


@oracle("116A")
def oracle_116a(text):
    values = ints(text)
    inside, best = 0, 0
    for index in range(values[0]):
        inside += values[2 + 2 * index] - values[1 + 2 * index]
        best = max(best, inside)
    return f"{best}\n"


@oracle("1374B")
def oracle_1374b(text):
    values = ints(text)
    out = []
    for n in values[1:1 + values[0]]:
        twos = threes = 0
        while n % 2 == 0:
            n //= 2
            twos += 1
        while n % 3 == 0:
            n //= 3
            threes += 1
        out.append(f"{2 * threes - twos if n == 1 and twos <= threes else -1}\n")
    return "".join(out)


@oracle("1374C")
def oracle_1374c(text):
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        sequence = rows[index + 1].strip()
        index += 2
        balance, moves = 0, 0
        for char in sequence:
            balance += 1 if char == "(" else -1
            if balance < 0:
                moves += 1
                balance = 0
        out.append(f"{moves}\n")
    return "".join(out)


@oracle("1475A")
def oracle_1475a(text):
    values = ints(text)
    out = []
    for n in values[1:1 + values[0]]:
        out.append(("NO" if n & (n - 1) == 0 else "YES") + "\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 16

@oracle("1764C")
def oracle_1764c(text):
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = sorted(values[position + 1:position + 1 + n])
        position += 1 + n
        if row[0] == row[-1]:
            out.append(f"{n // 2}\n")          # 全相等时只能两两配对
            continue
        best = 0
        for index in range(1, n):
            if row[index] != row[index - 1]:
                best = max(best, index * (n - index))
        out.append(f"{best}\n")
    return "".join(out)


@verifier("1793C")
def verify_1793c(text, answer):
    """输出任意一段两端既不是最小也不是最大的子段，或 -1。"""
    values = ints(text)
    tokens = answer.split()
    position, cursor = 1, 0
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        # 双指针判存在性：两端只要是当前区间的最小或最大就缩掉。
        left, right, low, high = 0, n - 1, 1, n
        while left <= right:
            if row[left] == low:
                left += 1
                low += 1
            elif row[left] == high:
                left += 1
                high -= 1
            elif row[right] == low:
                right -= 1
                low += 1
            elif row[right] == high:
                right -= 1
                high -= 1
            else:
                break
        exists = left <= right
        if tokens[cursor] == "-1":
            cursor += 1
            if exists:
                return f"n={n}: 存在合法子段（{left + 1},{right + 1}），不该输出 -1"
            continue
        l, r = int(tokens[cursor]), int(tokens[cursor + 1])
        cursor += 2
        if not exists:
            return f"n={n}: 不存在合法子段，却输出了 {l} {r}"
        if not 1 <= l <= r <= n:
            return f"n={n}: 下标 {l} {r} 越界"
        segment = row[l - 1:r]
        if (segment[0] in (min(segment), max(segment))
                or segment[-1] in (min(segment), max(segment))):
            return f"n={n}: 子段 [{l},{r}] 的端点是最小或最大值"
    return None


@oracle("1829D")
def oracle_1829d(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        n, m = values[1 + 2 * index], values[2 + 2 * index]

        def reachable(pile):
            while True:
                if pile == m:
                    return True
                if pile < m or pile % 3:
                    return False
                if reachable(pile // 3):
                    return True
                pile = pile // 3 * 2

        out.append(("YES" if reachable(n) else "NO") + "\n")
    return "".join(out)


@oracle("1883D")
def oracle_1883d(text):
    rows = lines(text)
    count = int(rows[0])
    lefts, rights = collections.Counter(), collections.Counter()
    left_heap, right_heap = [], []
    out = []
    for row in rows[1:1 + count]:
        sign, left, right = row.split()
        left, right = int(left), int(right)
        if sign == "+":
            lefts[left] += 1
            rights[right] += 1
            heapq.heappush(left_heap, -left)
            heapq.heappush(right_heap, right)
        else:
            lefts[left] -= 1
            rights[right] -= 1
        while left_heap and lefts[-left_heap[0]] <= 0:
            heapq.heappop(left_heap)
        while right_heap and rights[right_heap[0]] <= 0:
            heapq.heappop(right_heap)
        # 不相交 <=> 最小的右端点 < 最大的左端点
        ok = left_heap and right_heap and right_heap[0] < -left_heap[0]
        out.append(("YES" if ok else "NO") + "\n")
    return "".join(out)


def _trails(text):
    """1970E1/E2/E3 是同一道题的三档规模（n 最大 10^9，m 最大 10^5）。

    一天的走法数 T[i][j] = s_i*s_j + s_i*l_j + l_i*s_j（至少一条短路）。
    关键：这个 m×m 的转移只有秩 2 —— 把状态压成 (S, L) = (Σ cur_i*s_i, Σ cur_i*l_i)，
    一天就是一个 2×2 矩阵，于是 n 再大也只要快速幂。
    """
    rows = lines(text)
    m, n = ints(rows[0])
    short, long_ = ints(rows[1]), ints(rows[2])
    mod = 10 ** 9 + 7
    a = sum(short[j] * (short[j] + long_[j]) for j in range(m)) % mod
    b = sum(short[j] * short[j] for j in range(m)) % mod
    c = sum(long_[j] * (short[j] + long_[j]) for j in range(m)) % mod
    d = sum(short[j] * long_[j] for j in range(m)) % mod

    def multiply(x, y):
        return [(x[0] * y[0] + x[1] * y[2]) % mod, (x[0] * y[1] + x[1] * y[3]) % mod,
                (x[2] * y[0] + x[3] * y[2]) % mod, (x[2] * y[1] + x[3] * y[3]) % mod]

    power, base, steps = [1, 0, 0, 1], [a, b, c, d], n - 1
    while steps:
        if steps & 1:
            power = multiply(power, base)
        base = multiply(base, base)
        steps >>= 1
    state = [(power[0] * short[0] + power[1] * long_[0]) % mod,
             (power[2] * short[0] + power[3] * long_[0]) % mod]
    total = (state[0] * sum(short[j] + long_[j] for j in range(m))
             + state[1] * sum(short)) % mod
    return f"{total}\n"


ORACLES["1970E1"] = _trails
ORACLES["1970E2"] = _trails
ORACLES["1970E3"] = _trails


@oracle("2227B")
def oracle_2227b(text):
    """可以整段删掉再逐个任意插回 —— 删掉整串就能随意重排，所以只看左右括号数是否相等。"""
    rows = lines(text)
    index, out = 1, []
    for _ in range(int(rows[0])):
        sequence = rows[index + 1].strip()
        index += 2
        out.append(("YES" if sequence.count("(") == sequence.count(")") else "NO") + "\n")
    return "".join(out)


# --------------------------------------------------------------------- 批次 17

@oracle("1742A")
def oracle_1742a(text):
    values = ints(text)
    out = []
    for index in range(values[0]):
        row = values[1 + 3 * index:4 + 3 * index]
        out.append(("YES" if max(row) == sum(row) - max(row) else "NO") + "\n")
    return "".join(out)


@verifier("2140B")
def verify_2140b(text, answer):
    """任何满足 (x+y) | concat(x,y) 且 1<=y<=10^9 的 y 都算对。"""
    values = ints(text)
    ys = ints(answer)
    xs = values[1:1 + values[0]]
    if len(ys) != len(xs):
        return f"应输出 {len(xs)} 个 y，实际 {len(ys)} 个"
    for x, y in zip(xs, ys):
        if not 1 <= y <= 10 ** 9:
            return f"y={y} 越出题面 1<=y<=10^9"
        if int(f"{x}{y}") % (x + y):
            return f"x={x}, y={y}: concat 不能被 x+y 整除"
    return None


@oracle("2227E")
def oracle_2227e(text):
    """重力向右后会移动的方块数，允许把某一列减 1（或不减）。

    某列 i 高度 h 的方块**不动** <=> 它右边每一列都至少有 h 个方块，
    所以第 i 列不动的方块数 = min(a_i, 右侧后缀最小值)。把某列减 1 只会影响
    它自己那一项，以及左边那些「后缀最小值恰好等于 a_k」的列，逐项算差即可。
    """
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + n]
        position += 1 + n
        infinity = float("inf")
        suffix = [infinity] * (n + 1)
        for index in range(n - 1, -1, -1):
            suffix[index] = min(suffix[index + 1], row[index])
        stay = [min(row[index], suffix[index + 1]) for index in range(n)]
        total, kept = sum(row), sum(stay)
        best = total - kept
        # 按后缀最小值分组，便于数「左边有多少列的 m_i 恰好等于 a_k 且 a_i >= a_k」
        groups = collections.defaultdict(list)
        for index in range(n):
            groups[suffix[index + 1]].append(index)
        prefix = {}
        for value, indices in groups.items():
            running, table = 0, []
            for index in indices:
                running += 1 if row[index] >= value else 0
                table.append(running)
            prefix[value] = (indices, table)
        for k in range(n):
            if row[k] < 1:
                continue
            same = 0
            if row[k] in prefix:
                indices, table = prefix[row[k]]
                cut = bisect.bisect_left(indices, k)
                same = table[cut - 1] if cut else 0
            own = min(row[k], suffix[k + 1]) - min(row[k] - 1, suffix[k + 1])
            best = max(best, (total - 1) - (kept - same - own))
        out.append(f"{best}\n")
    return "".join(out)


@verifier("2171F")
def verify_2171f(text, answer):
    """存在性判据与 2171D 相同；YES 时还要给出一棵满足「小号在前」的树。"""
    values = ints(text)
    tokens = answer.split()
    position, cursor = 1, 0
    for _ in range(values[0]):
        n = values[position]
        permutation = values[position + 1:position + 1 + n]
        position += 1 + n
        smallest, split = n + 1, False
        for length in range(1, n):
            smallest = min(smallest, permutation[length - 1])
            if smallest == n - length + 1:
                split = True
                break
        decision = tokens[cursor].lower()
        cursor += 1
        if decision == "no":
            if not split:
                return f"n={n}: 存在合法的树，不该输出 No"
            continue
        if decision != "yes":
            return f"n={n}: 答案既不是 Yes 也不是 No：{decision!r}"
        if split:
            return f"n={n}: 不存在合法的树，却输出了 Yes"
        edges = []
        for _ in range(n - 1):
            u, v = int(tokens[cursor]), int(tokens[cursor + 1])
            cursor += 2
            edges.append((u, v))
        if not is_tree(n, edges):
            return f"n={n}: 给出的边不是一棵树"
        place = {value: index for index, value in enumerate(permutation)}
        for u, v in edges:
            small, large = min(u, v), max(u, v)
            if place[small] > place[large]:
                return f"n={n}: 边 ({u},{v}) 里小的一端没有排在前面"
    return None


@verifier("37C")
def verify_37c(text, answer):
    """给定长度的前缀码：每个词长度对得上、两两不互为前缀；构造不唯一。"""
    values = ints(text)
    lengths = values[1:1 + values[0]]
    tokens = answer.split()
    if tokens[0].upper() == "NO":
        # Kraft 不等式：Σ 2^-l > 1 时无解。**必须用整数算** —— 长度到 1000、词有 1000 个时
        # 浮点版会把 6.in 的和四舍五入成正好 1.0，于是把正确的 NO 判成错（2026-09-20 实测）。
        top = max(lengths)
        if sum(2 ** (top - length) for length in lengths) > 2 ** top:
            return None
        return "存在合法的前缀码，不该输出 NO"
    words = tokens[1:]
    if len(words) != len(lengths):
        return f"应输出 {len(lengths)} 个词，实际 {len(words)} 个"
    for word, length in zip(words, lengths):
        if len(word) != length or set(word) - {"0", "1"}:
            return f"{word!r} 不是长度 {length} 的 01 串"
    for i, first in enumerate(words):
        for second in words[i + 1:]:
            if first.startswith(second) or second.startswith(first):
                return f"{first!r} 与 {second!r} 互为前缀"
    return None


@verifier("2201G")
def verify_2201g(text, answer):
    """S 诱导出的子图必须同构于一个长度至少 ⌊n²/e⌋ 的环。"""
    n = int(text.split()[0])
    rows = [row for row in answer.split() if row]
    if len(rows) != n or any(len(row) != n or set(row) - {"0", "1"} for row in rows):
        return f"应输出 {n} 行、每行 {n} 个 0/1"
    chosen = [(r, c) for r in range(n) for c in range(n) if rows[r][c] == "1"]
    need = int(n * n / math.e)
    if len(chosen) < need:
        return f"只选了 {len(chosen)} 个点，题面要求至少 {need} 个"
    index = {point: number for number, point in enumerate(chosen)}
    degree = [0] * len(chosen)
    edges = []
    for (r, c) in chosen:
        for dr, dc in ((2, 3), (3, 2), (2, -3), (3, -2)):
            other = (r + dr, c + dc)
            if other in index:
                degree[index[(r, c)]] += 1
                degree[index[other]] += 1
                edges.append((index[(r, c)], index[other]))
    if any(value != 2 for value in degree):
        return "诱导子图里有点的度不是 2，不可能是一个环"
    if not edges or len(edges) != len(chosen):
        return f"环应当有 {len(chosen)} 条边，实际 {len(edges)} 条"
    seen, current, previous = {0}, 0, None
    neighbours = collections.defaultdict(list)
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    while True:
        nxt = next((node for node in neighbours[current] if node != previous), None)
        if nxt is None or nxt == 0:
            break
        if nxt in seen:
            return "诱导子图不是单个环"
        seen.add(nxt)
        previous, current = current, nxt
    if len(seen) != len(chosen):
        return f"环只穿过 {len(seen)} 个点，选了 {len(chosen)} 个"
    return None


# --------------------------------------------------------------------- 批次 18

def _stamina_2208c(text):
    """得分随 S 线性伸缩，所以从后往前一遍 DP：f(i) = max(f(i+1), c_i + (1-p_i/100)·f(i+1))。"""
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        tasks = [(values[position + 1 + 2 * i], values[position + 2 + 2 * i]) for i in range(n)]
        position += 1 + 2 * n
        best = 0.0
        for value, difficulty in reversed(tasks):
            best = max(best, value + (1 - difficulty / 100) * best)
        out.append(best)
    return out


float_verifier("2208C", _stamina_2208c, tolerance=1e-6)


@oracle("2227D")
def oracle_2227d(text):
    """回文子数组的最大 mex。每个值恰好出现两次，所以从每个中心往外扩的总步数是线性的。"""
    values = ints(text)
    position, out = 1, []
    for _ in range(values[0]):
        n = values[position]
        row = values[position + 1:position + 1 + 2 * n]
        position += 1 + 2 * n
        size = len(row)
        best = 0
        for centre in range(2 * size - 1):
            left, right = centre // 2, (centre + 1) // 2
            seen, mex = set(), 0
            while left >= 0 and right < size and row[left] == row[right]:
                seen.add(row[left])
                seen.add(row[right])
                while mex in seen:
                    mex += 1
                best = max(best, mex)
                left -= 1
                right += 1
        out.append(f"{best}\n")
    return "".join(out)
