import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def main():\n    # Read the input\n    n, w = map(int, input().split())\n    P, Q = map(int, input().split())\n    # The amplified skill damage\n    damage = P + Q\n\n    monsters = []\n    for i in range(n):\n        x, y = map(int, input().split())\n        if damage >= x:\n            monsters.append(y)\n\n    # Sort monsters by the magic cost (y) in ascending order\n    monsters.sort()\n\n    # Count how many monsters we can defeat\n    count = 0\n    for cost in monsters:\n        if w >= cost:\n            w -= cost\n            count += 1\n        else:\n            break\n\n    print(count)\n\n\nif __name__ == '__main__':\n    main()\n\n"
SAMPLE_IN = '10 13\n108 76\n33 6\n36 18\n102 19\n98 5\n114 11\n0 5\n39 12\n108 6\n99 0\n34 4\n'
SAMPLE_OUT = '3\n'
def generate_case(r):
    n = r.randint(2, 30); w = r.randint(0, 100); p, q = r.randint(0, 200), r.randint(0, 200)
    return f"{n} {w}\n{p} {q}\n" + "\n".join(f"{r.randint(0, 1000)} {r.randint(0, 70)}" for _ in range(n)) + "\n"

assert SAMPLE_IN == '10 13\n108 76\n33 6\n36 18\n102 19\n98 5\n114 11\n0 5\n39 12\n108 6\n99 0\n34 4\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(21535 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
