import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='for _ in range(int(input())):\n    s = input()\n    l, m, ma = s[0], 1, 1\n    for c in s[1:]:\n        m, l = m + 1 if c >= l else 1, c\n        ma = max(ma, m)\n    print(ma)'
SAMPLE='4\n112300125239\n1\n111\n1235111111\n'
GENERATOR_NAME='g26588'
def valid(text):
    """题面：第一行整数 n，1 < n < 100；接下来 n 行，每行一个由 '0'-'9' 构成、长度不超过 100 的字符串。"""
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    if not lines or not lines[0].isdigit() or (len(lines[0]) > 1 and lines[0][0] == "0"):
        return False
    n = int(lines[0])
    if not (1 < n < 100) or len(lines) != n + 1:
        return False
    for row in lines[1:]:
        if not (1 <= len(row) <= 100) or any(c not in "0123456789" for c in row):
            return False
    return True

def _row(r, kind, length):
    if kind == 0:  # 完全随机
        return "".join(r.choice("0123456789") for _ in range(length))
    if kind == 1:  # 整体不降（答案 = 长度）
        return "".join(sorted(r.choice("0123456789") for _ in range(length)))
    if kind == 2:  # 全相同字符（考 <= 而非 <）
        return r.choice("0123456789") * length
    if kind == 3:  # 严格下降段拼接（答案很小）
        start = r.randint(0, 9)
        return "".join(str(9 - (start + i) % 10) for i in range(length))
    if kind == 4:  # 若干不降段拼接，最长段在末尾或开头
        parts = []
        left = length
        while left > 0:
            k = min(left, r.randint(1, 30))
            parts.append("".join(sorted(r.choice("0123456789") for _ in range(k))))
            left -= k
        if r.random() < 0.5:
            parts.sort(key=len)
        return "".join(parts)
    # kind 5：少量字符取值，长平台
    return "".join(r.choice("01") for _ in range(length))

def g26588(r):
    mode = r.random()
    if mode < 0.2:
        t = 99
    elif mode < 0.3:
        t = 2
    else:
        t = r.randint(2, 99)
    rows = [str(t)]
    for _ in range(t):
        length = r.choice([1, 100, r.randint(1, 100), r.randint(1, 100)])
        rows.append(_row(r, r.randint(0, 5), length))
    return "\n".join(rows) + "\n"

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
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
