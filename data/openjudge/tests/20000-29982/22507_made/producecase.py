import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/22507/\n# Accepted submission: 52740160\n# Source: http://cs101.openjudge.cn/practice/solution/52740160/\n# License: not declared on the submission page; no license is inferred.\n\ndef check_unique(s):\n    # 检查是否有重复字符\n    return len(set(s)) == len(s)\n\ndef count_ways(pre, post):\n    # 基本不合法情况\n    if len(pre) != len(post):\n        return 0\n    if not check_unique(pre) or not check_unique(post):\n        return 0\n    \n    n = len(pre)\n    res = 1\n    \n    # 递归函数：返回子树是否合法，同时统计单孩子节点数\n    def dfs(pl, pr, pol, por):\n        nonlocal res\n        if pl > pr:\n            return True\n        # 前序第一个 = 后序最后一个 = 根\n        if pre[pl] != post[por]:\n            return False\n        # 只有一个节点\n        if pl == pr:\n            return True\n        \n        # 左子树根：pre[pl+1]\n        left_root = pre[pl+1]\n        # 在后序中找到左子树根位置\n        if left_root not in post[pol:por+1]:\n            return False\n        pos = post[pol:por].index(left_root) + pol\n        left_size = pos - pol + 1\n        \n        # 递归左右\n        ok1 = dfs(pl+1, pl+left_size, pol, pos)\n        ok2 = dfs(pl+left_size+1, pr, pos+1, por-1)\n        if not ok1 or not ok2:\n            return False\n        \n        # 只有一个孩子 → 2种形态\n        if (pl+left_size+1 > pr) or (pl+1 > pl+left_size):\n            res *= 2\n        return True\n    \n    valid = dfs(0, n-1, 0, n-1)\n    return res if valid else 0\n\n# 多组输入\nimport sys\nfor line in sys.stdin:\n    line = line.strip()\n    if not line:\n        continue\n    pre, post = line.split()\n    print(count_ways(pre, post))'
SAMPLE='ABCDE CDBEA\nBCD DCB\nAB C\nAA AA\n'
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAXL = 20


def valid(text):
    """题面：多组数据，每组一行：前序序列与后序序列（大写字母，长度均不超过 20），空格分开。
    不保证存在对应的树，也不保证字母互异（重复则答案为 0）。"""
    if not text.endswith("\n") or text == "\n":
        return False
    for line in text[:-1].split("\n"):
        parts = line.split(" ")
        if len(parts) != 2:
            return False
        for t in parts:
            if not 1 <= len(t) <= MAXL or any(ch not in UPPER for ch in t):
                return False
    return True


def rand_shape(r, n, mode):
    """返回 n 个节点的二叉树形状（嵌套 (left, right)，None 表示空）。"""
    if n == 0:
        return None
    if mode == "chain":
        sub = rand_shape(r, n - 1, mode)
        return (sub, None) if r.random() < .5 else (None, sub)
    if mode == "full":                 # 尽量每个内部节点都有两个孩子
        if n == 1:
            return (None, None)
        if n == 2:
            return (rand_shape(r, 1, mode), None) if r.random() < .5 else (None, rand_shape(r, 1, mode))
        k = r.randrange(1, n - 1, 2) if (n - 1) % 2 == 0 else r.randint(1, n - 2)
        return (rand_shape(r, k, mode), rand_shape(r, n - 1 - k, mode))
    k = r.randint(0, n - 1)
    return (rand_shape(r, k, mode), rand_shape(r, n - 1 - k, mode))


def orders(shape, letters):
    it = iter(letters)
    pre, post = [], []
    def go(s):
        if s is None:
            return
        c = next(it); pre.append(c)
        go(s[0]); go(s[1]); post.append(c)
    go(shape)
    return "".join(pre), "".join(post)


def good_line(r, n=None, mode=None):
    n = n or r.randint(1, MAXL)
    mode = mode or r.choice(["rand", "rand", "chain", "full"])
    letters = r.sample(UPPER, n)
    return orders(rand_shape(r, n, mode), letters)


def bad_line(r):
    pre, post = good_line(r, r.randint(2, MAXL))
    kind = r.randrange(7)
    if kind == 0:                       # 长度不同
        post = post[:-1] if r.random() < .5 or len(post) >= MAXL else post + r.choice([c for c in UPPER if c not in post])
        post = post or "A"
    elif kind == 1:                     # 前序有重复字母
        i, j = r.sample(range(len(pre)), 2); pre = pre[:i] + pre[j] + pre[i + 1:]
    elif kind == 2:                     # 后序有重复字母
        i, j = r.sample(range(len(post)), 2); post = post[:i] + post[j] + post[i + 1:]
    elif kind == 3:                     # 字母集合不同
        others = [c for c in UPPER if c not in pre]
        i = r.randrange(len(post)); post = post[:i] + r.choice(others) + post[i + 1:]
    elif kind == 4:                     # 交换后序中两个字母：集合相同但结构多半矛盾
        i, j = r.sample(range(len(post)), 2); p = list(post); p[i], p[j] = p[j], p[i]; post = "".join(p)
    elif kind == 5:                     # 根不一致
        post = post[-1] + post[:-1]
    else:                               # 前序配上另一棵同字母集的树的后序（多数情况结构矛盾）
        letters = list(pre); r.shuffle(letters)
        post = orders(rand_shape(r, len(pre), "rand"), letters)[1]
    return pre, post


def count_oracle(pre, post):
    """独立做法：区间 DP 直接数所有前序/后序同时吻合的二叉树。"""
    if len(pre) != len(post) or len(set(pre)) != len(pre) or len(set(post)) != len(post):
        return 0
    from functools import lru_cache
    @lru_cache(None)
    def f(a, b, ln):
        if ln == 0:
            return 1
        if pre[a] != post[b + ln - 1]:
            return 0
        return sum(f(a + 1, b, k) * f(a + 1 + k, b + k, ln - 1 - k) for k in range(ln))
    return f(0, 0, len(pre))


def g22507(r, idx):
    lines = []
    if idx <= 3:                        # 小规模、含长度 1、2
        for _ in range(r.randint(8, 20)):
            n = r.randint(1, 4)
            lines.append(good_line(r, n) if r.random() < .6 else bad_line(r) if n > 1 else (r.choice(UPPER), r.choice(UPPER)))
    elif idx <= 6:                      # 满长 20 的单链：答案 2^19
        for _ in range(r.randint(3, 8)):
            lines.append(good_line(r, MAXL, "chain"))
        lines.append(good_line(r, r.randint(10, 19), "chain"))
    else:
        for _ in range(r.randint(5, 25)):
            x = r.random()
            if x < .55:
                lines.append(good_line(r, r.choice([r.randint(1, MAXL), MAXL])))
            else:
                lines.append(bad_line(r))
    return "".join(f"{a} {b}\n" for a, b in lines)


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]
    # 1：手工边界
    cases.append("A A\nA B\nAB BA\nAB AB\nABC CBA\nABC BCA\nABC ACB\nABCDEFGHIJKLMNOPQRST TSRQPONMLKJIHGFEDCBA\n"
                 "ABCDEFGHIJKLMNOPQRST ABCDEFGHIJKLMNOPQRST\nZ ZZ\nAB A\nABA BAA\n")
    cases += [g22507(random.Random(22507 * 100 + s), s) for s in range(2, 40)]
    assert len(cases) == 40 and len(set(cases)) == 40
    for i,c in enumerate(cases):
        assert valid(c), i
        out = run(c)
        exp = [str(count_oracle(*line.split())) for line in c.split("\n") if line]
        assert out.split() == exp, i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(out)


if __name__=='__main__': main()
