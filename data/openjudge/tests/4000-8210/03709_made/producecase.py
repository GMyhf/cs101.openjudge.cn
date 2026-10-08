import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ndef f(s):\n n=int(s,2); out=[]\n if not n:return "0"\n while n: out.append(str(n%3)); n//=3\n return "".join(out[::-1])\na=sys.stdin.read().split(); print("\\n".join(f(x) for x in a[1:]))'
SAMPLE_IN='2\n10110\n1011\n'

def valid(text):
    # 题面：第 1 行组数 n，后跟 n 行，每行一个由 0 和 1 组成的字符串，长度 1..64
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*",lines[0]):
        return False
    n=int(lines[0])
    if len(lines)!=n+1:
        return False
    return all(re.fullmatch(r"[01]{1,64}",x) for x in lines[1:])

def rand_bin(r,length,lead_one=True):
    s="".join(r.choice("01") for _ in range(length))
    if lead_one:
        s="1"+s[1:]
    return s

def g3709(r,index):
    if index<=10:
        n=r.randint(1,6)
    elif index<=30:
        n=r.randint(10,60)
    else:
        n=r.randint(150,200)
    special=["0","1","10","11","000","0001","1"*64,"1"+"0"*63,"0"*64,"0"*63+"1",
             "1"*63,"1"*32,"1"+"0"*32,"0"*10+"1"*54]
    rows=[]
    for _ in range(n):
        k=r.random()
        if k<0.2:
            rows.append(r.choice(special))
        elif k<0.45:
            rows.append(rand_bin(r,64))
        elif k<0.6:
            rows.append(rand_bin(r,r.randint(60,64)))
        elif k<0.75:
            # 带前导零
            z=r.randint(1,20)
            rows.append("0"*z+rand_bin(r,r.randint(1,64-z)))
        else:
            rows.append(rand_bin(r,r.randint(1,64)))
    if index==1:
        rows=["0"]
    elif index==2:
        rows=["1"*64]
    elif index==3:
        rows=["1"*64,"1"+"0"*63,"0"*64,"1","0001","1"*63]
    return str(len(rows))+"\n"+"\n".join(rows)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3709(random.Random(3709+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
