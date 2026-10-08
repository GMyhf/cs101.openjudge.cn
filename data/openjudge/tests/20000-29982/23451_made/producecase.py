import random, subprocess, sys, tempfile
from fractions import Fraction
from pathlib import Path
REFERENCE_SOURCE = 'class stack():\n    def __init__(self):\n        self.val=[]\n    def isempty(self):\n        return len(self.val)==0\n    def push(self,item):\n        self.val.append(item)\n    def top(self):\n        return self.val[-1]\n    def pop(self):\n        del self.val[-1]\n\ndef operatorcheck():\n    for i in range(len(exp)):\n        if exp[i] not in ch:\n            return 0\n    return 1\n\ndef bracketcheck():\n    bracket=stack()\n    for i in range(len(exp)):\n        if exp[i]==\'(\':\n            bracket.push(\'(\')\n        if exp[i]==\')\':\n            if bracket.isempty():\n                return 0\n            else:\n                bracket.pop()\n    if bracket.isempty():\n        return 1\n    else:\n        return 0\n\ndef onlybracket():\n    for i in range(len(exp)):\n        if exp[i]!=\'(\' and exp[i]!=\')\':\n            return 0\n    return 1\n            \ndef cut():\n    i=0\n    while i<=len(exp)-1:\n        if exp[i]==\'*\' or exp[i]==\'/\' or exp[i]==\'(\' or exp[i]==\')\':\n            expression.append(exp[i])\n            i+=1\n            continue\n        if exp[i]==\'+\' or exp[i]==\'-\':\n            if i==0 or exp[i-1] not in ch[5:]:\n                temp=\'\'+exp[i]\n                i+=1\n                while i<=len(exp)-1 and exp[i] in ch[6:]:\n                    temp=temp+exp[i]\n                    i+=1\n                expression.append(float(temp))\n                continue\n            else:\n                expression.append(exp[i])\n                i+=1\n                continue\n        if exp[i] in ch[6:]:\n            temp=\'\'\n            while i<=len(exp)-1 and exp[i] in ch[6:]:\n                temp=temp+exp[i]\n                i+=1\n            expression.append(float(temp))\n            continue\ndef value(s,x,y):\n    if s==\'+\':\n        return x+y\n    if s==\'*\':\n        return x*y\n    if s==\'-\':\n        return x-y\n    if s==\'/\':\n        return x/y\n\ndef calc():\n    operator=stack()\n    operand=stack()\n    for i in range(len(expression)):\n        if expression[i] not in ch[0:6]:\n            operand.push(expression[i])\n        elif expression[i]==\'(\':\n            operator.push(\'(\')\n        elif expression[i]==\')\':\n            while operator.top()!=\'(\':\n                b=operand.top()\n                operand.pop()\n                a=operand.top()\n                operand.pop()\n                operand.push(value(operator.top(),a,b))\n                operator.pop()\n            operator.pop()\n        elif expression[i] in ch[0:4]:\n            while not operator.isempty() and prior[operator.top()]>=prior[expression[i]]:\n                b=operand.top()\n                operand.pop()\n                a=operand.top()\n                operand.pop()\n                operand.push(value(operator.top(),a,b))\n                operator.pop()\n            operator.push(expression[i])\n    while not operator.isempty():\n        b=operand.top()\n        operand.pop()\n        a=operand.top()\n        operand.pop()\n        operand.push(value(operator.top(),a,b))\n        operator.pop()\n    print(\'{:.3f}\'.format(operand.top()))\n                \n        \nch=[\'+\',\'-\',\'*\',\'/\',\'(\',\')\',\'.\',\'0\',\'1\',\'2\',\'3\',\'4\',\'5\',\'6\',\'7\',\'8\',\'9\']\nprior={\'*\':3,\'/\':3,\'+\':2,\'-\':2,\'(\':1}\nwhile True:\n    s=list(map(str,input().split()))\n    if s==["quit"]:\n        break\n    if len(s)==0:\n        print("No expression.")\n        continue\n    exp=""\n    for i in range(len(s)):\n        exp=exp+s[i]\n    if operatorcheck()==False:\n        print("Unknown operator.")\n        continue\n    if bracketcheck()==False:\n        print("Unmatched bracket.")\n        continue\n    if onlybracket()==True:\n        print("No expression.")\n        continue\n    expression=[]\n    try:\n        cut()\n        calc()\n    except:\n        print("Not implemented.")\n        continue\n'
SAMPLE_IN = '(((-10.1 + 4.3) * 8.5) - 6) / 4   \n((1+     2)*3\n      (1+1+1.   1) /    3\n\n1 ++ 1\n1 +++ 1\n1^2\nquit\n'
SAMPLE_OUT = '-13.825\nUnmatched bracket.\n1.033\nNo expression.\n2.000\nNot implemented.\nUnknown operator.\n'

ALLOWED = set("+-*/().0123456789")
DIGITS = set("0123456789")
LIMIT = 1000


class _Bad(Exception):
    pass


