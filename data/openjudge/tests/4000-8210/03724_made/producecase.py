import random,subprocess,tempfile,calendar
from pathlib import Path
REFERENCE_SOURCE='import sys\ndays=[31,28,31,30,31,30,31,31,30,31,30,31]\ndef leap(y): return y%400==0 or y%4==0 and y%100!=0\nfor token in sys.stdin.read().split():\n    rem=int(token); y=1970\n    while rem >= (366 if leap(y) else 365)*86400: rem-=(366 if leap(y) else 365)*86400; y+=1\n    month=1\n    while True:\n        md=days[month-1]+(month==2 and leap(y))\n        if rem < md*86400: break\n        rem-=md*86400; month+=1\n    print(f"{y:04d}-{month:02d}-{rem//86400+1:02d} {(rem%86400)//3600:02d}:{(rem%3600)//60:02d}:{rem%60:02d}")'
SAMPLE_IN='10\n1234567890\n'
LIMIT=2**31


def valid(text):
    """题面：若干行，每行一个整数 t，0<=t<2^31。"""
    if not text.endswith("\n"):
        return False
    lines=text[:-1].split("\n")
    if not lines:
        return False
    for line in lines:
        if not line.isdigit() or (len(line)>1 and line[0]=="0"):
            return False
        if not 0<=int(line)<LIMIT:
            return False
    return True


def boundary_values():
    """各月末/年末最后一秒与次月第一秒、闰日、上下界。"""
    vals=[0,1,59,60,3599,3600,86399,86400,LIMIT-1,LIMIT-2]
    for y in range(1970,2038):
        for m in range(1,13):
            t=calendar.timegm((y,m,1,0,0,0))
            if 0<t<LIMIT:
                vals.extend([t-1,t])
        if calendar.isleap(y):
            t=calendar.timegm((y,2,29,0,0,0))
            vals.extend([t,t+86399])
    return sorted(set(v for v in vals if 0<=v<LIMIT))


def g3724(index,r):
    b=boundary_values()
    if index==1: vals=[0]
    elif index==2: vals=[LIMIT-1]
    elif index==3: vals=b                       # 全部边界
    elif index==4:                              # 2000 年（被 400 整除的闰年）全年各月
        vals=[calendar.timegm((2000,m,d,h,mi,s)) for m in range(1,13) for d in (1,28) for h,mi,s in ((0,0,0),(23,59,59))]
        vals+= [calendar.timegm((2000,2,29,12,0,0)),calendar.timegm((2000,3,1,0,0,0))]
    elif index==5:                              # 满规模：2 万行随机
        vals=[r.randrange(LIMIT) for _ in range(20000)]
    elif index==6:                              # 2 万行，全部取自边界附近
        vals=[min(LIMIT-1,max(0,r.choice(b)+r.randint(-2,2))) for _ in range(20000)]
    elif index<=15:                             # 单个边界值
        vals=[r.choice(b)]
    else:
        k=r.choice([1,2,5,30,200,1000])
        vals=[r.randrange(LIMIT) if r.random()<0.5 else min(LIMIT-1,max(0,r.choice(b)+r.randint(-1,1))) for _ in range(k)]
    return "".join(f"{v}\n" for v in vals)


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0: content=SAMPLE_IN
            else:
                for attempt_no in range(100):
                    content=g3724(index,random.Random(3724+index+attempt_no*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
                seen.append(content)
            assert valid(content),index
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=60,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__=="__main__":
    main()
