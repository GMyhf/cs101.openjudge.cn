import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# 25580: 木板掉落（修正版）\n# 目标：木板落地后才能挡住到达木板处的小球\n# 需要挡住 k = floor(n/2)+1 个球（严格超过一半）\n\nimport sys\nimport math\n\ndata = sys.stdin.read().strip().split()\nH = float(data[0])\nL = float(data[1])\nn = int(data[2])\nvs = list(map(float, data[3:3+n]))\n\n# 计算每个球到达木板位置的时间\ntimes = []\nfor v in vs:\n    times.append(0.0 if L == 0 else L / v)\n\ntimes.sort()\n\nk = n // 2 + 1                  # “大于一半的最小整数”\nT = times[n - k]                # t_{n-k}，保证至少 k 个球到达时间 >= T\n\n# 要求 t_land <= T\n# t_land = sqrt((H - h)/5) <= T  =>  h >= H - 5*T^2\nh = H - 5.0 * T * T\nif h < 0:\n    h = 0.0\nif h > H:\n    h = H\n\nprint(f"{h:.2f}")\n'
SAMPLE='100 12 4\n1 2 3 4\n'
GENERATOR_NAME='g25580'
def g25580(r):
    h, l, n = r.randint(1, 99999), r.randint(0, 9999), r.randint(1, 99)
    vs = [f"{r.uniform(0.1, 999):.3f}" for _ in range(n)]
    return f"{h} {l} {n}\n{' '.join(vs)}\n"

def valid(text):
    """题面：第一行整数 H L n；第二行 n 个浮点数 v1..vn。
    0 < H < 100000, 0 < n < 100, 0 <= L < 10000, 0 < vi < 1000，速度互不相同，
    且答案满足 0 < h <= H（题面“范围限制”）。"""
    import math
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if len(lines) != 2: return False
    a = lines[0].split(" ")
    if len(a) != 3 or not all(x.isdigit() for x in a): return False
    H, L, n = map(int, a)
    if not (0 < H < 100000 and 0 < n < 100 and 0 <= L < 10000): return False
    b = lines[1].split(" ")
    if len(b) != n: return False
    try: vs = [float(x) for x in b]
    except ValueError: return False
    if not all(math.isfinite(v) and 0 < v < 1000 for v in vs): return False
    if len(set(vs)) != n: return False
    t = sorted(0.0 if L == 0 else L / v for v in vs)
    T = t[n - (n // 2 + 1)]
    h = min(H, H - 5 * T * T)
    return h > 0

def extra_cases():
    """边界与分支：n=1/2、L=0（h=H）、答案远离 H、偶数 n 卡 k 取错、整数速度、满规模。"""
    r = random.Random(255800)
    out = ["3000 120 5\n5 30 6 1 100\n", "3000 0 5\n5 30 6 1 100\n",
           "1 0 1\n999\n", "99999 0 99\n" + " ".join(str(i) for i in range(1, 100)) + "\n",
           "501 10 1\n1\n", "500 10 2\n1 2\n", "500 10 2\n2 1\n"]
    def designed(H, L, n, integer):
        lo = L / math.sqrt(H / 5) * 1.02  # 速度高于 lo 的球对应 h>0
        while True:
            if integer:
                lo_i = max(1, int(lo) + 1)
                if 999 - lo_i + 1 < n: return None
                vs = r.sample(range(lo_i, 1000), n); txt = [str(v) for v in vs]
            else:
                vs = sorted({round(r.uniform(lo, min(999.0, max(lo * 4, lo + 50))), 3) for _ in range(n * 2)})
                vs = [v for v in vs if lo < v < 1000]
                if len(vs) < n: return None
                vs = r.sample(vs, n); txt = [f"{v:.3f}" for v in vs]
            c = f"{H} {L} {n}\n{' '.join(txt)}\n"
            if valid(c): return c
    import math
    specs = [(99999, 9999, 99, False), (99999, 9999, 98, False), (1000, 9999, 50, False), (200, 3000, 60, True),
             (50000, 9999, 2, False), (80000, 9999, 4, True), (5, 9, 9, False), (99999, 1, 99, False),
             (12345, 6789, 10, False), (60000, 9000, 77, True)]
    for H, L, n, integer in specs:
        c = designed(H, L, n, integer)
        assert c is not None, (H, L, n)
        out.append(c)
    return out

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
    cases += extra_cases()
    assert len(set(cases)) == len(cases)
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
