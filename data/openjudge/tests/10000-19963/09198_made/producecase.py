import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '{}[(){}]()\n'
SAMPLE_OUT = 'Yes\n'
CASES = ['{}[(){}]()\n', '{}(){}{}(){}()()[][]()[][]{}[][](){}(){]\n', '()()()()()[]{}{}{}{}[]()[]()[]{}\n', '{}{}[]{}(){}()()(){}(}\n', '[]()(){}[]()()()\n', '{}[][]{}[]()\n', '[]{}[}\n', '()[][]()[]{}[][]{}()[](){}[]\n', '[]{}[][][][][]{}{}()()()(){}{}[](){}[]\n', '(){}(){}()(){}{}[][]{}[](}\n', '{}(){}[]{}()()()(){}()[][][]{}\n', '()(){}{}{}\n', '{}(){}{}{}()(){}()[]()\n', '(){}{}{}{}{}{}{}[{\n', '(){}{}()[]()()[][][][}\n', '(){}()\n', '[][][]()()[][][]()[]{}()()()[]{}{}\n', '{}(){}()()[]()[]{}{}(){}[]()[]{}[](){{\n', '{}{}{}()()\n', '{}[]()[][]{}{}\n']
REFERENCE_SOURCE = 'def is_beautiful_brackets(sequence):\n    stack = []\n    # 对应关系字典，键为右括号，值为对应的左括号\n    bracket_pairs = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}\n    \n    for bracket in sequence:\n        if bracket in bracket_pairs.values():\n            # 若是左括号，压入栈中\n            stack.append(bracket)\n        elif bracket in bracket_pairs:\n            # 若是右括号，检查栈顶元素是否匹配\n            if stack and stack[-1] == bracket_pairs[bracket]:\n                stack.pop()\n            else:\n                return "No"\n        else:\n            # 输入不合法的字符时，直接返回No\n            return "No"\n    # 栈为空表示括号序列美观\n    return "Yes" if not stack else "No"\n\n# 输入处理\nsequence = input().strip()\n\n# 输出结果\nprint(is_beautiful_brackets(sequence))\n'
assert CASES[0] == SAMPLE_IN
random.seed(9198)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
