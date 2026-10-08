import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='from collections import deque\np,q,x,y = map(int,input().split())\nqu = deque([p])\nans,found = 1,0\nvis = {p}\nwhile qu and ans <= 52:\n    l = len(qu)\n    for _ in range(l):\n        qi = qu.popleft()\n        if qi >= x and qi-x not in vis:\n            vis.add(qi-x)\n            qu.append(qi-x)\n            if qi-x == q:\n                found = 1\n                break\n        if qi*y not in vis and qi*y <= (52-ans)*x+q:\n            qu.append(qi*y)\n            vis.add(qi*y)\n            if qi*y == q:\n                found = 1\n                break\n    if found:\n        break\n    ans += 1\nprint(ans if found else "Failed")'
SAMPLE='2 2333 666 8\n'
GENERATOR_NAME='g24837'
def g24837(r):
    p = r.randint(100, 10**8); x = r.randint(1, 9); y = r.randint(2, 9)
    q = (p - x * r.randint(1, min(30, (p - 1) // x))
         if r.random() < .55 else r.randint(1, 10**8))
    return f"{p} {q} {x} {y}\n"

def valid(text):
    """题面：一行 4 个正整数 P Q X Y，0 < P, X, Q <= 2^31，1 < Y <= 225。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    t = text[:-1].split(" ")
    if len(t) != 4 or not all(v.isdigit() and v == str(int(v)) for v in t):
        return False
    p, q, x, y = map(int, t)
    M = 2 ** 31
    return 0 < p <= M and 0 < q <= M and 0 < x <= M and 1 < y <= 225


def extra_cases():
    """补充：题面样例 2、值到 2^31（int 溢出）、Y=225、恰好 52 次与 53 次（Failed）边界、P<X、乘减混合。
    刻意不放 X=1、Y=2、Q≈2^31 这类稠密状态：题库已 AC 的 BFS（即参考解）会用到 300MB 以上内存。"""
    M = 2 ** 31
    r = random.Random(248370)
    out = [
        (1264574, 285855522, 26746122, 3),   # 题面样例 2
        (M, M - 52 * 41297762, 41297762, 225),  # 纯减法恰好 52 次
        (M, M - 53 * 40518559, 40518559, 225),  # 纯减法要 53 次 -> Failed
        (M, 1, M - 1, 2),                    # 一次减法，P 取上限
        (M, M - 1, M, 2),                    # 减到 0 后再也回不来 -> Failed
        (1, M, M, 2),                        # 连乘 31 次恰到 2^31
        (M // 2, M, 3, 2),                   # 乘一次即到 2^31，int 会溢出
        (5, 6, 7, 2),                        # P<X，只能先乘
        (3, 1, 2, 225),
        (1, 225 ** 3, 1, 225),               # Y=225 连乘
        (1, 225 ** 3 + 1, 1, 225),           # 乘出去回不来 -> Failed
    ]
    # 乘减混合：a 次乘法、各阶段减法次数 c_k，总次数取 52/52/53/51/40/45
    for target in (52, 52, 53, 51, 40, 45):
        for _ in range(1000):
            y = r.randint(2, 225); a = r.randint(1, 6)
            x = r.randint(10 ** 3, 10 ** 7)
            c = [r.randint(0, y - 1) for _ in range(a)]
            rest = target - a - sum(c)
            if rest < 0: continue
            S = rest * y ** a + sum(c[k] * y ** k for k in range(a))
            P = r.randint(rest * x + 1, M)
            Q = P * y ** a - x * S
            if 0 < Q <= M and P != Q:
                out.append((P, Q, x, y)); break
    return [f"{p} {q} {x} {y}\n" for p, q, x, y in out]

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
