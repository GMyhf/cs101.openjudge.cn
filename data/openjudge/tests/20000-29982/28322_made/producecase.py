# 28322 小明的加密算法 测试数据生成器
# 用法：在本目录下 python3 producecase.py；答案由同目录 samplecode.py 生成。
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '2\nencrypt\nabcde\ndecrypt\nbadc\n'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
EVEN = [c for c in LOWER if (ord(c) - 96) % 2 == 0]
ODD = [c for c in LOWER if (ord(c) - 96) % 2 == 1]


def _even(c):
    return (ord(c) - 96) % 2 == 0


def enc(s):
    stack, out = [], []
    for c in s:
        stack.append(c)
        if _even(c):
            out += stack[::-1]
            stack.clear()
    if stack:
        out += ['0'] + stack[::-1]
    return ''.join(out)


def dec(t):
    """按密文结构直接拆段还原明文；结构不合法返回 None。"""
    head, tail = t, ''
    if '0' in t:
        k = t.index('0')
        head, tail = t[:k], t[k + 1:]
        if not tail or '0' in tail or any(_even(c) for c in tail):
            return None
    if head and not _even(head[0]):
        return None
    segs, cur = [], ''
    for c in head:
        if _even(c) and cur:
            segs.append(cur)
            cur = ''
        cur += c
    if cur:
        segs.append(cur)
    return ''.join(seg[::-1] for seg in segs) + tail[::-1]


def valid(text):
    """严格照题面核输入：1<=t<=100；操作只有 encrypt/decrypt；串长 1..100；
    encrypt 串只含小写字母；decrypt 串必须是某个小写字母串按题述算法加密的结果。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not re.fullmatch(r'[1-9]\d*', lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 100 or len(lines) != 1 + 2 * t:
        return False
    for i in range(t):
        op, s = lines[1 + 2 * i], lines[2 + 2 * i]
        if not 1 <= len(s) <= 100:
            return False
        if op == 'encrypt':
            if not re.fullmatch(r'[a-z]+', s):
                return False
        elif op == 'decrypt':
            if not re.fullmatch(r'[a-z0]+', s):
                return False
            p = dec(s)
            if not p or enc(p) != s:
                return False
        else:
            return False
    return True


def rand_str(r, n, p_even):
    return ''.join(r.choice(EVEN) if r.random() < p_even else r.choice(ODD) for _ in range(n))


def cipher_of(s):
    """返回长度不超过 100 的密文（明文太长导致密文 101 时去掉末字符）。"""
    t = enc(s)
    if len(t) > 100:
        t = enc(s[:-1])
    return t


def build(items):
    rows = [str(len(items))]
    for op, s in items:
        rows += [op, s]
    return '\n'.join(rows) + '\n'


def cases():
    out = [SAMPLE]
    r = random.Random(28322)
    # 满规模：t=100，串长 100 的加密与解密混合
    items = []
    for _ in range(100):
        s = rand_str(r, 100, 0.5)
        items.append(('encrypt', s) if r.random() < .5 else ('decrypt', cipher_of(s)))
    out.append(build(items))
    # 全是奇数字母：加密结果是 0 加逆序（101 字符），解密串以 0 开头
    items = []
    for i in range(100):
        s = rand_str(r, 100 if i % 2 == 0 else 99, 0)
        items.append(('encrypt', s) if i % 2 == 0 else ('decrypt', enc(s)))
    out.append(build(items))
    # 全是偶数字母：密文与明文相同，不出现 0
    items = []
    for i in range(100):
        s = rand_str(r, r.randint(90, 100), 1)
        items.append(('encrypt' if i % 2 else 'decrypt', s))
    out.append(build(items))
    # 每个字母单独加密、解密（长度 1 的边界）
    items = [('encrypt', c) for c in LOWER] + [('decrypt', enc(c)) for c in LOWER]
    out.append(build(items))
    # 恰好以偶数结尾（不补 0）与以奇数结尾（补 0）交替
    items = []
    for i in range(100):
        s = rand_str(r, r.randint(2, 99), 0.3)
        s = s[:-1] + (r.choice(EVEN) if i % 4 < 2 else r.choice(ODD))
        items.append(('encrypt', s) if i % 2 == 0 else ('decrypt', cipher_of(s)))
    out.append(build(items))
    # 只有解密 / 只有加密
    out.append(build([('decrypt', cipher_of(rand_str(r, r.randint(1, 100), r.random()))) for _ in range(100)]))
    out.append(build([('encrypt', rand_str(r, r.randint(1, 100), r.random())) for _ in range(100)]))
    # t=1 的边界
    out.append(build([('encrypt', 'z')]))
    out.append(build([('decrypt', '0a')]))
    out.append(build([('decrypt', cipher_of(rand_str(r, 100, 0.2)))]))
    out.append(build([('encrypt', rand_str(r, 100, 0.05))]))
    # 长奇数段夹偶数：多段出栈 + 末尾长段
    items = []
    for _ in range(100):
        s = ''.join(rand_str(r, r.randint(0, 30), 0) + r.choice(EVEN) for _ in range(3)) + rand_str(r, r.randint(1, 9), 0)
        items.append(('encrypt', s) if r.random() < .5 else ('decrypt', cipher_of(s)))
    out.append(build(items))
    # 其余随机组：不同奇偶比例、不同 t
    while len(out) < 30:
        p = r.choice([0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95])
        t = r.choice([r.randint(1, 10), r.randint(10, 100), 100])
        items = []
        for _ in range(t):
            s = rand_str(r, r.randint(1, 100), p)
            items.append(('encrypt', s) if r.random() < .5 else ('decrypt', cipher_of(s)))
        out.append(build(items))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(set(cs)) == len(cs), '组间重复'
    for i, c in enumerate(cs):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
