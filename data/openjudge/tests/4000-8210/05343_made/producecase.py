import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '8\nD8 A6 C3 B8 C5 A1 B5 D3\n'
SAMPLE_OUT = 'Queue1:A1\nQueue2:\nQueue3:C3 D3\nQueue4:\nQueue5:C5 B5\nQueue6:A6\nQueue7:\nQueue8:D8 B8\nQueue9:\nQueueA:A1 A6\nQueueB:B5 B8\nQueueC:C3 C5\nQueueD:D3 D8\nA1 A6 B5 B8 C3 C5 D3 D8\n'
CASES = ['8\nD8 A6 C3 B8 C5 A1 B5 D3\n', '11\nA4 D5 B8 C3 B1 C4 B4 D8 D3 D1 C2\n', '13\nD5 A3 A4 D9 A6 C8 B9 B7 C3 C4 A8 B3 C5\n', '22\nB2 B1 D3 D1 B3 A6 C8 D5 A9 D9 A5 A1 D2 C7 B8 B7 B6 D8 A3 C3 C6 B5\n', '20\nA3 C9 D8 A7 B3 B7 C6 D1 B9 A1 B1 A4 B4 D4 B2 A5 A2 A6 D3 B8\n', '19\nB8 A5 B7 A4 D8 C3 B5 C1 D6 A9 A3 B6 D4 A2 B4 C4 D2 C5 C6\n', '18\nC3 B8 B9 C2 D4 C4 D3 C5 A5 A4 B6 C9 A2 D6 A7 A3 D2 D1\n', '28\nC4 C2 C7 B6 A6 B4 A3 A1 D1 B9 A9 D9 C1 B7 D8 C9 A4 B5 D7 A7 D2 C6 A8 B3 A5 B2 A2 B1\n', '22\nC7 C2 C1 B4 A7 B1 A8 B6 C3 B2 D9 C6 B8 B9 C5 A6 D5 D7 A9 D1 D8 B7\n', '28\nC9 A1 A6 A2 D8 C6 C8 B1 B2 A5 B6 A8 B5 C5 B9 C1 D7 D6 A4 B8 C4 D2 D4 C2 B7 B3 A3 D5\n', '23\nD6 D5 C3 D1 B8 B7 C8 C7 D3 A7 C6 A4 B5 C4 B4 B1 D7 C9 B9 D2 A8 A2 B2\n', '24\nB7 A6 A4 D2 C8 B3 B9 A3 D4 C9 C7 C3 C4 D7 D3 A2 D1 D9 A8 A9 B2 B1 D6 A7\n', '18\nC3 C6 D7 A3 A9 A5 D9 B2 A6 C9 D1 C8 C4 D5 C7 B4 D3 B8\n', '28\nB1 A9 D9 B2 A6 D5 D4 D2 B4 A4 C3 B9 C1 D8 A7 D1 B8 C4 D6 A2 B3 C6 B7 C9 A1 B6 C7 A8\n', '30\nA5 C2 B8 B4 D4 C7 C3 C9 C4 A9 A7 D3 C6 D8 B6 B2 D9 D2 A8 A3 B5 B7 C8 A1 A4 B9 C5 B3 A6 A2\n', '10\nB2 C1 A8 B4 A2 A7 C4 B8 B9 C5\n', '14\nC4 A5 C7 C8 D1 A7 C5 B6 D9 A6 B8 A2 B4 C2\n', '5\nB7 C1 D2 B2 C6\n', '12\nA9 D1 C4 A4 D6 D3 B9 C1 C3 A8 C2 C7\n', '6\nD8 D5 D2 B8 A7 D9\n']
REFERENCE_SOURCE = "from collections import deque\n\n\nn = int(input())\nqueues = [deque() for _ in range(9)]\ncards = deque(list(input().split()))\n\nwhile cards:\n    card = cards.popleft()\n    queues[int(card[1])-1].append(card)\n\nqs = {'A': deque(), 'B': deque(), 'C': deque(), 'D': deque()}\nfor i in range(9):\n    tmp = []\n    while queues[i]:\n        card = queues[i].popleft()\n        qs[card[0]].append(card)\n        tmp.append(card)\n    print(f'Queue{i+1}:'+' '.join(tmp))\n\nresult = []\nfor char in qs.keys():\n    tmp = []\n    while qs[char]:\n        card = qs[char].popleft()\n        result.append(card)\n        tmp.append(card)\n    print(f'Queue{char}:' + ' '.join(tmp))\nprint(*result)\n"
assert CASES[0] == SAMPLE_IN
random.seed(5343)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
