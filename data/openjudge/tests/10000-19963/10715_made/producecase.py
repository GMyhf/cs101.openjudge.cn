import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="from itertools import permutations\n\n\ndef dfs(nums):\n    if len(nums) == 1:\n        return nums[0] == 42\n\n    for i in range(len(nums) - 1):\n        left = nums[i]\n        right = nums[i + 1]\n        results = [left + right, left - right, left * right]\n\n        if right != 0 and left % right == 0:  # 确保除法结果是整数\n            results.append(left // right)\n\n        # 对每种运算结果进行递归\n        for result in results:\n            if dfs(nums[:i] + [result] + nums[i + 2:]):\n                return True\n\n    return False\nn = int(input())\nif n == 1:\n    print('NO')\n    exit()\nt = list(map(int, input().split()))\np = list(map(list, permutations(t)))\nvis = {''}\nfor a in p:\n    if ''.join(str(i) for i in a) in vis:\n        continue\n    if dfs(a):\n        print('YES')\n        exit()\n    vis.add(''.join(str(i) for i in a))\nprint('NO')"
SAMPLE='6\n1 5 2 6 4 7\n'
GENERATOR_NAME='g10715'
def g10715(r):
    n=r.randint(2,6); return f"{n}\n"+" ".join(str(r.randint(1,13)) for _ in range(n))+"\n"

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
