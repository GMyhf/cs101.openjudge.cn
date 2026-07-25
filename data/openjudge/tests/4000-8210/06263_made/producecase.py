"""6263 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 6263
SAMPLE_IN = '( V | V ) & F & ( F| V)\n!V | V & V & !F & (F | V ) & (!F | F | !V & V)\n(F&F|V|!V&!F&!(F|F&V))\n'
SAMPLE_OUT = 'F\nV\nV\n'
REFERENCE_SOURCE = '# 23n2300011119(武)\ndef ShuntingYard(l:list):\n    stack,output=[],[]\n    for i in l:\n        if i==" ":continue\n        if i in \'VF\':output.append(i)\n        elif i==\'(\':stack.append(i)\n        elif i in \'&|!\':\n            while True:\n                if i==\'!\':break\n                elif not stack:break\n                elif stack[-1]=="(":\n                    break\n                else:output.append(stack.pop())\n            stack.append(i)\n        elif i==\')\':\n            while stack[-1]!=\'(\':\n                output.append(stack.pop())\n            stack.pop()\n    if stack:output.extend(reversed(stack))\n    return output\n\ndef Bool_shift(a):\n    if a==\'V\':return True\n    elif a==\'F\':return False\n    elif a==True:return \'V\'\n    elif a==False:return \'F\'\n\ndef cal(a,operate,b=None):\n    if operate=="&":return Bool_shift(Bool_shift(a) and Bool_shift(b))\n    if operate=="|":return Bool_shift(Bool_shift(a) or Bool_shift(b))\n    if operate=="!":return Bool_shift(not Bool_shift(a))\n\ndef post_cal(l:list):\n    stack=[]\n    for i in l:\n        if i in \'VF\':stack.append(i)\n        elif i in "&|!":\n            if i=="!":\n                stack.append(cal(stack.pop(),\'!\'))\n            else:\n                a,b=stack.pop(),stack.pop()\n                stack.append(cal(a,i,b))\n    return stack[0]\n\nwhile True:\n    try:print(post_cal(ShuntingYard(list(input()))))\n    except EOFError:break\n'

def g6263(r):
    atoms = ["V", "F"]
    for _ in range(r.randint(3, 12)):
        a, b = r.choice(atoms), r.choice(atoms)
        atoms.append(f"({a}&{b})" if r.random() < .5 else f"!({a}|{b})")
    return "\n".join(atoms[-r.randint(1, 3):]) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g6263(random.Random(NUMBER + i + attempt * 1000))
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
