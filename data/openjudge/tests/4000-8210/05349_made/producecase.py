import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "n=int(input())\nstrings=[]\nfor i in range(n):\n    strings.append(input())\nstan=input().upper().split('[')\nx=stan[1].split(']')\nstan[1]=x[0]\nstan.append(x[1])\nm=len(stan[0])\nn=len(stan[2])\nans=[]\ni=0\nfor s in strings:\n    S=s.upper()\n    if S[:m]==stan[0] and S[len(s)-n:]==stan[2] and S[m:len(s)-n] in stan[1] and len(s)==m+n+1:\n        ans.append((i+1,s))\n    i+=1\nfor a,s in ans:\n    print(a,s)"
SAMPLE = '4\nAab\na2B\nab\nABB\na[a2b]b\n'
GENERATOR_NAME = 'g5349'
def g5349(r):
    p,m,s=r.choice(["A","ab","Xy"]),r.choice(["a2","Q","0Z"]),r.choice(["b","T","9"])
    z=[p+r.choice([m,"bad",""])+s for _ in range(r.randint(3,8))]+["wrong",p+s]
    return f"{len(z)}\n"+"\n".join(z)+f"\n{p}[{m}]{s}\n"

ALNUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def _alnum(s):
    return all(c in ALNUM for c in s)


def valid(text):
    """题面：第一行整数 n（1<=n<=50）；中间 n 行作业字符串，长度小于 50，只含数字和字母；
    最后一行是模板「前缀[字符集]后缀」（与样例同形：恰一对方括号，括号内非空，其余为数字字母）。"""
    lines = text.split("\n")
    if len(lines) < 4 or lines[-1] != "":
        return False
    lines = lines[:-1]
    if not lines[0].isdigit() or not 1 <= int(lines[0]) <= 50 or len(lines) != int(lines[0]) + 2:
        return False
    if not all(1 <= len(s) < 50 and _alnum(s) for s in lines[1:-1]):
        return False
    t = lines[-1]
    if t.count("[") != 1 or t.count("]") != 1:
        return False
    a, rest = t.split("[")
    mid, b = rest.split("]")
    return bool(mid) and _alnum(a + mid + b)


def _rand_word(r, k):
    return "".join(r.choice(ALNUM) for _ in range(k))


def _flip(r, s):
    return "".join(c.swapcase() if r.random() < .5 else c for c in s)


def g5349_big(r):
    """加强组：前后缀长度 0~24（含空前缀/空后缀）、大小写混排、长度差一、括号外字符错一位、n 取到 50。"""
    pre = _rand_word(r, r.choice([0, 0, 1, 3, 10, 24]))
    suf = _rand_word(r, r.choice([0, 0, 1, 4, 12, 24]))
    mid = "".join(r.sample(ALNUM, r.randint(1, 8)))
    n = r.choice([1, 50, 50, r.randint(2, 49)])
    others = [c for c in ALNUM if c.lower() not in mid.lower()]
    rows = []
    for _ in range(n):
        kind = r.randrange(7)
        if kind <= 2:
            s = _flip(r, pre + r.choice(mid) + suf)                      # 合格
        elif kind == 3:
            s = _flip(r, pre + r.choice(others) + suf)                   # 中间字符不在集合里
        elif kind == 4:
            s = _flip(r, pre + "".join(r.choice(mid) for _ in range(r.choice([0, 2]))) + suf)  # 长度差一
        elif kind == 5 and pre + suf:
            body = list(pre + r.choice(mid) + suf)
            j = r.choice([i for i in range(len(body)) if i != len(pre)])
            body[j] = r.choice([c for c in ALNUM if c.lower() != body[j].lower()])
            s = _flip(r, "".join(body))                                  # 括号外错一位
        else:
            s = _rand_word(r, r.randint(1, 49))
        rows.append(s[:49] or "0")
    if not any(re.fullmatch(re.escape(pre) + "[" + mid + "]" + re.escape(suf), x, re.I) for x in rows):
        rows[r.randrange(n)] = _flip(r, pre + r.choice(mid) + suf)  # 至少一行合格，避免空输出
    return f"{n}\n" + "\n".join(rows) + f"\n{pre}[{mid}]{suf}\n"


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=[g5349_big(random.Random(534900+seed)) for seed in range(20)]
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复组"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
