import random, re, subprocess, sys, tempfile
from fractions import Fraction
from pathlib import Path
REFERENCE = 's=input()\nprint(f"{eval(s):.2f}")'
SAMPLES = ['3.4\n', '7+8.3\n', '3+4.5*(7+2)*(3)*((3+4)*(2+3.5)/(4+5))-34*(7-(2+3))\n']


def valid(text):
    """题面：一行，一个可带括号的四则运算表达式（数字可含小数点，运算符 + - * /）。
    题面未给长度/数值范围；这里只核语法：expr := term (('+'|'-') term)*，
    term := factor (('*'|'/') factor)*，factor := 数 | '(' expr ')'，不含空白、不含一元正负号，
    且不出现除以 0。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not s or not re.fullmatch(r"[0-9.+\-*/()]+", s):
        return False
    toks = re.findall(r"\d+(?:\.\d+)?|[+\-*/()]", s)
    if "".join(toks) != s:
        return False
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def factor():
        t = peek()
        if t is None:
            raise ValueError
        pos[0] += 1
        if t == "(":
            v = expr()
            if peek() != ")":
                raise ValueError
            pos[0] += 1
            return v
        if t[0].isdigit():
            return Fraction(t)
        raise ValueError

    def term():
        v = factor()
        while peek() in ("*", "/"):
            op = toks[pos[0]]; pos[0] += 1
            w = factor()
            if op == "*":
                v *= w
            else:
                if w == 0:
                    raise ValueError
                v /= w
        return v

    def expr():
        v = term()
        while peek() in ("+", "-"):
            op = toks[pos[0]]; pos[0] += 1
            w = term()
            v = v + w if op == "+" else v - w
        return v

    try:
        expr()
    except (ValueError, RecursionError):
        return False
    return pos[0] == len(toks)


def exact(s):
    return eval(re.sub(r"\d+(?:\.\d+)?", lambda m: f"Fraction('{m.group()}')", s))


def safe(s):
    """拒绝“四舍五入边界”与 -0.00，保证浮点 eval 与精确值舍入一致，避免判题歧义。"""
    try:
        v = exact(s)
    except ZeroDivisionError:
        return False
    if abs(v) > 10 ** 9:
        return False
    c = v * 100
    frac = abs(c - int(c))
    if abs(frac - Fraction(1, 2)) < Fraction(1, 10 ** 4):
        return False
    out = f"{eval(s):.2f}"
    if out.startswith("-0.00"):
        return False
    q = abs(c); r = int(q) + (1 if q - int(q) > Fraction(1, 2) else 0)
    want = ("-" if v < 0 and r else "") + f"{r // 100}.{r % 100:02d}"
    return out == want


def num(r, mode):
    if mode == 0 or r.random() < 0.5:
        return str(r.randint(0 if r.random() < 0.1 else 1, r.choice([9, 99, 1000])))
    return f"{r.randint(0, 99)}.{r.randint(0, 99):0{r.randint(1, 2)}d}"


def build(r, size, depth, mode):
    if size <= 1 or depth <= 0:
        x = num(r, mode)
        return f"({x})" if r.random() < 0.05 else x
    left = r.randint(1, size - 1)
    a = build(r, left, depth - 1, mode)
    b = build(r, size - left, depth - 1, mode)
    op = r.choice("+-*/")
    if op in "*/" and r.random() < 0.6:
        a, b = f"({a})" if any(c in a for c in "+-") else a, f"({b})"
    elif op == "-" and r.random() < 0.5:
        b = f"({b})"
    e = a + op + b
    if r.random() < 0.15 * (depth > 0):
        e = f"({e})"
    return e


def gen(r, size, depth, mode):
    while True:
        e = build(r, size, depth, mode)
        if valid(e + "\n") and safe(e):
            return e + "\n"


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p = Path(d) / "main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=30)
        if x.returncode:
            raise SystemExit(x.stderr)
        return x.stdout


def main():
    data = Path("data"); data.mkdir(exist_ok=True)
    cases = list(SAMPLES)
    cases += ["5\n", "0\n", "12.75\n", "((((7))))\n", "1/3\n", "2/3\n", "10-20\n", "3-4*5\n", "8/2/2\n", "8-2-2\n",
              "2*(3+4)*5/(1+1)\n", "100/7*7\n"]
    plan = [(2, 2, 0), (3, 3, 1), (4, 3, 1), (5, 4, 1), (6, 5, 1), (8, 5, 1), (10, 6, 1), (12, 6, 0),
            (15, 8, 1), (20, 10, 1), (30, 12, 1), (40, 15, 1), (60, 18, 1), (80, 20, 1), (100, 25, 1),
            (150, 25, 0), (200, 30, 1), (300, 30, 1), (400, 30, 1), (500, 30, 1), (600, 30, 1),
            (800, 30, 1), (1000, 30, 1), (1000, 30, 0), (1200, 30, 1)]
    for k, (size, depth, mode) in enumerate(plan):
        cases.append(gen(random.Random(4132 * 100 + k), size, depth, mode))
    seen = set()
    for i, text in enumerate(cases):
        assert valid(text), i
        assert text not in seen, i
        seen.add(text)
        (data / f"{i}.in").write_text(text, encoding="utf-8")
        (data / f"{i}.out").write_text(run(text), encoding="utf-8")


if __name__ == "__main__":
    main()
