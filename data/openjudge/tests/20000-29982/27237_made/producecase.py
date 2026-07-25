import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n#import heapq\n\ndef bfs(s, e):\n    q = deque()\n    q.append((0, s, ''))\n    vis = set()\n    vis.add(s)\n    # q = []\n    #heapq.heappush(q, (0, s, ''))\n\n    while q:\n        step, pos, path = q.popleft()\n        #step, pos, path = heapq.heappop(q)\n        if pos == e:\n            return step, path\n\n        if pos * 3 not in vis:\n            q.append((step+1, pos*3, path+'H'))\n            vis.add(pos*3)\n            #heapq.heappush(q, (step+1, pos*3, path+'H'))\n        if int(pos // 2) not in vis:\n            vis.add(int(pos//2))\n            q.append((step+1, int(pos//2), path+'O'))\n            #heapq.heappush(q, (step+1, int(pos//2), path+'O'))\n\nwhile True:\n    n, m = map(int, input().split())\n    if n == 0 and m == 0:\n        break\n    step, path = bfs(n, m)\n    print(step)\n    print(path)\n"
SAMPLE_IN = '1 6\n0 0\n'
def generate_case(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        start = r.randint(1, 3); pos = start; path = []
        for _ in range(r.randint(2, 5)):
            if pos <= 1 or r.random() < .55:
                path.append("H"); pos *= 3
            else:
                path.append("O"); pos //= 2
        end = pos; path = "".join(path)
        if end == start:
            path = "H"; end = start * 3
        assert 1 <= start <= 1000 and 1 <= end <= 1000 and 1 <= len(path) <= 25
        cases.append((start, end))
    return "\n".join(f"{a} {b}" for a, b in cases) + "\n0 0\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27237 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
