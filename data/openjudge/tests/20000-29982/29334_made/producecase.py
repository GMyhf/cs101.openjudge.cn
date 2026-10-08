import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/29334/\n# Accepted submission: 52829500\n# Source: http://cs101.openjudge.cn/practice/solution/52829500/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef titleToNumber(columnTitle: str) -> int:\n    ans = 0\n    for char in columnTitle:\n        # 计算字符对应的数值 (A -> 1, B -> 2, ..., Z -> 26)\n        value = ord(char) - ord(\'A\') + 1\n        ans = ans * 26 + value\n    return ans\n\nif __name__ == "__main__":\n    # 读取标准输入\n    input_data = sys.stdin.read().split()\n    if input_data:\n        columnTitle = input_data[0]\n        print(titleToNumber(columnTitle))'
SAMPLE='A\n'
EXTRA_CASE=None
GENERATOR_NAME='g29334'
import re

def valid(text):
    """题面：1 <= len(columnTitle) <= 7，仅由大写英文组成，范围在 ["A", "FXSHRXW"] 内（FXSHRXW = 2147483647）。"""
    if not text.endswith('\n'): return False
    L = text[:-1].split('\n')
    if len(L) != 1 or not re.fullmatch(r'[A-Z]{1,7}', L[0]): return False
    v = 0
    for c in L[0]: v = v * 26 + ord(c) - 64
    return v <= 2147483647

def _title(value):
    s = ""
    while value: value, rem = divmod(value - 1, 26); s = chr(65 + rem) + s
    return s + "\n"

def g29334(r):
    value = r.randint(1, 2_147_483_647); s = ""
    while value: value, rem = divmod(value - 1, 26); s = chr(65 + rem) + s
    return s + "\n"

def extra_cases():
    r = random.Random(293340)
    out = [t + "\n" for t in ["AB", "ZY", "Z", "AA", "AZ", "BA", "ZZ", "AAA", "ZZZ", "AAAA", "ZZZZZZ", "AAAAAAA", "FXSHRXW", "FXSHRXV", "FXSHRWZ", "EZZZZZZ"]]
    for length in range(1, 7):                                     # 每种长度各取一个随机值
        lo, hi = sum(26 ** k for k in range(length)), sum(26 ** k for k in range(1, length + 1))
        out.append(_title(r.randint(lo, hi)))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path(__file__).parent/'data'; d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    for c in extra_cases():
        if c not in cases: cases.append(c)
    for c in cases: assert valid(c), c
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
