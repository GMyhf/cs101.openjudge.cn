"""20576 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20576
SAMPLE_IN = '( not ( True or False ) ) and ( False or True and True )\n'
SAMPLE_OUT = 'not ( True or False ) and ( False or True and True )\n'
REFERENCE_SOURCE = 'class BinaryTree:\n    def __init__(self, root, left=None, right=None):\n        self.root = root\n        self.leftChild = left\n        self.rightChild = right\n\ndef postorder(string):  # 中缀改后缀 (Shunting Yard)\n    opStack, postList = [], []\n    inList = string.split()\n    prec = {\'(\': 0, \'or\': 1, \'and\': 2, \'not\': 3}\n    # 定义结合性：L 为左结合，R 为右结合\n    assoc = {\'or\': \'L\', \'and\': \'L\', \'not\': \'R\'}\n\n    for word in inList:\n        if word == \'(\':\n            opStack.append(word)\n        elif word == \')\':\n            while opStack and opStack[-1] != \'(\':\n                postList.append(opStack.pop())\n            opStack.pop()\n        elif word in (\'True\', \'False\'):\n            postList.append(word)\n        else:  # operator\n            # while opStack and prec[word] <= prec[opStack[-1]]:\n            # while opStack and (word != "not" and prec[word] <= prec[opStack[-1]]):\n            while (opStack and opStack[-1] in prec and (\n                    (assoc[word] == \'L\' and prec[word] <= prec[opStack[-1]]) or\n                    (assoc[word] == \'R\' and prec[word] < prec[opStack[-1]]))):\n                postList.append(opStack.pop())\n            opStack.append(word)\n    while opStack:\n        postList.append(opStack.pop())\n    return postList\n\ndef buildParseTree(infix):\n    postList = postorder(infix)\n    stack = []\n    for word in postList:\n        if word == \'not\':\n            child = stack.pop()\n            stack.append(BinaryTree(\'not\', child))\n        elif word in (\'True\', \'False\'):\n            stack.append(BinaryTree(word))\n        else:\n            right, left = stack.pop(), stack.pop()\n            stack.append(BinaryTree(word, left, right))\n    return stack[-1]\n\n# 定义运算符优先级\npriority = {\'or\': 1, \'and\': 2, \'not\': 3, \'True\': 4, \'False\': 4}\n\ndef printTree(tree):\n    """返回 token 列表"""\n    root = tree.root\n    if root in (\'True\', \'False\'):\n        return [root]\n\n    if root == \'not\':\n        child = tree.leftChild\n        # 若子优先级更低则加括号\n        child_tokens = printTree(child)\n        if priority[child.root] < priority[root]:\n            child_tokens = [\'(\'] + child_tokens + [\')\']\n        return [\'not\'] + child_tokens\n\n    # 二元操作符 and/or\n    left, right = tree.leftChild, tree.rightChild\n    left_tokens = printTree(left)\n    right_tokens = printTree(right)\n    if priority[left.root] < priority[root]:\n        left_tokens = [\'(\'] + left_tokens + [\')\']\n    if priority[right.root] < priority[root]:\n        right_tokens = [\'(\'] + right_tokens + [\')\']\n    return left_tokens + [root] + right_tokens\n\ndef main():\n    infix = input().strip()\n    Tree = buildParseTree(infix)\n    print(\' \'.join(printTree(Tree)))\n\nif __name__ == "__main__":\n    main()\n\n'

def g20576(r):
    a,b,c,d=r.choices(["True","False"],k=4); return f"( not ( {a} {r.choice(['and','or'])} {b} ) ) {r.choice(['and','or'])} ( {c} {r.choice(['and','or'])} {d} )\n"

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
    """题面契约（与 20555 同一输入格式）：一行，空格隔开的记号（括号、not/and/or、True/False），构成合法逻辑表达式。"""
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
    """补充：单个字面量、多余括号、连续 not、右侧同级嵌套、优先级陷阱、随机长表达式。"""
    out = ["True\n", "( False )\n", "( ( ( True ) ) )\n", "not ( not True )\n",
           "not ( ( not ( False ) ) )\n",
           "( True or False ) or ( False or True )\n",
           "True and ( False and True )\n",
           "( True and False ) or ( not True and False )\n",
           "( True or False ) and not ( False and True )\n",
           "not ( True and False ) or ( not ( False or True ) and True )\n",
           "( ( True or False ) and ( False or ( True and ( False or True ) ) ) )\n"]
    r = random.Random(NUMBER * 13 + 7)
    for size in (6, 10, 20, 40, 80, 200, 600, 2000):
        for _ in range(2):
            e = _rand_expr(r, size)[0]
            out.append(" ".join(e) + "\n")
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20576(random.Random(NUMBER + i + attempt * 1000))
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
        assert best < 60, "嵌套过深"
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
