import random
REFERENCE="# External reference: /practice/29739/statistics/\n# Accepted submission: 52298393\n# Source: http://cs101.openjudge.cn/practice/solution/52298393/\n# License: not declared on the submission page; no license is inferred.\n\nS=input()\nT=input()\nn=len(T)\npos1=0\nallzero=False\nwhile T[pos1]=='0':\n    pos1+=1\n    if pos1>=n:\n        allzero=True\n        break\nif allzero:\n    for i in 'abcdefghijklmnopqrstuvwxyz':\n        if i not in S:\n            print(i)\n            exit()\n    else:\n        print('a'*(n+1))\n        exit()\ntarget=S[pos1:]+'#'+S\nn=len(target)\nZ=[0]*n\nZ[0]=n\nleft=0\nright=0\nfor i in range(1,n):\n    if i>right: #那么开始暴力匹配\n        ptr=0\n        while ptr<n-i and target[ptr]==target[ptr+i]:\n            ptr+=1\n        Z[i]=ptr #暴力匹配好了，更新Z[i]\n        if ptr>0: #如果有效，那么更新安全区\n            left=i\n            right=i+ptr-1\n    elif i<=right: #看来我们有经验，无需暴力匹配\n        tmp=Z[i-left]\n        if i+tmp<right:\n            Z[i]=tmp\n        else: #于是，从i出发，到right截止的所有内容全部完成匹配，相当于Z[i]至少是right-i+1.于是我们要从S[right-i+1]开始比较起\n            ptr=right\n            while ptr<n and target[ptr]==target[ptr-i]:\n                ptr+=1\n            Z[i]=ptr-i\n            if ptr>i:\n                left=i\n                right=ptr-1\nmaxlen=float('inf')\nminlen=0\nnn=len(T)\nfor i,char in enumerate(T):\n    if char=='0':\n        minlen=max(minlen,Z[i+(nn-pos1)+1])\n    elif char=='1':\n        maxlen=min(maxlen,Z[i+(nn-pos1)+1])\nif minlen>=maxlen:\n    print(-1)\nelse:\n    print(S[pos1:pos1+minlen+1])\n\n\n\n\n"
SAMPLE='baaababaab\n0001010000\n'
GENERATOR_NAME='g29739'

def valid(text):
    """题面契约：第一行 S 仅含小写字母，1<=|S|<=10^6；第二行 P 为与 S 等长的 01 串。"""
    import re
    m = re.fullmatch(r'([a-z]+)\n([01]+)\n', text)
    return bool(m) and len(m.group(1)) == len(m.group(2)) <= 10 ** 6

LET = "abcdefghijklmnopqrstuvwxyz"

def _p_of(s, t):
    # 由真实的 T 生成掩码 P
    occ = bytearray(b'0' * len(s)); i = s.find(t)
    while i != -1:
        occ[i] = 49; i = s.find(t, i + 1)
    return occ.decode()

def _rand(r, n, k):
    return "".join(r.choice(LET[:k]) for _ in range(n))

def _fib(n):
    a, b = "b", "a"
    while len(b) < n:
        a, b = b, b + a
    return b[:n]

def _planted(r, s, lo, hi):
    L = r.randint(lo, min(hi, len(s))); st = r.randint(0, len(s) - L)
    return s + "\n" + _p_of(s, s[st:st + L]) + "\n"

def _flipped(r, s, lo, hi):
    L = r.randint(lo, min(hi, len(s))); st = r.randint(0, len(s) - L)
    p = list(_p_of(s, s[st:st + L])); j = r.randrange(len(s))
    p[j] = '1' if p[j] == '0' else '0'
    return s + "\n" + "".join(p) + "\n"

BIG = 500000  # .in 需 <= 1MB，S 与 P 共约 2|S| 字节

def g29739(r, idx):
    if idx == 1: return "a\n1\n"
    if idx == 2: return "a\n0\n"
    if idx == 3: return "zqjzqj\n000000\n"        # 题面样例 2
    if idx == 4: return "zqjzqj\n100001\n"        # 题面样例 3 -> -1
    if idx == 5: return LET + "\n" + "0" * 26 + "\n"   # 全字母出现、P 全 0
    if idx == 6: return "ab\n11\n"               # 无解：T 须以 a 开头又须从 b 开始出现
    if idx <= 15: return _planted(r, _rand(r, r.randint(1, 30), r.randint(1, 3)), 1, 10)
    if idx <= 20: return _flipped(r, _rand(r, r.randint(2, 30), r.randint(1, 3)), 1, 10)
    if idx == 21: return (lambda s: s + "\n" + "0" * len(s) + "\n")(_rand(r, 40, 3))
    if idx == 22: return (lambda s: s + "\n" + "0" * len(s) + "\n")(LET * 3 + _rand(r, 20, 26))
    n = BIG if idx in (23, 24, 30) else 100000  # 只留 3 组满规模，控制总体积
    if idx == 23: return _planted(r, _rand(r, n, 26), 5, 12)
    if idx == 24:  # 全 a，答案长度约 n/2，卡逐长度暴力
        L = n // 2; s = "a" * n
        return s + "\n" + "1" * (n - L + 1) + "0" * (L - 1) + "\n"
    if idx == 25:
        s = ("ab" * n)[:n]; return s + "\n" + _p_of(s, "ab" * 1000 + "a") + "\n"
    if idx == 26: return _planted(r, _rand(r, n, 2), 15, 30)
    if idx == 27: return _flipped(r, ("abc" * n)[:n], 3, 3000)
    if idx == 28: return (lambda s: s + "\n" + "0" * n + "\n")(LET + _rand(r, n - 26, 26))
    if idx == 29: return (lambda s: s + "\n" + "0" * n + "\n")(_rand(r, n, 26).replace("m", "n"))
    if idx == 30:
        s = _fib(n); return s + "\n" + _p_of(s, s[1000:1000 + 50000]) + "\n"
    if idx == 31:  # 只有一个 '1' 且在最后一位
        s = _rand(r, n, 3); return s + "\n" + "0" * (n - 1) + "1" + "\n"
    if idx == 32:  # 全 a，P 全 1 -> 'a'
        return "a" * n + "\n" + "1" * n + "\n"
    if idx == 33:  # 全 a，P 全 0 -> 'b'
        return "a" * n + "\n" + "0" * n + "\n"
    if idx == 34: return _flipped(r, _fib(n), 100, 5000)
    m = r.randint(1000, 100000)
    if idx == 35: return _planted(r, _rand(r, m, 2), 1, 60)
    if idx == 36: return _flipped(r, _rand(r, m, 2), 1, 8)
    if idx == 37: return _planted(r, ("aab" * m)[:m], 50, 500)
    if idx == 38: return _planted(r, _fib(m), 1, 3000)
    return _planted(r, _rand(r, m, 4), 1, 6)

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i, case in enumerate(cases):
        assert valid(case), i
        assert len(case) <= 1 << 20, i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
