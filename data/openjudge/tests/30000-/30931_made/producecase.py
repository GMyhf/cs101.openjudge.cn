import random
REFERENCE='# External reference: /practice/30931/statistics/\n# Accepted submission: 52760575\n# Source: http://cs101.openjudge.cn/practice/solution/52760575/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取输入并去除首尾可能的换行符\n    s = sys.stdin.readline().strip()\n    \n    stack = []\n    max_depth = 0\n    \n    # 定义左右括号的映射关系\n    match_map = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}\n    left_brackets = set([\'(\', \'[\', \'{\'])\n    \n    for char in s:\n        if char in left_brackets:\n            # 遇到左括号，入栈\n            stack.append(char)\n            # 更新最大嵌套深度\n            if len(stack) > max_depth:\n                max_depth = len(stack)\n        elif char in match_map:\n            # 遇到右括号\n            if not stack:\n                print("Invalid")\n                return\n            top = stack.pop()\n            # 检查是否匹配\n            if top != match_map[char]:\n                print("Invalid")\n                return\n        else:\n            # 题目保证只有这六种字符，但为了严谨可以忽略或报错\n            pass\n            \n    # 遍历结束后，检查栈是否为空\n    if stack:\n        print("Invalid")\n    else:\n        print(max_depth)\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='({[]})[]\n'
GENERATOR_NAME='g30931'
CPP=False
def valid(text):
    """题面约束：输入一行字符串 s，1<=len(s)<=100000，只包含 ()[]{} 六种字符。"""
    if text.endswith('\n'):
        text = text[:-1]
    if '\n' in text or not (1 <= len(text) <= 100000):
        return False
    return all(c in '()[]{}' for c in text)

_PAIR = {'(': ')', '[': ']', '{': '}'}

def balanced(r, length, p_open=0.5, kinds='([{'):
    """随机生成长度为 length（偶数）的合法括号串。"""
    out = []; st = []
    for pos in range(length):
        rem = length - pos
        if not st or (len(st) < rem and r.random() < p_open):
            c = r.choice(kinds); st.append(c); out.append(c)
        else:
            out.append(_PAIR[st.pop()])
    assert not st
    return ''.join(out)

def nested(r, depth):
    opens = [r.choice('([{') for _ in range(depth)]
    return ''.join(opens) + ''.join(_PAIR[c] for c in reversed(opens))

def build_cases():
    r = random.Random(30931)
    s = [SAMPLE.strip()]
    # 最小规模与各种非法类型
    s += ['(', ')', '()', '[]', '{}', '([)]', '((())', ']', '([]{})', '(([]))', ')(', '(]', '{[()()]}', '()[]{}', '}{', '((]]']
    # 小规模随机：一半合法、一半随机串
    for k in range(8):
        s.append(balanced(r, 2 * r.randint(1, 15), 0.55))
        s.append(''.join(r.choice('()[]{}') for _ in range(r.randint(1, 30))))
    # 大规模
    s.append(nested(r, 50000))                                  # 最大深度 50000，卡递归
    s.append(balanced(r, 100000, 0.5))                          # 随机合法
    s.append(balanced(r, 100000, 0.75))                         # 深度较大的随机合法
    s.append('()' * 50000)                                      # 深度 1
    s.append('(' * 100000)                                      # 全左括号
    s.append(')' * 100000)                                      # 全右括号
    b = balanced(r, 99998, 0.6); s.append(b[:-1] + {')': ']', ']': '}', '}': ')'}[b[-1]] + '()')  # 末尾附近类型错配，计数却平衡
    s.append('(' + balanced(r, 99998, 0.6))                     # 多一个左括号
    s.append(balanced(r, 99998, 0.6) + ']')                     # 多一个右括号
    # 每种括号各自计数平衡、但交叉错配，长度 1e5
    s.append('([' * 25000 + ')]' * 25000)
    s.append(nested(r, 49999) + '[]')                            # 深层合法后再接一对
    s.append(''.join(r.choice('()[]{}') for _ in range(99999)))  # 奇数长度随机
    return [x + '\n' for x in s]

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
    cases=build_cases()
    assert cases[0]==SAMPLE
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