def _parse(e):
    """按题面文法解析去掉空格后的表达式 e，返回 (精确值 Fraction, 浮点值, 是否越界/除零)。
    文法：expr := term (('+'|'-') term)* ; term := factor (('*'|'/') factor)* ;
    factor := number | '(' expr ')' ; number := ['+'|'-'] digits ['.' digits]
    （符号只能出现在需要操作数的位置，每个数最多一个符号）。不合文法时抛 _Bad。"""
    if sys.getrecursionlimit() < 20000:
        sys.setrecursionlimit(20000)      # 深层括号嵌套
    pos = 0
    n = len(e)
    flags = {"range": False}

    def check(v):
        if not -LIMIT <= v <= LIMIT:
            flags["range"] = True

    def number():
        nonlocal pos
        st = pos
        if pos < n and e[pos] in "+-":
            pos += 1
        d0 = pos
        while pos < n and e[pos] in DIGITS:
            pos += 1
        if pos == d0:
            raise _Bad
        if pos < n and e[pos] == ".":
            pos += 1
            d1 = pos
            while pos < n and e[pos] in DIGITS:
                pos += 1
            if pos == d1:
                raise _Bad
        t = e[st:pos]
        v = Fraction(t)
        check(v)
        return v, float(t)

    def factor():
        nonlocal pos
        if pos < n and e[pos] == "(":
            pos += 1
            v = expr()
            if pos >= n or e[pos] != ")":
                raise _Bad
            pos += 1
            return v
        return number()

    def term():
        nonlocal pos
        a, fa = factor()
        while pos < n and e[pos] in "*/":
            op = e[pos]; pos += 1
            b, fb = factor()
            if op == "*":
                a, fa = a * b, fa * fb
            else:
                if b == 0:
                    flags["range"] = True
                    a, fa = Fraction(0), 0.0
                else:
                    a, fa = a / b, (fa / fb if fb else 0.0)
            check(a)
        return a, fa

    def expr():
        nonlocal pos
        a, fa = term()
        while pos < n and e[pos] in "+-":
            op = e[pos]; pos += 1
            b, fb = term()
            if op == "+":
                a, fa = a + b, fa + fb
            else:
                a, fa = a - b, fa - fb
            check(a)
        return a, fa

    v, fv = expr()
    if pos != n:
        raise _Bad
    return v, fv, flags["range"]


def _exact_text(v):
    q, rem = divmod(abs(v) * 1000, 1)
    if rem * 2 == 1:
        return None                       # 恰在舍入分界
    q = int(q) + (1 if rem * 2 > 1 else 0)
    if v < 0 and q == 0:
        return None                       # 结果为 -0.000 还是 0.000 题面未定义
    return ("-" if v < 0 else "") + f"{q // 1000}.{q % 1000:03d}"


def judge_line(line):
    """独立实现的判定，返回期望输出；附带 ok 标志表示该行是否满足题面的数据保证。"""
    e = "".join(line.split())
    if not e:
        return "No expression.", True
    if any(ch not in ALLOWED for ch in e):
        return "Unknown operator.", True
    depth = 0
    for ch in e:
        depth += (ch == "(") - (ch == ")")
        if depth < 0:
            return "Unmatched bracket.", True
    if depth:
        return "Unmatched bracket.", True
    if all(ch in "()" for ch in e):
        return "No expression.", True
    try:
        v, fv, bad = _parse(e)
    except _Bad:
        return "Not implemented.", True
    t = _exact_text(v)
    ok = not bad and t is not None and "{:.3f}".format(fv) == t
    return t, ok


def line_ok(line):
    if any(not (32 <= ord(ch) < 127) for ch in line):
        return False
    if line.split() == ["quit"]:
        return False
    e = "".join(line.split())
    for i, ch in enumerate(e):
        if ch == "." and not (0 < i < len(e) - 1 and e[i - 1] in DIGITS and e[i + 1] in DIGITS):
            return False
    return judge_line(line)[1]


def valid(text):
    # 题面：输入 N+1 行，N 行为表达式，最后一行为 quit；每个表达式占一行；
    # 小数点两侧均有数字；运算中间量和结果均在 [-1000, 1000]；不存在精度损失问题。
    # （格式核对：只允许可打印 ASCII 与空格，不含制表符/回车；quit 之前不得出现 quit 行。）
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if lines[-1] != "quit":
        return False
    return all(line_ok(line) for line in lines[:-1])


# ---------------- 生成 ----------------

def _num(r, sign_ok=True):
    k = r.random()
    if k < 0.45:
        t = str(r.randint(0, 20))
    elif k < 0.8:
        t = f"{r.randint(0, 50)}.{r.randint(0, 9)}"
    elif k < 0.9:
        t = f"{r.randint(0, 9)}.{r.randint(0, 99):02d}"
    else:
        t = "0" + str(r.randint(1, 9))                    # 前导零，如 05
    if sign_ok and r.random() < 0.25:
        t = r.choice("+-") + t
    return t


def _tree(r, depth):
    if depth <= 0 or r.random() < 0.25:
        return _num(r)
    a = _tree(r, depth - 1)
    b = _tree(r, depth - 1)
    op = r.choice("+-*/")
    s = f"{a}{op}{b}"
    if r.random() < 0.45:
        s = "(" + s + ")"
    return s


