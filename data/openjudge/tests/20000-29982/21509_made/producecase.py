import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import heapq\nimport sys\n\ndef main():\n    data = sys.stdin.read().split()\n    n = int(data[0])\n    A = list(map(int, data[1:1+n]))\n    \n    lo = []  # max-heap: store negative values\n    hi = []  # min-heap\n    \n    result = []\n    \n    for i, num in enumerate(A):\n        # Push to lo first\n        heapq.heappush(lo, -num)\n        \n        # Move the largest in lo to hi to maintain order\n        heapq.heappush(hi, -heapq.heappop(lo))\n        \n        # If hi has more elements, move smallest back to lo\n        if len(hi) > len(lo):\n            heapq.heappush(lo, -heapq.heappop(hi))\n        \n        # After processing odd number of elements (1st, 3rd, 5th, ...)\n        if i % 2 == 0:  # 0-indexed: i=0 -> 1 element, i=2 -> 3 elements, etc.\n            median = -lo[0]\n            result.append(str(median))\n    \n    print("\\n".join(result))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '7\n1 3 5 7 9 11 6\n'
SAMPLE_OUT = '1\n3\n5\n6\n'
def generate_case(r):
    n = r.choice([5, 7, 9, 11, 21, 51]); values = [r.randint(0, 1000) for _ in range(n)]
    assert n % 2 == 1 and all(0 <= x <= 10**9 for x in values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

assert SAMPLE_IN == '7\n1 3 5 7 9 11 6\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(21509 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
