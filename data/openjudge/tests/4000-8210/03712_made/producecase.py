import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nm={"2":set("abc"),"3":set("def"),"4":set("ghi"),"5":set("jkl"),"6":set("mno"),"7":set("pqrs"),"8":set("tuv"),"9":set("wxyz")}\na=sys.stdin.read().split(); n=int(a[0]) if a else 0; out=[]\nfor i in range(n):\n w,d=a[1+2*i],a[2+2*i]\n out.append("Y" if len(w)==len(d) and all(x.lower() in m.get(y,set()) for x,y in zip(w,d)) else "N")\nprint("\\n".join(out))'
SAMPLE_IN='3\nILOVEYOU 45683968\ncomputer 26678837\nThankyou 84265967\n'
KEYS={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}
L2D={c:d for d,s in KEYS.items() for c in s}

def valid(text):
    # 题面：第一行整数 n，其后 n 行，每行「字符串 电话号码」用空格隔开，长度都不超过 20
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*",lines[0]):
        return False
    n=int(lines[0])
    if len(lines)!=n+1:
        return False
    return all(re.fullmatch(r"\S{1,20} \d{1,20}",x) for x in lines[1:])

def case(r,s,mode):
    if mode==0:return s
    if mode==1:return s.upper()
    return "".join(c.upper() if r.random()<0.5 else c for c in s)

def match_pair(r,ln):
    digits="".join(r.choice("23456789") for _ in range(ln))
    word="".join(r.choice(KEYS[d]) for d in digits)
    return word,digits

def make_row(r,maxlen):
    ln=r.randint(1,maxlen)
    mode=r.randrange(3)
    k=r.random()
    word,digits=match_pair(r,ln)
    if k<0.4:
        pass                                           # Y
    elif k<0.6:
        # 某一位换成相邻键上的字母（含 s/8、z/9 这类 4 字母键边界）
        p=r.randrange(ln)
        d=digits[p]
        nd=r.choice([x for x in KEYS if x!=d])
        word=word[:p]+r.choice(KEYS[nd])+word[p+1:]
    elif k<0.7:
        # 7 上的 s、9 上的 z 放到相邻键上（把每键当 3 个字母的写法会错）
        p=r.randrange(ln)
        c,d=r.choice([("s","8"),("z","0"),("s","7"),("z","9"),("t","7"),("w","8")])
        word=word[:p]+c+word[p+1:]
        digits=digits[:p]+d+digits[p+1:]
    elif k<0.8:
        # 号码里含 0 或 1（无对应字母）
        p=r.randrange(ln)
        digits=digits[:p]+r.choice("01")+digits[p+1:]
    else:
        # 长度不等：重叠部分也有一位不匹配，按任何理解都应为 N
        ln2=r.choice([x for x in range(1,21) if x!=ln and abs(x-ln)<=3] or [x for x in range(1,21) if x!=ln])
        m=min(ln,ln2)
        digits=(digits+"".join(r.choice("23456789") for _ in range(ln2)))[:ln2]
        p=r.randrange(m)
        digits=digits[:p]+r.choice([x for x in KEYS if word[p] not in KEYS[x]])+digits[p+1:]
    return f"{case(r,word,mode)} {digits}"

def g3712(r,index):
    if index<=10:
        n=r.randint(1,6)
    elif index<=30:
        n=r.randint(20,100)
    else:
        n=r.randint(400,500)
    maxlen=r.choice([20,20,8]) if index>10 else r.randint(1,20)
    rows=[make_row(r,maxlen) for _ in range(n)]
    if index==1:
        rows=["a 2"]
    elif index==2:
        rows=["SZ 79","sz 89","PQRSWXYZ 77779999"]
    elif index==3:
        rows=["abcdefghijklmnopqrst 22233344455566677778","ABCDEFGHIJKLMNOPQRST 22233344455566677777","Z 0","z 1"]
    return str(len(rows))+"\n"+"\n".join(rows)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3712(random.Random(3712+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
