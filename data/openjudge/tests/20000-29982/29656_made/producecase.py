import random
REFERENCE='# External reference: /practice/29656/statistics/\n# Accepted submission: 52686108\n# Source: http://cs101.openjudge.cn/practice/solution/52686108/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\nleft = [0] * (n + 1)\nright = [0] * (n + 1)\nparent = [0] * (n + 1)\n\nfor i in range(1, n + 1):\n    l, r = map(int, input().split())\n    left[i] = l\n    right[i] = r\n    if l:\n        parent[l] = i\n    if r:\n        parent[r] = i\n\n# 后序遍历计算 left_len 和 right_len（一直向左/右的节点数，包括自身）\nleft_len = [1] * (n + 1)\nright_len = [1] * (n + 1)\nstack = [(1, 0)]  # (node, state) 0=未处理子节点, 1=子节点已处理\norder = []\nwhile stack:\n    u, state = stack.pop()\n    if state == 0:\n        stack.append((u, 1))\n        if right[u]:\n            stack.append((right[u], 0))\n        if left[u]:\n            stack.append((left[u], 0))\n    else:\n        order.append(u)\n\nfor u in order:\n    if left[u]:\n        left_len[u] = 1 + left_len[left[u]]\n    if right[u]:\n        right_len[u] = 1 + right_len[right[u]]\n\n# 计算 up_len（向上直线可达节点数，包括自身）\nup_len = [1] * (n + 1)  # 根节点 up_len[1]=1\nfor v in range(2, n + 1):\n    p = parent[v]\n    # 判断是否与父节点的方向一致，且父节点也满足相同方向（或父节点为根）\n    if (left[p] == v and (p == 1 or (parent[p] and left[parent[p]] == p))) or \\\n       (right[p] == v and (p == 1 or (parent[p] and right[parent[p]] == p))):\n        up_len[v] = up_len[p] + 1\n    else:\n        up_len[v] = 2   # 只能到自身和父节点\n\nbest_cnt = -1\nbest_node = -1\nfor v in range(1, n + 1):\n    cnt = left_len[v] + right_len[v] + up_len[v] - 2   # 减去重复的自身（被加了3次，应只算1次）\n    if cnt > best_cnt or (cnt == best_cnt and v < best_node):\n        best_cnt = cnt\n        best_node = v\n\nprint(best_node, best_cnt)'
SAMPLE='10\n2 3\n4 5\n0 0\n0 0\n6 7\n8 9\n0 0\n10 0\n0 0\n0 0\n'
GENERATOR_NAME='g29656'
def g29656(r):
    n = r.randint(1, 100); left = [0] * (n + 1); right = [0] * (n + 1)
    free = [1]
    for node in range(2, n + 1):
        while True:
            parent = r.choice(free)
            side = r.choice((0, 1))
            if side == 0 and not left[parent]: left[parent] = node; break
            if side == 1 and not right[parent]: right[parent] = node; break
        free.append(node)
        if left[parent] and right[parent]: free.remove(parent)
    return f"{n}\n" + "\n".join(f"{left[i]} {right[i]}" for i in range(1, n + 1)) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
