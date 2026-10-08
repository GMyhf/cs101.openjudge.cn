import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面契约：若干组「整数 + 至少一个空白 + S 表达式二叉树」，直到 EOF；
    整数与树之间为一个或多个空格；树 ::= () | (整数 树 树)，整数形如 -?\\d+，记号间可有任意空白（含换行）。至少一组。"""
    import re
    toks=[(m.group(),m.start()) for m in re.finditer(r'-?\d+|[()]|\S',text)]
    p=0
    def tree():
        nonlocal p
        if p>=len(toks) or toks[p][0]!='(':raise ValueError
        p+=1
        if p<len(toks) and toks[p][0]==')':p+=1;return
        if p>=len(toks) or not re.fullmatch(r'-?\d+',toks[p][0]):raise ValueError
        p+=1;tree();tree()
        if p>=len(toks) or toks[p][0]!=')':raise ValueError
        p+=1
    import sys
    old=sys.getrecursionlimit();sys.setrecursionlimit(max(old,100000))
    try:
        cnt=0
        while p<len(toks):
            t,pos=toks[p]
            if not re.fullmatch(r'-?\d+',t):return False
            end=pos+len(t);p+=1
            gap=text[end:toks[p][1]] if p<len(toks) else ''
            if not gap or set(gap)!={' '}:return False   # 题面：整数后跟一个或多个空格
            tree();cnt+=1
        return cnt>=1
    except (ValueError,RecursionError):
        return False
    finally:
        sys.setrecursionlimit(old)

def _rand_tree(r,nodes,maxdep,lo,hi):
    """随机二叉树：返回嵌套元组 (v,L,R) 或 None。"""
    import sys
    def build(n,d):
        if n==0:return None
        if d>=maxdep:n=1
        k=r.randint(0,n-1) if r.random()<.6 else (n-1 if r.random()<.5 else 0)
        return (r.randint(lo,hi),build(k,d+1),build(n-1-k,d+1))
    return build(nodes,1)

def _paths(t):
    if t is None:return []
    v,L,R=t
    if L is None and R is None:return [v]
    return [v+x for x in _paths(L)+_paths(R)]
def _internal_sums(t,acc=0):
    if t is None:return []
    v,L,R=t;s=acc+v
    if L is None and R is None:return []
    return [s]+_internal_sums(L,s)+_internal_sums(R,s)

def _fmt(r,t,style,ind=0):
    if t is None:return '()' if style!=1 else r.choice(['()','( )','(  )'])
    v,L,R=t
    if style==0:return f'({v}{_fmt(r,L,0)}{_fmt(r,R,0)})'
    if style==1:  # 随机空格
        sp=lambda:r.choice(['',' ','  '])
        return f'({sp()}{v}{r.choice([" ",""])}{sp()}{_fmt(r,L,1)}{sp()}{_fmt(r,R,1)}{sp()})'
    # style 2：多行缩进
    pad='\n'+' '*(ind+2)
    return f'({v}{pad}{_fmt(r,L,2,ind+2)}{pad}{_fmt(r,R,2,ind+2)} )'

def _case(r,t,want):
    ps=_paths(t)
    if want=='yes' and ps:I=r.choice(ps)
    elif want=='inner' and _internal_sums(t):
        I=r.choice(_internal_sums(t))
        if I in ps:I=r.randint(-10**6,10**6)
    else:
        I=r.choice([r.randint(-10**6,10**6),(r.choice(ps)+r.choice([-1,1])) if ps else 0])
    style=r.choice([0,0,1,2]) if len(str(t))<20000 else r.choice([0,1])
    sep=r.choice([' ',' ','   '])
    return f'{I}{sep}{_fmt(r,t,style)}\n'

def g1145(seed):
    r=random.Random(1145*1000+seed)
    out=[]
    if seed==1:
        out=['0 ()\n','0 (0 () ())\n','1 (1 () ())\n','-1 (-1 () ())\n','2 (1 (1 () ()) ())\n','1 (1 (1 () ()) ())\n','1 (1 () (2 () ()))\n',
             '3 (1 () (2 () ()))\n','-5 (-2 (-3 () ()) (4 () ()))\n','2 (-2 (-3 () ()) (4 () ()))\n','0 (5 (-5 () (3 () ())) ())\n',
             '-7 (\n-7\n(\n)\n(\n)\n)\n','7 ( 7 ( ) ( ) )\n','100 ()\n']
    elif seed>=34:   # 大树：节点数大、深度受限（多数解法递归）
        for _ in range(r.randint(2,4)):
            t=_rand_tree(r,r.randint(3000,6000),120,-1000,1000)
            out.append(_case(r,t,r.choice(['yes','no','inner'])))
    else:
        for _ in range(r.randint(3,40)):
            n=r.choice([0,1,2,r.randint(3,15),r.randint(15,200)])
            lo,hi=r.choice([(-30,30),(-1000,1000),(0,9),(-10**4,10**4)])
            t=_rand_tree(r,n,r.choice([8,20,60]),lo,hi)
            out.append(_case(r,t,r.choice(['yes','yes','no','inner'])))
    return ''.join(out)

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1145: Tree Summing\n# Fenced code block index: 3\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01145/\n# License: not declared in source collection; no license is inferred.\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef has_path_sum(root, target_sum):\n    if root is None:\n        return False\n\n    if root.left is None and root.right is None:  # The current node is a leaf node\n        return root.val == target_sum\n\n    left_exists = has_path_sum(root.left, target_sum - root.val)\n    right_exists = has_path_sum(root.right, target_sum - root.val)\n\n    return left_exists or right_exists\n\n\n# Parse the input string and build a binary tree\ndef parse_tree(s):\n    stack = []\n    i = 0\n\n    while i < len(s):\n        if s[i].isdigit() or s[i] == \'-\':\n            j = i\n            while j < len(s) and (s[j].isdigit() or s[j] == \'-\'):\n                j += 1\n            num = int(s[i:j])\n            node = TreeNode(num)\n            if stack:\n                parent = stack[-1]\n                if parent.left is None:\n                    parent.left = node\n                else:\n                    parent.right = node\n            stack.append(node)\n            i = j\n        elif s[i] == \'[\':\n            i += 1\n        elif s[i] == \']\' and s[i - 1] != \'[\' and len(stack) > 1:\n            stack.pop()\n            i += 1\n        else:\n            i += 1\n\n    return stack[0] if len(stack) > 0 else None\n\n\nwhile True:\n    try:\n        s = input()\n    except:\n        break\n\n    s = s.split()\n    target_sum = int(s[0])\n    tree = ("").join(s[1:])\n    tree = tree.replace(\'(\', \',[\').replace(\')\', \']\')\n    while True:\n        try:\n            tree = eval(tree[1:])\n            break\n        except SyntaxError:\n            s = input().split()\n            s = ("").join(s)\n            s = s.replace(\'(\', \',[\').replace(\')\', \']\')\n            tree += s\n\n    tree = str(tree)\n    tree = tree.replace(\',[\', \'[\')\n    if tree == \'[]\':\n        print("no")\n        continue\n\n    root = parse_tree(tree)\n\n    if has_path_sum(root, target_sum):\n        print("yes")\n    else:\n        print("no")\n'
SAMPLE='22 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))\n20 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))\n10 (3\n     (2 (4 () () )\n        (8 () () ) )\n     (1 (6 () () )\n        (4 () () ) ) )\n5 ()\n'
GENERATOR='g1145'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        assert valid(case),i
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
