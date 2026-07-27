import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='import sys\n\n\ndef solve():\n    # 使用 sys.stdin.read 能够一次性读取所有输入，避免因多余空格或换行导致解析错误\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    n = int(input_data[0])\n    m = int(input_data[1])\n\n    edges = []\n    idx = 2\n    for _ in range(m):\n        u = int(input_data[idx])\n        v = int(input_data[idx + 1])\n        w = float(input_data[idx + 2])\n        idx += 3\n        # 保证编号小的在前面，方便后续输出\n        if u > v:\n            u, v = v, u\n        edges.append((w, u, v))\n\n    # 按花费从小到大排序\n    edges.sort(key=lambda x: x[0])\n\n    # 并查集初始化\n    parent = list(range(n))\n\n    def find(i):\n        if parent[i] == i:\n            return i\n        parent[i] = find(parent[i])  # 路径压缩\n        return parent[i]\n\n    def union(i, j):\n        root_i = find(i)\n        root_j = find(j)\n        if root_i != root_j:\n            parent[root_i] = root_j\n            return True\n        return False\n\n    mst_edges = []\n    total_cost = 0.0\n    edges_count = 0\n\n    # Kruskal 算法核心\n    for w, u, v in edges:\n        if union(u, v):\n            total_cost += w\n            mst_edges.append((u, v))\n            edges_count += 1\n            if edges_count == n - 1:\n                break\n\n    # 检查是否所有人都连通\n    # 找寻所有节点的根节点，如果唯一，说明全部连通\n    roots = set(find(i) for i in range(n))\n\n    if len(roots) == 1:\n        # 输出最小花销，保留两位小数\n        print(f"{total_cost:.2f}")\n        # 按照花费从小到大输出每一对人（因为 edges 已经按花费排过序，mst_edges 里的顺序自然也是从小到大）\n        for u, v in mst_edges:\n            print(f"{u} {v}")\n    else:\n        print("NOT CONNECTED")\n\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='5 9\n0 1 10.0\n0 3 7.0\n0 4 25.0\n1 2 8.0\n1 3 9.0\n1 4 35.0\n2 3 11.0\n2 4 50.0\n3 4 24.0\n'
GENERATOR_NAME='g26835'
def g26835(r):
    n = r.randint(2, 30); edges = []
    for i in range(1, n): edges.append((r.randrange(i), i, float(r.randint(1, 99999))))
    seen = {(min(a, b), max(a, b)) for a, b, _ in edges}
    target = min(4999, n * (n - 1) // 2)
    while len(edges) < target:
        a, b = r.sample(range(n), 2); key = (min(a, b), max(a, b))
        if key not in seen: seen.add(key); edges.append((a, b, r.uniform(0, 99999)))
    r.shuffle(edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w:.3f}" for a, b, w in edges) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
