#!/usr/bin/env python3
"""Build deterministic 21-case data for basic exact-output Codeforces problems."""
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
CATALOG = MIRROR / "catalog.json"


def case_1a(r):
    n, m, a = r.randint(1, 10**9), r.randint(1, 10**9), r.randint(1, 10**9)
    return f"{n} {m} {a}\n", f"{(n + a - 1) // a * ((m + a - 1) // a)}\n"


def case_25a(r):
    n = r.randrange(3, 52, 2)
    parity = r.randrange(2)
    values = [2 * r.randint(1, 100) + parity for _ in range(n - 1)]
    outlier = 2 * r.randint(1, 100) + (1 - parity)
    index = r.randrange(n)
    values.insert(index, outlier)
    return f"{n}\n{' '.join(map(str, values))}\n", f"{index + 1}\n"


def case_58a(r):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    if r.randrange(2):
        slots = [r.randint(0, 3) for _ in range(6)]
        text = "".join("".join(r.choice(alphabet) for _ in range(slots[i])) + ("hello"[i] if i < 5 else "") for i in range(6))
    else:
        text = "".join(r.choice("abcdfgijkmnpqrstuvwxyz") for _ in range(r.randint(1, 30)))
    pointer = 0
    for char in text:
        if pointer < 5 and char == "hello"[pointer]: pointer += 1
    return text + "\n", ("YES" if pointer == 5 else "NO") + "\n"


def case_69a(r):
    n = r.randint(1, 30)
    vectors = [[r.randint(-20, 20) for _ in range(3)] for _ in range(n)]
    if r.randrange(2) and n > 1:
        sums = [sum(row[column] for row in vectors[:-1]) for column in range(3)]
        vectors[-1] = [-value for value in sums]
    balanced = all(sum(row[column] for row in vectors) == 0 for column in range(3))
    return str(n) + "\n" + "".join(" ".join(map(str, row)) + "\n" for row in vectors), ("YES" if balanced else "NO") + "\n"