def _space(r, e, p=0.3):
    out = []
    for ch in e:
        if r.random() < p:
            out.append(" " * r.randint(1, 3))
        out.append(ch)
    if r.random() < 0.3:
        out.append(" " * r.randint(1, 4))
    return "".join(out)


def _good_expr(r, depth):
    while True:
        e = _tree(r, depth)
        if r.random() < 0.2:
            e = "(" * (k := r.randint(1, 4)) + e + ")" * k
        try:
            v, fv, bad = _parse(e)
        except _Bad:
            continue
        t = _exact_text(v)
        if not bad and t is not None and "{:.3f}".format(fv) == t:
            return e


def _bad_line(r, kind):
    while True:
        e = _good_expr(r, r.randint(1, 4))
        if kind == "unmatched":
            if r.random() < 0.5:
                e = e + ")" if r.random() < 0.5 else "(" + e
            else:
                idx = [i for i, ch in enumerate(e) if ch in "()"]
                if not idx:
                    e = ")" + e + "("
                else:
                    i = r.choice(idx); e = e[:i] + e[i + 1:]
        elif kind == "unknown":
            i = r.randint(0, len(e))
            e = e[:i] + r.choice("^%x=&!#a[]{}<>?:;,_$@~|") + e[i:]
        elif kind == "notimpl":
            k = r.randint(0, 5)
            if k == 0:
                e = e + r.choice("+-*/")
            elif k == 1:
                e = r.choice("*/") + e
            elif k == 2:
                e = e + "+++" + _num(r, False)
            elif k == 3:
                e = "(" + e + r.choice("*/") + ")"
            elif k == 4:
                e = e + "*" + r.choice("*/") + _num(r, False)
            else:
                e = e + "--" + r.choice("+-") + _num(r, False)
        line = _space(r, e)
        want = {"unmatched": "Unmatched bracket.", "unknown": "Unknown operator.", "notimpl": "Not implemented."}[kind]
        if judge_line(line)[0] == want and line_ok(line):
            return line


def _empty_line(r):
    k = r.randint(0, 3)
    if k == 0:
        return ""
    if k == 1:
        return " " * r.randint(1, 5)
    if k == 2:
        return _space(r, "()" * r.randint(1, 3))
    d = r.randint(1, 5)
    return _space(r, "(" * d + ")" * d + "()" * r.randint(0, 2))


def gen_case(r, n_lines, depth):
    lines = []
    for _ in range(n_lines):
        k = r.random()
        if k < 0.55:
            lines.append(_space(r, _good_expr(r, r.randint(0, depth))))
        elif k < 0.67:
            lines.append(_bad_line(r, "unmatched"))
        elif k < 0.79:
            lines.append(_bad_line(r, "unknown"))
        elif k < 0.91:
            lines.append(_bad_line(r, "notimpl"))
        else:
            lines.append(_empty_line(r))
    return "\n".join(lines + ["quit"]) + "\n"


def _deep(r, levels):
    # 深层嵌套：每层 ( x op ... )，保持数值很小
    e = _num(r, False)
    for _ in range(levels):
        op = r.choice("+-")
        e = "(" + e + op + str(r.randint(0, 3)) + ")" if r.random() < 0.5 else "(" + str(r.randint(0, 3)) + op + e + ")"
    return e


def fixed_cases():
    r = random.Random(234510)
    out = []
    # 只含一行，覆盖结合性与题面举例
    out.append("2 / 4 / 2\n-10.1 + 4.3 * 8.5 - 6 / 4\n-10 * 3.4\n0.1 + 1.0 + -2 / 3\n0.85 * (10 / -2) * 05\n1 - -1\n+5 - +5\n10 - 4 - 3\n(-1)\nquit\n")
    out.append("()\n(())\n  ( ( ) )  ()\n\n     \n)(\n1 + 2)\n(1 + 2\n1 +\n* 2\n1 * / 2\n(1 +)\n1 a 2\n1 % 2\n= 3\n1 ++ 1\n1 +++ 1\n1 -- 1\n1 --- 1\nquit\n")
    out.append("\n".join(_space(r, _deep(r, 400)) for _ in range(3)) + "\n" + _space(r, "(" * 300 + "1" + ")" * 300) + "\n" + "(" * 200 + "1+2" + ")" * 199 + "\nquit\n")
    out.append("1\nquit\n")
    return out


def main():
    root = Path(__file__).parent / "data"
    cases = [SAMPLE_IN] + fixed_cases()
    total = 20
    rest = total - len(cases)
    for index in range(rest):
        r = random.Random(23451 * 7 + index)
        if index < rest - 3:
            n_lines, depth = r.randint(5, 40), r.randint(1, 4)
        else:
            n_lines, depth = 3000, 6                       # 规模组
        cases.append(gen_case(r, n_lines, depth))
    assert len(set(cases)) == len(cases) == total
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            want = "".join(judge_line(l)[0] + "\n" for l in content.split("\n")[:-2])
            assert result.stdout == want, (index, result.stdout[:200], want[:200])
            if index == 0:
                assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
