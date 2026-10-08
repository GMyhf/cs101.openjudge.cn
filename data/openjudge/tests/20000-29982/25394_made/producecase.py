import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='def solve():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    k = int(input[ptr])\n    ptr += 1\n    for _ in range(k):\n        n = int(input[ptr])\n        ptr += 1\n        arr = list(map(int, input[ptr:ptr+n]))\n        ptr += n\n        max_get = 0\n        # 枚举A子集mask1，B子集mask2，无交集\n        for mask1 in range(1, 1 << n):\n            s1 = 0\n            cnt1 = 0\n            for i in range(n):\n                if mask1 & (1 << i):\n                    s1 += arr[i]\n                    cnt1 += 1\n            if cnt1 == 0:\n                continue\n            for mask2 in range(1, 1 << n):\n                if mask1 & mask2 != 0:  # 元素不能重叠\n                    continue\n                s2 = 0\n                cnt2 = 0\n                for i in range(n):\n                    if mask2 & (1 << i):\n                        s2 += arr[i]\n                        cnt2 += 1\n                if s1 == s2:\n                    if cnt1 + cnt2 > max_get:\n                        max_get = cnt1 + cnt2\n        print(max_get)\n\nsolve()'
SAMPLE='3\n4\n1 2 3 8\n4\n1 3 4 8\n5\n3 6 11 12 13\n'
GENERATOR_NAME='g25394'
def valid(text):
    """题面契约：第一行数据组数 k（题面未给上界，只要求正整数）；每组两行：N（4<=N<=8），
    以及 N 个 1..13 的整数点数，单空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])) or int(lines[0]) < 1:
        return False
    k = int(lines[0])
    if len(lines) != 2 * k + 1:
        return False
    for i in range(k):
        a, b = lines[1 + 2 * i], lines[2 + 2 * i]
        if a not in {"4", "5", "6", "7", "8"}:
            return False
        parts = b.split(" ")
        if len(parts) != int(a) or not all(p.isdigit() and p == str(int(p)) and 1 <= int(p) <= 13 for p in parts):
            return False
    return True
def g25394(r):
    k = r.randint(1, 5); rows = []
    for _ in range(k):
        n = r.randint(4, 8)
        rows += [str(n), " ".join(str(r.randint(1, 13)) for _ in range(n))]
    return f"{k}\n" + "\n".join(rows) + "\n"

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
