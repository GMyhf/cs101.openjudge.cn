import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import heapq\nfrom collections import defaultdict\n\nout = defaultdict(int)\npigs_heap = []\npigs_stack = []\n\nwhile True:\n    try:\n        s = input()\n    except EOFError:\n        break\n\n    if s == "pop":\n        if pigs_stack:\n            out[pigs_stack.pop()] += 1\n    elif s == "min":\n        if pigs_stack:\n            while True:\n                x = heapq.heappop(pigs_heap)\n                if not out[x]:\n                    heapq.heappush(pigs_heap, x)\n                    print(x)\n                    break\n                out[x] -= 1\n    else:\n        y = int(s.split()[1])\n        pigs_stack.append(y)\n        heapq.heappush(pigs_heap, y)\n'
SAMPLE_IN = 'pop\nmin\npush 5\npush 2\npush 3\nmin\npush 4\nmin\n'
SAMPLE_OUT = '2\n2\n'
def generate_case(r):
    lines = []; size = 0
    for _ in range(r.randint(10, 50)):
        if not size or r.random() < .6: lines.append(f"push {r.randint(0, 20000)}"); size += 1
        elif r.random() < .5: lines.append("min")
        else: lines.append("pop"); size -= 1
    return "\n".join(lines) + "\n"

assert SAMPLE_IN == 'pop\nmin\npush 5\npush 2\npush 3\nmin\npush 4\nmin\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22067 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
