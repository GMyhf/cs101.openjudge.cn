import re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/22007/\n# Accepted submission: 52245294\n# Source: http://cs101.openjudge.cn/practice/solution/52245294/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\nboard=[[0]*n for i in range(n)]\ndef issafe(lines,x,y):\n    for i in range(len(lines)):\n        if i-lines[i]==x-y or i+lines[i]==x+y:\n            return False\n    return True\n\nans=[]\ndef dfs(lines,count):\n    if count==n:\n        ans.append(lines[:])\n        return\n    if len(lines)>n:\n        return\n    for j in range(n):\n        if j not in lines and issafe(lines,len(lines),j):\n            lines.append(j)\n            dfs(lines,count+1)\n            lines.pop()\n\ndfs([],0)\nans.sort()\nif not ans:\n    print('NO ANSWER')\nelse:\n    for lines in ans:\n        print(*lines)"
SAMPLE='4\n'
GENERATOR_NAME='g22007'
# 题面：1<=N<=9，输入只有一个整数，本质上只有 9 种不同输入，组间不可能全部两两不同。
# 0 组为样例 N=4；其余每个 N 至少一组，再补「行末无换行」的写法；
# 剩下的组重复最卡时间的 N=8、9 与无解分支 N=2、3。
def valid(text):
    return re.fullmatch(r"[1-9]\n?",text) is not None

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[f"{n}\n" for n in (1,2,3,5,6,7,8,9)]+[f"{n}" for n in range(1,10)]
    cases+=["9\n","8\n","2\n","3\n","9"]
    assert len(cases)==23
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
