import random
REFERENCE="# External reference: /practice/30062/statistics/\n# Accepted submission: 52831617\n# Source: http://cs101.openjudge.cn/practice/solution/52831617/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 从标准输入读取所有数据并解析为整数\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    nums = []\n    for token in input_data:\n        try:\n            nums.append(int(token))\n        except ValueError:\n            pass\n            \n    count = 0\n    n = len(nums)\n    \n    def backtrack(start, path):\n        nonlocal count\n        # 如果当前子序列长度大于等于 2，计数加 1\n        if len(path) >= 2:\n            count += 1\n            \n        # 使用集合对当前层级的选择进行去重\n        used = set()\n        for i in range(start, n):\n            # 如果当前元素已经在这一层被使用过，则跳过\n            if nums[i] in used:\n                continue\n            \n            # 判断是否满足非递减条件\n            if not path or nums[i] >= path[-1]:\n                used.add(nums[i])\n                backtrack(i + 1, path + [nums[i]])\n                \n    backtrack(0, [])\n    print(count)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='4 6 7 7\n'
GENERATOR_NAME='g30062'
CPP=False
def g30062(r): return " ".join(str(r.randint(-20, 20)) for _ in range(r.randint(2, 12))) + "\n"

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
