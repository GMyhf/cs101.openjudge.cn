import random,re,string,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na,b=sys.stdin.read().split()\nif len(a)<len(b): a,b=b,a\nprint("true" if b in a+a else "false")'
SAMPLE_IN='AABCD CDAA\n'
ALNUM=string.ascii_letters+string.digits

def valid(text):
    # 题面：一行，两个字符串由单个空格隔开；只含字母和数字，长度不超过 30
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    return re.fullmatch(r"[A-Za-z0-9]{1,30} [A-Za-z0-9]{1,30}",text[:-1]) is not None

def g3711(r,index):
    alpha=r.choice(["AB","ABCD","01","aA","abc123",ALNUM])
    if index>=30:
        ln=30
    else:
        ln=r.randint(1,30)
    long="".join(r.choice(alpha) for _ in range(ln))
    kind=index%5
    if kind in (0,1,2):
        # true：取某个循环移位的子串，尽量跨越首尾
        k=r.randint(0,ln-1)
        rot=long[k:]+long[:k]
        sl=r.randint(1,ln)
        st=r.randint(0,ln-sl)
        short=rot[st:st+sl]
        if kind==2 and ln>=2:
            # 必须跨越原串首尾的情形
            sl=r.randint(2,ln)
            st=r.randint(ln-sl+1,ln-1) if ln-sl+1<=ln-1 else ln-1
            short=(long+long)[st:st+sl]
    else:
        # 大概率 false：在 true 串上改一位或随机串
        sl=r.randint(1,ln)
        if kind==3:
            k=r.randint(0,ln-1)
            short=list((long+long)[k:k+sl])
            p=r.randrange(sl)
            short[p]=r.choice([c for c in alpha+"Z9" if c!=short[p]])
            short="".join(short)
        else:
            short="".join(r.choice(alpha) for _ in range(sl))
    if index==1:
        long,short="A","A"
    elif index==2:
        long,short="A","a"
    elif index==3:
        long="abcdefghijklmnopqrstuvwxyz0123";short=long[25:]+long[:25]
    elif index==4:
        long="ABCD";short="ACBD"
    a,b=(long,short) if r.random()<0.5 else (short,long)
    return f"{a} {b}\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3711(random.Random(3711+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
