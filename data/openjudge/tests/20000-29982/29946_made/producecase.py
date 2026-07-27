import random
REFERENCE="# External reference: /practice/29946/statistics/\n# Accepted submission: 52733385\n# Source: http://cs101.openjudge.cn/practice/solution/52733385/\n# License: not declared on the submission page; no license is inferred.\n\ns = input().strip()\nk = int(input())\n\nstack = []\nfor c in s:\n    # 还能删，且栈顶比当前大，就删栈顶\n    while k > 0 and stack and stack[-1] > c:\n        stack.pop()\n        k -= 1\n    stack.append(c)\n\n# 如果还剩删除次数，从末尾删\nif k > 0:\n    stack = stack[:-k]\n\n# 去掉前导零\nres = ''.join(stack).lstrip('0')\n\n# 全零情况输出 0\nprint(res if res else '0')"
SAMPLE='175438 \n4\n'
GENERATOR_NAME='g29946'
def g29946(r):
    n = r.randint(1, 100); s = str(r.randint(1, 9)) + "".join(str(r.randint(0, 9)) for _ in range(n - 1)); return f"{s}\n{r.randint(0, n - 1)}\n"

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
