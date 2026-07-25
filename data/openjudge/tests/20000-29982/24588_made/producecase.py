import random, subprocess, tempfile
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
            if _postfix_value(expr) is not None: break
        else:
            expr = str(r.randint(1, 30))
        lines.append(expr)
    assert all(_postfix_value(line) is not None for line in lines)
    return str(len(lines)) + "\n" + "\n".join(lines) + "\n"

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
