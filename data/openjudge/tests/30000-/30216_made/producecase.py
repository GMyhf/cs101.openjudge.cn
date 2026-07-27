import random
REFERENCE="# External reference: /practice/30216/statistics/\n# Accepted submission: 52831634\n# Source: http://cs101.openjudge.cn/practice/solution/52831634/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    n = int(input_data[0])\n    size = 1 << n\n    \n    # 1 代表不被赦免，初始化整个矩阵\n    grid = [[1] * size for _ in range(size)]\n    \n    def pardon(x, y, L):\n        if L == 1:\n            return\n        \n        half = L // 2\n        # 将左上角的子矩阵全部设为 0 (赦免)\n        for r in range(x, x + half):\n            grid[r][y : y + half] = [0] * half\n            \n        # 递归处理剩下的 3 个子矩阵\n        pardon(x, y + half, half)          # 右上角\n        pardon(x + half, y, half)          # 左下角\n        pardon(x + half, y + half, half)    # 右下角\n        \n    # 从整个矩阵开始分治\n    pardon(0, 0, size)\n    \n    # 按要求输出矩阵\n    for row in grid:\n        print(*(row))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3\n'
GENERATOR_NAME='g30216'
CPP=False
def g30216(r): return f"{r.randint(1, 10)}\n"

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
