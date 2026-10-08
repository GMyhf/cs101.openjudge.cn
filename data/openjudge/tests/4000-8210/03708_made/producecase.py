import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfor x in sys.stdin.read().split()[1:]: print(bin(int(x)).count("1"))'
SAMPLE_IN='4\n2\n100\n1000\n66\n'
INT_MAX=2**31-1

def valid(text):
    # 题面：第一个整数 N 为组数，其后 N 行每行一个（十进制）整数
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*",lines[0]):
        return False
    n=int(lines[0])
    if len(lines)!=n+1:
        return False
    return all(re.fullmatch(r"-?(0|[1-9]\d*)",x) and x!="-0" for x in lines[1:])

def g3708(r,index):
    # 题面未给值域；生成时保持在 [0, 2^31-1]，兼容 C/C++ int
    if index<=10:
        n=r.randint(1,8)
    elif index<=30:
        n=r.randint(20,200)
    else:
        n=r.randint(800,1000)
    special=[0,1,2,3,INT_MAX,INT_MAX-1,2**30,2**30-1,2**16,2**16-1,255,256,1023,1024]
    vals=[]
    for _ in range(n):
        k=r.random()
        if k<0.25:
            vals.append(r.choice(special))
        elif k<0.45:
            vals.append(r.randint(0,1000))
        elif k<0.6:
            b=r.randint(1,31)
            vals.append(r.randint(2**(b-1),2**b-1))
        else:
            vals.append(r.randint(0,INT_MAX))
    if index==1:
        vals=[0]
    elif index==2:
        vals=[INT_MAX]
    elif index==3:
        vals=[1,0,INT_MAX,2**30]
    return str(n if index>3 else len(vals))+"\n"+"\n".join(map(str,vals))+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3708(random.Random(3708+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()
