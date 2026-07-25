import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def infix_to_postfix(expression):\n    precedence = {'+':1, '-':1, '*':2, '/':2}\n    stack = []\n    postfix = []\n    number = ''\n\n    for char in expression:\n        if char.isnumeric() or char == '.':\n            number += char\n        else:\n            if number:\n                num = float(number)\n                postfix.append(int(num) if num.is_integer() else num)\n                number = ''\n            if char in '+-*/':\n                while stack and stack[-1] in '+-*/' and precedence[char] <= precedence[stack[-1]]:\n                    postfix.append(stack.pop())\n                stack.append(char)\n            elif char == '(':\n                stack.append(char)\n            elif char == ')':\n                while stack and stack[-1] != '(':\n                    postfix.append(stack.pop())\n                stack.pop()\n\n    if number:\n        num = float(number)\n        postfix.append(int(num) if num.is_integer() else num)\n\n    while stack:\n        postfix.append(stack.pop())\n\n    return ' '.join(str(x) for x in postfix)\n\nn = int(input())\nfor _ in range(n):\n    expression = input()\n    print(infix_to_postfix(expression))\n"
SAMPLE_IN = '3\n7+8.3 \n3+4.5*(7+2)\n(3)*((3+4)*(2+3.5)/(4+5))\n'
SAMPLE_OUT = '7 8.3 +\n3 4.5 7 2 + * +\n3 3 4 + 2 3.5 + * 4 5 + / *\n'
def _infix(r, depth=0):
    if depth >= 3 or r.random() < .35:
        return str(r.randint(1, 99))
    return "(" + _infix(r, depth + 1) + r.choice("+-*/") + _infix(r, depth + 1) + ")"

def generate_case(r):
    lines = [_infix(r) for _ in range(r.randint(3, 8))]
    assert all(line and " " not in line for line in lines)
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
                content = generate_case(random.Random(24591 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
