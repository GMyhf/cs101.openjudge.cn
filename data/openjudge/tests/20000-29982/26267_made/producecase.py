import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='def kmp_match(s, t):\n    n = len(s)\n    m = len(t)\n    if m == 0:\n        return True\n    # 计算前缀函数\n    pi = [0] * m\n    for i in range(1, m):\n        j = pi[i-1]\n        while j > 0 and t[i] != t[j]:\n            j = pi[j-1]\n        if t[i] == t[j]:\n            j += 1\n        pi[i] = j\n    # KMP匹配\n    j = 0\n    for i in range(n):\n        while j > 0 and s[i] != t[j]:\n            j = pi[j-1]\n        if s[i] == t[j]:\n            j += 1\n        if j == m:\n            return True\n    return False\n\n# 读取输入\nS = input().strip()\nT = input().strip()\n\n# 输出结果\nprint("YES" if kmp_match(S, T) else "NO")'
SAMPLE='SOFUNNYANDTIRINGWASHERGAME\nINGWA\n'
GENERATOR_NAME='g26267'
def g26267(r):
    n, m = r.randint(1, 10000), r.randint(1, 1000)
    t = "".join(r.choice("ABCD") for _ in range(m)); s = "".join(r.choice("ABCD") for _ in range(n))
    if r.random() < .5 and m <= n:
        at = r.randint(0, n - m); s = s[:at] + t + s[at + m:]
    return f"{s}\n{t}\n"

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
