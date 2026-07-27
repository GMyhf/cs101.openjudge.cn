import random
REFERENCE="# External reference: /practice/29739/statistics/\n# Accepted submission: 52298393\n# Source: http://cs101.openjudge.cn/practice/solution/52298393/\n# License: not declared on the submission page; no license is inferred.\n\nS=input()\nT=input()\nn=len(T)\npos1=0\nallzero=False\nwhile T[pos1]=='0':\n    pos1+=1\n    if pos1>=n:\n        allzero=True\n        break\nif allzero:\n    for i in 'abcdefghijklmnopqrstuvwxyz':\n        if i not in S:\n            print(i)\n            exit()\n    else:\n        print('a'*(n+1))\n        exit()\ntarget=S[pos1:]+'#'+S\nn=len(target)\nZ=[0]*n\nZ[0]=n\nleft=0\nright=0\nfor i in range(1,n):\n    if i>right: #那么开始暴力匹配\n        ptr=0\n        while ptr<n-i and target[ptr]==target[ptr+i]:\n            ptr+=1\n        Z[i]=ptr #暴力匹配好了，更新Z[i]\n        if ptr>0: #如果有效，那么更新安全区\n            left=i\n            right=i+ptr-1\n    elif i<=right: #看来我们有经验，无需暴力匹配\n        tmp=Z[i-left]\n        if i+tmp<right:\n            Z[i]=tmp\n        else: #于是，从i出发，到right截止的所有内容全部完成匹配，相当于Z[i]至少是right-i+1.于是我们要从S[right-i+1]开始比较起\n            ptr=right\n            while ptr<n and target[ptr]==target[ptr-i]:\n                ptr+=1\n            Z[i]=ptr-i\n            if ptr>i:\n                left=i\n                right=ptr-1\nmaxlen=float('inf')\nminlen=0\nnn=len(T)\nfor i,char in enumerate(T):\n    if char=='0':\n        minlen=max(minlen,Z[i+(nn-pos1)+1])\n    elif char=='1':\n        maxlen=min(maxlen,Z[i+(nn-pos1)+1])\nif minlen>=maxlen:\n    print(-1)\nelse:\n    print(S[pos1:pos1+minlen+1])\n\n\n\n\n"
SAMPLE='baaababaab\n0001010000\n'
GENERATOR_NAME='g29739'
def g29739(r):
    s = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(20, 150)))
    length = r.randint(1, min(20, len(s))); start = r.randint(0, len(s) - length)
    t = s[start:start + length]
    p = "".join("1" if s.startswith(t, i) else "0" for i in range(len(s)))
    return s + "\n" + p + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
