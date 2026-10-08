import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def mininumRefill(plants, capacityA, capacityB):\n    l, r = 0, len(plants) - 1\n    Alice, Bob = capacityA, capacityB\n    ans = 0\n    while l <= r:\n        if l == r:\n            if Alice >= plants[l] or Bob >= plants[r]:\n                break\n\n            Alice = capacityA\n            ans += 1\n            if Alice >= plants[l]:\n                break\n            ans -= 1\n\n            Bob = capacityB\n            ans += 1\n            if Bob >= plants[r]:\n                break\n\n        if Alice < plants[l]:\n            Alice = capacityA\n            ans += 1\n\n        if Bob < plants[r]:\n            Bob = capacityB\n            ans += 1\n\n        if Alice >= plants[l]:\n            Alice -= plants[l]\n            l += 1\n        if Bob >= plants[r]:\n            Bob -= plants[r]\n            r -= 1\n\n    return ans\n\nn, AliceRaw, BobRaw = map(int, input().split())\n*plants, = map(int, input().split())\nprint(mininumRefill(plants, AliceRaw, BobRaw))\n'
SAMPLE_IN = '4 3 4\n2 2 3 3\n'
def valid(text):
    """题面：第一行正整数 n a b（n<=100）；第二行 n 个正整数。
    题面写“a 和 b 均大于任意一株植物”，但样例 1（a=3、植物 3）是等于，原题 LeetCode 2105 为 <=，故按 a,b >= max 校验。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head, body = lines[0].split(" "), lines[1].split(" ")
    if len(head) != 3 or not all(re.fullmatch(r"[1-9][0-9]*", x) for x in head + body):
        return False
    n, a, b = map(int, head)
    if not (1 <= n <= 100) or len(body) != n:
        return False
    mx = max(map(int, body))
    return a >= mx and b >= mx


def _fmt(a, b, plants):
    return f"{len(plants)} {a} {b}\n" + " ".join(map(str, plants)) + "\n"


def generate_case(r, index):
    if index == 1:
        return "1 10 8\n5\n"
    if index <= 12:
        # 原有风格：小规模
        n = r.randint(1, 20); plants = [r.randint(1, 30) for _ in range(n)]
        a = max(plants) + r.randint(0, 15); b = max(plants) + r.randint(0, 15)
        return _fmt(a, b, plants)
    if index <= 20:
        # 奇数 n、对称：两人到中间时水量相同（平局给 Alice），且常常不够需重灌
        half = [r.randint(1, 10) for _ in range(r.randint(1, 49))]
        mid = r.randint(1, 10)
        plants = half + [mid] + half[::-1]
        cap = max(plants) + r.randint(0, 3)
        return _fmt(cap, cap, plants)
    if index <= 26:
        # 奇数 n、中间株很大：比较谁水多、谁都不够时重灌一次
        n = r.choice([3, 5, 7, 99, 51, 101 - 2])
        plants = [r.randint(1, 5) for _ in range(n)]
        plants[n // 2] = r.randint(5, 9)
        a, b = r.randint(9, 12), r.randint(9, 12)
        return _fmt(a, b, plants)
    if index <= 32:
        # 满规模 n=100（或 99）、容量紧
        n = r.choice([100, 99])
        plants = [r.randint(1, 1000) for _ in range(n)]
        a = max(plants) + r.choice([0, 1, r.randint(0, 500)])
        b = max(plants) + r.choice([0, 1, r.randint(0, 500)])
        return _fmt(a, b, plants)
    if index <= 36:
        # 大数值
        n = r.randint(90, 100)
        plants = [r.randint(1, 10**6) for _ in range(n)]
        a = r.randint(max(plants), 10**9); b = r.randint(max(plants), 10**9)
        if index == 36:
            a = b = max(plants)
        return _fmt(a, b, plants)
    if index == 37:
        return _fmt(1, 1, [1] * 100)
    if index == 38:
        return _fmt(2, 3, [2] * 99)
    return _fmt(5, 5, [1] * 100)


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(27301 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content)
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
