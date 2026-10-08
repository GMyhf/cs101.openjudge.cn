import random, re, subprocess, tempfile
from fractions import Fraction
from pathlib import Path
REFERENCE_SOURCE = 'def evaluate_postfix(expression):\n    stack = []\n    tokens = expression.split()\n    \n    for token in tokens:\n        if token in \'+-*/\':\n            # 弹出栈顶的两个元素\n            right_operand = stack.pop()\n            left_operand = stack.pop()\n            # 执行运算\n            if token == \'+\':\n                stack.append(left_operand + right_operand)\n            elif token == \'-\':\n                stack.append(left_operand - right_operand)\n            elif token == \'*\':\n                stack.append(left_operand * right_operand)\n            elif token == \'/\':\n                stack.append(left_operand / right_operand)\n        else:\n            # 将操作数转换为浮点数后入栈\n            stack.append(float(token))\n    \n    # 栈顶元素就是表达式的结果\n    return stack[0]\n\n# 读取输入行数\nn = int(input())\n\n# 对每个后序表达式求值\nfor _ in range(n):\n    expression = input()\n    result = evaluate_postfix(expression)\n    # 输出结果，保留两位小数\n    print(f"{result:.2f}")\n'
SAMPLE_IN = '3\n5 3.4 +\n5 3.4 + 6 /\n5 3.4 + 6 * 3 +\n'
SAMPLE_OUT = '8.40\n1.40\n53.40\n'
def _postfix(r, letters=False, depth=0):
    if depth >= 3 or r.random() < .35:
        return r.choice("abcdefghijklmnopqrstuvwxyz") if letters else str(r.randint(1, 30))
    op = r.choice("+-*/") if not letters else r.choice("PQRS")
    return _postfix(r, letters, depth + 1) + " " + _postfix(r, letters, depth + 1) + " " + op

def _postfix_value(expr):
    """求值后缀表达式；除数为 0 时返回 None（而不是抛）。"""
    stack = []
    for token in expr.split():
        if token in "+-*/":
            b = stack.pop(); a = stack.pop()
            if token == "/":
                if b == 0: return None
                stack.append(a / b)
            elif token == "+": stack.append(a + b)
            elif token == "-": stack.append(a - b)
            else: stack.append(a * b)
        else:
            stack.append(float(token))
    return stack[0]

def generate_case(r):
    lines = []
    for _ in range(r.randint(3, 8)):
        for _ in range(200):                       # 拒绝采样：真求值一遍，除零就重摇
            expr = _postfix(r)
            if safe(expr): break  # 除零、贴着舍入边界（如 -0.035）、-0.00 都重摇
        else:
            expr = str(r.randint(1, 30))
        lines.append(expr)
    assert all(safe(line) for line in lines)
    return str(len(lines)) + "\n" + "\n".join(lines) + "\n"

_NUM = re.compile(r"-?[0-9]+(\.[0-9]+)?")

def valid(text):
    # 题面：第一行整数 n（n<100，这里取 1..99），接下来 n 行每行一个后序表达式，长度不超过 1000 个字符；
    # 操作数是整数或小数，运算符 + - * /，操作数与运算符之间用一个空格分隔；表达式须合法且不出现除以 0
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])): return False
    n = int(lines[0])
    if not 1 <= n <= 99 or len(lines) != n + 1: return False
    for line in lines[1:]:
        if not 1 <= len(line) <= 1000: return False
        depth = 0
        for tok in line.split(" "):
            if tok in ("+", "-", "*", "/"):
                if depth < 2: return False
                depth -= 1
            elif _NUM.fullmatch(tok): depth += 1
            else: return False
        if depth != 1 or exact_value(line) is None: return False
    return True

def exact_value(expr):
    # 用有理数精确求值；除以 0 返回 None
    st = []
    for tok in expr.split():
        if tok in "+-*/":
            b = st.pop(); a = st.pop()
            if tok == "/":
                if b == 0: return None
                st.append(a / b)
            else: st.append(a + b if tok == "+" else a - b if tok == "-" else a * b)
        else: st.append(Fraction(tok))
    return st[0]

