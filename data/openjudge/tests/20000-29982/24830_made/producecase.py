import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n = int(input())\nh = list(map(int, input().split()))\n# 环形处理，加倍\narr = h + h\n\nmax_len = 0\ncurrent = 0\n\nfor i in range(len(arr) - 1):\n    if arr[i] > arr[i + 1]:\n        current += 1\n        if current > max_len:\n            max_len = current\n    else:\n        current = 0\n\n# 最长不能超过一圈\nmax_len = min(max_len, n)\n# 全相等输出 0\nif max_len == 0:\n    print(0)\nelse:\n    print(max_len)'
SAMPLE='5\n2 1 5 6 3\n'
GENERATOR_NAME='g24830'
def g24830(r):
    n = r.randint(2, 100)
    h = [r.randint(0, 10000) for _ in range(n)]
    if r.random() < .65:
        start = r.randint(0, 9999); h = [max(0, start - i * r.randint(1, 100)) for i in range(n)]
    return f"{n}\n{' '.join(map(str, h))}\n"

def valid(text):
    """题面：第一行整数 n（2<=n<=100）；第二行 n 个整数，每个在 [0,10000]。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not lines[0].isdigit():
        return False
    n = int(lines[0])
    if not (2 <= n <= 100) or lines[0] != str(n):
        return False
    t = lines[1].split(" ")
    if len(t) != n or not all(x.isdigit() and x == str(int(x)) for x in t):
        return False
    return all(0 <= int(x) <= 10000 for x in t)


def extra_cases():
    """补充：另两组题面样例、全相等（0）、n=2、严格递减一整圈（n-1）、跨越首尾的最长段、平台不算下坡。"""
    r = random.Random(248300)
    f = lambda h: f"{len(h)}\n{' '.join(map(str, h))}\n"
    dec = list(range(10000, 10000 - 100 * 100, -100))  # 10000..100 严格递减
    k = 37
    run_ = list(range(9000, 9000 - 60 * 150, -150))  # 长 60 点的下坡（59 米）
    # 下坡被首尾切开：前 35 点放在末尾、后 25 点放在开头
    wrap = run_[35:] + [9800] + [r.randint(0, 10000) for _ in range(39)] + run_[:35]
    plateau = []
    for i in range(20):
        plateau += [5000 - i * 10] * 5  # 每段等高，跨段只下降一次
    return [
        "5\n2 1 5 4 3\n",
        "4\n1 1 1 1\n",
        f([7] * 100),
        f([0, 0]),
        f([10000, 0]),
        f(dec),
        f(dec[k:] + dec[:k]),
        f(wrap),
        f(plateau),
        f([10000 if i % 2 == 0 else 0 for i in range(100)]),
        f(list(range(0, 100))),
        f([r.randint(0, 10000) for _ in range(100)]),
    ]

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
