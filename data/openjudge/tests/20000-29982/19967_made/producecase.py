import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19967 statistics, Accepted solution 51312141.\n# Source: http://cs101.openjudge.cn/practice/solution/51312141/\n# Statistics: http://cs101.openjudge.cn/practice/19967/statistics/\n# License: not declared on submission page; no license inferred\nN = int(input())\nl = []\nfor _ in range(N):\n    inp = input().split()\n    if inp[0] == '+':\n        idx, data = int(inp[1]), int(inp[2])\n        l.insert(idx, data)\n    elif inp[0] == '-':\n        idx = int(inp[1])\n        del l[idx]\n    elif inp[0] == '*':\n        idx, data = int(inp[1]), int(inp[2])\n        l[idx] = data\n    elif inp[0] == '?':\n        data = int(inp[1])\n        if data not in l:\n            print('Failed')\n        else:\n            print(l.index(data))\n"
LANGUAGE='Python3'
SAMPLE='6\n+ 0 1\n+ 0 2\n? 2\n* 1 3\n- 1\n? 1\n'
GENERATOR_NAME='g19967'
def g19967(r):
    ops=[]; size=0
    for _ in range(r.randint(8,30)):
        choices=["+"] if size==0 else ["+","?","*","-"]
        op=r.choice(choices)
        if op=="+": idx=r.randint(0,size); ops.append(f"+ {idx} {r.randint(-20,20)}"); size+=1
        elif op=="-": idx=r.randrange(size); ops.append(f"- {idx}"); size-=1
        elif op=="*": ops.append(f"* {r.randrange(size)} {r.randint(-20,20)}")
        else: ops.append(f"? {r.randint(-20,20)}")
    return f"{len(ops)}\n"+"\n".join(ops)+"\n"

def valid(text):
    """题面契约：首行 N（N<=1000），其后恰 N 行操作；+ p v / - p / * p v / ? v，
    p、v 为整数；插入 0<=p<=当前长度（样例在空数组上 + 0 1），删/改 0<=p<当前长度。"""
    import re
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"\d+", lines[0]):
        return False
    n = int(lines[0])
    if n > 1000 or len(lines) != n + 1:
        return False
    size = 0
    num = r"-?\d+"
    for ln in lines[1:]:
        tok = ln.split(" ")
        if tok[0] == "+" and len(tok) == 3 and all(re.fullmatch(num, t) for t in tok[1:]):
            if not 0 <= int(tok[1]) <= size:
                return False
            size += 1
        elif tok[0] in ("-", "*") and len(tok) == (2 if tok[0] == "-" else 3) and all(re.fullmatch(num, t) for t in tok[1:]):
            if not 0 <= int(tok[1]) < size:
                return False
            if tok[0] == "-":
                size -= 1
        elif tok[0] == "?" and len(tok) == 2 and re.fullmatch(num, tok[1]):
            pass
        else:
            return False
    return True

def gbig(r, n, lo, hi, mode):
    """追加的规模组：n 次操作；mode 控制增删比例，'drain' 会反复删空再在空表上查。"""
    ops = []; size = 0
    for k in range(n):
        if size == 0:
            choices = ["+", "?"] if mode == "drain" else ["+"]
        elif mode == "grow":
            choices = ["+", "+", "?", "?", "*", "-"]
        elif mode == "drain":
            choices = ["-", "-", "-", "?", "+", "*"]
        else:
            choices = ["+", "?", "*", "-"]
        op = r.choice(choices)
        if op == "+": ops.append(f"+ {r.randint(0, size)} {r.randint(lo, hi)}"); size += 1
        elif op == "-": ops.append(f"- {r.randrange(size)}"); size -= 1
        elif op == "*": ops.append(f"* {r.randrange(size)} {r.randint(lo, hi)}")
        else: ops.append(f"? {r.randint(lo, hi)}")
    return f"{len(ops)}\n" + "\n".join(ops) + "\n"

EXTRA = [  # (种子, n, 值域下界, 值域上界, 模式)
    (102, 1000, -5, 5, "grow"),        # 满规模、小值域：大量重复值，考"首次出现"下标
    (103, 1000, -10**9, 10**9, "grow"),# 满规模、大值域：几乎全是 Failed
    (104, 1000, 0, 30, "mixed"),
    (105, 1000, 0, 3, "drain"),        # 反复删空，空表上查询
    (106, 500, -100, 100, "mixed"),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 34)]  # 尾部 6 组让给下面的定制组，总数仍为 40（catalog 按文件列组）
    cases+=["1\n? 5\n"]  # 最小规模：空表上查询，输出 Failed
    cases+=[gbig(random.Random(sd), n, lo, hi, mode) for sd, n, lo, hi, mode in EXTRA]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