def safe(expr):
    # 结果不能过大，不能贴着两位小数的舍入边界（浮点/精确值舍入要一致），也不出现 -0.00
    v = _postfix_value(expr); e = exact_value(expr)
    if v is None or e is None or abs(e) > 10 ** 12: return False
    frac = (abs(e) * 100) % 1
    if abs(frac - Fraction(1, 2)) < Fraction(1, 10 ** 6): return False
    if e < 0 and abs(e) < Fraction(5, 1000): return False
    return f"{v:.2f}" == f"{float(e):.2f}"

def operand(r):
    k = r.random()
    if k < .55: return str(r.randint(0, 99))
    if k < .8: return f"{r.randint(0, 99)}.{r.randint(0, 99):d}"
    if k < .9: return str(r.randint(100, 99999))
    return f"0.{r.randint(1, 999):03d}"

def random_postfix(r, maxlen, ops="+-*/", push=.55):
    # 随机栈过程：栈里不足两个就压操作数，否则按概率压数或做运算；总长度不超过 maxlen
    toks, depth, length = [], 0, -1
    while True:
        if depth >= 2 and (r.random() > push or length + 6 >= maxlen):
            t = r.choice(ops); depth -= 1
        elif length + 6 >= maxlen and depth == 1:
            break
        else:
            t = operand(r); depth += 1
        toks.append(t); length += len(t) + 1
        if depth == 1 and length + 6 >= maxlen: break
    return " ".join(toks)

def chunk(r, ops):
    for _ in range(1000):
        e = random_postfix(r, r.randint(3, 60), ops=ops)
        v = exact_value(e)
        if v is not None and abs(v) < 10 ** 6: return e
    return operand(r)

def gen_line(r, maxlen, ops="+-*/", push=.55):
    # 由若干小块（可含 * /）用 + - 串起来，偶尔整体乘/除一个小数，控制数值规模；栈形状随 push 变化
    for _ in range(1000):
        toks, depth, length = [], 0, -1
        while True:
            c = chunk(r, ops)
            if length + len(c) + 1 + 2 * (depth + 1) > maxlen: break
            toks.append(c); depth += 1; length += len(c) + 1
            while depth >= 2 and r.random() > push:
                op = r.choice("+-") if r.random() < .85 or "*" not in ops else r.choice(["*", "/"])
                toks.append(op); depth -= 1; length += 2
        while depth >= 2:
            toks.append(r.choice("+-")); depth -= 1
        if not toks: continue
        e = " ".join(toks)
        if len(e) <= 1000 and safe(e): return e
    raise AssertionError("no safe expression")

def big_case(r, n, lo, hi, **kw):
    lines = [gen_line(r, r.randint(lo, hi), **kw) for _ in range(n)]
    return f"{n}\n" + "\n".join(lines) + "\n"

def extra_cases():
    r = random.Random(245880)
    out = []
    out.append("1\n3.4\n")                                              # 单个操作数
    out.append("2\n5\n0\n")
    out.append("4\n10 3 -\n3 10 -\n1 4 /\n4 1 /\n")                  # 操作数顺序
    out.append("3\n100 25 / 2 *\n12.5 0.5 * 0.25 -\n1000 999.99 -\n")
    left = " ".join(["1"] * 200) + " " + " ".join(["+"] * 199)            # 栈深 200
    right = "1 " + " ".join(["2 +"] * 199)
    out.append(f"2\n{left}\n{right}\n")
    for k in range(15):
        n = [99, 99, 50, 99, 20][k % 5]
        out.append(big_case(r, n, 600 if k % 2 else 900, 1000,
                            ops="+-*/" if k % 3 else "+-", push=[.5, .55, .6][k % 3]))
    return out

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24588 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for content in extra_cases():
            assert valid(content) and content not in seen
            seen.append(content); index += 1
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
