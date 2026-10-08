def solve_text(text):
    it = iter(text.split()); out = []
    while True:
        radius, n = int(next(it)), int(next(it))
        if radius == n == -1: break
        troops = sorted(int(next(it)) for _ in range(n)); index = 0; answer = 0
        while index < n:
            left = troops[index]
            while index < n and troops[index] <= left + radius: index += 1
            marker = troops[index - 1]
            while index < n and troops[index] <= marker + radius: index += 1
            answer += 1
        out.append(str(answer))
    return "\n".join(out) + "\n"


def generate_case(rng):
    lines = []
    for _ in range(8):
        n = rng.randint(1, 30); lines += [f"{rng.randint(0, 20)} {n}", " ".join(map(str, [rng.randint(0, 100) for _ in range(n)]))]
    return "\n".join(lines) + "\n-1 -1\n"

import random
from pathlib import Path
SAMPLE_IN = '0 3\n10 20 20\n10 7\n70 30 1 7 15 20 50\n-1 -1\n'
SAMPLE_OUT = '2\n4\n'
def valid(text):
    """题面：多组数据，每组一行 R n（0<=R<=1000, 1<=n<=1000），下一行 n 个整数 x_i（0<=x_i<=1000）；
    以 R = n = -1 的一行结束。"""
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    def ints(line):
        t=line.split(" ")
        try: v=[int(x) for x in t]
        except ValueError: return None
        if any(str(a)!=b for a,b in zip(v,t)): return None
        return v
    i=0
    while True:
        if i>=len(lines): return False
        h=ints(lines[i]); i+=1
        if h is None or len(h)!=2: return False
        R,n=h
        if R==-1 and n==-1: return i==len(lines)
        if not (0<=R<=1000 and 1<=n<=1000): return False
        if i>=len(lines): return False
        x=ints(lines[i]); i+=1
        if x is None or len(x)!=n or not all(0<=v<=1000 for v in x): return False

def extra_cases(seed):
    """补充：n、R、x 取到上限 1000；R=0；全部同位置；n=1；间距恰为 R / R+1 的边界。"""
    r=random.Random(seed); out=[]
    def fmt(cs): return "".join(f"{R} {len(x)}\n"+" ".join(map(str,x))+"\n" for R,x in cs)+"-1 -1\n"
    out.append(fmt([(r.randint(0,1000),[r.randint(0,1000) for _ in range(1000)]) for _ in range(5)]))
    out.append(fmt([(0,[r.randint(0,1000) for _ in range(1000)]),(1000,[r.randint(0,1000) for _ in range(1000)]),(1,[r.randint(0,1000) for _ in range(1000)])]))
    out.append(fmt([(R,[r.randint(0,1000) for _ in range(1000)]) for R in (2,3,5,8,13,21,50,100,333,499,500)]))
    out.append(fmt([(0,[1000]),(1000,[0]),(0,[0]),(1000,[0,1000]),(999,[0,1000]),(500,[0,1000]),(499,[0,1000,500]),(0,[7]*1000),(1000,[1000]*1000)]))
    out.append(fmt([(10,list(range(0,1000,10))+[1000]),(10,list(range(0,1000,11))),(10,list(range(0,1000,21))),(5,sorted(range(0,1001,1),key=lambda v:-v)[:1000])]))
    for _ in range(3):
        out.append(fmt([(r.randint(0,30),[r.randint(0,1000) for _ in range(r.randint(1,1000))]) for _ in range(r.randint(1,10))]))
    return out

def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(19757)
    root = Path(__file__).parent / "data"
    cases = [SAMPLE_IN] + [generate_case(rng) for _ in range(19)] + extra_cases(197570)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 19757")

if __name__ == "__main__":
    main()
