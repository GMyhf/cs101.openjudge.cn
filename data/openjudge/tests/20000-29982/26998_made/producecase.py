import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='import sys\ninput = sys.stdin.read\ndata = input().split()\n\nidx = 0\nT = int(data[idx])\nidx += 1\n\nfor _ in range(T):\n    n = int(data[idx])\n    idx += 1\n    a = list(map(int, data[idx:idx+n]))\n    idx += n\n    \n    dp = [0] * 32  # 0~31位足够\n    \n    for num in a:\n        if num == 0:\n            continue  # 0 & 任何数 =0，不能选\n        \n        # 收集所有为1的二进制位\n        bits = []\n        for b in range(32):\n            if num & (1 << b):\n                bits.append(b)\n        \n        # 当前能达到的最大长度\n        max_len = 0\n        for b in bits:\n            if dp[b] > max_len:\n                max_len = dp[b]\n        cur = max_len + 1\n        \n        # 更新所有位\n        for b in bits:\n            if cur > dp[b]:\n                dp[b] = cur\n    \n    print(max(dp))'
SAMPLE='2\n3\n1 2 3\n5\n1 10 100 1000 10000\n'
GENERATOR_NAME='g26998'
def valid(text):
    """题面：首行 T（T <= 100）；每组两行：n（n <= 100000），再一行 n 个正整数 ai（ai <= 1e9）。"""
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    def num(tok):
        return tok.isdigit() and (tok == "0" or tok[0] != "0")
    if not lines or not num(lines[0]):
        return False
    t = int(lines[0])
    if not (1 <= t <= 100) or len(lines) != 1 + 2 * t:
        return False
    for k in range(t):
        ln, la = lines[1 + 2 * k], lines[2 + 2 * k]
        if not num(ln):
            return False
        n = int(ln)
        if not (1 <= n <= 100000):
            return False
        tok = la.split(" ")
        if len(tok) != n or any(not num(x) or not (1 <= int(x) <= 10**9) for x in tok):
            return False
    return True

POW2 = [1 << b for b in range(30)]

def _val(r, kind, hi_bit=29):
    if kind == "pow2":  # 单个二进制位，答案取决于同一位出现次数
        return 1 << r.randint(0, hi_bit)
    if kind == "two":  # 两个二进制位，形成链式转移
        x = (1 << r.randint(0, hi_bit)) | (1 << r.randint(0, hi_bit))
        return x
    if kind == "small":
        return r.randint(1, 15)
    if kind == "big":
        return r.choice([10**9, r.randint(10**9 - 1000, 10**9), r.randint(1, 10**9)])
    return _val(r, r.choice(["pow2", "two", "small", "big"]), hi_bit)

def _case(r, t, nlo, nhi, kinds, hi_bit=29):
    rows = [str(t)]
    for _ in range(t):
        n = r.randint(nlo, nhi); kind = r.choice(kinds)
        rows += [str(n), " ".join(str(_val(r, kind, hi_bit)) for _ in range(n))]
    return "\n".join(rows) + "\n"

def g26998(r, s):
    allk = ["pow2", "two", "small", "big", "mix"]
    if s <= 12:  # 小规模，便于暴力核对
        return _case(r, r.randint(1, 100), 1, 10, allk, r.choice([2, 4, 29]))
    if s == 13:  # 最小：每组 n=1
        return _case(r, 100, 1, 1, allk)
    if s <= 20:  # 中等规模
        return _case(r, r.randint(1, 10), 100, 3000, allk, r.choice([3, 8, 29]))
    if s == 21:  # T 满 100，总长 1e5
        return _case(r, 100, 1000, 1000, allk)
    if s == 22:  # 值取上限 1e9 附近
        return _case(r, 1, 80000, 80000, ["big"])
    if s <= 34:  # 单组 n = 1e5，稀疏位，卡 O(n^2) 与贪心
        kinds = [["pow2"], ["two"], ["mix"], ["small"]][s % 4]
        return _case(r, 1, 100000, 100000, kinds, r.choice([5, 12, 19]))
    return _case(r, r.randint(1, 5), 1, 20000, allk, r.choice([6, 29]))

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
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
