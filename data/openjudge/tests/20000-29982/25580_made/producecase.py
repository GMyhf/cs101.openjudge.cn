import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# 25580: 木板掉落（修正版）\n# 目标：木板落地后才能挡住到达木板处的小球\n# 需要挡住 k = floor(n/2)+1 个球（严格超过一半）\n\nimport sys\nimport math\n\ndata = sys.stdin.read().strip().split()\nH = float(data[0])\nL = float(data[1])\nn = int(data[2])\nvs = list(map(float, data[3:3+n]))\n\n# 计算每个球到达木板位置的时间\ntimes = []\nfor v in vs:\n    times.append(0.0 if L == 0 else L / v)\n\ntimes.sort()\n\nk = n // 2 + 1                  # “大于一半的最小整数”\nT = times[n - k]                # t_{n-k}，保证至少 k 个球到达时间 >= T\n\n# 要求 t_land <= T\n# t_land = sqrt((H - h)/5) <= T  =>  h >= H - 5*T^2\nh = H - 5.0 * T * T\nif h < 0:\n    h = 0.0\nif h > H:\n    h = H\n\nprint(f"{h:.2f}")\n'
SAMPLE='100 12 4\n1 2 3 4\n'
GENERATOR_NAME='g25580'
def g25580(r):
    h, l, n = r.randint(1, 99999), r.randint(0, 9999), r.randint(1, 99)
    vs = [f"{r.uniform(0.1, 999):.3f}" for _ in range(n)]
    return f"{h} {l} {n}\n{' '.join(vs)}\n"

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
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