def case_71a(r):
    words = []
    for _ in range(r.randint(1, 20)):
        words.append("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 25))))
    answer = [word if len(word) <= 10 else f"{word[0]}{len(word) - 2}{word[-1]}" for word in words]
    return str(len(words)) + "\n" + "\n".join(words) + "\n", "\n".join(answer) + "\n"


def case_118a(r):
    text = "".join(r.choice("aoyeuiBCDFGHJKLMNPQRSTVWXYZ") for _ in range(r.randint(1, 80)))
    answer = "".join("." + char.lower() for char in text if char.lower() not in "aoyeui")
    return text + "\n", answer + "\n"


def case_122a(r):
    value = r.randint(1, 1000)
    lucky = (4, 7, 44, 47, 74, 77, 444, 447, 474, 477, 744, 747, 774, 777)
    return f"{value}\n", ("YES" if any(value % item == 0 for item in lucky) else "NO") + "\n"


def case_131a(r):
    text = r.choice("abcdefghijklmnopqrstuvwxyz") + "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(0, 12)))
    mode = r.randrange(3)
    if mode == 1: text = text.upper()
    elif mode == 2: text = text[0].lower() + text[1:].upper()
    answer = text.swapcase() if text.isupper() or (text[0].islower() and text[1:].isupper()) else text
    return text + "\n", answer + "\n"


def case_158a(r):
    n, k = r.randint(1, 50), None
    scores = sorted((r.randint(0, 100) for _ in range(n)), reverse=True)
    k = r.randint(1, n)
    answer = sum(score > 0 and score >= scores[k - 1] for score in scores)
    return f"{n} {k}\n{' '.join(map(str, scores))}\n", f"{answer}\n"


def case_160a(r):
    coins = [r.randint(1, 100) for _ in range(r.randint(1, 50))]
    total = sum(coins); taken = count = 0
    for coin in sorted(coins, reverse=True):
        taken += coin; count += 1
        if taken > total - taken: break
    return str(len(coins)) + "\n" + " ".join(map(str, coins)) + "\n", f"{count}\n"


def case_230a(r):
    strength, n = r.randint(1, 100), r.randint(1, 30)
    dragons = [(r.randint(1, 150), r.randint(0, 100)) for _ in range(n)]
    current = strength
    for need, reward in sorted(dragons):
        if current <= need: break
        current += reward
    else:
        return f"{strength} {n}\n" + "".join(f"{need} {reward}\n" for need, reward in dragons), "YES\n"
    return f"{strength} {n}\n" + "".join(f"{need} {reward}\n" for need, reward in dragons), "NO\n"


def case_34b(r):
    n, m = r.randint(1, 50), r.randint(1, 50)
    prices = [r.randint(-100, 100) for _ in range(n)]
    gain = -sum(value for value in sorted(prices)[:m] if value < 0)
    return f"{n} {m}\n{' '.join(map(str, prices))}\n", f"{gain}\n"


def case_339b(r):
    n, m = r.randint(1, 1000), r.randint(1, 100)
    houses = [r.randint(1, n) for _ in range(m)]
    current, distance = 1, 0
    for house in houses:
        distance += house - current if house >= current else n - current + house
        current = house
    return f"{n} {m}\n{' '.join(map(str, houses))}\n", f"{distance}\n"


def case_427a(r):
    events = [r.randint(-5, 5) for _ in range(r.randint(1, 100))]
    officers = missing = 0
    for event in events:
        if event > 0: officers += event
        elif officers: officers -= 1
        else: missing += 1
    return str(len(events)) + "\n" + " ".join(map(str, events)) + "\n", f"{missing}\n"


def case_455a(r):
    values = [r.randint(1, 100) for _ in range(r.randint(1, 100))]
    counts = [0] * 102
    for value in values: counts[value] += value
    previous, current = 0, 0
    for value in counts:
        previous, current = current, max(current, previous + value)
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", f"{current}\n"


def case_456a(r):
    rows = [(r.randint(1, 1000), r.randint(1, 1000)) for _ in range(r.randint(2, 50))]
    ordered, answer = sorted(rows), "Poor Alex"
    for left, right in zip(ordered, ordered[1:]):
        if left[0] < right[0] and left[1] > right[1]: answer = "Happy Alex"; break
    return str(len(rows)) + "\n" + "".join(f"{price} {quality}\n" for price, quality in rows), answer + "\n"


def case_460a_fixed(r):
    initial, every = r.randint(1, 100), r.randint(2, 20)
    socks, day = initial, 0
    while socks:
        day += 1; socks -= 1
        if day % every == 0: socks += 1
    return f"{initial} {every}\n", f"{day}\n"


def case_466a(r):
    rides, pack, single, pack_price = r.randint(1, 1000), r.randint(1, 1000), r.randint(1, 1000), r.randint(1, 1000)
    answer = min(rides * single, (rides // pack) * pack_price + (rides % pack) * single,
                 ((rides + pack - 1) // pack) * pack_price)
    return f"{rides} {pack} {single} {pack_price}\n", f"{answer}\n"


def case_579a(r):
    value = r.randint(1, 10**9)
    return f"{value}\n", f"{bin(value).count('1')}\n"


def case_580a(r):
    values = [r.randint(1, 1000) for _ in range(r.randint(1, 200))]
    best = run = 1
    for left, right in zip(values, values[1:]):
        run = run + 1 if right >= left else 1; best = max(best, run)
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", f"{best}\n"


def case_615a(r):
    bulbs, buttons = r.randint(1, 100), r.randint(1, 30)
    groups = []
    for _ in range(buttons):
        chosen = sorted(r.sample(range(1, bulbs + 1), r.randint(0, bulbs)))
        groups.append(chosen)
    lit = set().union(*map(set, groups)) if groups else set()
    text = f"{bulbs} {buttons}\n" + "".join(str(len(group)) + (" " + " ".join(map(str, group)) if group else "") + "\n" for group in groups)
    return text, ("YES" if len(lit) == bulbs else "NO") + "\n"


def case_698a(r):
    days = [r.randint(0, 3) for _ in range(r.randint(1, 100))]
    rest, contest, gym = 0, 10**9, 10**9
    for value in days:
        rest, contest, gym = min(rest, contest, gym), min(rest, gym) + 1 if value & 1 else 10**9, min(rest, contest) + 1 if value & 2 else 10**9
    return str(len(days)) + "\n" + " ".join(map(str, days)) + "\n", f"{min(rest, contest, gym)}\n"


def case_705a(r):
    count = r.randint(1, 100)
    pieces = ["I hate" if index % 2 == 0 else "I love" for index in range(count)]
    return f"{count}\n", " that ".join(pieces) + " it\n"


def case_706b(r):
    prices = [r.randint(1, 1000) for _ in range(r.randint(1, 100))]
    queries = [r.randint(1, 1200) for _ in range(r.randint(1, 100))]
    ordered = sorted(prices)
    import bisect
    answer = [str(bisect.bisect_right(ordered, query)) for query in queries]
    return str(len(prices)) + "\n" + " ".join(map(str, prices)) + "\n" + str(len(queries)) + "\n" + "\n".join(map(str, queries)) + "\n", "\n".join(answer) + "\n"


def case_723a(r):
    values = [r.randint(1, 100) for _ in range(3)]
    ordered = sorted(values)
    return " ".join(map(str, values)) + "\n", f"{ordered[2] - ordered[0]}\n"


def case_903c(r):
    text = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 100)))
    return str(len(text)) + "\n" + text + "\n", f"{max(text.count(char) for char in set(text))}\n"

def case_200b(r):
    values = [r.randint(0, 100) for _ in range(r.randint(1, 100))]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", f"{sum(values) / len(values):.10f}\n"

def case_474a(r):
    keyboard = "qwertyuiopasdfghjkl;zxcvbnm,./"
    direction = r.choice("LR")
    typed = "".join(r.choice(keyboard[1:-1]) for _ in range(r.randint(1, 40)))
    shift = -1 if direction == "R" else 1
    answer = "".join(keyboard[keyboard.index(char) + shift] for char in typed)
    return direction + "\n" + typed + "\n", answer + "\n"

def case_545d(r):
    times = [r.randint(1, 100) for _ in range(r.randint(1, 100))]
    elapsed = count = 0
    for value in sorted(times):
        if elapsed <= value: count += 1; elapsed += value
    return str(len(times)) + "\n" + " ".join(map(str, times)) + "\n", f"{count}\n"

def case_1154a(r):
    values = [r.randint(1, 100) for _ in range(3)]
    values.append(sum(values))
    r.shuffle(values)
    maximum = max(values)
    answer = sorted(maximum - value for value in values if value != maximum)
    return " ".join(map(str, values)) + "\n", " ".join(map(str, answer)) + "\n"

def case_1221a(r):
    values = [2 ** r.randint(0, 12) for _ in range(r.randint(1, 30))]
    answer = "YES" if sum(value for value in values if value <= 2048) >= 2048 else "NO"
    return "1\n" + str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", answer + "\n"

def case_1327a(r):
    n, k = r.randint(1, 10**4), r.randint(1, 100)
    answer = n >= k * k and (n - k * k) % 2 == 0
    return f"1\n{n} {k}\n", ("YES" if answer else "NO") + "\n"

def case_1328a(r):
    n, k = r.randint(1, 10**6), r.randint(1, 10**6)
    answer = (-n) % k
    return f"1\n{n} {k}\n", f"{answer}\n"

def case_1335a(r):
    candies = r.randint(1, 10**9)
    return f"1\n{candies}\n", f"{max(0, (candies - 1) // 2)}\n"

def case_1352c(r):
    n, k = r.randint(2, 1000), r.randint(1, 10**6)
    return f"1\n{n} {k}\n", f"{k + (k - 1) // (n - 1)}\n"

def case_1374b(r):
    value = r.randint(1, 10**9)
    original, twos, threes = value, 0, 0
    while value % 2 == 0: value //= 2; twos += 1
    while value % 3 == 0: value //= 3; threes += 1
    answer = threes if value == 1 and threes >= twos else -1
    return f"1\n{original}\n", f"{answer}\n"

def case_1475a(r):
    value = r.randint(1, 10**9)
    reduced = value
    while reduced % 2 == 0: reduced //= 2
    return f"1\n{value}\n", ("YES" if reduced > 1 else "NO") + "\n"

def case_1742a(r):
    values = [r.randint(1, 100) for _ in range(3)]
    answer = any(values[index] == values[(index + 1) % 3] + values[(index + 2) % 3] for index in range(3))
    return "1\n" + " ".join(map(str, values)) + "\n", ("YES" if answer else "NO") + "\n"

def case_158b(r):
    groups = [r.randint(1, 4) for _ in range(r.randint(1, 100))]
    counts = [groups.count(size) for size in range(5)]
    taxis = counts[4] + counts[3]
    counts[1] = max(0, counts[1] - counts[3])
    taxis += counts[2] // 2
    if counts[2] % 2:
        taxis += 1; counts[1] = max(0, counts[1] - 2)
    taxis += (counts[1] + 3) // 4
    return str(len(groups)) + "\n" + " ".join(map(str, groups)) + "\n", f"{taxis}\n"

def case_189a(r):
    n, a, b, c = r.randint(1, 4000), r.randint(1, 100), r.randint(1, 100), r.randint(1, 100)
    dp = [-10**9] * (n + 1); dp[0] = 0
    for length in range(1, n + 1):
        dp[length] = max((dp[length - cut] + 1 for cut in (a, b, c) if length >= cut), default=-10**9)
    return f"{n} {a} {b} {c}\n", f"{dp[n]}\n"

def case_368b(r):
    values = [r.randint(1, 50) for _ in range(r.randint(1, 200))]
    queries = [r.randint(1, len(values)) for _ in range(r.randint(1, 100))]
    answer = [str(len(set(values[index - 1:]))) for index in queries]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n" + str(len(queries)) + "\n" + "\n".join(map(str, queries)) + "\n", "\n".join(answer) + "\n"

def case_431c(r):
    n, k, d = r.randint(1, 100), r.randint(1, 100), r.randint(1, 100)
    mod = 1_000_000_007
    small = [0] * (n + 1); total = [0] * (n + 1); small[0] = total[0] = 1
    for value in range(1, n + 1):
        small[value] = sum(small[value - step] for step in range(1, min(k, d - 1, value) + 1)) % mod
        total[value] = sum(total[value - step] for step in range(1, min(k, value) + 1)) % mod
    return f"{n} {k} {d}\n", f"{(total[n] - small[n]) % mod}\n"

def case_433b(r):
    values = [r.randint(1, 1000) for _ in range(r.randint(1, 100))]
    ordered = sorted(values); queries = []
    for _ in range(r.randint(1, 100)):
        kind = r.randint(1, 2); left = r.randint(1, len(values)); right = r.randint(left, len(values)); queries.append((kind, left, right))
    answer = [str(sum((values if kind == 1 else ordered)[left - 1:right])) for kind, left, right in queries]
    text = str(len(values)) + "\n" + " ".join(map(str, values)) + "\n" + str(len(queries)) + "\n" + "".join(f"{kind} {left} {right}\n" for kind, left, right in queries)
    return text, "\n".join(answer) + "\n"

def case_466c(r):
    values = [r.randint(-20, 20) for _ in range(r.randint(1, 100))]
    total = sum(values)
    answer = 0
    if total % 3 == 0:
        target, prefix, first = total // 3, 0, 0
        for value in values[:-1]:
            prefix += value
            if prefix == 2 * target: answer += first
            if prefix == target: first += 1
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", f"{answer}\n"

def case_230b(r):
    import math
    values = [r.randint(1, 10**12) for _ in range(r.randint(1, 80))]
    def prime(value):
        if value < 2: return False
        for divisor in range(2, int(math.isqrt(value)) + 1):
            if value % divisor == 0: return False
        return True
    answer = ["YES" if (root := math.isqrt(value)) ** 2 == value and prime(root) else "NO" for value in values]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n", "\n".join(answer) + "\n"

def case_474d(r):
    k = r.randint(1, 30); queries = []
    for _ in range(r.randint(1, 50)):
        left = r.randint(1, 200); queries.append((left, r.randint(left, 200)))
    mod = 1_000_000_007; dp = [0] * 201; dp[0] = 1
    for value in range(1, 201): dp[value] = (dp[value - 1] + (dp[value - k] if value >= k else 0)) % mod
    prefix = [0]
    for value in dp[1:]: prefix.append((prefix[-1] + value) % mod)
    return f"{len(queries)} {k}\n" + "".join(f"{a} {b}\n" for a, b in queries), "\n".join(str((prefix[b] - prefix[a - 1]) % mod) for a, b in queries) + "\n"

def case_489b(r):
    boys = [r.randint(1, 100) for _ in range(r.randint(1, 80))]; girls = [r.randint(1, 100) for _ in range(r.randint(1, 80))]
    i = j = answer = 0
    for boy in sorted(boys):
        while j < len(girls) and sorted(girls)[j] < boy - 1: j += 1
        if j < len(girls) and abs(sorted(girls)[j] - boy) <= 1: answer += 1; j += 1
    return f"{len(boys)}\n{' '.join(map(str,boys))}\n{len(girls)}\n{' '.join(map(str,girls))}\n", f"{answer}\n"

def case_1364a(r):
    x = r.randint(1, 30); values = [r.randint(1, 100) for _ in range(r.randint(1, 100))]
    total = sum(values)
    if total % x: answer = len(values)
    else:
        left = next((i for i, value in enumerate(values) if value % x), None)
        right = next((i for i, value in enumerate(reversed(values)) if value % x), None)
        answer = -1 if left is None else len(values) - 1 - min(left, right)
    return f"1\n{len(values)} {x}\n{' '.join(map(str,values))}\n", f"{answer}\n"

def case_1374c(r):
    text = "".join(r.choice("()") for _ in range(r.randint(1, 200)))
    opened = removed = 0
    for char in text:
        if char == '(': opened += 1
        elif opened: opened -= 1
        else: removed += 1
    return f"1\n{text}\n", f"{removed + opened}\n"

def case_1398c(r):
    text = "".join(str(r.randint(0, 9)) for _ in range(r.randint(1, 200)))
    counts = {0: 1}; prefix = answer = 0
    for index, char in enumerate(text, 1):
        prefix += int(char); key = prefix - index; answer += counts.get(key, 0); counts[key] = counts.get(key, 0) + 1
    return f"1\n{len(text)}\n{text}\n", f"{answer}\n"

def case_1520d(r):
    values = [r.randint(1, 1000) for _ in range(r.randint(1, 200))]; counts = {}; answer = 0
    for index, value in enumerate(values):
        key = value - index; answer += counts.get(key, 0); counts[key] = counts.get(key, 0) + 1
    return f"1\n{len(values)}\n{' '.join(map(str,values))}\n", f"{answer}\n"

def case_1195c(r):
    top = [r.randint(1, 1000) for _ in range(r.randint(1, 100))]; bottom = [r.randint(1, 1000) for _ in top]
    none = up = down = 0
    for a, b in zip(top, bottom):
        none, up, down = max(none, up, down), max(none, down) + a, max(none, up) + b
    return str(len(top)) + "\n" + " ".join(map(str, top)) + "\n" + " ".join(map(str, bottom)) + "\n", f"{max(none, up, down)}\n"

def case_1829d(r):
    n, m = r.randint(1, 10**6), r.randint(1, 10**6)
    def possible(value):
        if value == m: return True
        return value % 3 == 0 and (possible(value // 3) or possible(value // 3 * 2))
    return f"1\n{n} {m}\n", ("YES" if possible(n) else "NO") + "\n"

def case_1829e(r):
    rows, cols = r.randint(1, 20), r.randint(1, 20)
    grid = [[r.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
    seen, best = set(), 0
    for i in range(rows):
        for j in range(cols):
            if not grid[i][j] or (i, j) in seen: continue
            seen.add((i, j)); stack = [(i, j)]; total = 0
            while stack:
                x, y = stack.pop(); total += grid[x][y]
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] and (nx, ny) not in seen:
                        seen.add((nx, ny)); stack.append((nx, ny))
            best = max(best, total)
    return f"1\n{rows} {cols}\n" + "".join(" ".join(map(str,row)) + "\n" for row in grid), f"{best}\n"

def case_1850h(r):
    nodes, edges = r.randint(2, 30), r.randint(1, 60)
    graph = [[] for _ in range(nodes)]; rows = []
    for _ in range(edges):
        a, b, weight = r.randrange(nodes), r.randrange(nodes), r.randint(-20, 20)
        if a == b: b = (b + 1) % nodes
        rows.append((a, b, weight)); graph[a].append((b, weight)); graph[b].append((a, -weight))
    values, valid = {}, True
    for root in range(nodes):
        if root in values: continue
        values[root] = 0; stack = [root]
        while stack:
            node = stack.pop()
            for nxt, weight in graph[node]:
                target = values[node] + weight
                if nxt in values:
                    valid &= values[nxt] == target
                else: values[nxt] = target; stack.append(nxt)
    return f"1\n{nodes} {len(rows)}\n" + "".join(f"{a+1} {b+1} {w}\n" for a,b,w in rows), ("YES" if valid else "NO") + "\n"

def case_1881c(r):
    n = r.choice((2, 4, 6, 8, 10)); grid = [[r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n)] for _ in range(n)]
    answer = 0
    for i in range(n // 2):
        for j in range(i, n - i - 1):
            cells = (grid[i][j], grid[j][n-1-i], grid[n-1-i][n-1-j], grid[n-1-j][i])
            highest = max(cells)
            answer += sum(ord(highest) - ord(char) for char in cells)
    return f"1\n{n}\n" + "".join("".join(row) + "\n" for row in grid), f"{answer}\n"

def case_1425a(r):
    n, m = r.randint(1, 10**6), r.randint(1, 10**6)
    return f"1\n{n} {m}\n", f"{(n - 1) * (m - 1)}\n"

def case_1526c1(r):
    import heapq
    values = [r.randint(-1000, 1000) for _ in range(r.randint(1, 200))]
    total = count = 0; chosen = []
    for value in values:
        total += value; count += 1; heapq.heappush(chosen, value)
        if total < 0: total -= heapq.heappop(chosen); count -= 1
    return f"{len(values)}\n{' '.join(map(str, values))}\n", f"{count}\n"

def case_1879b(r):
    first = [r.randint(1, 1000) for _ in range(r.randint(1, 100))]
    second = [r.randint(1, 1000) for _ in first]
    answer = len(first) * (min(first) + min(second))
    return f"1\n{len(first)}\n{' '.join(map(str, first))}\n{' '.join(map(str, second))}\n", f"{answer}\n"

def case_1b(r):
    row, column = r.randint(1, 10**6), r.randint(1, 10**6)
    letters = ""; value = column
    while value: value, remain = divmod(value - 1, 26); letters = chr(65 + remain) + letters
    if r.randrange(2):
        payload, answer = f"R{row}C{column}", f"{letters}{row}"
    else:
        payload, answer = f"{letters}{row}", f"R{row}C{column}"
    return f"1\n{payload}\n", answer + "\n"

def case_460b(r):
    a, b, c = r.randint(1, 5), r.randint(1, 20), r.randint(-100, 100)
    answers = []
    for digit_sum in range(1, 82):
        value = b * digit_sum ** a + c
        if 0 < value < 10**9 and sum(map(int, str(value))) == digit_sum: answers.append(value)
    return f"{a} {b} {c}\n", str(len(answers)) + ("\n" + " ".join(map(str, answers)) if answers else "\n")

def case_545c(r):
    count = r.randint(1, 100); positions = sorted(r.sample(range(1, 5000), count)); heights = [r.randint(1, 100) for _ in positions]
    answer, right = 0, -10**9
    for index, (position, height) in enumerate(zip(positions, heights)):
        next_position = positions[index + 1] if index + 1 < count else 10**18
        if position - height > right: answer += 1; right = position
        elif position + height < next_position: answer += 1; right = position + height
        else: right = position
    return str(count) + "\n" + "".join(f"{p} {h}\n" for p,h in zip(positions,heights)), f"{answer}\n"

def case_580c(r):
    nodes, limit = r.randint(1, 100), r.randint(0, 10); cats = [r.randint(0, 1) for _ in range(nodes)]
    edges = []
    for node in range(1, nodes): edges.append((r.randrange(node), node))
    graph = [[] for _ in range(nodes)]
    for a,b in edges: graph[a].append(b); graph[b].append(a)
    answer = 0; stack = [(0, -1, cats[0])]
    while stack:
        node, parent, consecutive = stack.pop()
        if consecutive > limit: continue
        children = [child for child in graph[node] if child != parent]
        if not children: answer += 1
        for child in children: stack.append((child, node, consecutive + 1 if cats[child] else 0))
    return f"{nodes} {limit}\n{' '.join(map(str,cats))}\n" + "".join(f"{a+1} {b+1}\n" for a,b in edges), f"{answer}\n"

def case_893c(r):
    nodes, edges = r.randint(1, 100), r.randint(0, 150); costs = [r.randint(1, 1000) for _ in range(nodes)]
    pairs = set()
    while len(pairs) < min(edges, nodes * (nodes - 1) // 2):
        a,b = r.sample(range(nodes),2); pairs.add(tuple(sorted((a,b))))
    graph = [[] for _ in range(nodes)]
    for a,b in pairs: graph[a].append(b); graph[b].append(a)
    seen, answer = set(), 0
    for root in range(nodes):
        if root in seen: continue
        seen.add(root); stack=[root]; cheapest=costs[root]
        while stack:
            node=stack.pop(); cheapest=min(cheapest,costs[node])
            for nxt in graph[node]:
                if nxt not in seen: seen.add(nxt); stack.append(nxt)
        answer += cheapest
    return f"{nodes} {len(pairs)}\n{' '.join(map(str,costs))}\n" + "".join(f"{a+1} {b+1}\n" for a,b in pairs), f"{answer}\n"

def case_1443c(r):
    a = [r.randint(1, 1000) for _ in range(r.randint(1, 100))]
    b = [r.randint(1, 1000) for _ in a]
    pairs = sorted(zip(a, b)); remaining = sum(b); answer = remaining; current = 0
    for left, right in pairs:
        current = max(current, left); remaining -= right; answer = min(answer, max(current, remaining))
    return f"1\n{len(a)}\n{' '.join(map(str,a))}\n{' '.join(map(str,b))}\n", f"{answer}\n"

def case_2033d(r):
    values = [r.randint(-20, 20) for _ in range(r.randint(1, 200))]
    prefixes, running, answer = {0}, 0, 0
    for value in values:
        running += value
        if running in prefixes:
            answer += 1; prefixes = {0}; running = value
        prefixes.add(running)
    return f"1\n{len(values)}\n{' '.join(map(str,values))}\n", f"{answer}\n"

def case_508a(r):
    rows, cols, moves = r.randint(1, 20), r.randint(1, 20), r.randint(1, 100)
    plan = [(r.randint(0, rows - 1), r.randint(0, cols - 1)) for _ in range(moves)]; black=set(); answer=-1
    for index,(x,y) in enumerate(plan,1):
        black.add((x,y))
        if any({(a,b),(a+1,b),(a,b+1),(a+1,b+1)} <= black for a in (x-1,x) for b in (y-1,y)): answer=index; break
    return f"{rows} {cols} {moves}\n" + "".join(f"{x+1} {y+1}\n" for x,y in plan), f"{answer}\n"

def case_1163b2(r):
    values = [r.randint(1, 30) for _ in range(r.randint(1, 100))]; answer=0
    from collections import Counter
    for length in range(1,len(values)+1):
        counts=Counter(values[:length]); good=False
        for color in list(counts):
            counts[color]-=1
            if counts[color]==0: del counts[color]
            if len(set(counts.values()))<=1: good=True
            counts[color]=counts.get(color,0)+1
            if good: answer=length; break
    return str(len(values))+"\n"+" ".join(map(str,values))+"\n",f"{answer}\n"

def case_1427b(r):
    n,k=r.randint(1,100),r.randint(0,100); text="".join(r.choice("LW") for _ in range(n)); k=min(k,n); original_k=k
    wins=[i for i,ch in enumerate(text) if ch=='W']
    if not wins: answer=0 if not k else 2*min(n,k)-1
    else:
        score=len(wins)+sum(text[i]==text[i-1]=='W' for i in range(1,n)); gaps=sorted(wins[i]-wins[i-1]-1 for i in range(1,len(wins)))
        for gap in gaps:
            if k>=gap: k-=gap; score+=2*gap+1
        score+=2*min(k, text.count('L')); answer=score
    return f"1\n{n} {original_k}\n{text}\n",f"{answer}\n"

def case_2075c(r):
    n,m=r.randint(2,30),r.randint(2,20); capacity=[r.randint(1,n) for _ in range(m)]; answer=0
    for split in range(1,n):
        for i in range(m):
            for j in range(m):
                if i!=j and capacity[i]>=split and capacity[j]>=n-split: answer+=1
    return f"1\n{n} {m}\n{' '.join(map(str,capacity))}\n",f"{answer}\n"

def case_2132b(r):
    value=r.randint(11,10**12); answers=[]; power=10
    while power<=10**18:
        divisor=power+1
        if value%divisor==0 and value//divisor>0: answers.append(value//divisor)
        power*=10
    answers=sorted(set(answers))
    return f"1\n{value}\n",str(len(answers))+("\n"+" ".join(map(str,answers)) if answers else "")+"\n"

def case_986b(r):
    n=r.randint(3,100); perm=list(range(1,n+1)); r.shuffle(perm)
    inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2
    return f"{n}\n{' '.join(map(str,perm))}\n",("Petr" if inversions==n%2 else "Um_nik")+"\n"

def case_1000b(r):
    limit=r.randint(3,200); points=sorted(r.sample(range(1,limit),r.randint(1,min(20,limit-1))))
    def lit(sequence):
        all_points=[0]+sequence+[limit]
        return sum(all_points[i+1]-all_points[i] for i in range(0,len(all_points)-1,2))
    answer=max(lit(points),*(lit(sorted(points+[time])) for time in range(1,limit) if time not in points))
    return f"{len(points)} {limit}\n{' '.join(map(str,points))}\n",f"{answer}\n"

def case_2196b(r):
    values=[r.randint(1,100) for _ in range(r.randint(2,200))]
    answer=sum(values[i]*values[j]==j-i for i in range(len(values)) for j in range(i+1,len(values)))
    return f"1\n{len(values)}\n{' '.join(map(str,values))}\n",f"{answer}\n"

def case_1875d(r):
    from functools import lru_cache
    values=tuple(r.randint(0,8) for _ in range(r.randint(1,9)))
    @lru_cache(None)
    def solve(state):
        if not state:return 0
        available=set(state); mex=0
        while mex in available:mex+=1
        return mex+min(solve(state[:i]+state[i+1:]) for i in range(len(state)))
    return f"1\n{len(values)}\n{' '.join(map(str,values))}\n",f"{solve(values)}\n"

def case_1985h1(r):
    rows,cols=r.randint(1,8),r.randint(1,8); grid=[[r.choice('.#') for _ in range(cols)] for _ in range(rows)]
    def largest(board):
        seen=set(); best=0
        for i in range(rows):
            for j in range(cols):
                if board[i][j]!='#' or (i,j) in seen:continue
                seen.add((i,j)); stack=[(i,j)]; size=0
                while stack:
                    x,y=stack.pop(); size+=1
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<rows and 0<=ny<cols and board[nx][ny]=='#' and (nx,ny) not in seen:seen.add((nx,ny));stack.append((nx,ny))
                best=max(best,size)
        return best
    answer=largest(grid)
    for index in range(rows+cols):
        board=[row[:] for row in grid]
        if index<rows:
            for j in range(cols):board[index][j]='#'
        else:
            for i in range(rows):board[i][index-rows]='#'
        answer=max(answer,largest(board))
    return f"1\n{rows} {cols}\n"+"".join("".join(row)+"\n" for row in grid),f"{answer}\n"

def case_2193d(r):
    n=r.randint(1,50); swords=[r.randint(1,100) for _ in range(n)]; strikes=[r.randint(1,n) for _ in range(n)]
    answer=0
    for level in set(swords):
        available=sum(value>=level for value in swords); used=completed=0
        for required in strikes:
            used+=required
            if used>available:break
            completed+=1
        answer=max(answer,level*completed)
    return f"1\n{n}\n{' '.join(map(str,swords))}\n{' '.join(map(str,strikes))}\n",f"{answer}\n"

def case_803a(r):
    n=r.randint(1,4); k=r.randint(0,n*n); pairs=[(i,j) for i in range(n) for j in range(i,n)]
    best=None
    for mask in range(1<<len(pairs)):
        board=[[0]*n for _ in range(n)]
        for bit,(i,j) in enumerate(pairs):
            if mask>>bit&1: board[i][j]=board[j][i]=1
        if sum(map(sum,board))==k:
            flat=tuple(value for row in board for value in row)
            if best is None or flat>best:best=flat
    if best is None:return f"{n} {k}\n","-1\n"
    return f"{n} {k}\n","\n".join(" ".join(map(str,best[i*n:(i+1)*n])) for i in range(n))+"\n"

def case_20b(r):
    a,b,c=r.randint(-100,100),r.randint(-100,100),r.randint(-100,100)
    if not a and not b:a=1
    if not a:
        root=-c/b; answer=f"1\n{root:.10f}\n"
    else:
        disc=b*b-4*a*c
        if disc<0:answer="0\n"
        elif disc==0:answer=f"1\n{-b/(2*a):.10f}\n"
        else:
            import math
            roots=sorted(((-b-math.sqrt(disc))/(2*a),(-b+math.sqrt(disc))/(2*a)))
            answer=f"2\n{roots[0]:.10f}\n{roots[1]:.10f}\n"
    return f"{a} {b} {c}\n",answer

def case_492b(r):
    length=r.randint(1,10000); positions=sorted(r.sample(range(length+1),r.randint(1,min(100,length+1))))
    gaps=[positions[0],length-positions[-1]]+[ (positions[i]-positions[i-1])/2 for i in range(1,len(positions))]
    return f"{len(positions)} {length}\n{' '.join(map(str,positions))}\n",f"{max(gaps):.10f}\n"

def case_2131c(r):
    n,k=r.randint(1,30),r.randint(1,20); first=[r.randint(0,100) for _ in range(n)]; second=[r.randint(0,100) for _ in range(n)]
    key=lambda value:min(value%k,(-value)%k)
    answer=sorted(map(key,first))==sorted(map(key,second))
    return f"1\n{n} {k}\n{' '.join(map(str,first))}\n{' '.join(map(str,second))}\n",("YES" if answer else "NO")+"\n"

def case_2193e(r):
    n=r.randint(1,30); values=[r.randint(1,n) for _ in range(n)]; inf=10**9; dp=[inf]*(n+1)
    if 1 in values:dp[1]=1
    for target in range(2,n+1):
        dp[target]=min((dp[target//value]+1 for value in values if value>1 and target%value==0),default=inf)
    answer=[str(value if value<inf else -1) for value in dp[1:]]
    return f"1\n{n}\n{' '.join(map(str,values))}\n", " ".join(answer)+"\n"

def case_2209e(r):
    text="".join(r.choice("abc") for _ in range(r.randint(1,25))); queries=[]
    for _ in range(r.randint(1,30)):
        left=r.randint(1,len(text)); queries.append((left,r.randint(left,len(text))))
    def parts(word):
        dp=[-10**9]*(len(word)+1);dp[0]=0
        for index in range(len(word)):
            for size in range(1,len(word)-index+1):
                if word[index:index+size]==word[:size]:dp[index+size]=max(dp[index+size],dp[index]+1)
        return dp[-1]
    answer=[]
    for left,right in queries:answer.append(str(sum(parts(text[left-1:end]) for end in range(left,right+1))))
    return f"1\n{len(text)} {len(queries)}\n{text}\n"+"".join(f"{a} {b}\n" for a,b in queries),"\n".join(answer)+"\n"

def case_2200g(r):
    from fractions import Fraction
    from itertools import permutations
    operations=[(r.choice("+-x/"),r.randint(1,10)) for _ in range(r.randint(1,6))]; initial=r.randint(1,20)
    total=Fraction(0)
    for order in permutations(operations):
        value=Fraction(initial)
        for op,arg in order:
            if op=='+':value+=arg
            elif op=='-':value-=arg
            elif op=='x':value*=arg
            else:value/=arg
        total+=value
    average=total/Fraction(len(list(permutations(operations))))
    mod=1_000_000_007; answer=(average.numerator%mod)*pow(average.denominator%mod,mod-2,mod)%mod
    return f"1\n{len(operations)} {initial}\n"+"\n".join(op+str(arg) for op,arg in operations)+"\n",f"{answer}\n"

def case_313b(r):
    text="".join(r.choice(".#") for _ in range(r.randint(2,200))); queries=[]
    for _ in range(r.randint(1,100)):
        left=r.randint(1,len(text)-1);queries.append((left,r.randint(left+1,len(text))))
    answer=[str(sum(text[i]==text[i+1] for i in range(a-1,b-1))) for a,b in queries]
    return text+"\n"+str(len(queries))+"\n"+"".join(f"{a} {b}\n" for a,b in queries),"\n".join(answer)+"\n"

def case_1749c(r):
    values=[r.randint(1,100) for _ in range(r.randint(1,100))]; answer=0
    for value in sorted(values):
        if value>answer:answer+=1
    return f"1\n{len(values)}\n{' '.join(map(str,values))}\n",f"{answer}\n"

def case_2184f(r):
    nodes=r.randint(1,10); edges=[]
    for node in range(1,nodes):edges.append((r.randrange(node),node))
    children=[[] for _ in range(nodes)]
    for a,b in edges:children[a].append(b)
    subtree=[]
    def visit(node):
        found=[]
        if not children[node]:found=[node]
        for child in children[node]:found+=visit(child)
        subtree.append(set(found)); return found
    leaf_set=set(visit(0))
    answer=False
    for mask in range(1<<nodes):
        if bin(mask).count("1")%3:continue
        covered=set(); good=True
        for node in range(nodes):
            if mask>>node&1:
                group=subtree[node]
                if covered&group:good=False;break
                covered|=group
        if good and covered==leaf_set:answer=True;break
    return f"1\n{nodes}\n"+"".join(f"{a+1} {b+1}\n" for a,b in edges),("YES" if answer else "NO")+"\n"


def case_50a(r):
    m, n = r.randint(1, 16), r.randint(1, 16)
    return f"{m} {n}\n", f"{m * n // 2}\n"


def case_96a(r):
    groups = [str(r.randrange(2)) * r.randint(1, 8) for _ in range(r.randint(1, 8))]
    text = "".join(groups)
    return text + "\n", ("YES" if "0000000" in text or "1111111" in text else "NO") + "\n"


def case_112a(r):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    first = "".join(r.choice(alphabet) for _ in range(r.randint(1, 12)))
    mode = r.randrange(3)
    if mode == 0:
        second = first
    elif mode == 1:
        second = first[:-1] + chr(min(ord('z'), ord(first[-1]) + 1))
    else:
        second = first[:-1] + chr(max(ord('a'), ord(first[-1]) - 1))
    decorate = lambda word: "".join(ch.upper() if r.randrange(2) else ch for ch in word)
    first, second = decorate(first), decorate(second)
    answer = (first.lower() > second.lower()) - (first.lower() < second.lower())
    return f"{first}\n{second}\n", f"{answer}\n"


def case_151a(r):
    n, k, liters, limes, slices, salt, need = (r.randint(1, 20), r.randint(1, 20),
                                                r.randint(1, 20), r.randint(1, 30),
                                                r.randint(1, 10), r.randint(1, 200), r.randint(1, 10))
    value = min(k * liters // need, limes * slices, salt // need) // n
    return f"{n} {k} {liters} {limes} {slices} {salt} {need}\n", f"{value}\n"


def case_231a(r):
    rows = [[r.randrange(2) for _ in range(3)] for _ in range(r.randint(1, 20))]
    return str(len(rows)) + "\n" + "".join(" ".join(map(str, row)) + "\n" for row in rows), f"{sum(sum(row) >= 2 for row in rows)}\n"


def case_236a(r):
    text = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 30)))
    return text + "\n", ("CHAT WITH HER!" if len(set(text)) % 2 == 0 else "IGNORE HIM!") + "\n"


def case_263a(r):
    row, col = r.randrange(5), r.randrange(5)
    grid = [[0] * 5 for _ in range(5)]
    grid[row][col] = 1
    return "".join(" ".join(map(str, line)) + "\n" for line in grid), f"{abs(row - 2) + abs(col - 2)}\n"


def case_266a(r):
    text = "".join(r.choice("RGB") for _ in range(r.randint(1, 50)))
    return f"{len(text)}\n{text}\n", f"{sum(a == b for a, b in zip(text, text[1:]))}\n"


def case_270a(r):
    angle = r.randint(1, 179)
    return f"1\n{angle}\n", ("YES" if 360 % (180 - angle) == 0 else "NO") + "\n"


def case_281a(r):
    text = r.choice("abcdefghijklmnopqrstuvwxyz") + "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(0, 20)))
    return text + "\n", text[0].upper() + text[1:] + "\n"


def case_282a(r):
    operations = [r.choice(("X++", "++X", "X--", "--X")) for _ in range(r.randint(1, 50))]
    value = sum(1 if "+" in op else -1 for op in operations)
    return str(len(operations)) + "\n" + "\n".join(operations) + "\n", f"{value}\n"


def case_339a(r):
    values = [str(r.randint(1, 3)) for _ in range(r.randint(1, 50))]
    return "+".join(values) + "\n", "+".join(sorted(values)) + "\n"


def case_479a(r):
    a, b, c = r.randint(1, 10), r.randint(1, 10), r.randint(1, 10)
    answer = max(a + b + c, a * b * c, (a + b) * c, a * (b + c))
    return f"{a}\n{b}\n{c}\n", f"{answer}\n"


def case_996a_fixed(r):
    value = r.randint(1, 10**9)
    original, count = value, 0
    for bill in (100, 20, 10, 5, 1):
        count, value = count + value // bill, value % bill
    return f"{original}\n", f"{count}\n"


def case_2140b(r):
    x = r.randint(1, 1000)
    for y in range(1, 100_000):
        if int(str(x) + str(y)) % (x + y) == 0:
            return f"1\n{x}\n", f"{y}\n"
    raise RuntimeError("no witness found")


def case_363b(r):
    values = [r.randint(1, 1000) for _ in range(r.randint(1, 200))]
    width = r.randint(1, len(values))
    sums = [sum(values[index:index + width]) for index in range(len(values) - width + 1)]
    return f"{len(values)} {width}\n{' '.join(map(str, values))}\n", f"{sums.index(min(sums)) + 1}\n"


def case_550c(r):
    text = "".join(str(r.randint(0, 9)) for _ in range(r.randint(1, 12)))
    witness = next(("".join(text[index] for index in range(len(text)) if mask >> index & 1)
                    for mask in range(1, 1 << len(text))
                    if int("".join(text[index] for index in range(len(text)) if mask >> index & 1)) % 8 == 0), None)
    return text + "\n", ("YES\n" + witness + "\n" if witness else "NO\n")


def case_584a(r):
    digits, divisor = r.randint(2, 6), r.randint(2, 9)
    lower = 10 ** (digits - 1)
    value = ((lower + divisor - 1) // divisor) * divisor
    return f"{digits} {divisor}\n", f"{value}\n"


def case_1352a(r):
    value = r.randint(1, 10**9)
    parts = [int(char) * 10**index for index, char in enumerate(reversed(str(value))) if char != "0"]
    return f"1\n{value}\n", str(len(parts)) + "\n" + " ".join(map(str, parts)) + "\n"


def case_1366d(r):
    values = [r.choice((2**r.randint(1,10), 3**r.randint(1,8), 2**r.randint(1,6)*3**r.randint(1,6), 2**r.randint(1,5)*5**r.randint(1,5))) for _ in range(r.randint(1,30))]
    first=[]; second=[]
    for value in values:
        factor=next((d for d in range(2,value+1) if value%d==0),value); rest=value
        while rest%factor==0:rest//=factor
        if rest==1:first.append(-1);second.append(-1)
        else:first.append(factor);second.append(rest)
    return str(len(values))+"\n"+" ".join(map(str,values))+"\n"," ".join(map(str,first))+"\n"+" ".join(map(str,second))+"\n"


def case_20c(r):
    nodes=r.randint(2,30); edges=[]
    for node in range(2,nodes+1): edges.append((r.randint(1,node-1),node,r.randint(1,100)))
    extra=r.randint(0,30)
    for _ in range(extra):
        a,b=r.sample(range(1,nodes+1),2); edges.append((a,b,r.randint(1,100)))
    return f"{nodes} {len(edges)}\n"+"".join(f"{a} {b} {w}\n" for a,b,w in edges),"\n"


def case_1729c(r):
    text="".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(2,100)))
    increasing=text[0]<=text[-1]; indices=[0]+[i for i in range(1,len(text)-1) if min(text[0],text[-1])<=text[i]<=max(text[0],text[-1])]+[len(text)-1]
    indices=sorted(indices,key=lambda i:ord(text[i]),reverse=not increasing)
    return f"1\n{text}\n",f"{abs(ord(text[0])-ord(text[-1]))} {len(indices)}\n"+" ".join(str(i+1) for i in indices)+"\n"


def case_1833b(r):
    n, limit = r.randint(1,100), r.randint(0,100)
    forecast = [r.randint(-1000,1000) for _ in range(n)]
    actual = [value+r.randint(-limit,limit) for value in forecast]
    r.shuffle(actual)
    # A valid witness exists by retaining the pre-shuffle assignment.
    return f"1\n{n} {limit}\n{' '.join(map(str,forecast))}\n{' '.join(map(str,actual))}\n", "\n"


def case_1843d(r):
    nodes=r.randint(2,100); edges=[]
    for node in range(1,nodes):edges.append((r.randrange(node),node))
    graph=[[] for _ in range(nodes)]
    for a,b in edges:graph[a].append(b);graph[b].append(a)
    leaves=[0]*nodes
    def dfs(node,parent):
        children=[nxt for nxt in graph[node] if nxt!=parent]
        leaves[node]=1 if not children else sum(dfs(nxt,node) for nxt in children)
        return leaves[node]
    dfs(0,-1); queries=[(r.randrange(nodes),r.randrange(nodes)) for _ in range(r.randint(1,100))]
    return f"1\n{nodes}\n"+"".join(f"{a+1} {b+1}\n" for a,b in edges)+str(len(queries))+"\n"+"".join(f"{a+1} {b+1}\n" for a,b in queries),"\n".join(str(leaves[a]*leaves[b]) for a,b in queries)+"\n"


def case_2171d(r):
    from itertools import product
    n=r.randint(2,6); permutation=list(range(1,n+1));r.shuffle(permutation); position={value:index for index,value in enumerate(permutation)}
    def edges(code):
        degree=[1]*n
        for value in code:degree[value]+=1
        result=[]
        for value in code:
            leaf=next(i for i,d in enumerate(degree) if d==1);result.append((leaf,value));degree[leaf]-=1;degree[value]-=1
        tail=[i for i,d in enumerate(degree) if d==1];result.append(tuple(tail));return result
    answer=False
    for code in product(range(n),repeat=n-2):
        if all(position[min(a,b)+1]<position[max(a,b)+1] for a,b in edges(code)):answer=True;break
    return f"1\n{n}\n{' '.join(map(str,permutation))}\n",("YES" if answer else "NO")+"\n"


def case_2171e(r):
    from itertools import permutations
    import math
    def witness(n):
        for permutation in permutations(range(1, n + 1)):
            bad = sum(math.gcd(a, b) == math.gcd(a, c) == math.gcd(b, c) == 1
                      for a, b, c in zip(permutation, permutation[1:], permutation[2:]))
            if bad <= 6:
                return permutation
        raise RuntimeError("no good permutation")
    sizes = [r.randint(3, 8), r.randint(3, 8)]
    return "2\n" + "\n".join(map(str, sizes)) + "\n", "\n".join(" ".join(map(str, witness(n))) for n in sizes) + "\n"


def case_1868a(r):
    from itertools import product, permutations
    def mex(values):
        value = 0
        while value in values: value += 1
        return value
    def solve(n, m):
        best, witness = -1, None
        for rows in product(list(permutations(range(m))), repeat=n):
            beauty = mex([mex([rows[i][j] for i in range(n)]) for j in range(m)])
            if beauty > best: best, witness = beauty, rows
        return str(best) + "\n" + "\n".join(" ".join(map(str, row)) for row in witness) + "\n"
    sizes = [(r.randint(1, 3), r.randint(1, 3)), (r.randint(1, 3), r.randint(1, 3))]
    return "2\n" + "".join(f"{n} {m}\n" for n,m in sizes), "".join(solve(n,m) for n,m in sizes)


def case_2196a(r):
    p, q = r.randint(1, 10**12), r.randint(1, 10**12)
    delta = q - p
    winner = "Bob" if delta > 0 and p >= 2 * delta and q >= 3 * delta else "Alice"
    return f"1\n{p} {q}\n", winner + "\n"


def case_2218a(r):
    values = [r.randint(-67, 67) for _ in range(r.randint(1, 20))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n", "\n".join(map(str, values)) + "\n"


def case_2218b(r):
    values = [r.randint(-67, 67) for _ in range(7)]
    return "1\n" + " ".join(map(str, values)) + "\n", f"{2 * max(values) - sum(values)}\n"


def case_2218e(r):
    values = [r.randint(0, 10**6) for _ in range(r.randint(2, 100))]
    answer = max(a ^ b for index, a in enumerate(values) for b in values[index+1:])
    return f"1\n{len(values)}\n{' '.join(map(str, values))}\n", f"{answer}\n"


def case_2218c(r):
    sizes = [r.randint(1, 30), r.randint(1, 30)]
    rows = []
    for n in sizes:
        values = []
        for i in range(1, n + 1): values += [i, n + 2*i - 1, n + 2*i]
        rows.append(" ".join(map(str, values)))
    return "2\n" + "\n".join(map(str, sizes)) + "\n", "\n".join(rows) + "\n"


def case_2218d(r):
    sizes = [r.randint(2,100), r.randint(2,100)]
    rows = [" ".join(str((2*i-1)*(2*i+1)) for i in range(1,n+1)) for n in sizes]
    return "2\n" + "\n".join(map(str, sizes)) + "\n", "\n".join(rows) + "\n"


def case_2227b(r):
    text = "".join(r.choice("()") for _ in range(r.randint(1,200)))
    return f"1\n{len(text)}\n{text}\n", ("YES" if text.count("(") == text.count(")") else "NO") + "\n"


def case_2227a(r):
    x, y = r.randint(1, 10), r.randint(1, 10)
    return f"1\n{x} {y}\n", ("NO" if x % 2 and y % 2 else "YES") + "\n"


def case_2227c(r):
    from itertools import permutations
    values = [r.randint(1, 30) for _ in range(r.randint(1, 8))]
    def score(sequence):
        total = 0
        for left in range(len(sequence)):
            product = 1
            for right in range(left, len(sequence)):
                product *= sequence[right]
                if product % 6 == 0: total += 1
        return total
    witness = min(permutations(values), key=score)
    return f"1\n{len(values)}\n{' '.join(map(str, values))}\n", " ".join(map(str, witness)) + "\n"


BUILDERS = {
    "1A": case_1a, "25A": case_25a, "50A": case_50a, "58A": case_58a,
    "69A": case_69a, "71A": case_71a, "96A": case_96a, "112A": case_112a,
    "118A": case_118a, "122A": case_122a, "131A": case_131a,
    "151A": case_151a, "231A": case_231a, "236A": case_236a, "263A": case_263a,
    "266A": case_266a, "270A": case_270a, "281A": case_281a, "282A": case_282a,
    "339A": case_339a, "479A": case_479a, "996A": case_996a_fixed, "158A": case_158a,
    "160A": case_160a, "230A": case_230a,
    "34B": case_34b, "339B": case_339b, "427A": case_427a, "455A": case_455a,
    "456A": case_456a, "460A": case_460a_fixed, "466A": case_466a, "579A": case_579a,
    "580A": case_580a,
    "615A": case_615a, "698A": case_698a, "705A": case_705a, "706B": case_706b,
    "723A": case_723a, "903C": case_903c,
    "200B": case_200b, "474A": case_474a, "545D": case_545d,
    "1154A": case_1154a, "1221A": case_1221a, "1327A": case_1327a, "1328A": case_1328a,
    "1335A": case_1335a, "1352C": case_1352c, "1374B": case_1374b, "1475A": case_1475a,
    "1742A": case_1742a,
    "158B": case_158b, "189A": case_189a, "368B": case_368b, "431C": case_431c,
    "433B": case_433b, "466C": case_466c,
    "230B": case_230b, "474D": case_474d, "489B": case_489b, "1364A": case_1364a,
    "1374C": case_1374c, "1398C": case_1398c, "1520D": case_1520d,
    "1195C": case_1195c, "1829D": case_1829d, "1829E": case_1829e, "1850H": case_1850h,
    "1881C": case_1881c,
    "1425A": case_1425a, "1526C1": case_1526c1, "1879B": case_1879b,
    "1B": case_1b, "460B": case_460b, "545C": case_545c, "580C": case_580c, "893C": case_893c,
    "1443C": case_1443c, "2033D": case_2033d,
    "508A": case_508a, "1163B2": case_1163b2, "1427B": case_1427b, "2075C": case_2075c,
    "2132B": case_2132b,
    "986B": case_986b, "1000B": case_1000b, "2196B": case_2196b,
    "1875D": case_1875d, "1985H1": case_1985h1, "2193D": case_2193d,
    "803A": case_803a, "2184F": case_2184f,
    "20B": case_20b, "492B": case_492b,
    "2131C": case_2131c, "2193E": case_2193e, "2209E": case_2209e,
    "2200G": case_2200g,
    "313B": case_313b, "1749C": case_1749c,
    "2140B": case_2140b,
    "363B": case_363b,
    "550C": case_550c,
    "584A": case_584a,
    "1352A": case_1352a,
    "1366D": case_1366d,
    "20C": case_20c,
    "1729C": case_1729c,
    "1833B": case_1833b,
    "1843D": case_1843d,
    "2171D": case_2171d,
    "2171E": case_2171e,
    "1868A": case_1868a,
    "2196A": case_2196a,
    "2218A": case_2218a,
    "2218B": case_2218b,
    "2218E": case_2218e,
    "2218C": case_2218c,
    "2218D": case_2218d,
    "2227B": case_2227b,
    "2227A": case_2227a,
    "2227C": case_2227c,
}


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = {(item["book"], item["id"]): item for item in catalog["problems"]}
    for problem, builder in BUILDERS.items():
        cases, seen = [], set()
        attempt = 0
        while len(cases) < 21:
            attempt += 1
            if attempt > 10_000:
                raise RuntimeError(f"{problem}: unable to generate 21 distinct inputs")
            payload, output = builder(random.Random(10_000_019 * attempt + sum(map(ord, problem))))
            if payload in seen:
                continue
            seen.add(payload)
            seed = len(cases)
            directory = MIRROR / "tests" / "codeforces" / f"{problem}_made" / "data"
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{seed}.in").write_text(payload, encoding="utf-8")
            (directory / f"{seed}.out").write_text(output, encoding="utf-8")
            cases.append({"input": str((directory / f"{seed}.in").relative_to(MIRROR)),
                          "output": str((directory / f"{seed}.out").relative_to(MIRROR))})
        row = rows[("codeforces", problem)]
        row.update({"tests": True, "test_count": len(cases), "test_cases": cases,
                    "data_status": "generated_tests", "sample_count": row.get("sample_count", 0)})
        if problem in {"20B", "492B"}:
            row["comparison"] = "float_tokens"
        if problem == "2140B":
            row["special_checker"] = "concat_divisible"
        if problem == "550C":
            row["special_checker"] = "divisible_by_8_subsequence"
        if problem == "584A":
            row["special_checker"] = "n_digit_divisible"
        if problem == "1352A":
            row["special_checker"] = "round_number_decomposition"
        if problem == "1366D":
            row["special_checker"] = "coprime_divisor_pairs"
        if problem == "20C":
            row["special_checker"] = "shortest_path"
        if problem == "1729C":
            row["special_checker"] = "tile_jump_path"
        if problem == "1833B":
            row["special_checker"] = "weather_permutation"
        if problem == "2171E":
            row["special_checker"] = "good_permutation"
        if problem == "1868A":
            row["special_checker"] = "matrix_beauty"
        if problem == "2218C":
            row["special_checker"] = "max_median_blocks"
        if problem == "2218D":
            row["special_checker"] = "distinct_adjacent_gcd"
        if problem == "2227C":
            row["special_checker"] = "min_divisible_by_six_subarrays"
        if problem == "2218A":
            row["special_checker"] = "maximize_min"
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(BUILDERS)} problems x 21 cases")


if __name__ == "__main__":
    main()
