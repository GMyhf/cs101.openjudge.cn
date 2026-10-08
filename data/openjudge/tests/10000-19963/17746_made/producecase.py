import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='// External reference: cs101.openjudge.cn practice/17746 statistics, Accepted solution 52515040.\n// Source: http://cs101.openjudge.cn/practice/solution/52515040/\n// Statistics: http://cs101.openjudge.cn/practice/17746/statistics/\n// License: not declared on submission page; no license inferred\n#include<iostream>\n#include<cstdio>\n#include<string>\n#include<cstring>\n#include<vector>\n#include<queue>\n#include<stack>\n#include<unordered_map>\n#include<unordered_set>\n#include<algorithm>\n#include<climits>\n#include<sstream>\n#include<set>\n#include<map>\n\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int n, m, c;\n    cin >> n >> m >> c;\n    vector<int> v(n + 1);\n    for (int i = 1;i <= n;++i)cin >> v[i];\n    deque<int> max_st, min_st;\n    bool flag = false;\n    for (int i = 1;i <= n;++i) {\n        while (!max_st.empty() && v[i] > max_st.back()) {\n            max_st.pop_back();\n        }\n        max_st.push_back(v[i]);\n        if (i > m) {\n            if (v[i - m] == max_st.front()) {\n                max_st.pop_front();\n            }\n        }\n        while (!min_st.empty() && v[i] < min_st.back()) {\n            min_st.pop_back();\n        }\n        min_st.push_back(v[i]);\n        if (i > m) {\n            if (v[i - m] == min_st.front()) {\n                min_st.pop_front();\n            }\n        }\n        if (i >= m) {\n            if (max_st.front() - min_st.front() <= c) {\n                cout << i-m+1 << \'\\n\';\n                flag = true;\n            }\n        }\n    }\n    if (!flag)cout << "NONE";\n    return 0;\n}\n'
LANGUAGE='G++'
SAMPLE='7 2 0\n0 1 1 2 3 2 2\n'
GENERATOR_NAME='g17746'
def valid(text):
    """题面：第一行 n m c；第二行 n 个整数 ai；
    1<=n<=1000000，1<=m<=10000，0<=c<=10000，0<=ai<=1000000。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    if len(lines)!=2: return False
    try:
        head=lines[0].split()
        if len(head)!=3 or lines[0]!=" ".join(head): return False
        n,m,c=map(int,head)
        if not (1<=n<=10**6 and 1<=m<=10**4 and 0<=c<=10**4): return False
        a=lines[1].split()
        if len(a)!=n or lines[1]!=" ".join(a): return False
        return all(x.isascii() and x.isdigit() and x==str(int(x)) and int(x)<=10**6 for x in head+a)
    except ValueError:
        return False

def _signal(r,n,m,c,vmax,amps=None):
    """分段信号：每段一个基准值加噪声，噪声幅度在 c 上下浮动，制造成片静音与非静音。"""
    a=[]
    while len(a)<n:
        L=r.randint(1,3*m)
        amp=min(vmax,r.choice(amps or [0,c//2,c,c,c+1,2*c+1,vmax])); base=r.randint(0,vmax-amp)
        a+=[base+r.randint(0,amp) for _ in range(L)]
    return a[:n]

def g17746(r,kind):
    if kind=="small":                       # 小规模，可人工核对
        n=r.randint(1,60); m=r.randint(1,min(10,n)+2); c=r.randint(0,20)
        a=[r.randint(0,r.choice([5,100])) for _ in range(n)]
    elif kind=="mid":
        n=r.randint(1000,5000); m=r.choice([1,r.randint(2,50),r.randint(100,10**4)]); c=r.choice([0,r.randint(1,100),10**4])
        a=_signal(r,n,m,c,r.choice([50,10**6]))
    elif kind in ("bigval","bigval_s"):     # 大值域、m 接近 1e4；满规模约 1MB，其余缩小控制总体积
        n=130000 if kind=="bigval" else 30000; m=r.choice([10**4,r.randint(5000,10**4)]); c=r.choice([10**4,r.randint(0,10**4)])
        a=_signal(r,n,m,c,10**6)
    elif kind in ("bign","bign_s"):         # 一位数取值，满规模 n 接近 1MB 能容纳的上限，卡 O(nm)
        n=480000 if kind=="bign" else 100000; m=r.choice([10**4,r.randint(3000,10**4)]); c=r.randint(0,7)
        a=_signal(r,n,m,c,9,[0,c,c+1,9,9])   # 偏向非静音，控制输出不超过 2MB
    return f"{n} {m} {c}\n"+" ".join(map(str,a))+"\n"

KINDS=["small"]*16+["mid"]*10+["bigval"]+["bigval_s"]*4+["bign"]*2+["bign_s"]*2
FIXED=["1 1 0\n1000000\n","3 5 10000\n0 0 0\n","5 5 0\n7 7 7 7 7\n","6 2 10000\n0 1000000 0 1000000 10000 0\n"]

def build_cases():
    cases=[SAMPLE]+list(FIXED)
    for seed,kind in enumerate(KINDS,1):
        for attempt in range(100):
            t=g17746(random.Random(seed*1000+attempt),kind)
            if t not in cases: cases.append(t); break
        else: raise AssertionError("生成器多样性不足")
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.cpp'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
