import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="import sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    w = int(input_data[1])\n    \n    items = []\n    for i in range(n):\n        items.append(int(input_data[2 + i]))\n        \n    # 核心剪枝 1：从大到小排序，优先放大的道具\n    items.sort(reverse=True)\n    \n    # ans 记录全局最优解，最坏情况下需要 n 个包（每个道具一个包）\n    ans = n\n    # bags 数组就是你要的“记录装了一半的包”的数据结构\n    bags = []\n\n    def dfs(idx):\n        nonlocal ans\n        \n        # 核心剪枝 2：如果当前用的包数已经大于等于已知的最优解，直接放弃这条搜索分支\n        if len(bags) >= ans:\n            return\n            \n        # 如果所有道具都放完了，更新最优解\n        if idx == n:\n            ans = min(ans, len(bags))\n            return\n            \n        current_item = items[idx]\n        \n        # 尝试 1：把当前道具放进已经开过的包里\n        for i in range(len(bags)):\n            if bags[i] + current_item <= w:\n                bags[i] += current_item  # 放进去\n                dfs(idx + 1)             # 继续放下一个道具\n                bags[i] -= current_item  # 回溯：拿出来，尝试下一种可能\n                \n        # 尝试 2：新开一个包来装当前道具\n        bags.append(current_item)\n        dfs(idx + 1)\n        bags.pop() # 回溯：把新开的包撤销\n\n    dfs(0)\n    print(ans)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE='5 1996\n1\n2\n1994\n12\n29\n'
GENERATOR_NAME='g15286'
def g15286(r):
    n=r.randint(3,10); w=r.randint(10,100); z=[r.randint(1,w) for _ in range(n)]
    return f"{n} {w}\n"+"\n".join(map(str,z))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
