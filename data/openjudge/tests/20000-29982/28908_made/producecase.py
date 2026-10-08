import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/28908/\n# Accepted submission: 52734356\n# Source: http://cs101.openjudge.cn/practice/solution/52734356/\n# License: not declared on the submission page; no license is inferred.\n\n# 初始化变量\na = b = c = 0\ns = input().strip()\n\n# 按分号分割语句\nstatements = s.split(';')\nfor stmt in statements:\n    stmt = stmt.strip()\n    if not stmt:\n        continue\n    # 提取变量和值\n    var = stmt[0]       # 第一个字符是变量名\n    num = stmt[-1]     # 最后一个字符是数字\n    # 赋值\n    if var == 'a':\n        a = int(num)\n    elif var == 'b':\n        b = int(num)\n    elif var == 'c':\n        c = int(num)\n\n# 输出结果\nprint(a, b, c)"
SAMPLE='a:=3;b:=4;c:=5;\n'
EXTRA_CASE=None
GENERATOR_NAME='g28908'
def g28908(r):
    rows = []
    for _ in range(r.randint(1, 3)): rows.append(f"{r.choice('abc')}:={r.randint(0,9)};")
    return "".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
import re


def valid(text):
    """题面契约：一行，1-3 句 [变量]:=[一位整数]; ，变量只有 a/b/c，总长不超过 255。"""
    if not text.endswith("\n") or text.count("\n") != 1 or len(text) - 1 > 255:
        return False
    return re.fullmatch(r"(?:[abc]:=[0-9];){1,3}", text[:-1]) is not None


# 追加：题面样例 2、倒序赋值（按 a,b,c 位置硬取会错）、全 9、全 0、同变量连写三次
EXTRA_CASES=['a:=3;b:=4;\n', 'c:=1;b:=2;a:=3;\n', 'a:=9;b:=9;c:=9;\n', 'c:=0;b:=0;a:=0;\n', 'c:=7;c:=0;c:=4;\n', 'b:=5;a:=1;b:=0;\n']


def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+EXTRA_CASES
    seed=1
    while len(cases) < 46:  # 随机组去重（原先 39 组里有 4 组与别组重复）
        c=globals()[GENERATOR_NAME](random.Random(seed)); seed+=1
        if c not in cases: cases.append(c)
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
