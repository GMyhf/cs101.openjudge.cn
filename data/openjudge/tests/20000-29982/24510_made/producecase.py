import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/24510/\n# Accepted submission: 52740116\n# Source: http://cs101.openjudge.cn/practice/solution/52740116/\n# License: not declared on the submission page; no license is inferred.\n\ndef time2sec(t):\n    h, m, s = map(int, t.split(':'))\n    return h * 3600 + m * 60 + s\n\nfrom collections import defaultdict\ndic = defaultdict(int)\n\nn = int(input())\nfor _ in range(n):\n    name, st, ed = input().split()\n    sec1 = time2sec(st)\n    sec2 = time2sec(ed)\n    dic[name] += sec2 - sec1\n\n# 找总时长最大的文件名\nmax_name = max(dic, key=lambda k: dic[k])\nprint(max_name)"
SAMPLE='4\nindex.html 10:25:00 10:25:06\nstudy.html 10:25:45 10:28:50\nindex.html 10:26:00 10:29:03\nteachers.html 10:59:01 11:01:03\n'
GENERATOR_NAME='g24510'
def _sec(t): h,m,x=map(int,t.split(':')); return h*3600+m*60+x
def _hms(a): return f"{a//3600:02d}:{a//60%60:02d}:{a%60:02d}"
_TIME=re.compile(r'([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
def totals(text):
    lines=text.split('\n'); n=int(lines[0]); d={}
    for l in lines[1:n+1]:
        nm,a,b=l.split(' '); d[nm]=d.get(nm,0)+_sec(b)-_sec(a)
    return d
def valid(text):
    # 题面：第一行正整数 n；其后 n 行「网页 开始时间 结束时间」，空格分隔；
    # 时间为当天内的 时:分:秒（不跨 24:00），结束时间 >= 开始时间
    if not text.endswith('\n'): return False
    lines=text[:-1].split('\n')
    if not lines[0].isdigit() or lines[0]!=str(int(lines[0])) or int(lines[0])<1: return False
    n=int(lines[0])
    if len(lines)!=n+1: return False
    for l in lines[1:]:
        p=l.split(' ')
        if len(p)!=3 or not p[0] or any(c.isspace() for c in p[0]): return False
        if not _TIME.fullmatch(p[1]) or not _TIME.fullmatch(p[2]): return False
        if _sec(p[2])<_sec(p[1]): return False
    return True
def unique_max(text):
    # 题面没说并列怎么办，生成器保证最长网页唯一
    d=totals(text); m=max(d.values()); return sum(v==m for v in d.values())==1
def _row(name,a,b): return f"{name} {_hms(a)} {_hms(b)}"
def g24510(r):
    # 原生成器的分布，但结束时间不越过 23:59:59
    while True:
        n=r.randint(2,20); rows=[]
        for i in range(n):
            a=r.randint(0,23)*3600+r.randint(0,59)*60+r.randint(0,59); b=min(86399,a+r.randint(0,1000))
            rows.append(_row(f"page{r.randint(1,5)}",a,b))
        c=f"{n}\n"+"\n".join(rows)+"\n"
        if unique_max(c): return c
NAMES=['index.html','study.html','teachers.html','about.html','news.html','login.html','courses/cs101.html','a.html','search.php','img/logo.png']
def big(r,n,pages,maxdur):
    while True:
        names=[r.choice(NAMES)+'' if i<len(NAMES) and r.random()<.3 else f"p{r.randint(1,10**6)}.html" for i in range(pages)]
        names=list(dict.fromkeys(names)); rows=[]
        for _ in range(n):
            a=r.randint(0,86399); b=min(86399,a+r.randint(0,maxdur)); rows.append(_row(r.choice(names),a,b))
        c=f"{n}\n"+"\n".join(rows)+"\n"
        if unique_max(c): return c
def extra():
    r=random.Random(245100); out=[]
    out.append("1\nindex.html 00:00:00 00:00:00\n")                       # n=1，时长 0
    out.append("1\nonly.html 00:00:00 23:59:59\n")                        # 整天
    out.append("3\na.html 10:00:00 10:00:00\nb.html 10:00:00 10:00:01\na.html 12:00:00 12:00:00\n")
    # 单次最长的网页不是总时长最长：多次累加反超
    out.append("5\nlong.html 08:00:00 09:00:00\nmany.html 09:00:00 09:20:00\nmany.html 10:00:00 10:20:00\nmany.html 11:00:00 11:20:01\nlong.html 12:00:00 12:00:00\n")
    out.append("4\nx.html 00:00:00 00:00:59\ny.html 00:00:00 00:59:00\nz.html 00:00:00 00:01:00\nx.html 23:00:00 23:59:00\n")
    # 规模组受单组 .in<=1MB 限制，最多约 2.8 万行
    out.append(big(r,1000,50,3000)); out.append(big(r,10000,500,600)); out.append(big(r,20000,2000,5000))
    out.append(big(r,28000,5000,86399)); out.append(big(r,28000,3,100))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra()
    assert all(valid(c) and unique_max(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
