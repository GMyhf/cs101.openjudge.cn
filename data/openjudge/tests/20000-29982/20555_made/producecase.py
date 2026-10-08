"""20555 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20555
SAMPLE_IN = '( not ( True or False ) ) and ( False or True and True )\n'
SAMPLE_OUT = '0\n'
REFERENCE_SOURCE = 'def evaluate_expression(expression):\n    # Replace logical operators with Python equivalents\n    expression = expression.replace("not", "not ").replace("and", " and ").replace("or", " or ")\n    # Evaluate the expression\n    return int(eval(expression))\n\n# 读取输入并处理\nexpression = input()\nprint(evaluate_expression(expression))\n'

def g20555(r):
    a=r.choices(["True","False"],k=4); op1=r.choice(["and","or"]); op2=r.choice(["and","or"]); return f"( {a[0]} {op1} {a[1]} ) {op2} ( not {a[2]} or {a[3]} )\n"

TOKENS = {"(", ")", "not", "and", "or", "True", "False"}


def _parse(tokens):
    """按 or < and < not < 括号 的文法做递归下降；返回求值结果，非法抛 ValueError。"""
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def eat(tok):
        nonlocal pos
        if peek() != tok:
            raise ValueError(tok)
        pos += 1

    def p_or():
        v = p_and()
        while peek() == "or":
            eat("or")
            v = p_and() or v
        return v

    def p_and():
        v = p_not()
        while peek() == "and":
            eat("and")
            v = p_not() and v
        return v

    def p_not():
        nonlocal pos
        if peek() == "not":
            eat("not")
            return not p_not()
        t = peek()
        if t == "(":
            eat("(")
            v = p_or()
            eat(")")
            return v
        if t in ("True", "False"):
            pos += 1
            return t == "True"
        raise ValueError(t)

    v = p_or()
    if pos != len(tokens):
        raise ValueError("trailing")
    return v


def valid(text):
    """题面契约：一行，空格隔开的记号（括号、not/and/or、True/False），构成合法逻辑表达式。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    tokens = text[:-1].split(" ")
    if not all(t in TOKENS for t in tokens):
        return False
    try:
        _parse(tokens)
    except (ValueError, RecursionError):
        return False
    return True


PREC = {"or": 1, "and": 2, "not": 3, "lit": 4}


def _rand_expr(r, size, depth=0):
    """返回 (记号列表, 顶层优先级)；只在需要时加括号，偶尔加多余括号。"""
    if size <= 1 or depth > 12:
        e, p = [r.choice(["True", "False"])], PREC["lit"]
    else:
        kind = r.choice(["and", "or", "or", "and", "not"])
        if kind == "not":
            sub, sp = _rand_expr(r, size - 1, depth + 1)
            if sp < PREC["not"]:
                sub = ["("] + sub + [")"]
            e, p = ["not"] + sub, PREC["not"]
        else:
            k = r.randint(1, size - 1)
            a, ap = _rand_expr(r, k, depth + 1)
            b, bp = _rand_expr(r, size - k, depth + 1)
            if ap < PREC[kind]:
                a = ["("] + a + [")"]
            if bp <= PREC[kind] and r.random() < 0.3 or bp < PREC[kind]:
                b = ["("] + b + [")"]
            e, p = a + [kind] + b, PREC[kind]
    if r.random() < 0.08:
        e, p = ["("] + e + [")"], PREC["lit"]
    return e, p


def extra_cases():
    """补充：单个字面量、连续 not、and/or 优先级陷阱（从左到右求值会错）、随机长表达式。"""
    out = ["True\n", "False\n", "not True\n", "not not False\n",
           "( ( ( True ) ) )\n",
           "True or False and False\n",          # 1；从左到右算成 0
           "False and True or True\n",           # 1
           "not False and False\n",              # 0；not 若吞掉整段会得 1
           "not True or True\n",                 # 1
           "True or True and False or False and not True\n"]
    r = random.Random(NUMBER * 11 + 3)
    for size in (8, 15, 30, 60, 120, 300, 1000, 3000):
        for _ in range(2):
            out.append(" ".join(_rand_expr(r, size)[0]) + "\n")
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20555(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for value in extra_cases():
        if value not in cases:
            cases.append(value)
    for value in cases:
        assert valid(value), "生成的数据越出题面约束"
        depth = best = 0
        for t in value.split():
            depth += (t == "(") - (t == ")")
            best = max(best, depth)
        assert best < 60, "嵌套过深，eval 类解法会撞 CPython 的括号嵌套上限"
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
