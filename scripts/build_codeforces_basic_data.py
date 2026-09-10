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


BUILDERS = {
    "1A": case_1a, "25A": case_25a, "50A": case_50a, "58A": case_58a,
    "69A": case_69a, "71A": case_71a, "96A": case_96a, "112A": case_112a,
    "118A": case_118a, "122A": case_122a, "131A": case_131a,
    "151A": case_151a, "231A": case_231a, "236A": case_236a, "263A": case_263a,
    "266A": case_266a, "270A": case_270a, "281A": case_281a, "282A": case_282a,
    "339A": case_339a, "479A": case_479a, "996A": case_996a_fixed, "158A": case_158a,
    "160A": case_160a, "230A": case_230a,
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
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(BUILDERS)} problems x 21 cases")


if __name__ == "__main__":
    main()
