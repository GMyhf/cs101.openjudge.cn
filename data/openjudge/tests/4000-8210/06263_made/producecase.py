"""6263 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 6263
SAMPLE_IN = '( V | V ) & F & ( F| V)\n!V | V & V & !F & (F | V ) & (!F | F | !V & V)\n(F&F|V|!V&!F&!(F|F&V))\n'
SAMPLE_OUT = 'F\nV\nV\n'
REFERENCE_SOURCE = '# 23n2300011119(武)\ndef ShuntingYard(l:list):\n    stack,output=[],[]\n    for i in l:\n        if i==" ":continue\n        if i in \'VF\':output.append(i)\n        elif i==\'(\':stack.append(i)\n        elif i in \'&|!\':\n            while True:\n                if i==\'!\':break\n                elif not stack:break\n                elif stack[-1]=="(":\n                    break\n                else:output.append(stack.pop())\n            stack.append(i)\n        elif i==\')\':\n            while stack[-1]!=\'(\':\n                output.append(stack.pop())\n            stack.pop()\n    if stack:output.extend(reversed(stack))\n    return output\n\ndef Bool_shift(a):\n    if a==\'V\':return True\n    elif a==\'F\':return False\n    elif a==True:return \'V\'\n    elif a==False:return \'F\'\n\ndef cal(a,operate,b=None):\n    if operate=="&":return Bool_shift(Bool_shift(a) and Bool_shift(b))\n    if operate=="|":return Bool_shift(Bool_shift(a) or Bool_shift(b))\n    if operate=="!":return Bool_shift(not Bool_shift(a))\n\ndef post_cal(l:list):\n    stack=[]\n    for i in l:\n        if i in \'VF\':stack.append(i)\n        elif i in "&|!":\n            if i=="!":\n                stack.append(cal(stack.pop(),\'!\'))\n            else:\n                a,b=stack.pop(),stack.pop()\n                stack.append(cal(a,i,b))\n    return stack[0]\n\nwhile True:\n    try:print(post_cal(ShuntingYard(list(input()))))\n    except EOFError:break\n'

def g6263(r):
    atoms = ["V", "F"]
    for _ in range(r.randint(3, 12)):
        a, b = r.choice(atoms), r.choice(atoms)
        atoms.append(f"({a}&{b})" if r.random() < .5 else f"!({a}|{b})")
    return "\n".join(atoms[-r.randint(1, 3):]) + "\n"

# 题面：多行，每行一个由 V、F、&、|、!、括号和空格组成的布尔表达式，总长度不超过 1000。
# 「总长度」按最严的理解：整个输入（含换行）不超过 1000 个字符，单行自然也不超过。
def valid(text):
    if not text.endswith("\n") or len(text) > 1000:
        return False
    lines = text[:-1].split("\n")
    for ln in lines:
        if any(c not in "VF&|!() " for c in ln):
            return False
        toks = [c for c in ln if c != " "]
        if not toks:
            return False
        pos = 0
        def term():
            nonlocal pos
            while pos < len(toks) and toks[pos] == "!":
                pos += 1
            if pos >= len(toks):
                return False
            if toks[pos] in "VF":
                pos += 1
                return True
            if toks[pos] == "(":
                pos += 1
                if not expr() or pos >= len(toks) or toks[pos] != ")":
                    return False
                pos += 1
                return True
            return False
        def expr():
            nonlocal pos
            if not term():
                return False
            while pos < len(toks) and toks[pos] in "&|":
                pos += 1
                if not term():
                    return False
            return True
        if not expr() or pos != len(toks):
            return False
    return True


def eval_std(ln):
    """常规优先级 ! > & > |。"""
    py = ln.replace("V", " True ").replace("F", " False ").replace("&", " and ").replace("|", " or ").replace("!", " not ")
    return "V" if eval(py) else "F"


def eval_flat(ln):
    """& 与 | 同级、从左到右（内嵌参考解的做法）。"""
    toks = [c for c in ln if c != " "]; pos = 0
    def term():
        nonlocal pos
        neg = 0
        while toks[pos] == "!":
            neg ^= 1; pos += 1
        if toks[pos] == "(":
            pos += 1; v = expr(); pos += 1
        else:
            v = toks[pos] == "V"; pos += 1
        return v ^ bool(neg)
    def expr():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] in "&|":
            op = toks[pos]; pos += 1; w = term()
            v = (v and w) if op == "&" else (v or w)
        return v
    return "V" if expr() else "F"


def sp(r, rate):
    return " " if r.random() < rate else ""


def bexpr(r, depth, rate, top=False):
    """同一括号层内只用一种二元运算符，题面没写 & 与 | 的优先级，这样两种理解结果一致。"""
    if depth <= 0 or r.random() < 0.3:
        e = r.choice("VF")
    else:
        op = r.choice("&|")
        kids = [bexpr(r, depth - 1, rate) for _ in range(r.randint(2, 4))]
        e = (sp(r, rate) + op + sp(r, rate)).join(kids)
        if not top:
            e = "(" + sp(r, rate) + e + sp(r, rate) + ")"
    if not top and r.random() < 0.35:
        e = "!" * r.choice([1, 1, 1, 2, 3]) + sp(r, rate / 2) + e
    return e


def g6263_hard(r, kind):
    rate = r.choice([0.0, 0.3, 0.8])
    lines = []
    if kind == "long":
        # 单行接近 999 个字符
        while True:
            e = bexpr(r, r.randint(4, 7), rate, top=True)
            if 850 <= len(e) <= 999:
                lines = [e]
                break
    elif kind == "deep":
        # 左深嵌套括号，每层一个运算符
        d = r.randint(120, 180)  # Python 解析器最多 200 层括号，留余量给 eval 写法
        e = "(" * d + r.choice("VF")
        for _ in range(d):
            e += r.choice("&|") + r.choice(["V", "F", "!V", "!F"]) + ")"
        lines = [e[:999]] if len(e) <= 999 else None
        if lines is None:
            return g6263_hard(r, kind)
    elif kind == "nots":
        lines = ["!" * r.randint(1, 400) + r.choice("VF"), "!" * r.randint(1, 400) + "(" + "!" * r.randint(0, 50) + "V)"]
    elif kind == "atoms":
        lines = [r.choice(["V", "F", "!V", "!F", " V", "F ", "( V )", "!(F)", "((((V))))"]) for _ in range(r.randint(1, 120))]
    else:
        total = 0
        while True:
            e = bexpr(r, r.randint(1, 5), rate, top=r.random() < 0.7)
            if total + len(e) + 1 > 999:
                break
            lines.append(e); total += len(e) + 1
            if r.random() < 0.08:
                break
    for ln in lines:
        assert eval_std(ln) == eval_flat(ln), ln
    text = "\n".join(lines) + "\n"
    return text if valid(text) else g6263_hard(r, kind)


def build_cases():
    kinds = ["long", "long", "long", "deep", "deep", "nots", "atoms", "atoms"] + ["mix"] * 12
    base = build_cases_base(); out = []
    for i, k in enumerate(kinds):
        v = g6263_hard(random.Random(NUMBER * 100 + i), k)
        assert v not in base + out
        out.append(v)
    return base + out


def build_cases_base():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g6263(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
