import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/24510/\n# Accepted submission: 52740116\n# Source: http://cs101.openjudge.cn/practice/solution/52740116/\n# License: not declared on the submission page; no license is inferred.\n\ndef time2sec(t):\n    h, m, s = map(int, t.split(':'))\n    return h * 3600 + m * 60 + s\n\nfrom collections import defaultdict\ndic = defaultdict(int)\n\nn = int(input())\nfor _ in range(n):\n    name, st, ed = input().split()\n    sec1 = time2sec(st)\n    sec2 = time2sec(ed)\n    dic[name] += sec2 - sec1\n\n# 找总时长最大的文件名\nmax_name = max(dic, key=lambda k: dic[k])\nprint(max_name)"
SAMPLE='4\nindex.html 10:25:00 10:25:06\nstudy.html 10:25:45 10:28:50\nindex.html 10:26:00 10:29:03\nteachers.html 10:59:01 11:01:03\n'
GENERATOR_NAME='g24510'
def g24510(r):
    n=r.randint(2,20); rows=[]
    for i in range(n):
        a=r.randint(0,23)*3600+r.randint(0,59)*60+r.randint(0,59); b=a+r.randint(0,1000)
        rows.append(f"page{r.randint(1,5)} {a//3600:02d}:{a//60%60:02d}:{a%60:02d} {b//3600:02d}:{b//60%60:02d}:{b%60:02d}")
    return f"{n}\n"+"\n".join(rows)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
