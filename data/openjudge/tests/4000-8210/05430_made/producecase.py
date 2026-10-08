"""5430 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 41 组数据（第 20 组起为边界组与随机长表达式组）。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5430
SAMPLE_IN = 'a+b*c\n3\na 2\nb 7\nc 5\n'
SAMPLE_OUT = 'abc*+\n   +\n  / \\\n a   *\n    / \\\n    b c\n37\n'
REFERENCE_SOURCE = '\'\'\'\n表达式树是一种特殊的二叉树。对于你的问题，需要先将中缀表达式转换为后缀表达式\n（逆波兰式），然后根据后缀表达式建立表达式树，最后进行计算。\n\n首先使用stack进行中缀到后缀的转换，然后根据后缀表达式建立表达式二叉树，\n再通过递归和映射获取表达式的值。\n最后，打印出整棵树（取自 23n2300017735，夏天明BrightSummer）\n\n中缀表达式转后缀表达式 https://zq99299.github.io/dsalg-tutorial/dsalg-java-hsp/05/05.html\n\'\'\'\n#from collections import deque as q\nimport operator as op\n#import os\n\n\nclass Node:\n    def __init__(self, x):\n        self.value = x\n        self.left = None\n        self.right = None\n\n\ndef priority(x):\n    if x == \'*\' or x == \'/\':\n        return 2\n    if x == \'+\' or x == \'-\':\n        return 1\n    return 0\n\n\ndef infix_trans(infix):\n    postfix = []\n    op_stack = []\n    for char in infix:\n        if char.isalpha():\n            postfix.append(char)\n        else:\n            if char == \'(\':\n                op_stack.append(char)\n            elif char == \')\':\n                while op_stack and op_stack[-1] != \'(\':\n                    postfix.append(op_stack.pop())\n                op_stack.pop()\n            else:\n                while op_stack and priority(op_stack[-1]) >= priority(char) and op_stack[-1] != \'(\':\n                    postfix.append(op_stack.pop())\n                op_stack.append(char)\n    while op_stack:\n        postfix.append(op_stack.pop())\n    return postfix\n\n\ndef build_tree(postfix):\n    stack = []\n    for item in postfix:\n        if item in \'+-*/\':\n            node = Node(item)\n            node.right = stack.pop()\n            node.left = stack.pop()\n        else:\n            node = Node(item)\n        stack.append(node)\n    return stack[0]\n\n\ndef get_val(expr_tree, var_vals):\n    if expr_tree.value in \'+-*/\':\n        operator = {\'+\': op.add, \'-\': op.sub, \'*\': op.mul, \'/\': lambda x, y: abs(x) // abs(y) * (1 if (x >= 0) == (y > 0) else -1)}  # 题面：整除即舍弃小数部分（向零取整）\n        return operator[expr_tree.value](get_val(expr_tree.left, var_vals), get_val(expr_tree.right, var_vals))\n    else:\n        return var_vals[expr_tree.value]\n\n# 计算表达式树的深度。它通过递归地计算左右子树的深度，并取两者中的最大值再加1，得到整个表达式树的深度。\n\n\ndef getDepth(tree_root):\n    #return max([self.child[i].getDepth() if self.child[i] else 0 for i in range(2)]) + 1\n    left_depth = getDepth(tree_root.left) if tree_root.left else 0\n    right_depth = getDepth(tree_root.right) if tree_root.right else 0\n    return max(left_depth, right_depth) + 1\n\n    \'\'\'\n    首先，根据表达式树的值和深度信息构建第一行，然后构建第二行，该行包含斜线和反斜线，\n    用于表示子树的链接关系。接下来，如果当前深度为0，表示已经遍历到叶子节点，直接返回该节点的值。\n    否则，递减深度并分别获取左子树和右子树的打印结果。最后，将左子树和右子树的每一行拼接在一起，\n    形成完整的树形打印图。\n    \n打印表达式树的函数。表达式树是一种抽象数据结构，它通过树的形式来表示数学表达式。在这段程序中，\n函数printExpressionTree接受两个参数：tree_root表示树的根节点，d表示树的总深度。\n首先，函数会创建一个列表graph，列表中的每个元素代表树的一行。第一行包含根节点的值，\n并使用空格填充左右两边以保持树的形状。第二行显示左右子树的链接情况，使用斜杠/表示有左子树，\n反斜杠\\表示有右子树，空格表示没有子树。\n\n接下来，函数会判断深度d是否为0，若为0则表示已经达到树的最底层，直接返回根节点的值。否则，\n将深度减1，然后递归调用printExpressionTree函数打印左子树和右子树，\n并将结果分别存储在left和right中。\n\n最后，函数通过循环遍历2倍深度加1次，将左子树和右子树的每一行连接起来，存储在graph中。\n最后返回graph，即可得到打印好的表达式树。\n    \'\'\'\n\n\ndef printExpressionTree(tree_root, d):  # d means total depth\n\n    graph = [" "*(2**d-1) + tree_root.value + " "*(2**d-1)]\n    graph.append(" "*(2**d-2) + ("/" if tree_root.left else " ")\n                 + " " + ("\\\\" if tree_root.right else " ") + " "*(2**d-2))\n\n    if d == 0:\n        return tree_root.value\n    d -= 1\n    \'\'\'\n    应该是因为深度每增加一层，打印宽度就增加一倍，打印行数增加两行\n    \'\'\'\n    #left = printExpressionTree(tree_root.left, d) if tree_root.left else [\n    #    " "*(2**(d+1)-1)]*(2*d+1)\n    if tree_root.left:\n        left = printExpressionTree(tree_root.left, d)\n    else:\n        #print("left_d",d)\n        left = [" "*(2**(d+1)-1)]*(2*d+1)\n        #print("left_left",left)\n\n    right = printExpressionTree(tree_root.right, d) if tree_root.right else [\n        " "*(2**(d+1)-1)]*(2*d+1)\n\n    for i in range(2*d+1):\n        graph.append(left[i] + " " + right[i])\n        #print(\'graph=\',graph)\n    return graph\n\n\n\ninfix = input().strip()\nn = int(input())\nvars_vals = {}\nfor i in range(n):\n    line = input().split()\n    vars_vals[line[0]] = int(line[1])\n    \n\'\'\'\ninfix = "a+(b-c*d*e)"\n#infix = "a+b*c"\nn = 5\nvars_vals = {\'a\': 2, \'b\': 7, \'c\': 5, \'d\':1, \'e\':1}\n\'\'\'\n\npostfix = infix_trans(infix)\ntree_root = build_tree(postfix)\nprint(\'\'.join(str(x) for x in postfix))\nexpression_value = get_val(tree_root, vars_vals)\n\n\nfor line in printExpressionTree(tree_root, getDepth(tree_root)-1):\n    print(line.rstrip())\n\n\nprint(expression_value)\n'

EXPRESSIONS = ['a+b*c', '(a+b)*c', 'a*(b+c)-d', 'a/(b-c)+d', '(a+b)/(c+d)', 'a-b/c', '((a+b)*c-d)/e', 'a*(b-c)+d/e', '(a+b*c)-(d/e-f)', 'a/(b+c*d)-e', '(a-b)*(c+d)', 'a+b-c*d/e', '((a+b)-(c*d))/e', 'a*(b+(c-d))', '(a+b)*(c-d/e)', 'a/(b-c+d)', '(a+b+c)*d-e', 'a-b-(c+d)*e', 'a/(b+c)-d*e']

def g5430(r):
    expr = EXPRESSIONS[r.randrange(len(EXPRESSIONS))]
    variables = sorted(set(ch for ch in expr if ch.isalpha()))
    values = {ch: r.randint(1, 9) for ch in variables}
    # Keep every denominator nonzero for the expression families used here.
    if "b-c" in expr and values.get("b") == values.get("c"):
        values["c"] = values["c"] % 9 + 1
    if "b+c" in expr and values.get("b", 1) + values.get("c", 1) == 0:
        values["c"] = 1
    return expr + "\n" + str(len(variables)) + "\n" + "\n".join(f"{x} {values[x]}" for x in variables) + "\n"

def _parse(expr):
    """按题面文法解析（只有二元 + - * / 与括号，变量为单个小写字母），返回 (树, 深度)；不合法返回 None。"""
    pos = 0

    def factor():
        nonlocal pos
        if pos < len(expr) and expr[pos].islower():
            pos += 1
            return expr[pos - 1]
        if pos < len(expr) and expr[pos] == "(":
            pos += 1
            node = sum_()
            if node is None or pos >= len(expr) or expr[pos] != ")":
                return None
            pos += 1
            return node
        return None

    def chain(sub, ops):
        nonlocal pos
        node = sub()
        while node is not None and pos < len(expr) and expr[pos] in ops:
            op = expr[pos]; pos += 1
            rhs = sub()
            node = None if rhs is None else (op, node, rhs)
        return node

    def term():
        return chain(factor, "*/")

    def sum_():
        return chain(term, "+-")

    tree = sum_()
    if tree is None or pos != len(expr):
        return None
    return tree


def _depth(tree):
    return 1 if isinstance(tree, str) else 1 + max(_depth(tree[1]), _depth(tree[2]))


def _eval(tree, values, floor_div):
    """求值；除零返回 None。floor_div=True 用向下取整，False 用题面的「舍弃小数部分」。"""
    if isinstance(tree, str):
        return values[tree]
    op, a, b = tree[0], _eval(tree[1], values, floor_div), _eval(tree[2], values, floor_div)
    if a is None or b is None:
        return None
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if b == 0: return None
    if floor_div: return a // b
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


def valid(text):
    """题面：第一行中缀表达式（长度不大于 50，只含小写字母变量与 + - * / 小括号，无数字无空格）；
    第二行整数 n（n<10），为表达式的变量数；之后 n 行「C x」；保证不会除以 0。"""
    lines = text.split("\n")
    if len(lines) < 3 or lines[-1] != "":
        return False
    lines = lines[:-1]
    expr = lines[0]
    if not 1 <= len(expr) <= 50 or any(c not in "abcdefghijklmnopqrstuvwxyz+-*/()" for c in expr):
        return False
    tree = _parse(expr)
    if tree is None or not lines[1].isdigit():
        return False
    n = int(lines[1])
    names = set(c for c in expr if c.islower())
    if not n < 10 or n != len(names) or len(lines) != n + 2:
        return False
    values = {}
    for line in lines[2:]:
        parts = line.split(" ")
        if len(parts) != 2 or len(parts[0]) != 1 or parts[0] in values:
            return False
        if not parts[1].lstrip("-").isdigit():
            return False
        values[parts[0]] = int(parts[1])
    if set(values) != names:
        return False
    return _eval(tree, values, False) is not None


def _render(tree, parent_prec=0, right_side=False, r=None):
    if isinstance(tree, str):
        return f"({tree})" if r is not None and r.random() < .04 else tree
    op = tree[0]; prec = 2 if op in "*/" else 1
    text = _render(tree[1], prec, False, r) + op + _render(tree[2], prec, True, r)
    need = prec < parent_prec or (right_side and prec == parent_prec)
    if need or (r is not None and r.random() < .08):
        text = "(" + text + ")"
    return text


def _random_tree(r, leaves, names):
    if leaves == 1:
        return r.choice(names)
    k = r.randint(1, leaves - 1)
    return (r.choice("+-*/"), _random_tree(r, k, names), _random_tree(r, leaves - k, names))


def g5430_big(r, leaves, max_depth, nvars, lo=0, hi=20):
    """随机表达式：叶子数 leaves、变量 nvars 个（取自 a~z）、树高不超过 max_depth；
    值域 [lo, hi]；拒绝除零，也拒绝向下取整与截断取整不一致的组（参考解与题面两种理解都给同一答案）。"""
    while True:
        names = r.sample("abcdefghijklmnopqrstuvwxyz", nvars)
        tree = _random_tree(r, leaves, names)
        expr = _render(tree, r=r)
        if len(expr) > 50 or len(set(c for c in expr if c.islower())) != nvars:
            continue
        parsed = _parse(expr)
        if _depth(parsed) > max_depth:
            continue
        values = {c: r.randint(lo, hi) for c in names}
        a, b = _eval(parsed, values, False), _eval(parsed, values, True)
        if a is None or a != b or not _same_divisions(parsed, values):
            continue
        order = sorted(names) if r.random() < .5 else r.sample(names, nvars)
        return expr + "\n" + str(nvars) + "\n" + "".join(f"{c} {values[c]}\n" for c in order)


def _same_divisions(tree, values):
    """每一处除法上两种取整都相同。"""
    if isinstance(tree, str):
        return True
    if not (_same_divisions(tree[1], values) and _same_divisions(tree[2], values)):
        return False
    if tree[0] == "/":
        a, b = _eval(tree[1], values, False), _eval(tree[2], values, False)
        return b != 0 and a % b == 0 or (a >= 0) == (b > 0)
    return True


EDGE_CASES = [
    "a\n1\na 7\n",                       # 单变量，树高 1
    "((z))\n1\nz 0\n",                   # 冗余括号
    "a-b-c-d\n4\na 9\nb 1\nc 2\nd 3\n",   # 左结合减法链
    "a/b/c\n3\na 100\nb 3\nc 4\n",       # 左结合除法链（整除）
    "a-(b-(c-(d-e)))\n5\na 1\nb 2\nc 3\nd 4\ne 5\n",  # 右偏链
    "a*b+c*d-e/f\n6\na 3\nb 4\nc 5\nd 6\ne 17\nf 5\n",
    "a+a*a\n1\na 5\n",                   # 同一变量多次出现
]


def build_cases():
    cases = [SAMPLE_IN] + [g5430(random.Random(NUMBER + i)) for i in range(1, 20)] + EDGE_CASES
    r = random.Random(543000)
    for leaves, depth, nvars in ((4, 4, 4), (6, 5, 6), (8, 6, 8), (9, 7, 9), (12, 7, 9), (16, 8, 9),
                                 (20, 9, 9), (21, 10, 9), (10, 10, 9), (18, 6, 7), (19, 9, 9),
                                 (15, 9, 5), (20, 8, 8), (17, 10, 9)):
        cases.append(g5430_big(r, leaves, depth, nvars))
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
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
