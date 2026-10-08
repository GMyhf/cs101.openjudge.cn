import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20722/\n# Accepted submission: 43080163\n# Source: http://cs101.openjudge.cn/practice/solution/43080163/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Mon Nov 13 16:59:14 2023\n\n@author: Lenovo\n"""\n\nimport re\nwhile True:\n    try:\n        s=input()\n        m="<([A-Za-z]{1,5})>(.*)</\\\\1>"\n        lst=re.findall(m,s)\n        v=0\n        if lst:\n            for i in lst:\n                s=i[1]\n                m=".<([A-Za-z]{1,5})>(.*?)</\\\\1>."\n                nlst=re.findall(m,s)\n                if nlst:\n                    for j in nlst:\n                        s=j[1]\n                        m="(\\d+)"\n                        result=re.findall(m,s)\n                        if result:\n                            for n in result:\n                                if n==\'0\' or (len(n)<5 and n[0]!=\'0\'):\n                                    print(n,end=" ")\n                                    v=1\n        if v==1:\n            print("")\n        else:\n            print("NONE")\n    except:\n        break'
SAMPLE='bac<x><a>bb123<c>aaa 292 bbb 384 j 67477 0 dd 04 05hd</c>c12c</a></y>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</x></y>k</x>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</y>k</x>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</y></x>def\nk<a>1<c>12 35</c>78</c></a></a><abcdefg>d<y>3 4</y></abcdefg>def\nk<a>1<c>12 35</a>78</a></c></B><x>d<y>3 4</y></x>def\n'
GENERATOR_NAME='g20722'
def g20722(r):
    nums = [str(r.choice([0, r.randint(1, 9999)])) for _ in range(r.randint(1, 6))]
    good = "x<a>" + " ".join(nums) + "<b>" + str(r.randint(1, 9999)) + "</b>z</a>y"
    bad = "plain text" if r.random() < .35 else "<a>12 <b>345</b></a>"
    return good + "\n" + bad + "\n"

def valid(text):
    """题面输入只说「若干行」，并保证一个 tag 内部最多只有一个 tag（该结构保证难以一般化校验，不核）。
    这里只核格式：至少一行、以换行结尾、每行非空、只含可打印 ASCII。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    return len(lines) >= 1 and all(line and all(" " <= c <= "~" for c in line) for line in lines)


ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _name(r, avoid=()):
    while True:
        x = "".join(r.choice(ALPHA) for _ in range(r.randint(1, 5)))
        if x not in avoid:
            return x


def _filler(r, lo=1, hi=8, digits=True):
    """不含 <、> 的普通文本；digits=True 时可夹带数字（位于 B 之外，不应输出）。"""
    pool = ALPHA + " " + ("0123456789" if digits else "")
    return "".join(r.choice(pool) for _ in range(r.randint(lo, hi)))


def _body(r):
    """生成内重 tag 的内容 B，同时返回应输出的整数列表。"""
    parts, want = [], []
    for _ in range(r.randint(1, 8)):
        kind = r.random()
        if kind < .45:
            v = str(r.choice([0, r.randint(1, 9), r.randint(10, 99), r.randint(100, 999), r.randint(1000, 9999)]))
            want.append(v)
        elif kind < .6:
            v = str(r.randint(10000, 99999999))                 # 超过 4 位
        elif kind < .8:
            v = "0" * r.randint(1, 3) + str(r.randint(0, 999))  # 前导 0（含 00、0007）
            if v == "0":
                v = "00"
        else:
            v = None
        if v is not None:
            parts.append(v)
        parts.append(r.choice([" ", "  ", r.choice(ALPHA), r.choice(ALPHA) + " ", " ab "]))
    if r.random() < .5:
        parts.insert(0, r.choice(ALPHA + " "))
    return "".join(parts), want


def _line(r):
    """返回 (行, 期望输出的整数列表)；None 表示应输出 NONE。"""
    X = _name(r); Y = _name(r, (X,))
    B, want = _body(r)
    P = _filler(r, 0, 6); Q = _filler(r, 0, 6)
    A = _filler(r); C = _filler(r)
    kind = r.random()
    if kind < .55:                                           # 合法双重 tag
        return f"{P}<{X}>{A}<{Y}>{B}</{Y}>{C}</{X}>{Q}", (want or None)
    if kind < .63:                                           # 只有单层 tag
        return f"{P}<{X}>{B}</{X}>{Q}", None
    if kind < .71:                                           # A 为空，不构成双重 tag
        return f"{P}<{X}><{Y}>{B}</{Y}>{C}</{X}>{Q}", None
    if kind < .79:                                           # C 为空，不构成双重 tag
        return f"{P}<{X}>{A}<{Y}>{B}</{Y}></{X}>{Q}", None
    if kind < .86:                                           # 外层名字超过 5 个字母
        X6 = X + "".join(r.choice(ALPHA) for _ in range(6 - len(X)))
        return f"{P}<{X6}>{A}<{Y}>{B}</{Y}>{C}</{X6}>{Q}", None
    if kind < .93:                                           # 内层闭合名不匹配
        Z = _name(r, (X, Y))
        return f"{P}<{X}>{A}<{Y}>{B}</{Z}>{C}</{X}>{Q}", None
    return _filler(r, 1, 30), None                           # 完全没有 tag


def extra_cases():
    """补充：原 39 组都是同一个两行模板（名字固定 a/b，B 里只有一个 1..9999），
    没有前导 0、超过 4 位、多行、tag 名大小写/长度变化、A/C 为空等情况。"""
    r = random.Random(20722)
    out = []
    for lines in [1, 1, 2, 3, 5, 8, 10, 20, 30, 50, 100, 200, 500, 1000, 2000]:
        rows = [_line(r) for _ in range(lines)]
        text = "\n".join(x for x, _ in rows) + "\n"
        out.append((text, [w for _, w in rows]))
    return out


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    extras = extra_cases()
    cases += [t for t, _ in extras]
    assert len(set(cases)) == len(cases)
    expect = {t: w for t, w in extras}
    for i,c in enumerate(cases):
        assert valid(c), i
        res = run(c)
        if c in expect:  # 构造时已知答案，独立核对参考解
            got = [line.split() for line in res.split("\n")[:-1]]
            assert got == [w if w else ["NONE"] for w in expect[c]], i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(res)
if __name__=='__main__': main()
