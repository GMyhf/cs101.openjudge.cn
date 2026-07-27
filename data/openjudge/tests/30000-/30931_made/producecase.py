import random
REFERENCE='# External reference: /practice/30931/statistics/\n# Accepted submission: 52760575\n# Source: http://cs101.openjudge.cn/practice/solution/52760575/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取输入并去除首尾可能的换行符\n    s = sys.stdin.readline().strip()\n    \n    stack = []\n    max_depth = 0\n    \n    # 定义左右括号的映射关系\n    match_map = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}\n    left_brackets = set([\'(\', \'[\', \'{\'])\n    \n    for char in s:\n        if char in left_brackets:\n            # 遇到左括号，入栈\n            stack.append(char)\n            # 更新最大嵌套深度\n            if len(stack) > max_depth:\n                max_depth = len(stack)\n        elif char in match_map:\n            # 遇到右括号\n            if not stack:\n                print("Invalid")\n                return\n            top = stack.pop()\n            # 检查是否匹配\n            if top != match_map[char]:\n                print("Invalid")\n                return\n        else:\n            # 题目保证只有这六种字符，但为了严谨可以忽略或报错\n            pass\n            \n    # 遍历结束后，检查栈是否为空\n    if stack:\n        print("Invalid")\n    else:\n        print(max_depth)\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='({[]})[]\n'
GENERATOR_NAME='g30931'
CPP=False
def g30931(r):
    depth = r.randint(1, 20)
    if r.randint(0, 2) == 0:
        return "(" * depth + ")" * depth + "\n"
    if r.randint(0, 1) == 0:
        return "[" * depth + "]" * depth + "\n"
    text = "".join(r.choice("()[]{}") for _ in range(r.randint(1, 40)))
    return text + "\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
