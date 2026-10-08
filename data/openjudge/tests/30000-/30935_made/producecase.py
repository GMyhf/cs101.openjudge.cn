import random
REFERENCE='# External reference: /practice/30935/statistics/\n# Accepted submission: 52760559\n# Source: http://cs101.openjudge.cn/practice/solution/52760559/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    orders = []\n    index = 1\n    for i in range(n):\n        d = int(input_data[index])\n        p = int(input_data[index + 1])\n        index += 2\n        orders.append((d, p))\n    \n    # 1. 按照收益 P 从大到小排序\n    orders.sort(key=lambda x: x[1], reverse=True)\n    \n    # 找到最大的截止时间，作为时间槽的上限\n    max_deadline = max(d for d, p in orders)\n    \n    # 2. 初始化时间槽，False 表示该分钟空闲\n    # 索引从 1 开始，所以大小为 max_deadline + 1\n    time_slots = [False] * (max_deadline + 1)\n    \n    total_profit = 0\n    \n    # 3. 遍历每个订单，尝试安排\n    for deadline, profit in orders:\n        # 从截止时间往前找，寻找第一个空闲的分钟\n        # 注意：最晚只能安排到第 1 分钟\n        start_time = min(deadline, max_deadline)\n        for t in range(start_time, 0, -1):\n            if not time_slots[t]:\n                time_slots[t] = True\n                total_profit += profit\n                break  # 安排成功，跳出循环处理下一个订单\n                \n    print(total_profit)\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='4\n4 20\n1 10\n1 40\n1 30\n'
GENERATOR_NAME='g30935'
CPP=False
import re
_INT = re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    """题面约束：第 1 行 N（1<=N<=1000）；接下来 N 行每行 Di Pi（1<=Di<=1000，1<=Pi<=10000）。"""
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if not lines or not _INT.match(lines[0].strip()):
        return False
    n = int(lines[0])
    if not (1 <= n <= 1000) or len(lines) != n + 1:
        return False
    for row in lines[1:]:
        tok = row.split()
        if len(tok) != 2 or not all(_INT.match(t) for t in tok):
            return False
        d, p = map(int, tok)
        if not (1 <= d <= 1000 and 1 <= p <= 10000):
            return False
    return True

def _fmt(rows):
    return f"{len(rows)}\n" + "\n".join(f"{d} {p}" for d, p in rows) + "\n"

def _rand(r, n, dmax, pmax, dmin=1, pmin=1):
    return [(r.randint(dmin, dmax), r.randint(pmin, pmax)) for _ in range(n)]

def build_cases():
    r = random.Random(30935)
    cases = [SAMPLE]
    cases.append(_fmt([(1, 10000)]))
    cases.append(_fmt([(1000, 1)]))
    cases.append(_fmt([(1, 5), (1, 5)]))
    cases.append(_fmt([(2, 10), (1, 9), (1, 8)]))        # 按截止时间贪心会丢掉 10 以外的最优
    cases.append(_fmt([(2, 50), (1, 40), (2, 30)]))      # 按收益放到“最早空位”会错：50 应放第 2 分钟
    cases.append(_fmt([(3, 1), (3, 1), (3, 1), (3, 1)]))
    # 小规模随机（可暴力枚举子集核对）
    for k in range(18):
        n = r.randint(2, 12)
        cases.append(_fmt(_rand(r, n, r.choice([2, 4, 8, 15]), r.choice([10, 100, 10000]))))
    # 中等规模
    cases.append(_fmt(_rand(r, 100, 30, 1000)))
    cases.append(_fmt(_rand(r, 300, 300, 10000)))
    # 大规模 N=1000
    cases.append(_fmt(_rand(r, 1000, 1, 10000)))               # 全部 D=1，只能选一个
    cases.append(_fmt(_rand(r, 1000, 1000, 10000, dmin=1000))) # 全部 D=1000，全选
    cases.append(_fmt([(1000, 10000)] * 1000))                 # 总收益取上限 10^7
    cases.append(_fmt(_rand(r, 1000, 1000, 10000)))
    cases.append(_fmt(_rand(r, 1000, 50, 10000)))              # 截止时间集中，激烈竞争
    cases.append(_fmt(_rand(r, 1000, 500, 10000)))
    cases.append(_fmt(_rand(r, 1000, 200, 3)))                 # 收益大量相同
    cases.append(_fmt([(i, 10000 - i) for i in range(1, 1001)]))
    cases.append(_fmt([(1 + (i % 10), r.randint(1, 10000)) for i in range(1000)]))
    cases.append(_fmt(_rand(r, 1000, 600, 10000, dmin=400)))  # D 都在 400~600，只能选 600 个
    rows = [(r.randint(1, 1000), 10000 if r.random() < 0.3 else r.randint(1, 100)) for _ in range(1000)]
    cases.append(_fmt(rows))
    # 截止时间远大于 N 的小 N
    cases.append(_fmt(_rand(r, 20, 1000, 10000, dmin=900)))
    cases.append(_fmt(sorted(_rand(r, 1000, 700, 10000), key=lambda x: -x[0])))
    return cases

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert cases[0]==SAMPLE
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
