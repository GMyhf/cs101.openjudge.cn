import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'def build_preorder(inorder, postorder):\n    if not inorder or not postorder:\n        return []\n\n    root = postorder[-1]  # 后序遍历的最后一个节点是根节点\n    root_index = inorder.index(root)  # 在中序遍历中找到根节点\n\n    # 递归构造左子树和右子树的前序遍历\n    left_preorder = build_preorder(inorder[:root_index], postorder[:root_index])\n    right_preorder = build_preorder(inorder[root_index + 1:], postorder[root_index:-1])\n\n    return [root] + left_preorder + right_preorder \n\n\ninorder = list(map(int, input().split())) \npostorder = list(map(int, input().split()))  \npreorder = build_preorder(inorder, postorder)\nprint(*preorder)'
SAMPLE = '9 5 32 67\n9 32 67 5\n'
GENERATOR_NAME = 'g5414'
def g5414(r):
    z=r.sample(range(65535),r.randint(2,10))
    def walk(a):
        if not a: return [],[],[]
        l,i,_=walk(a[1::2]); rr,p,_=walk(a[2::2])
        return l+[a[0]]+rr,i+p+[a[0]],[a[0]]+i+p
    i,p,_=walk(z)
    return " ".join(map(str,i))+"\n"+" ".join(map(str,p))+"\n"

def valid(text):
    """题面：两行，第一行中根序列、第二行后根序列，空格分隔；结点用互不相同的整数标识，范围 0～65535；
    「暂不必考虑不合理的输入」即两序列必须对应同一棵二叉树。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    rows = [line.split(" ") for line in lines[:2]]
    if not all(x.isdigit() and int(x) <= 65535 for row in rows for x in row):
        return False
    ino, post = [list(map(int, row)) for row in rows]
    if not ino or sorted(ino) != sorted(post) or len(set(ino)) != len(ino):
        return False
    where = {v: i for i, v in enumerate(ino)}
    stack = [(0, len(ino), 0, len(post))]
    while stack:  # 迭代地核对 (中根区间, 后根区间) 能否切成根 + 左右子树
        a, b, c, d = stack.pop()
        if a == b:
            continue
        k = where[post[d - 1]]
        if not a <= k < b:
            return False
        left = k - a
        stack.append((a, k, c, c + left)); stack.append((k + 1, b, c + left, d - 1))
    return True


def tree_case(r, n, shape):
    """按形状造一棵 n 结点的树，返回 (中根, 后根) 文本。shape: left/right/zigzag/random/bst。"""
    labels = r.sample(range(65536), n)
    if shape != "random":
        labels[0], labels[-1] = 0, 65535
        r.shuffle(labels)
    left = [-1] * n; right = [-1] * n
    for i in range(1, n):
        if shape == "left": left[i - 1] = i
        elif shape == "right": right[i - 1] = i
        elif shape == "zigzag":
            (left if i % 2 else right)[i - 1] = i
        else:  # 随机挂到某个空孩子位
            while True:
                p = r.randrange(i)
                side = left if r.random() < .5 else right
                if side[p] == -1:
                    side[p] = i; break
    ino, post = [], []
    stack = [(0, False)]
    while stack:
        u, done = stack.pop()
        if done: post.append(labels[u]); continue
        stack.append((u, True))
        if right[u] != -1: stack.append((right[u], False))
        if left[u] != -1: stack.append((left[u], False))
    def inorder():
        out, st, u = [], [], 0
        while st or u != -1:
            while u != -1: st.append(u); u = left[u]
            u = st.pop(); out.append(labels[u]); u = right[u]
        return out
    ino = inorder()
    return " ".join(map(str, ino)) + "\n" + " ".join(map(str, post)) + "\n"


def extra_cases():
    r = random.Random(541400)
    specs = [(1, "left"), (2, "left"), (2, "right"), (3, "zigzag"), (500, "left"), (500, "right"),
             (500, "zigzag"), (300, "random"), (1000, "random"), (2000, "random"), (3000, "random"),
             (3000, "random"), (64, "random"), (20, "left")]
    return [tree_case(r, n, shape) for n, shape in specs]


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复组"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
