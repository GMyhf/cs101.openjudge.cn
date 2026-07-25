"""5430 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

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
REFERENCE_SOURCE = '\'\'\'\n表达式树是一种特殊的二叉树。对于你的问题，需要先将中缀表达式转换为后缀表达式\n（逆波兰式），然后根据后缀表达式建立表达式树，最后进行计算。\n\n首先使用stack进行中缀到后缀的转换，然后根据后缀表达式建立表达式二叉树，\n再通过递归和映射获取表达式的值。\n最后，打印出整棵树（取自 23n2300017735，夏天明BrightSummer）\n\n中缀表达式转后缀表达式 https://zq99299.github.io/dsalg-tutorial/dsalg-java-hsp/05/05.html\n\'\'\'\n#from collections import deque as q\nimport operator as op\n#import os\n\n\nclass Node:\n    def __init__(self, x):\n        self.value = x\n        self.left = None\n        self.right = None\n\n\ndef priority(x):\n    if x == \'*\' or x == \'/\':\n        return 2\n    if x == \'+\' or x == \'-\':\n        return 1\n    return 0\n\n\ndef infix_trans(infix):\n    postfix = []\n    op_stack = []\n    for char in infix:\n        if char.isalpha():\n            postfix.append(char)\n        else:\n            if char == \'(\':\n                op_stack.append(char)\n            elif char == \')\':\n                while op_stack and op_stack[-1] != \'(\':\n                    postfix.append(op_stack.pop())\n                op_stack.pop()\n            else:\n                while op_stack and priority(op_stack[-1]) >= priority(char) and op_stack[-1] != \'(\':\n                    postfix.append(op_stack.pop())\n                op_stack.append(char)\n    while op_stack:\n        postfix.append(op_stack.pop())\n    return postfix\n\n\ndef build_tree(postfix):\n    stack = []\n    for item in postfix:\n        if item in \'+-*/\':\n            node = Node(item)\n            node.right = stack.pop()\n            node.left = stack.pop()\n        else:\n            node = Node(item)\n        stack.append(node)\n    return stack[0]\n\n\ndef get_val(expr_tree, var_vals):\n    if expr_tree.value in \'+-*/\':\n        operator = {\'+\': op.add, \'-\': op.sub, \'*\': op.mul, \'/\': op.floordiv}\n        return operator[expr_tree.value](get_val(expr_tree.left, var_vals), get_val(expr_tree.right, var_vals))\n    else:\n        return var_vals[expr_tree.value]\n\n# 计算表达式树的深度。它通过递归地计算左右子树的深度，并取两者中的最大值再加1，得到整个表达式树的深度。\n\n\ndef getDepth(tree_root):\n    #return max([self.child[i].getDepth() if self.child[i] else 0 for i in range(2)]) + 1\n    left_depth = getDepth(tree_root.left) if tree_root.left else 0\n    right_depth = getDepth(tree_root.right) if tree_root.right else 0\n    return max(left_depth, right_depth) + 1\n\n    \'\'\'\n    首先，根据表达式树的值和深度信息构建第一行，然后构建第二行，该行包含斜线和反斜线，\n    用于表示子树的链接关系。接下来，如果当前深度为0，表示已经遍历到叶子节点，直接返回该节点的值。\n    否则，递减深度并分别获取左子树和右子树的打印结果。最后，将左子树和右子树的每一行拼接在一起，\n    形成完整的树形打印图。\n    \n打印表达式树的函数。表达式树是一种抽象数据结构，它通过树的形式来表示数学表达式。在这段程序中，\n函数printExpressionTree接受两个参数：tree_root表示树的根节点，d表示树的总深度。\n首先，函数会创建一个列表graph，列表中的每个元素代表树的一行。第一行包含根节点的值，\n并使用空格填充左右两边以保持树的形状。第二行显示左右子树的链接情况，使用斜杠/表示有左子树，\n反斜杠\\表示有右子树，空格表示没有子树。\n\n接下来，函数会判断深度d是否为0，若为0则表示已经达到树的最底层，直接返回根节点的值。否则，\n将深度减1，然后递归调用printExpressionTree函数打印左子树和右子树，\n并将结果分别存储在left和right中。\n\n最后，函数通过循环遍历2倍深度加1次，将左子树和右子树的每一行连接起来，存储在graph中。\n最后返回graph，即可得到打印好的表达式树。\n    \'\'\'\n\n\ndef printExpressionTree(tree_root, d):  # d means total depth\n\n    graph = [" "*(2**d-1) + tree_root.value + " "*(2**d-1)]\n    graph.append(" "*(2**d-2) + ("/" if tree_root.left else " ")\n                 + " " + ("\\\\" if tree_root.right else " ") + " "*(2**d-2))\n\n    if d == 0:\n        return tree_root.value\n    d -= 1\n    \'\'\'\n    应该是因为深度每增加一层，打印宽度就增加一倍，打印行数增加两行\n    \'\'\'\n    #left = printExpressionTree(tree_root.left, d) if tree_root.left else [\n    #    " "*(2**(d+1)-1)]*(2*d+1)\n    if tree_root.left:\n        left = printExpressionTree(tree_root.left, d)\n    else:\n        #print("left_d",d)\n        left = [" "*(2**(d+1)-1)]*(2*d+1)\n        #print("left_left",left)\n\n    right = printExpressionTree(tree_root.right, d) if tree_root.right else [\n        " "*(2**(d+1)-1)]*(2*d+1)\n\n    for i in range(2*d+1):\n        graph.append(left[i] + " " + right[i])\n        #print(\'graph=\',graph)\n    return graph\n\n\n\ninfix = input().strip()\nn = int(input())\nvars_vals = {}\nfor i in range(n):\n    line = input().split()\n    vars_vals[line[0]] = int(line[1])\n    \n\'\'\'\ninfix = "a+(b-c*d*e)"\n#infix = "a+b*c"\nn = 5\nvars_vals = {\'a\': 2, \'b\': 7, \'c\': 5, \'d\':1, \'e\':1}\n\'\'\'\n\npostfix = infix_trans(infix)\ntree_root = build_tree(postfix)\nprint(\'\'.join(str(x) for x in postfix))\nexpression_value = get_val(tree_root, vars_vals)\n\n\nfor line in printExpressionTree(tree_root, getDepth(tree_root)-1):\n    print(line.rstrip())\n\n\nprint(expression_value)\n'

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

def build_cases():
    return [SAMPLE_IN] + [g5430(random.Random(NUMBER + i)) for i in range(1, 20)]

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
