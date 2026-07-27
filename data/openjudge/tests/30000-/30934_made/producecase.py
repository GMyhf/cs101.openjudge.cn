import random
REFERENCE='# External reference: /practice/30934/statistics/\n# Accepted submission: 52760566\n# Source: http://cs101.openjudge.cn/practice/solution/52760566/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    it = iter(input_data)\n    T = int(next(it))\n    results = []\n    \n    for _ in range(T):\n        N = int(next(it))\n        # 使用数组存储每个节点的左右孩子，索引从 1 到 N\n        left_child = [0] * (N + 1)\n        right_child = [0] * (N + 1)\n        \n        for i in range(1, N + 1):\n            l = int(next(it))\n            r = int(next(it))\n            left_child[i] = l\n            right_child[i] = r\n            \n        # 定义递归检查镜像的函数\n        def is_mirror(n1, n2):\n            # 两个节点都为空，说明这部分是对称的\n            if n1 == -1 and n2 == -1:\n                return True\n            # 只有一个为空，不对称\n            if n1 == -1 or n2 == -1:\n                return False\n            # 都不为空，继续递归检查：\n            # n1的左孩子 对应 n2的右孩子\n            # n1的右孩子 对应 n2的左孩子\n            return (is_mirror(left_child[n1], right_child[n2]) and \n                    is_mirror(right_child[n1], left_child[n2]))\n        \n        # 如果只有根节点，天然对称；否则比较根的左右孩子\n        if N == 1:\n            results.append("YES")\n        else:\n            if is_mirror(left_child[1], right_child[1]):\n                results.append("YES")\n            else:\n                results.append("NO")\n                \n    print("\\n".join(results))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='2\n7\n2 3\n4 5\n6 7\n-1 -1\n-1 -1\n-1 -1\n-1 -1\n4\n2 3\n-1 4\n-1 -1\n-1 -1\n'
GENERATOR_NAME='g30934'
CPP=False
def g30934(r):
    t=r.randint(1,4); rows=[str(t)]
    for _ in range(t):
        n=r.randint(1,20); rows.append(str(n));
        for i in range(1,n+1): rows.append(f"{2*i if 2*i<=n else -1} {2*i+1 if 2*i+1<=n else -1}")
    return "\n".join(rows)+"\n"

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
