import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/22507/\n# Accepted submission: 52740160\n# Source: http://cs101.openjudge.cn/practice/solution/52740160/\n# License: not declared on the submission page; no license is inferred.\n\ndef check_unique(s):\n    # 检查是否有重复字符\n    return len(set(s)) == len(s)\n\ndef count_ways(pre, post):\n    # 基本不合法情况\n    if len(pre) != len(post):\n        return 0\n    if not check_unique(pre) or not check_unique(post):\n        return 0\n    \n    n = len(pre)\n    res = 1\n    \n    # 递归函数：返回子树是否合法，同时统计单孩子节点数\n    def dfs(pl, pr, pol, por):\n        nonlocal res\n        if pl > pr:\n            return True\n        # 前序第一个 = 后序最后一个 = 根\n        if pre[pl] != post[por]:\n            return False\n        # 只有一个节点\n        if pl == pr:\n            return True\n        \n        # 左子树根：pre[pl+1]\n        left_root = pre[pl+1]\n        # 在后序中找到左子树根位置\n        if left_root not in post[pol:por+1]:\n            return False\n        pos = post[pol:por].index(left_root) + pol\n        left_size = pos - pol + 1\n        \n        # 递归左右\n        ok1 = dfs(pl+1, pl+left_size, pol, pos)\n        ok2 = dfs(pl+left_size+1, pr, pos+1, por-1)\n        if not ok1 or not ok2:\n            return False\n        \n        # 只有一个孩子 → 2种形态\n        if (pl+left_size+1 > pr) or (pl+1 > pl+left_size):\n            res *= 2\n        return True\n    \n    valid = dfs(0, n-1, 0, n-1)\n    return res if valid else 0\n\n# 多组输入\nimport sys\nfor line in sys.stdin:\n    line = line.strip()\n    if not line:\n        continue\n    pre, post = line.split()\n    print(count_ways(pre, post))'
SAMPLE='ABCDE CDBEA\nBCD DCB\nAB C\nAA AA\n'
GENERATOR_NAME='g22507'
def g22507(r):
    n = r.randint(2, 9); chars = list("ABCDEFGHIJKLMNO")[:n]
    if r.random() < .25: return "".join(chars) + " " + "".join(chars[1:] + chars[:1]) + "\n"
    def tree(items):
        if not items: return [], []
        if len(items) == 1: return items, items
        cut = r.randint(1, len(items)-1)
        a,b=tree(items[1:1+cut]),tree(items[1+cut:])
        return [items[0]]+a[0]+b[0], a[1]+b[1]+[items[0]]
    pre, post = tree(chars)
    return "".join(pre) + " " + "".join(post) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
