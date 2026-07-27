import random
REFERENCE='# External reference: /practice/30935/statistics/\n# Accepted submission: 52760559\n# Source: http://cs101.openjudge.cn/practice/solution/52760559/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    orders = []\n    index = 1\n    for i in range(n):\n        d = int(input_data[index])\n        p = int(input_data[index + 1])\n        index += 2\n        orders.append((d, p))\n    \n    # 1. 按照收益 P 从大到小排序\n    orders.sort(key=lambda x: x[1], reverse=True)\n    \n    # 找到最大的截止时间，作为时间槽的上限\n    max_deadline = max(d for d, p in orders)\n    \n    # 2. 初始化时间槽，False 表示该分钟空闲\n    # 索引从 1 开始，所以大小为 max_deadline + 1\n    time_slots = [False] * (max_deadline + 1)\n    \n    total_profit = 0\n    \n    # 3. 遍历每个订单，尝试安排\n    for deadline, profit in orders:\n        # 从截止时间往前找，寻找第一个空闲的分钟\n        # 注意：最晚只能安排到第 1 分钟\n        start_time = min(deadline, max_deadline)\n        for t in range(start_time, 0, -1):\n            if not time_slots[t]:\n                time_slots[t] = True\n                total_profit += profit\n                break  # 安排成功，跳出循环处理下一个订单\n                \n    print(total_profit)\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='4\n4 20\n1 10\n1 40\n1 30\n'
GENERATOR_NAME='g30935'
CPP=False
def g30935(r):
    n=r.randint(1,50); return f"{n}\n"+"\n".join(f"{r.randint(1,50)} {r.randint(1,1000)}" for _ in range(n))+"\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
