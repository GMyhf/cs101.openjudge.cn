import random, subprocess
from pathlib import Path
ROOT=Path(__file__).parent
SAMPLE='3\n3+5*8\n(3+5)*8\n(23+34*45/(5+6+7))\n'
import tempfile, sys

INT_MIN, INT_MAX = -2**31, 2**31 - 1

def cdiv(a, b):
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q

def eval_c_int(s):
    """严格解析并按 C++ int 语义求值；语法不合法、除数为 0 或任何中间值越出 int 时返回 None。"""
    toks = []; i = 0
    while i < len(s):
        c = s[i]
        if c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit(): j += 1
            toks.append(int(s[i:j])); i = j
        elif c in "+-*/()":
            toks.append(c); i += 1
        else:
            return None
    nums = []; ops = []; prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    def apply():
        op = ops.pop(); b = nums.pop(); a = nums.pop()
        if op == "/":
            if b == 0: return False
            v = cdiv(a, b)
        else:
            v = a + b if op == "+" else a - b if op == "-" else a * b
        if not INT_MIN <= v <= INT_MAX: return False
        nums.append(v); return True
    expect_operand = True; depth = 0
    for t in toks:
        if expect_operand:
            if t == "(":
                ops.append(t); depth += 1
            elif isinstance(t, int):
                if not 1 <= t <= INT_MAX: return None   # 操作数都是正整数
                nums.append(t); expect_operand = False
            else:
                return None
        else:
            if t == ")":
                if depth == 0: return None
                while ops[-1] != "(":
                    if not apply(): return None
                ops.pop(); depth -= 1
            elif t in prec:
                while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[t]:
                    if not apply(): return None
                ops.append(t); expect_operand = True
            else:
                return None
    if expect_operand or depth: return None
    while ops:
        if not apply(): return None
    return nums[0]

