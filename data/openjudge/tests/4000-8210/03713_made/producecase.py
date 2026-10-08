import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nsmall={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19}\ntens={"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90}\nfor line in sys.stdin:\n    cur=total=0; neg=False\n    for w in line.split():\n        if w=="negative": neg=True\n        elif w in small: cur+=small[w]\n        elif w in tens: cur+=tens[w]\n        elif w=="hundred": cur*=100\n        elif w=="thousand": total+=cur*1000; cur=0\n        elif w=="million": total+=cur*1000000; cur=0\n    value=total+cur\n    print(-value if neg else value)'
SAMPLE_IN='six\nnegative seven hundred twenty nine\none million one hundred one\neight hundred fourteen thousand twenty two\n'
SMALL="zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS="_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
LIMIT=999999999

def below_thousand(x):
    words=[]
    if x>=100:
        words+=[SMALL[x//100],"hundred"]; x%=100
    if x>=20:
        words.append(TENS[x//10]); x%=10
        if x:words.append(SMALL[x])
    elif x:
        words.append(SMALL[x])
    return words

def to_words(v):
    if v==0:return "zero"
    words=["negative"] if v<0 else []
    v=abs(v)
    for unit,name in ((1000000,"million"),(1000,"thousand")):
        if v>=unit:
            words+=below_thousand(v//unit)+[name]; v%=unit
    words+=below_thousand(v)
    return " ".join(words)

def parse(line):
    small={w:i for i,w in enumerate(SMALL)}
    tens={w:i*10 for i,w in enumerate(TENS) if w!="_"}
    cur=total=0;neg=False
    for w in line.split(" "):
        if w=="negative":neg=True
        elif w in small:cur+=small[w]
        elif w in tens:cur+=tens[w]
        elif w=="hundred":cur*=100
        elif w=="thousand":total+=cur*1000;cur=0
        elif w=="million":total+=cur*1000000;cur=0
        else:return None
    v=total+cur
    return -v if neg else v

def valid(text):
    # 题面：若干行，每行一个用题面所列英文单词表达的整数，范围 -999,999,999..+999,999,999；
    # 负号用 negative；超过千时不用 hundred 合写（1600 写作 one thousand six hundred）。
    # 这里要求每行与该数的规范英文写法逐字一致（单空格分隔）。
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not lines or lines==[""]:
        return False
    for line in lines:
        v=parse(line)
        if v is None or abs(v)>LIMIT or to_words(v)!=line:
            return False
    return True

def rand_val(r):
    k=r.random()
    if k<0.15:
        v=r.choice([0,1,10,11,19,20,99,100,101,110,999,1000,1001,1010,1100,1600,10000,100000,
                    1000000,1000001,1000100,1001000,100000000,999999999,999000000,999999,
                    120000019,700000000,10000010,99000099])
    elif k<0.3:
        v=r.randint(0,999)
    elif k<0.45:
        v=r.randint(1000,999999)
    elif k<0.6:
        # 中间某段为 0
        a,b,c=r.randint(0,999),r.randint(0,999),r.randint(0,999)
        z=r.randrange(3)
        if z==0:b=0
        elif z==1:c=0
        else:b=c=0
        v=max(a,1)*1000000+b*1000+c
    else:
        v=r.randint(1000000,LIMIT)
    if v and r.random()<0.4:
        v=-v
    return v

def g3713(r,index):
    if index<=10:
        n=r.randint(1,6)
    elif index<=30:
        n=r.randint(20,100)
    else:
        n=r.randint(800,1000)
    vals=[rand_val(r) for _ in range(n)]
    if index==1:
        vals=[0]
    elif index==2:
        vals=[LIMIT,-LIMIT]
    elif index==3:
        vals=[1600,-1000000,100000,1000100,-20,90,1001001,-999]
    return "\n".join(to_words(v) for v in vals)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt_no in range(100):
                    content=g3713(random.Random(3713+index+attempt_no*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
