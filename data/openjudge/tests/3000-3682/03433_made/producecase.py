import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN='1\n20 1 10 10 1000\n20 20 30 10 20\n5 5 5 5 5\n'

def valid(text):
    """题面输入：第一行 t（数据组数）；每组三行：
    M N R K T（1<=M<=10000，1<=N<=20，0<=T<=5000；R、K 题面未给范围，只要求是整数）；
    五个初始生命值、五个攻击力，均满足 0 < x <= 10000。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(ln, k):
        t = ln.split(' ')
        if len(t) != k:
            return None
        try:
            v = [int(x) for x in t]
        except ValueError:
            return None
        return v if [str(x) for x in v] == t else None
    h = ints(lines[0], 1)
    if h is None or h[0] < 1 or len(lines) != 1 + 3 * h[0]:
        return False
    for g in range(h[0]):
        a = ints(lines[1 + 3 * g], 5)
        hp = ints(lines[2 + 3 * g], 5)
        atk = ints(lines[3 + 3 * g], 5)
        if a is None or hp is None or atk is None:
            return False
        M, N, R, K, T = a
        if not (1 <= M <= 10000 and 1 <= N <= 20 and 0 <= T <= 5000):
            return False
        if not all(0 < x <= 10000 for x in hp + atk):
            return False
    return True

def one(r, kind):
    if kind == 'tiny':      # 生命元极少，可能一个武士都造不出来
        M = r.randint(1, 30); N = r.randint(1, 20); T = r.randint(0, 5000)
        hp = [r.randint(1, 40) for _ in range(5)]; atk = [r.randint(1, 40) for _ in range(5)]
    elif kind == 'T0':
        M = r.randint(1, 10000); N = r.randint(1, 20); T = 0
        hp = [r.randint(1, 100) for _ in range(5)]; atk = [r.randint(1, 100) for _ in range(5)]
    elif kind == 'long':    # 满规模：N=20、T=5000、生命元充足、生命值小 → 武士多、事件多
        M = r.randint(5000, 10000); N = r.choice((19, 20)); T = 5000
        hp = [r.randint(1, 60) for _ in range(5)]; atk = [r.randint(1, 60) for _ in range(5)]
    elif kind == 'big':     # 数值接近上限
        M = 10000; N = r.randint(1, 20); T = r.randint(3000, 5000)
        hp = [r.randint(1000, 10000) for _ in range(5)]; atk = [r.randint(1000, 10000) for _ in range(5)]
    else:                   # 一般随机
        M = r.randint(1, 10000); N = r.randint(1, 20); T = r.randint(0, 5000)
        hp = [r.randint(1, 200) for _ in range(5)]; atk = [r.randint(1, 200) for _ in range(5)]
    R = r.randint(1, 100); K = r.randint(1, 100)
    if r.random() < 0.15: K = 0
    return f"{M} {N} {R} {K} {T}\n{' '.join(map(str, hp))}\n{' '.join(map(str, atk))}\n"

def g3433(r, i):
    if i == 1: kinds = ['tiny', 'T0', 'tiny']
    elif i == 2: groups = ["1 1 1 1 0\n1 1 1 1 1\n1 1 1 1 1\n", "10000 20 100 100 5000\n10000 10000 10000 10000 10000\n10000 10000 10000 10000 10000\n",
                           "1 1 1 1 5000\n1 1 1 1 1\n1 1 1 1 1\n"]; return f"{len(groups)}\n" + ''.join(groups)
    elif i <= 6: kinds = ['long']
    elif i <= 10: kinds = ['big'] * r.randint(1, 3)
    elif i <= 30: kinds = [r.choice(('rand', 'rand', 'long', 'big', 'tiny')) for _ in range(r.randint(1, 4))]
    else: kinds = ['rand'] * r.randint(1, 10)
    return f"{len(kinds)}\n" + ''.join(one(r, k) for k in kinds)

def main():
    root = Path(__file__).parent
    with tempfile.TemporaryDirectory() as folder:
        binary = Path(folder) / "reference"
        subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode_ac.cpp"), "-o", str(binary)], check=True)
        for i in range(40):
            c = SAMPLE_IN if i == 0 else g3433(random.Random(3433 + i), i)
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c); (root / "data" / f"{i}.out").write_text(p.stdout)

if __name__ == "__main__":
    main()
