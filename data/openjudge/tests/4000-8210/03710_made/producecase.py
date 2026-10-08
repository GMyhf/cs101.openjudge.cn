import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split()))\nprint("\\n".join(str(bin(x^y).count("1")) for x,y in zip(a[1::2],a[2::2])))'
SAMPLE_IN='1\n3 9\n'
INT_MAX=2**31-1

def valid(text):
    # 题面：第 1 行整数 n，紧接着 n 行，每行两个十进制正整数 A、B，用空格隔开
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*",lines[0]):
        return False
    n=int(lines[0])
    if len(lines)!=n+1:
        return False
    return all(re.fullmatch(r"[1-9]\d* [1-9]\d*",x) for x in lines[1:])

def rand_pos(r):
    # 题面未给值域；生成时保持在 [1, 2^31-1]，兼容 C/C++ int
    k=r.random()
    if k<0.15:
        return r.choice([1,2,3,INT_MAX,INT_MAX-1,2**30,2**30-1,2**16,2**16-1,1024])
    if k<0.4:
        return r.randint(1,1000)
    if k<0.6:
        b=r.randint(1,31)
        return r.randint(2**(b-1),2**b-1)
    return r.randint(1,INT_MAX)

def g3710(r,index):
    if index<=10:
        n=r.randint(1,6)
    elif index<=30:
        n=r.randint(20,200)
    else:
        n=r.randint(800,1000)
    rows=[]
    for _ in range(n):
        k=r.random()
        a=rand_pos(r)
        if k<0.1:
            b=a                       # 答案 0
        elif k<0.2:
            b=a^(1<<r.randint(0,30))  # 只差一位
            if b==0 or b>INT_MAX:b=a
        elif k<0.3:
            b=INT_MAX^a if INT_MAX^a else 1  # 互补，答案接近 31
        else:
            b=rand_pos(r)
        rows.append(f"{a} {b}")
    if index==1:
        rows=["1 1"]
    elif index==2:
        rows=[f"1 {INT_MAX}"]
    elif index==3:
        rows=[f"{INT_MAX} {2**30}","5 5","1 2","9 3",f"{2**30} 1"]
    return str(len(rows))+"\n"+"\n".join(rows)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3710(random.Random(3710+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
