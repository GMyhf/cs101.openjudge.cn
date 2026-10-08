import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom datetime import date\nlines=sys.stdin.read().splitlines(); n=int(lines[0]); rows=[]\nfor i in range(n):\n    parts=lines[1+i].split(); name=parts[0]; y,m,d,Y,M,D=map(int,parts[1:])\n    rows.append((name,(date(Y,M,D)-date(y,m,d)).days+1,i))\nfor row in sorted(rows,key=lambda x:(-x[1],x[2])): print(row[0],row[1])'
SAMPLE_IN='3\njohn 2007 10 1 2007 10 2\nabbot 2008 2 21 2008 3 1\nalcott 2006 2 20 2006 3 1\n'
from datetime import date,timedelta
LO=date(1900,1,1);HI=date(9999,12,31)

def valid(text):
    # 题面：只有一个测试样例；第一行整数 n，其后 n 行：人名（长度不超过 10）与 6 个整数，单空格分隔；
    # 依次为加入年月日、离开年月日；日期不小于 1900 1 1、不大于 9999 12 31。
    # 另要求日期真实存在且离开不早于加入（题意结构性保证）。
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*",lines[0]):
        return False
    n=int(lines[0])
    if len(lines)!=n+1:
        return False
    for line in lines[1:]:
        m=re.fullmatch(r"(\S{1,10})((?: [1-9]\d*){6})",line)
        if not m:return False
        y,mo,d,Y,M,D=map(int,m.group(2).split())
        try:
            a=date(y,mo,d);b=date(Y,M,D)
        except ValueError:
            return False
        if not (LO<=a<=b<=HI):return False
    return True

def rand_date(r,lo=LO,hi=HI):
    return lo+timedelta(days=r.randint(0,(hi-lo).days))

def rand_name(r,used):
    while True:
        s="".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,10)))
        if r.random()<0.3:s=s.capitalize()
        if s not in used:
            used.add(s);return s

SPECIAL=[(date(1900,1,1),date(9999,12,31)),(date(1900,2,28),date(1900,3,1)),(date(2000,2,28),date(2000,3,1)),
         (date(2100,2,28),date(2100,3,1)),(date(2400,2,28),date(2400,3,1)),(date(2004,2,29),date(2004,2,29)),
         (date(1999,12,31),date(2000,1,1)),(date(9999,12,31),date(9999,12,31)),(date(1900,1,1),date(1900,1,1)),
         (date(1900,1,1),date(1900,12,31)),(date(1999,1,1),date(2001,1,1)),(date(2096,3,1),date(2104,3,1))]

def make_pair(r,tie_lens):
    k=r.random()
    if k<0.1:
        return r.choice(SPECIAL)
    if k<0.4:
        ln=r.choice(tie_lens)                 # 制造天数相同
    elif k<0.6:
        ln=r.randint(0,400)
    elif k<0.85:
        ln=r.randint(0,40000)
    else:
        ln=r.randint(0,(HI-LO).days)
    a=rand_date(r,LO,HI-timedelta(days=ln))
    if r.random()<0.15:
        # 起点落在 2 月底/3 月初附近
        y=r.randint(1900,9990);a=date(y,2,r.randint(20,28))+timedelta(days=r.randint(0,3))
        if ln>(HI-a).days:a=LO
    return a,a+timedelta(days=ln)

def g3715(r,index):
    if index<=10:
        n=r.randint(1,8)
    elif index<=30:
        n=r.randint(20,200)
    else:
        n=r.randint(800,1000)
    tie_lens=[r.randint(0,3000) for _ in range(r.randint(1,4))]
    used=set();rows=[]
    pairs=[make_pair(r,tie_lens) for _ in range(n)]
    if index==1:
        pairs=[(date(1900,1,1),date(1900,1,1))]
    elif index==2:
        pairs=[(date(1900,1,1),date(9999,12,31)),(date(9999,12,31),date(9999,12,31))]
    elif index==3:
        pairs=SPECIAL[:]
    elif index==4:
        # 全部天数相同，必须保持输入顺序
        a=date(2000,1,1);pairs=[(a+timedelta(days=i*37),a+timedelta(days=i*37+99)) for i in range(n+3)]
    for a,b in pairs:
        rows.append(f"{rand_name(r,used)} {a.year} {a.month} {a.day} {b.year} {b.month} {b.day}")
    return str(len(rows))+"\n"+"\n".join(rows)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt_no in range(100):
                    content=g3715(random.Random(3715+index+attempt_no*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
