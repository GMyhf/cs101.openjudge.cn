import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/18076 statistics, Accepted solution 17302978.\n# Source: http://cs101.openjudge.cn/practice/solution/17302978/\n# Statistics: http://cs101.openjudge.cn/practice/18076/statistics/\n# License: not declared on submission page; no license inferred\na, b = map(int, input().split())\nGA_bond = {}\nfor i in range(a):\n    temp = list(map(int, input().split()))\n    GA_bond[temp[0]] = GA_bond.get(temp[0], [[]]) + temp[-2:-1]\n    root = GA_bond.get(temp[1], [[]])\n    root[0].append([temp[0], temp[-1]])\n    GA_bond[temp[1]] = root\nGB_bond = {}\nfor i in range(b):\n    temp = list(map(int, input().split()))\n    GB_bond[temp[0]] = GB_bond.get(temp[0], [[]]) + temp[-2:-1]\n    root = GB_bond.get(temp[1], [[]])\n    root[0].append([temp[0], temp[-1]])\n    GB_bond[temp[1]] = root\nG = [GA_bond, GB_bond]\n\ndef get_connect(g, m):\n    connect = []\n    for i in g[0]:\n        for j in range(i[1]):\n            connect.append(G[m][i[0]][1])\n    return connect\n\ndef compare(a, b):\n    if a>b:\n        return 1\n    if a<b:\n        return 2\n    return 0\n\ndef get_next_index(connect):\n    connect.append(-2)\n    same = 0\n    while True:\n        if connect[same]!=connect[same+1]:\n            break\n        same += 1\n    ma = 0\n    for i in range(same):\n        if main(connect[ma], connect[i+1])==2:\n            ma = i+1\n    return connect[ma]\n\ndef main(ia=0, ib=0):\n    i = 0\n    while i<1000000:\n        ga = GA_bond[ia]\n        gb = GB_bond[ib]\n        if compare(ga[1], gb[1]): return compare(ga[1], gb[1])\n        connect_a = get_connect(ga, 0)\n        connect_b = get_connect(gb, 1)\n        connect_a.sort(reverse=True)\n        connect_b.sort(reverse=True)\n        for i in range(min(len(connect_a), len(connect_b))):\n            if compare(connect_a[i], connect_b[i]): return compare(connect_a[i], connect_b[i])\n        ia = get_next_index(connect_a)\n        ib = get_next_index(connect_b)\n        i += 1\n\nprint(main())\n'
LANGUAGE='Python3'
SAMPLE='4 4\n0 -1 6 1\n1 0 1 1\n2 0 1 1\n3 0 1 1\n0 -1 6 1\n1 0 1 1\n2 0 1 1\n3 0 9 1\n'
GENERATOR_NAME='g18076'
def g18076(r):
    n,m=r.randint(2,8),r.randint(2,8)
    def mol(size,carbon):
        rows=[f"0 -1 {carbon} 1"]
        for i in range(1,size): rows.append(f"{i} {i-1} {1 if i%2 else carbon} 1")
        return rows
    # Keep the two generated molecules different; the accepted submission's
    # traversal assumes the problem's non-identical-molecule precondition.
    return f"{n} {m}\n"+"\n".join(mol(n,6)+mol(m,8))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
