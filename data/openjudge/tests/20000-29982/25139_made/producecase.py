import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='from itertools import permutations\n\nt = int(input())\n\nfor _ in range(t):\n    s1, s2, s3 = input().split()\n\n    letters = sorted(set(s1 + s2 + s3))\n\n    # 需要非零的字母\n    lead = set()\n    if len(s1) > 1:\n        lead.add(s1[0])\n    if len(s2) > 1:\n        lead.add(s2[0])\n    if len(s3) > 1:\n        lead.add(s3[0])\n\n    found = False\n\n    def dfs(idx, mp, used):\n        global found\n\n        if idx == len(letters):\n            a = int("".join(str(mp[ch]) for ch in s1))\n            b = int("".join(str(mp[ch]) for ch in s2))\n            c = int("".join(str(mp[ch]) for ch in s3))\n\n            if a + b == c:\n                print(f"{a}+{b}={c}")\n                return True\n            return False\n\n        ch = letters[idx]\n\n        for d in range(10):\n            if d in used:\n                continue\n\n            if d == 0 and ch in lead:\n                continue\n\n            mp[ch] = d\n            used.add(d)\n\n            if dfs(idx + 1, mp, used):\n                return True\n\n            used.remove(d)\n            del mp[ch]\n\n        return False\n\n    found = dfs(0, {}, set())\n\n    if not found:\n        print("No Solution")'
SAMPLE='5\nA A B\nAA AA AAA\nAB ABC ACDD\nA A BC\nABCD BCD ACEA\n'
GENERATOR_NAME='g25139'
def g25139(r):
    letters = list("ABCDE")
    def word(): return "".join(r.choice(letters[:r.randint(2, 5)]) for _ in range(r.randint(1, 6)))
    a, b = word(), word(); c = word()
    known = r.choice(["A A BC", "ABCD BCD ACEA", "A A B"])
    return f"3\nA A BC\n{a} {b} {c}\n{known}\n"

def valid(text):
    """题面：首行整数 n；接下来 n 行，每行三个空格分隔的字符串 s1 s2 s3，长度至多 10，只含 'A'-'E'。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if n < 1 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        t = line.split(" ")
        if len(t) != 3:
            return False
        if not all(1 <= len(w) <= 10 and set(w) <= set("ABCDE") for w in t):
            return False
    return True


def _solvable_eq(r):
    """先定字母到数字的映射，再造出必有解的等式（解未必是最小解，最小解由参考解求）。"""
    while True:
        k = r.randint(2, 5)
        letters = "ABCDE"[:k]
        digits = r.sample(range(10), k)
        mp = dict(zip(letters, digits)); inv = {d: ch for ch, d in mp.items()}
        la, lb = r.randint(1, 9), r.randint(1, 9)
        w1 = "".join(r.choice(letters) for _ in range(la)); w2 = "".join(r.choice(letters) for _ in range(lb))
        if (len(w1) > 1 and mp[w1[0]] == 0) or (len(w2) > 1 and mp[w2[0]] == 0):
            continue
        c = str(int("".join(str(mp[x]) for x in w1)) + int("".join(str(mp[x]) for x in w2)))
        if len(c) <= 10 and all(int(d) in inv for d in c):
            return f"{w1} {w2} {''.join(inv[int(d)] for d in c)}"


def _random_eq(r, maxlen):
    w = lambda: "".join(r.choice("ABCDE") for _ in range(r.randint(1, maxlen)))
    return f"{w()} {w()} {w()}"


def extra_cases():
    """补充：有解等式（原数据随机等式全是 No Solution）、长度 10、最小解比较、单个 0 合法、多解取最小。"""
    r = random.Random(251390)
    fmt = lambda eqs: f"{len(eqs)}\n" + "\n".join(eqs) + "\n"
    cases = []
    for _ in range(4):
        cases.append(fmt([_solvable_eq(r) for _ in range(20)]))
    mix = []
    for _ in range(20):
        mix.append(_solvable_eq(r) if r.random() < .5 else _random_eq(r, 10))
    cases.append(fmt(mix))
    cases.append(fmt([
        "ABC ACDE DCABC",                       # 题面描述中的等式形式
        "A B C",                                 # 多解取最小：1+2=3
        "B A B",                                 # 单个字母可为 0，A 最小取 0：1+0=1
        "A B A",
        "AB A AB",                               # A 只能为 0 但是前导 -> No Solution
        "D E DE",                                # 不含 A-C 的字母
        "AAAAAAAAAA AAAAAAAAAA BBBBBBBBBB",      # 长度 10
        "EDCBAEDCBA ABCDEABCDE AAAAAAAAAA",
        "A A A",                                 # 只能 0+0=0
        "AB BA CC",
        "ABCDE ABCDE ABCDE",
        "E E AB",
    ]))
    cases.append(fmt(["ABCDEABCDE EDCBAEDCBA AAAAAAAAAA"] + [_random_eq(r, 10) for _ in range(19)]))
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
