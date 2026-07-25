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
