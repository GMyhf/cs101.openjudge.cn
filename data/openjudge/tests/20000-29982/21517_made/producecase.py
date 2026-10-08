import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21517/\n# Accepted submission: 52740168\n# Source: http://cs101.openjudge.cn/practice/solution/52740168/\n# License: not declared on the submission page; no license is inferred.\n\ndef main():\n    import sys\n    from collections import defaultdict\n    input = sys.stdin.read().split()\n    ptr = 0\n    N = int(input[ptr])\n    ptr += 1\n    \n    strs = []\n    for _ in range(N):\n        M = int(input[ptr])\n        ptr += 1\n        a = list(map(int, input[ptr:ptr+M]))\n        ptr += M\n        # 生成差分序列\n        diff = []\n        for i in range(M-1):\n            diff.append(str(a[i+1] - a[i]))\n        strs.append(diff)\n    \n    # 二分最长长度\n    l = 0\n    r = max(len(s) for s in strs)\n    ans = 0\n    \n    while l <= r:\n        mid = (l + r) // 2\n        if mid == 0:\n            ans = max(ans, 0)\n            l = mid + 1\n            continue\n        \n        cnt = defaultdict(int)\n        ok = False\n        \n        # 处理第一个串\n        s = strs[0]\n        se = set()\n        for i in range(len(s) - mid + 1):\n            sub = \',\'.join(s[i:i+mid])\n            se.add(sub)\n        for k in se:\n            cnt[k] += 1\n        \n        # 处理其他串\n        for idx in range(1, N):\n            s = strs[idx]\n            se = set()\n            for i in range(len(s) - mid + 1):\n                sub = \',\'.join(s[i:i+mid])\n                se.add(sub)\n            for k in se:\n                cnt[k] += 1\n        \n        # 检查是否有全部串都出现的子串\n        if N in cnt.values():\n            ok = True\n        \n        if ok:\n            ans = mid\n            l = mid + 1\n        else:\n            r = mid - 1\n    \n    print(ans + 1)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='2\n2 1 2\n3 4 5 9\n'
GENERATOR_NAME='g21517'
def valid(text):
    """题面：第一行 N；随后 N 行，每行首个数 M_i 后跟 M_i 个数。
    提示：40<=n<=1000，2<=M_i<=101，每个数在 [0,1864]。
    题面样例 N=2 与提示的 40<=n 矛盾，只对与样例逐字相同的输入放行 N<40。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        if lines[0] != lines[0].strip() or not re.fullmatch(r"\d+", lines[0]):
            return False
        n = int(lines[0])
        if not (40 <= n <= 1000 or (text == SAMPLE and n == 2)):
            return False
        if len(lines) != n + 1:
            return False
        for line in lines[1:]:
            toks = line.split(" ")
            if any(not re.fullmatch(r"\d+", t) for t in toks):
                return False
            m = int(toks[0])
            if not 2 <= m <= 101 or len(toks) != m + 1:
                return False
            if any(not 0 <= int(t) <= 1864 for t in toks[1:]):
                return False
    except (ValueError, IndexError):
        return False
    return True

LO, HI = 0, 1864

def _pattern(r, length, spread):
    """长度为 length 的值序列，相邻差在 [-spread, spread]，整体落在可平移的范围内。"""
    vals = [0]
    for _ in range(length - 1):
        vals.append(vals[-1] + r.randint(-spread, spread))
    mn = min(vals); vals = [v - mn for v in vals]
    assert max(vals) <= HI
    return vals

def _shifted(r, pat):
    """把模式整体平移一个随机常数（相同的定义：全部元素加上同一个数）。"""
    s = r.randint(LO, HI - max(pat))
    return [v + s for v in pat]

def _card(r, m, pats):
    """长度 m 的卡片，把 pats 中各模式（已平移）嵌入，其余随机填充。"""
    need = sum(len(p) for p in pats)
    assert need <= m
    filler = [r.randint(LO, HI) for _ in range(m - need)]
    pieces = [_shifted(r, p) for p in pats]
    r.shuffle(pieces)
    # 随机把填充数分到各模式之间
    cuts = sorted(r.randint(0, len(filler)) for _ in pieces)
    out, prev = [], 0
    for c, piece in zip(cuts, pieces):
        out += filler[prev:c] + piece; prev = c
    out += filler[prev:]
    return out

def g21517(r, s):
    kind = s % 8
    if s >= 36:
        n = 1000
    elif r.random() < 0.3:
        n = 40
    else:
        n = r.randint(40, 400)
    cards = []
    if kind == 0:
        # 纯随机大值域：几乎不会有公共差分，答案多为 1
        for _ in range(n):
            m = r.randint(2, 101)
            cards.append([r.randint(LO, HI) for _ in range(m)])
    elif kind == 1:
        # 小值域随机：偶然出现的公共子串，答案由参考解决定
        for _ in range(n):
            m = r.randint(60, 101)
            cards.append([r.randint(0, 2) for _ in range(m)])
    elif kind == 2:
        # 长公共模式 + 每张卡片平移不同常数（只比原值不比差分会错）
        L = r.randint(30, 101)
        pat = _pattern(r, L, 40)
        for _ in range(n):
            m = r.randint(L, 101)
            cards.append(_card(r, m, [pat]))
    elif kind == 3:
        # 公共模式 + 更长的诱饵模式（除一张外都有）
        L = r.randint(3, 20)
        pat = _pattern(r, L, 30)
        bait = _pattern(r, r.randint(L + 5, 60), 30)
        miss = r.randrange(n)
        for i in range(n):
            pats = [pat] if i == miss else [pat, bait]
            m = r.randint(sum(map(len, pats)), 101)
            cards.append(_card(r, m, pats))
    elif kind == 4:
        # 整张卡片就是模式（M_i 恰为 L），含负差分
        L = r.randint(2, 101)
        pat = _pattern(r, L, 15)
        for _ in range(n):
            cards.append(_shifted(r, pat))
    elif kind == 5:
        # 有一张 M_i=2 的卡片，限制答案 <=2
        pat = _pattern(r, r.randint(10, 50), 25)
        two = _pattern(r, 2, 25)
        for i in range(n):
            if i == 0:
                cards.append(_shifted(r, two))
            else:
                m = r.randint(len(pat) + 2, 101)
                cards.append(_card(r, m, [pat, two]))
        r.shuffle(cards)
    elif kind == 6:
        # 公共模式在同一张卡片里重复出现多次（按卡片计数，不能按出现次数）
        L = r.randint(4, 15)
        pat = _pattern(r, L, 20)
        longer = _pattern(r, L + 3, 20)
        for i in range(n):
            if i < n // 2:
                pats = [pat, longer, longer]
            else:
                pats = [pat, pat, pat]
            m = r.randint(sum(map(len, pats)), 101)
            cards.append(_card(r, m, pats))
        r.shuffle(cards)
    else:
        # 满长度 101：每张卡片都含若干共享模式，随机长度
        L = r.randint(5, 80)
        pat = _pattern(r, L, 50)
        for _ in range(n):
            cards.append(_card(r, 101, [pat]))
    rows = [" ".join(map(str, [len(c)] + c)) for c in cards]
    return f"{n}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g21517(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
