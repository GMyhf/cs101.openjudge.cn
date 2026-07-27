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
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
