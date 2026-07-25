import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def mininumRefill(plants, capacityA, capacityB):\n    l, r = 0, len(plants) - 1\n    Alice, Bob = capacityA, capacityB\n    ans = 0\n    while l <= r:\n        if l == r:\n            if Alice >= plants[l] or Bob >= plants[r]:\n                break\n\n            Alice = capacityA\n            ans += 1\n            if Alice >= plants[l]:\n                break\n            ans -= 1\n\n            Bob = capacityB\n            ans += 1\n            if Bob >= plants[r]:\n                break\n\n        if Alice < plants[l]:\n            Alice = capacityA\n            ans += 1\n\n        if Bob < plants[r]:\n            Bob = capacityB\n            ans += 1\n\n        if Alice >= plants[l]:\n            Alice -= plants[l]\n            l += 1\n        if Bob >= plants[r]:\n            Bob -= plants[r]\n            r -= 1\n\n    return ans\n\nn, AliceRaw, BobRaw = map(int, input().split())\n*plants, = map(int, input().split())\nprint(mininumRefill(plants, AliceRaw, BobRaw))\n'
SAMPLE_IN = '4 3 4\n2 2 3 3\n'
def generate_case(r):
    n = r.randint(1, 20); plants = [r.randint(1, 30) for _ in range(n)]
    a = max(plants) + r.randint(0, 15); b = max(plants) + r.randint(0, 15)
    assert a > max(plants) - 1 and b > max(plants) - 1
    return f"{n} {a} {b}\n" + " ".join(map(str, plants)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27301 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
