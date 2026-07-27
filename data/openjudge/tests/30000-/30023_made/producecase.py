import random
REFERENCE="# External reference: /practice/30023/statistics/\n# Accepted submission: 52824900\n# Source: http://cs101.openjudge.cn/practice/solution/52824900/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nimport re\n\ndef solve():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    m = int(input_data[0])\n    n = int(input_data[1])\n    \n    # 读取原子及其分子量\n    weights = {}\n    idx = 2\n    for _ in range(m):\n        atom = input_data[idx]\n        weight = int(input_data[idx+1])\n        weights[atom] = weight\n        idx += 2\n        \n    # 读取待计算的化学式\n    formulas = []\n    for _ in range(n):\n        formulas.append(input_data[idx])\n        idx += 1\n        \n    # 用于匹配原子（一个大写字母或一个大写加一个小写字母）、数字、左括号和右括号的正则表达式\n    token_pattern = re.compile(r'([A-Z][a-z]?|\\d+|\\(|\\))')\n    \n    for formula in formulas:\n        tokens = token_pattern.findall(formula)\n        stack = []\n        \n        for token in tokens:\n            if token == '(':\n                stack.append('(')\n            elif token == ')':\n                # 弹出并累加，直到遇到 '('\n                temp_sum = 0\n                while stack and stack[-1] != '(':\n                    temp_sum += stack.pop()\n                if stack and stack[-1] == '(':\n                    stack.pop()  # 弹出左括号\n                stack.append(temp_sum)\n            elif token.isdigit():\n                val = int(token)\n                if stack:\n                    stack[-1] *= val\n            else:\n                # 如果是原子，将其分子量入栈\n                stack.append(weights.get(token, 0))\n        \n        # 栈中剩余数值的总和即为该化学式的分子量\n        print(sum(stack))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='8 4\nH 1\nHe 4\nC 12\nO 16\nF 19\nNa 23\nAl 27\nCu 64\n(H2C)He\nCu(OH)2\nH((CO)2F)99\nNa1(Al)1O4H4\n'
GENERATOR_NAME='g30023'
def g30023(r):
    atoms = [("H", 1), ("He", 4), ("C", 12), ("O", 16), ("F", 19), ("Na", 23), ("Al", 27), ("Cu", 64)]
    formulas = []
    for _ in range(r.randint(1, 30)):
        a, b = r.choice(atoms)[0], r.choice(atoms)[0]
        formulas.append(f"{a}{r.randint(1, 4)}({b}{r.randint(1, 3)}){r.randint(1, 4)}")
    return f"{len(atoms)} {len(formulas)}\n" + "\n".join(f"{a} {w}" for a, w in atoms) + "\n" + "\n".join(formulas) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
