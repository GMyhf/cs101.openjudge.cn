import random, subprocess, tempfile
from pathlib import Path
# 原 REFERENCE（samplecode.py 旧版）是 O(N·轮数) 的分组贪心，N=1e5 的一般数据上要跑几十秒以上；
# 换成与之逐组等价（小规模穷举/暴力已对拍）的 O(N log N) 实现。
REFERENCE_SOURCE = "# 拓扑序视角：i<j 且 |h_i-h_j|>D 时 i 必须在 j 前；每次取入度为 0 的最小身高（同值取靠左者）。\n# 入度按身高排名放进带懒标记的线段树：删掉 v 后，所有身高在 [v-D, v+D] 之外的未处理者入度减 1。\nimport sys\nfrom bisect import bisect_left, bisect_right\ndef main():\n    data=sys.stdin.buffer.read().split(); n=int(data[0]); D=int(data[1]); h=list(map(int,data[2:2+n]))\n    order=sorted(range(n),key=lambda i:(h[i],i)); rank=[0]*n\n    for r,i in enumerate(order): rank[i]=r\n    vals=[h[i] for i in order]\n    # 初始入度：i<j 且 |h_i-h_j|>D 的个数（BIT 按值排名计数）\n    bit=[0]*(n+1); indeg=[0]*n\n    def add(p):\n        p+=1\n        while p<=n: bit[p]+=1; p+=p&-p\n    def pre(p):  # count ranks < p\n        s=0\n        while p>0: s+=bit[p]; p-=p&-p\n        return s\n    for j in range(n):\n        lo=bisect_left(vals,h[j]-D); hi=bisect_right(vals,h[j]+D)\n        indeg[rank[j]]=pre(lo)+(j-pre(hi))\n        add(rank[j])\n    size=1\n    while size<n: size*=2\n    INF=float('inf')\n    mn=[INF]*(2*size); lz=[0]*(2*size)\n    for r in range(n): mn[size+r]=indeg[r]\n    for x in range(size-1,0,-1): mn[x]=min(mn[2*x],mn[2*x+1])\n    def upd(l,r,v,x=1,a=0,b=None):\n        if b is None: b=size\n        if r<=a or b<=l: return\n        if l<=a and b<=r: mn[x]+=v; lz[x]+=v; return\n        m=(a+b)//2; upd(l,r,v,2*x,a,m); upd(l,r,v,2*x+1,m,b); mn[x]=min(mn[2*x],mn[2*x+1])+lz[x]\n    out=[]\n    for _ in range(n):\n        # 找最左（值最小、同值下标最小）入度为 0 的叶子\n        x=1; acc=0\n        assert mn[1]==0\n        while x<size:\n            acc+=lz[x]\n            x=2*x if mn[2*x]+acc==0 else 2*x+1\n        r=x-size; out.append(vals[r])\n        # 删除：设为 INF\n        y=x; mn[y]=INF\n        y//=2\n        while y: mn[y]=min(mn[2*y],mn[2*y+1])+lz[y]; y//=2\n        v=vals[r]\n        lo=bisect_left(vals,v-D); hi=bisect_right(vals,v+D)\n        if lo>0: upd(0,lo,-1)\n        if hi<n: upd(hi,n,-1)\n    sys.stdout.write('\\n'.join(map(str,out))+'\\n')\nmain()\n"
SAMPLE_IN = '5 3\n7\n7\n3\n6\n2\n'
SAMPLE_OUT = '6\n7\n7\n2\n3\n'
def generate_case(r):
    n = r.randint(2, 45); d = r.randint(1, 40); heights = [r.randint(1, 1000) for _ in range(n)]
    assert 1 <= n <= 10**5 and 1 <= d <= 10**9 and all(1 <= x <= 10**9 for x in heights)
    return f"{n} {d}\n" + "\n".join(map(str, heights)) + "\n"

import re
INT = re.compile(r"[1-9][0-9]*")

def valid(text):
    """题面契约：第一行 N D（1<=N<=1e5，1<=D<=1e9）；接下去恰好 N 行，每行一个正整数 h_i（1<=h_i<=1e9）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    first = lines[0].split(" ")
    if len(first) != 2 or not all(INT.fullmatch(x) for x in first):
        return False
    n, d = map(int, first)
    if not 1 <= n <= 10**5 or not 1 <= d <= 10**9 or len(lines) != n + 1:
        return False
    return all(INT.fullmatch(x) and int(x) <= 10**9 for x in lines[1:])

def _fmt(d, hs):
    return f"{len(hs)} {d}\n" + "\n".join(map(str, hs)) + "\n"

def extra_cases():
    """第 8..19 组：按题面「10% N<=100、20% N<=5000、其余 N<=1e5」分层的边界与规模数据。"""
    r = random.Random(253530)
    cases = []
    cases.append(_fmt(10**9, [10**9]))                                   # N=1，取值上限
    cases.append(_fmt(1, [1] * 37 + [2] * 30 + [10**9] * 33))            # 大量相等身高，D=1 最小
    cases.append(_fmt(10**9, [r.randint(1, 10**9) for _ in range(100)])) # D 足够大：答案即排序
    cases.append(_fmt(r.randint(1, 50), [r.randint(1, 200) for _ in range(5000)]))
    cases.append(_fmt(10, [10 if i % 2 == 0 else (0 if i % 4 == 1 else 20) + (i % 4 == 1) for i in range(5000)]))
    cases.append(_fmt(3, [r.randint(1, 10) for _ in range(5000)]))
    n = 10**5
    # 严格递增、步长 2、D=1：每对都不能交换，答案等于原序列
    cases.append(_fmt(1, [2 * i + 1 for i in range(n)]))
    # 严格递减、D=1：同样一个都换不动（排序类写法会错）
    cases.append(_fmt(1, [3 * (n - i) for i in range(n)]))
    # 交替的 10/1/20 结构：每轮只能取出一个，逐轮扫描的写法退化为 O(N^2)
    cases.append(_fmt(9, [10 if i == 0 else (1 if i % 2 else 20) for i in range(n)]))
    # 中等 D 的大规模随机（值 <= 1e8 控制文件大小）
    cases.append(_fmt(r.randint(10**6, 10**7), [r.randint(1, 10**8) for _ in range(n)]))
    cases.append(_fmt(r.randint(10**7, 5 * 10**7), [r.randint(1, 10**8) for _ in range(n)]))
    # 小值域、大量重复的大规模数据
    cases.append(_fmt(r.randint(2, 30), [r.randint(1, 100) for _ in range(n)]))
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()  # 末尾若干组：边界与满规模（catalog 固定 20 组）
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20 - len(extras):
                content = extras[index - (20 - len(extras))]
                assert content not in seen, index
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(25353 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=300, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
