import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：若干块；块首行 n（0 < n ≤ 200），次行 n 个两两不同的 1..n；
    之后每行「k 空格 消息」（消息为 ASCII、长度 ≤ n），以单独一行 0 结束本块；最后一块后单独一行 0。
    k 题面未给上界，按正整数且不超过 32 位有符号范围核。消息只收可打印 ASCII（不含行尾）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'(0|[1-9][0-9]*)$')
    i = 0; blocks = 0
    while True:
        if i >= len(lines) or not num.match(lines[i]):
            return False
        n = int(lines[i]); i += 1
        if n == 0:
            return i == len(lines) and blocks >= 1
        if n > 200 or i >= len(lines):
            return False
        key = lines[i].split(' '); i += 1
        if len(key) != n or not all(num.match(x) for x in key) or sorted(map(int, key)) != list(range(1, n + 1)):
            return False
        while True:
            if i >= len(lines):
                return False
            line = lines[i]; i += 1
            if line == '0':
                break
            m = re.match(r'([1-9][0-9]*) (.*)$', line, re.S)
            if not m or int(m.group(1)) > 2147483647:
                return False
            msg = m.group(2)
            if not 1 <= len(msg) <= n or not all(32 <= ord(ch) <= 126 for ch in msg):
                return False
        blocks += 1
_CHARS = ''.join(chr(c) for c in range(33, 127))
def _key(r, n, kind):
    if kind == 'identity':
        return list(range(1, n + 1))
    if kind == 'cycle':                      # 一个长为 n 的大环
        order = list(range(1, n + 1)); r.shuffle(order)
        key = [0] * n
        for i in range(n):
            key[order[i] - 1] = order[(i + 1) % n]
        return key
    if kind == 'coprime':                    # 若干互素长度的环，整体周期很大
        lens = []; left = n
        for L in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
            if L <= left:
                lens.append(L); left -= L
        lens += [1] * left
        order = list(range(1, n + 1)); r.shuffle(order); key = [0] * n; p = 0
        for L in lens:
            cyc = order[p:p + L]; p += L
            for i in range(L):
                key[cyc[i] - 1] = cyc[(i + 1) % L]
        return key
    key = list(range(1, n + 1)); r.shuffle(key); return key
def _msg(r, n):
    L = r.choice([1, n, n, r.randint(1, n), r.randint(1, n)])
    s = [r.choice(_CHARS) if r.random() < 0.8 else ' ' for _ in range(L)]
    s[0] = r.choice(_CHARS)                  # 消息不以空格开头（与「k 空格 消息」的分隔不混淆）
    return ''.join(s)
def _k(r):
    return r.choice([1, 2, r.randint(1, 10), r.randint(1, 1000), r.randint(1, 10 ** 6),
                     r.randint(10 ** 8, 2147483647), 2147483647])
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    blocks = []
    if seed == 1:
        blocks = [(1, [1], [(1, 'a'), (2147483647, 'Z')]),
                  (2, [2, 1], [(1, 'ab'), (2, 'ab'), (3, 'a'), (2147483647, 'xy')]),
                  (3, [1, 2, 3], [(5, 'abc'), (1, 'a')])]
    else:
        big = seed >= 25
        for _ in range(r.randint(1, 3) if big else r.randint(1, 6)):
            n = r.randint(150, 200) if big else r.randint(1, 30)
            if seed in (25, 26):
                n = 200
            kind = r.choice(['random', 'random', 'cycle', 'coprime', 'identity'])
            key = _key(r, n, kind)
            m = r.randint(20, 60) if big else r.randint(1, 15)
            blocks.append((n, key, [(_k(r), _msg(r, n)) for _ in range(m)]))
    out = []
    for n, key, msgs in blocks:
        out.append(str(n)); out.append(' '.join(map(str, key)))
        out += [f'{k} {m}' for k, m in msgs]; out.append('0')
    return '\n'.join(out) + '\n0\n'
REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1026: Cipher\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01026/\n# License: not declared; no license is inferred.\nimport sys\ndef move(st, t, a):\n    for i in range(t):\n        st = a[st]\n    return st\n\n\n# 计算周期，即加密多少次后导致的效果是相同的\ndef find_cir(a, n):\n    ret = []    # 保存每个位置的周期，即循环节\n    for i in range(n):\n        x = a[i]\n        cnt = 1\n        while (x != i):\n            x = a[x]\n            cnt += 1\n        ret.append(cnt)\n    return ret\n\n\nwhile (1):\n    n = int(input())\n    if (n == 0):\n        break\n    a = list(map(int, input().split()))\n    for i in range(n):\n        a[i] -= 1\n    cir = find_cir(a, n)\n\n    while (1):\n        st = input().split(' ', 1)\n        k = int(st[0])\n        if (k == 0):\n            break\n        st = list(st[1])\n        while (len(st) < n):\n            st.append(' ')\n        ans = [''] * n\n        for i in range(n):\n            # 取模省略了之前的多次不必要计算\n            ans[move(i, k % cir[i], a)] = st[i]\n        print(''.join(ans))\n    print()\n"
NUMBER=1026
SAMPLE='10\n4 5 3 7 2 8 1 6 10 9\n1 Hello Bob\n1995 CERC\n0\n0\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
