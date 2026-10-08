import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def infix_to_postfix(expression):\n    precedence = {'+':1, '-':1, '*':2, '/':2}\n    stack = []\n    postfix = []\n    number = ''\n\n    for char in expression:\n        if char.isnumeric() or char == '.':\n            number += char\n        else:\n            if number:\n                num = float(number)\n                postfix.append(int(num) if num.is_integer() else num)\n                number = ''\n            if char in '+-*/':\n                while stack and stack[-1] in '+-*/' and precedence[char] <= precedence[stack[-1]]:\n                    postfix.append(stack.pop())\n                stack.append(char)\n            elif char == '(':\n                stack.append(char)\n            elif char == ')':\n                while stack and stack[-1] != '(':\n                    postfix.append(stack.pop())\n                stack.pop()\n\n    if number:\n        num = float(number)\n        postfix.append(int(num) if num.is_integer() else num)\n\n    while stack:\n        postfix.append(stack.pop())\n\n    return ' '.join(str(x) for x in postfix)\n\nn = int(input())\nfor _ in range(n):\n    expression = input()\n    print(infix_to_postfix(expression))\n"
SAMPLE_IN = '3\n7+8.3 \n3+4.5*(7+2)\n(3)*((3+4)*(2+3.5)/(4+5))\n'
SAMPLE_OUT = '7 8.3 +\n3 4.5 7 2 + * +\n3 3 4 + 2 3.5 + * 4 5 + / *\n'

_TOKEN = re.compile(r"\d+(?:\.\d+)?|[-+*/()]")


def _is_infix(expr):
    """按题面递归定义检查：数 | (a) | a c b，c 为 + - * /。"""
    pos, toks = 0, []
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m:
            return False
        toks.append(m.group()); pos = m.end()
    depth, want_operand = 0, True
    for t in toks:
        if want_operand:
            if t == "(":
                depth += 1
            elif t[0].isdigit():
                want_operand = False
            else:
                return False
        else:
            if t == ")":
                if depth == 0:
                    return False
                depth -= 1
            elif t in "+-*/":
                want_operand = True
            else:
                return False
    return depth == 0 and not want_operand


def valid(text):
    """题面：第一行整数 n(n<100)，接下来 n 行各一个中序表达式，数和运算符之间无空格，长度不超过 700。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if not 1 <= n < 100 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        expr = line.rstrip(" \r")          # 题面样例第一行带一个行尾空格
        if not 1 <= len(expr) <= 700 or not _is_infix(expr):
            return False
    return True


# ---- 生成 ----
def _num(r):
    """规范写法的数：整数无前导 0；小数末位非 0（参考解按 float 输出，避免 3.50 之类的歧义）。"""
    if r.random() < .3:
        ip = str(r.randint(0, 999))
        fp = "".join(r.choice("0123456789") for _ in range(r.randint(0, 2))) + r.choice("123456789")
        return ip + "." + fp
    return str(r.choice([r.randint(0, 9), r.randint(10, 999), r.randint(1000, 999999999)]))


def _infix(r, depth=0):
    """原生成器：全括号表达式。"""
    if depth >= 3 or r.random() < .35:
        return str(r.randint(1, 99))
    return "(" + _infix(r, depth + 1) + r.choice("+-*/") + _infix(r, depth + 1) + ")"


def _infix_value(expr):
    try:
        return eval(expr, {"__builtins__": {}}, {})    # 表达式由 _infix 用数字和 +-*/() 自造
    except ZeroDivisionError:
        return None


def old_case(r):
    lines = []
    for _ in range(r.randint(3, 8)):
        for _ in range(200):
            expr = _infix(r)
            if _infix_value(expr) is not None: break
        else:
            expr = str(r.randint(1, 99))
        lines.append(expr)
    return str(len(lines)) + "\n" + "\n".join(lines) + "\n"


def _free(r, budget, paren=0.25, ops="+-*/"):
    """不带多余括号的一般表达式：链式运算考优先级与左结合，偶尔套括号/冗余括号。"""
    if budget <= 0 or r.random() < .15:
        s = _num(r)
    else:
        k = r.randint(1, 4)
        parts = [_free(r, budget // (k + 1) - 2, paren, ops) for _ in range(k + 1)]
        s = parts[0]
        for p in parts[1:]:
            s += r.choice(ops) + p
    if r.random() < paren:
        k = r.randint(1, 2)
        s = "(" * k + s + ")" * k
    return s


def free_expr(r, maxlen, ops="+-*/", paren=0.25):
    for _ in range(1000):
        e = _free(r, r.randint(maxlen // 4, maxlen), paren, ops)
        if len(e) <= maxlen and _is_infix(e):
            return e
    raise AssertionError


def long_expr(r, target=700):
    """长度恰在 640~700 之间的长表达式。"""
    while True:
        e = free_expr(r, 700, paren=.3)
        while len(e) < target - 60:
            nxt = r.choice("+-*/") + free_expr(r, 60)
            if len(e) + len(nxt) > 700: break
            e += nxt
        if target - 60 <= len(e) <= 700 and _is_infix(e):
            return e


def deep_expr(r):
    """深层嵌套括号，长度接近 700。"""
    e = _num(r)
    while True:
        cand = "(" + e + r.choice("+-*/") + _num(r) + ")" if r.random() < .5 else "(" + _num(r) + r.choice("+-*/") + e + ")"
        if len(cand) > 700: break
        e = cand
    return e


def pack(lines):
    return f"{len(lines)}\n" + "\n".join(lines) + "\n"


def build_cases():
    r = random.Random(24591)
    cases = [SAMPLE_IN]
    # 1-8：原随机全括号数据保留前 8 组
    seen = [SAMPLE_IN]
    for index in range(1, 9):
        for attempt in range(100):
            content = old_case(random.Random(24591 + index + attempt * 1000))
            if content not in seen: break
        seen.append(content); cases.append(content)
    # 9：最小规模，单个数
    cases.append(pack(["5"]))
    # 10：单个数/小数/大整数/单层括号
    cases.append(pack(["0", "123456789", "0.5", "999.999", "(7)", "((((42))))", "1-2-3", "8/4/2"]))
    # 11：纯优先级与左结合（无括号）
    cases.append(pack(["1-2-3-4", "1-2+3", "2*3+4", "2+3*4", "2-3*4-5", "8/2/2*3", "1+2*3-4/5", "6/3*2", "1*2-3*4+5/6", "9-8/4*2+1",
                       "1.5*2.25-3.75/0.5", "10-2*3/4+5*6-7"]))
    # 12-13：一般表达式（括号随机）
    for _ in range(2):
        cases.append(pack([free_expr(r, r.choice([30, 80, 200])) for _ in range(r.randint(20, 40))]))
    # 14：只含 + - 或只含 * /，考同优先级左结合
    cases.append(pack([free_expr(r, 120, ops="+-", paren=.1) for _ in range(15)] + [free_expr(r, 120, ops="*/", paren=.1) for _ in range(15)]))
    # 15：深层嵌套括号
    cases.append(pack([deep_expr(r) for _ in range(10)]))
    # 16-18：n=99，每行长度接近 700
    for _ in range(3):
        cases.append(pack([long_expr(r) for _ in range(99)]))
    # 19：n=99，混合长短/深浅
    mix = [long_expr(r) if i % 3 == 0 else deep_expr(r) if i % 3 == 1 else free_expr(r, 50) for i in range(99)]
    cases.append(pack(mix))
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 20 and len(set(cases)) == len(cases)
    assert all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
