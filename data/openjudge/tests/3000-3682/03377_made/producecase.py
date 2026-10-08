import random, subprocess, tempfile
from pathlib import Path
# 参考解：双指针贪心；两端相等时比较 s[l..r] 与其反串（用预先算好的反串切片，C 速度比较），
# 取字典序更小的一端。最坏（全同字母，N=30000）本地约 0.1s。
# 原先的参考解并列时逐字符 Python 循环向内比较，全同字母 N=30000 要 20s+。
REFERENCE_SOURCE = r'''import sys
a=sys.stdin.read().split();s=''.join(a[1:]);n=len(s);rv=s[::-1];l,r,out=0,n-1,[]
while l<=r:
    if s[l]<s[r]:out.append(s[l]);l+=1
    elif s[l]>s[r]:out.append(s[r]);r-=1
    elif s[l:r+1]<=rv[n-1-r:n-l]:out.append(s[l]);l+=1
    else:out.append(s[r]);r-=1
t=''.join(out);print('\n'.join(t[i:i+80] for i in range(0,len(t),80)))
'''
SAMPLE_IN='6\nA\nC\nD\nB\nC\nB\n'
UP='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def valid(text):
    """题面：第 1 行 N（1<=N<=30000）；第 2..N+1 行每行一个 'A'..'Z' 的大写字母。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not lines[0].isdigit() or lines[0][0] == '0':
        return False
    n = int(lines[0])
    if not 1 <= n <= 30000 or len(lines) != n + 1:
        return False
    return all(len(x) == 1 and 'A' <= x <= 'Z' for x in lines[1:])

def rnd(r, n, alpha):
    return ''.join(r.choice(alpha) for _ in range(n))

def g3377(r, i):
    N = 30000
    if i == 1: s = r.choice(UP)
    elif i == 2: s = 'ZZ'
    elif i == 3: s = rnd(r, 80, 'ABC')          # 恰好一整行 80 个
    elif i == 4: s = rnd(r, 81, 'ABC')          # 81 个，第二行只有 1 个
    elif i == 5: s = rnd(r, 160, 'AB')
    elif i == 6: s = 'A' * N                    # 全同字母：并列比较最坏
    elif i == 7:
        h = rnd(r, N // 2, 'AB'); s = h + h[::-1]  # 长回文
    elif i == 8:
        h = rnd(r, N // 2, 'AB'); s = h + 'A' + h[::-1][1:]  # 近回文，中间一处不同
        s = s[:N]
    elif i == 9: s = 'AB' * (N // 2)            # 周期串
    elif i == 10: s = rnd(r, N, UP)
    elif i == 11: s = rnd(r, N, 'AB')
    elif i == 12:
        k = (N - 2) // 2; s = 'B' * k + 'A' + 'C' + 'B' * (N - 2 - k)  # 长并列后才分出大小
    elif i == 13:
        k = (N - 1) // 2; s = 'C' * k + 'B' + 'C' * (N - 1 - k - 1) + 'A'
    elif i == 14: s = rnd(r, N - 1, 'ZY')
    elif i == 15: s = 'Z' * (N // 3) + rnd(r, N - 2 * (N // 3), 'XYZ') + 'Z' * (N // 3)
    elif i <= 25: s = rnd(r, r.randint(1, N), UP[:r.choice((2, 3, 6, 26))])
    elif i <= 32: s = rnd(r, i - 20, UP[:r.choice((2, 3))])  # 长度 6..12 互不相同
    else: s = rnd(r, r.randint(13, 300), UP[:r.choice((2, 3, 4))])
    return f"{len(s)}\n" + "\n".join(s) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py") as h:
        h.write(REFERENCE_SOURCE); h.flush(); root = Path(__file__).parent / "data"
        root.mkdir(exist_ok=True)
        for p in root.glob("*"): p.unlink()
        for i in range(40):
            c = SAMPLE_IN if i == 0 else g3377(random.Random(3377 + i), i)
            assert valid(c), i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c); (root / f"{i}.out").write_text(p.stdout)

if __name__ == "__main__":
    main()
