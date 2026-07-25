import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import defaultdict, deque\n\ndef min_bonus(n, m, matches):\n    # 图结构：记录谁打败了谁（反向边）\n    graph = defaultdict(list)\n    indegree = [0] * n\n    \n    for a, b in matches:\n        graph[b].append(a)  # a > b，所以 b 是 a 的前驱\n        indegree[a] += 1\n\n    # 初始化奖金为 100\n    bonus = [100] * n\n\n    # 拓扑排序队列\n    queue = deque([i for i in range(n) if indegree[i] == 0])\n\n    while queue:\n        curr = queue.popleft()\n        for neighbor in graph[curr]:\n            # 如果邻居的奖金不大于当前的，就调整它\n            if bonus[neighbor] <= bonus[curr]:\n                bonus[neighbor] = bonus[curr] + 1\n            indegree[neighbor] -= 1\n            if indegree[neighbor] == 0:\n                queue.append(neighbor)\n\n    return sum(bonus)\n\n# 读取输入\nif __name__ == "__main__":\n    input = sys.stdin.read\n    data = input().split()\n    \n    n = int(data[0])\n    m = int(data[1])\n    \n    matches = []\n    idx = 2\n    for _ in range(m):\n        a = int(data[idx])\n        b = int(data[idx+1])\n        matches.append((a, b))\n        idx += 2\n\n    result = min_bonus(n, m, matches)\n    print(result)\n'
SAMPLE_IN = '5 6\n1 0\n2 0\n3 0\n4 1\n4 2\n4 3\n'
SAMPLE_OUT = '505\n'
def generate_case(r):
    n = r.randint(2, 20); edges = [(i, j) for i in range(n) for j in range(i) if r.random() < .18]
    assert len(edges) == len(set(edges)) and all(0 <= b < a < n for a, b in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + ("\n" if edges else "")

assert SAMPLE_IN == '5 6\n1 0\n2 0\n3 0\n4 1\n4 2\n4 3\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22508 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
