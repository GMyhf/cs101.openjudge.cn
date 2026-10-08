import random
REFERENCE='# External reference: /practice/29694/statistics/\n# Accepted submission: 52824892\n# Source: http://cs101.openjudge.cn/practice/solution/52824892/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 从标准输入中读取所有音节\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    stack = []\n    for x in input_data:\n        stack.append(x)\n        \n        # 优先检测单音节叠音 (如 3 3)\n        if len(stack) >= 2 and stack[-1] == stack[-2]:\n            stack.pop()\n        # 检测双音节叠音 (如 1 2 1 2)\n        elif len(stack) >= 4 and stack[-4:-2] == stack[-2:]:\n            stack.pop()\n            stack.pop()\n            \n    # 输出还原后的原始歌词\n    print(" ".join(stack))\n\nif __name__ == \'__main__\':\n    solve()'
SAMPLE='1 2 1 2 1 2 1 3 3 4\n'
GENERATOR_NAME='g29694'
def g29694(r):
    return " ".join(str(r.randint(1, 6)) for _ in range(r.randint(2, 120))) + "\n"


def valid(text):
    """题面只说“一段叠音后的歌曲音节”、用数字表示音节，未给规模与取值范围。
    这里只核格式：恰一行，至少一个音节，音节为非负整数，单空格分隔，换行结尾。"""
    import re
    return re.fullmatch(r'(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*\n', text) is not None

def _nested(r, depth):
    # 递归插入叠音，制造需要连续（级联）删除的输入
    if depth == 0:
        return [str(r.randint(1, 9))]
    out = []
    for _ in range(r.randint(1, 3)):
        part = _nested(r, depth - 1)
        if len(part) >= 2 and r.random() < 0.5:
            out += part[:2] + part[:2] + part[2:]
        elif r.random() < 0.5:
            out += part[:1] + part
        else:
            out += part
    return out

def extra_cases():
    cases = ['7\n', '3 3 3 3 3 3 3\n', '1 2 1 2 1 2 1 2 1 2 1 2\n', '1 2 2 1 2\n']
    r = random.Random(29694)
    for k in range(4):
        cases.append(" ".join(_nested(r, 6)) + "\n")
    cases.append(" ".join(str(r.randint(1, 3)) for _ in range(3000)) + "\n")
    return cases

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 31)] + extra_cases()
    for i, case in enumerate(cases):
        assert valid(case), i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