def valid(text):
    """题面契约：第一行组数 N；其后恰 N 行，每行一个中缀表达式，只含数字、+-*/ 和圆括号，
    操作数都是正整数、无空格，长度不超过 600；除数不为 0；
    运算按 C++ int 进行，故操作数与每个中间结果都须落在 32 位有符号 int 内。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0][0] == "0":
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    for e in lines[1:]:
        if not 1 <= len(e) <= 600 or eval_c_int(e) is None:
            return False
    return True

PREC = {"+": 1, "-": 1, "*": 2, "/": 2}

def rnd_tree(r, budget, big):
    """随机表达式树，返回 (串, 值, 最外层优先级)；组合时只选不越界、除数非 0 的运算。"""
    if budget <= 1:
        if big and r.random() < 0.3: v = r.randint(1, 100000)
        else: v = r.choice([r.randint(1, 9), r.randint(1, 99), r.randint(1, 999)])
        return str(v), v, 3
    left = r.randint(1, budget - 1)
    sa, va, pa = rnd_tree(r, left, big); sb, vb, pb = rnd_tree(r, budget - left, big)
    ops = list("+-*/") + ["-", "/"]
    r.shuffle(ops)
    for op in ops:
        if op == "/" and vb == 0: continue
        v = va + vb if op == "+" else va - vb if op == "-" else va * vb if op == "*" else cdiv(va, vb)
        if INT_MIN <= v <= INT_MAX: break
    else:
        op = "+"; v = va + vb
        if not INT_MIN <= v <= INT_MAX: op = "-"; v = va - vb
    if pa < PREC[op] or r.random() < 0.1: sa = "(" + sa + ")"
    if pb <= PREC[op] or (pb == 3 and r.random() < 0.05) or r.random() < 0.1: sb = "(" + sb + ")"
    return sa + op + sb, v, PREC[op]

def gen_ok(r, budget, big, maxlen=600):
    while True:
        e = rnd_tree(r, budget, big)[0]
        if len(e) <= maxlen:
            assert eval_c_int(e) is not None
            return e

def neg_div(r):
    # 负数参与除法：C++ 向零截断与 Python // 向下取整不同
    a = r.randint(1, 50); b = a + r.randint(1, 500); c = r.randint(2, 9)
    form = r.choice(["({a}-{b})/{c}", "{c}/({a}-{b})", "({a}-{b})/({a}-{b}+{c}*{c}*{c})", "{a}-{b}/{c}*{c}-{b}"])
    return form.format(a=a, b=b, c=c)

def chain(r, ops, length):
    # 同级运算长链，检验左结合；逐个追加，保证每一步都不越出 int
    e = str(r.randint(1, 9))
    while len(e) < length - 6:
        for _ in range(50):
            cand = e + r.choice(ops) + str(r.randint(1, 99))
            if eval_c_int(cand) is not None:
                e = cand; break
        else:
            break
    return e

def nested(depth, r):
    e = str(r.randint(1, 9))
    for k in range(depth):
        e = "(" + e + ")" + r.choice("+-*") + str(r.randint(1, 3)) if k % 2 else "(" + e + ")"
    return e

FIXED = [
    "5", "2147483647", "46340*46340", "1-2147483647-1", "1-2147483647-2+1", "100-20-30", "100/5/2",
    "2*3/4", "2*(3/4)", "7-3+2", "7-(3+2)", "3/5", "(3-10)/2", "(3-10)/(1-3)", "7/(1-3)", "(1-8)/(3-5)/1",
    "((((((((((1))))))))))", "(2147483647)/(2147483647)", "1000000*2000/1000000", "(1-100)*(1-100)*(1-100)",
    "65536*32767+65535", "(0+1)" if False else "(1+1)*(2+2)/(3+3)-4", "123456789+987654321", "9/3*3/9*9",
]

def build_cases():
    cases = [SAMPLE]
    r = random.Random(388200)
    def pack(ex): return str(len(ex)) + "\n" + "\n".join(ex) + "\n"
    cases.append(pack(FIXED))
    cases.append(pack([neg_div(r) for _ in range(60)]))
    for i in range(3, 13):    # 小规模随机
        cases.append(pack([gen_ok(r, r.randint(2, 8), i % 2 == 0) for _ in range(r.randint(1, 10))]))
    for i in range(13, 23):   # 中等规模
        cases.append(pack([gen_ok(r, r.randint(10, 40), i % 3 == 0) for _ in range(r.randint(20, 60))]))
    for i in range(23, 31):   # 长表达式（接近 600）
        cases.append(pack([gen_ok(r, r.randint(90, 130), i % 2 == 0) for _ in range(r.randint(30, 60))]))
    cases.append(pack([chain(r, "+-", 600) for _ in range(40)]))
    cases.append(pack([chain(r, "-", 600) for _ in range(40)]))
    cases.append(pack([chain(r, "*/", 120) for _ in range(40)]))
    cases.append(pack([chain(r, "+-*/", 600) for _ in range(40)]))
    cases.append(pack([nested(d, r) for d in range(1, 120, 3)]))
    cases.append(pack(["(" * d + "1" + ")" * d for d in (1, 50, 100, 149)] + [nested(149, r)]))
    cases.append(pack(["+".join(["99999"] * 100), "2147483647-" + "-".join(["1"] * 290), "-".join(["2147483647"] + ["9999"] * 100)]))
    cases.append(pack([gen_ok(r, r.randint(100, 130), True) for _ in range(200)]))
    cases.append(pack([gen_ok(r, r.randint(1, 130), False) for _ in range(300)]))
    return cases

def main():
    cases = build_cases()
    assert len(cases) == 40 and len(set(cases)) == 40
    for i, inp in enumerate(cases):
        assert valid(inp), i
        out = subprocess.run(["python3", str(ROOT / "samplecode.py")], input=inp, text=True, capture_output=True, check=True).stdout
        (ROOT / "data" / f"{i}.in").write_text(inp); (ROOT / "data" / f"{i}.out").write_text(out)

if __name__ == "__main__":
    main()
