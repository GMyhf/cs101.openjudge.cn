import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20074 statistics, Accepted solution 51318992.\n# Source: http://cs101.openjudge.cn/practice/solution/51318992/\n# Statistics: http://cs101.openjudge.cn/practice/20074/statistics/\n# License: not declared on submission page; no license inferred\nn = int(input())\nMan, Woman = 0, 0\nfor _ in range(n):\n    h, w, s = input().split()\n    min_w = 18.5*(float(h)/100)**2\n    max_w = 24.9*(float(h)/100)**2\n    cur_w = float(w)\n    num = 0\n    while cur_w < min_w or cur_w > max_w:\n        if cur_w < min_w:\n            cur_w += 8\n        elif cur_w > max_w:\n            cur_w -= 5\n        num += 1\n    if s == 'M':\n        Man = max(Man, num)\n    elif s == 'F':\n        Woman = max(Woman, num)\nprint(int(Man), int(Woman))\n"
SAMPLE='2\n170 75 M \n165 45 F\n'
GENERATOR_NAME='g20074'
from fractions import Fraction


def valid(text):
    """题面：第一行 n（1<=n<=12），其后 n 行 "h w s"，150<=h<=190，45<=w<=100，s 为 M 或 F。
    （样例第一行学生信息带行尾空格，按 token 校验，行尾空白放行。）"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 1 <= n <= 12 or len(lines) != n + 1:
        return False
    for row in lines[1:]:
        tok = row.rstrip(" ").split(" ")
        if len(tok) != 3 or not tok[0].isdigit() or not tok[1].isdigit():
            return False
        h, w, sex = int(tok[0]), int(tok[1]), tok[2]
        if not (150 <= h <= 190 and 45 <= w <= 100 and sex in ("M", "F")):
            return False
    return True


def ambiguous(h, w):
    """题面"正常 18.5-24.9、超重 >25"在 (24.9, 25] 留了空档：
    轨迹上任一步 BMI 落进空档，答案就取决于空档怎么算。生成时避开这类学生。"""
    w = Fraction(w)
    hh = Fraction(h, 100) ** 2
    while True:
        b = w / hh
        if Fraction(249, 10) < b <= 25:
            return True
        if b < Fraction(37, 2):
            w += 8
        elif b > Fraction(249, 10):
            w -= 5
        else:
            return False


def _row(r):
    while True:
        h, w = r.randint(150, 190), r.randint(45, 100)
        if not ambiguous(h, w):
            return f"{h} {w} {r.choice(['M', 'F'])}"


def g20074(r):
    n = r.randint(1, 12)
    rows = [_row(r) for _ in range(n)]
    return f"{n}\n" + "\n".join(rows) + "\n"


def _fixed(rows):
    assert all(not ambiguous(int(x.split()[0]), int(x.split()[1])) for x in rows)
    return f"{len(rows)}\n" + "\n".join(rows) + "\n"


# 手工边界：最多月数（矮且最重 / 高且最轻）、单人、只有一种性别、全部正常、满 n=12
EXTRA = [
    "2\n180 65 M\n187 53 M\n",                       # 题面样例 2（只有男生）
    _fixed(["150 100 M"]),
    _fixed(["190 45 F"]),
    _fixed(["150 100 F", "190 45 M"]),
    _fixed(["170 60 F", "160 55 M", "180 70 F"]),      # 全部正常 -> 0 0
    _fixed(["150 100 M", "151 100 M", "152 99 M", "190 45 M", "189 46 M", "188 45 M",
            "150 100 F", "151 99 F", "190 45 F", "189 45 F", "153 98 F", "155 97 F"]),
    _fixed(["190 45 F"] * 12),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases += EXTRA
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
