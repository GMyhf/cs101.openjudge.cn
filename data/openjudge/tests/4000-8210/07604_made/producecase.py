import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nstring = input()\ndict_ = {} # 注意用dict()或者{}都可以但是不能用dict\nfor i in range(len(string) - n + 1): # 注意要- n + 1\n    if string[i: i + n] in dict_:\n        dict_[string[i: i + n]] += 1\n    else:\n        dict_[string[i: i + n]] = 1\nmaxim_count = max(dict_.values()) # 注意value写法\nif maxim_count <= 1: # 注意是小于等于不是小于\n    print("NO")\nelse:\n    print(maxim_count)\n    for gram in dict_:\n        if dict_[gram] == maxim_count:\n            print(gram)'
SAMPLE='3\nabcdefabcd\n'
LETTERS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def valid(text):
    """题面：第一行 n（1<n<5）；第二行只含大小写字母、长度不多于 500 的字符串。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) != 2:
        return False
    if not re.fullmatch(r"[234]", lines[0]):
        return False
    s = lines[1]
    if not re.fullmatch(r"[A-Za-z]{1,500}", s):
        return False
    return len(s) >= int(lines[0])   # 至少形成一个 n-gram，否则「最高频度」无定义


def grams(n,s):
    c={}
    for i in range(len(s)-n+1): c[s[i:i+n]]=c.get(s[i:i+n],0)+1
    return c

def rand_str(r,length,alpha):
    return "".join(r.choice(alpha) for _ in range(length))

def distinct_str(r,n,length):
    # 所有 n-gram 互不相同（最高频度 = 1，应输出 NO）
    while True:
        seen=set(); s=rand_str(r,n-1,LETTERS)
        ok=True
        while len(s)<length:
            for _ in range(60):
                ch=r.choice(LETTERS)
                if (s[len(s)-n+1:]+ch) not in seen:
                    seen.add(s[len(s)-n+1:]+ch); s+=ch; break
            else:
                ok=False; break
        if ok: return s

def g7604(r,kind):
    n=r.randint(2,4)                 # 题面：1 < n < 5
    if kind=="small":                # 小字母表随机，多为有重复
        s=rand_str(r,r.randint(n,40),"abcde")
    elif kind=="mixed":              # 大小写混合、区分大小写
        s=rand_str(r,r.randint(50,500),r.choice(["aA","abAB","xyXY","abcABC"]))
    elif kind=="case":               # 只差大小写的 gram 不能合并
        base=rand_str(r,n,"abcdefgh")
        parts=[]
        for _ in range(r.randint(3,40)):
            parts.append("".join(ch.upper() if r.random()<.5 else ch for ch in base)); parts.append(r.choice("XYZ"))
        s="".join(parts)[:500]
    elif kind=="overlap":            # 重叠出现，str.count 不重叠计数会错
        ch=r.choice(LETTERS); s=ch*r.randint(n+1,500)
        if r.random()<.5:
            s=(ch+r.choice(LETTERS))*r.randint(n,250)
    elif kind=="tie":                # 多个并列最高，按首次出现顺序（非字典序）输出
        k=r.randint(2,6); pool=[]
        while len(pool)<k:
            g=rand_str(r,n,"zyxwvu")
            if g not in pool: pool.append(g)
        t=r.randint(2,8); seq=[]
        for _ in range(t): seq+=pool
        r.shuffle(seq)
        s="".join(seq)[:500]
    elif kind=="distinct":           # 最高频度为 1 → NO
        s=distinct_str(r,n,r.randint(n,500))
    elif kind=="single":             # 长度恰为 n，只有一个 gram → NO
        s=rand_str(r,n,LETTERS)
    elif kind=="two":                # 最高频度恰为 2（边界：>1 才输出）
        s=distinct_str(r,n,r.randint(n+5,200))
        i=r.randint(0,len(s)-n); s=(s+s[i:i+n])[:500]
    else:                            # 满长 500 随机
        s=rand_str(r,500,r.choice([LETTERS,"abcdefghij","ab","AbCd"]))
    return f"{n}\n{s}\n"

KINDS=["small"]*6+["mixed"]*5+["case"]*4+["overlap"]*4+["tie"]*5+["distinct"]*5+["single"]*2+["two"]*3+["full"]*5

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7604(random.Random(seed),KINDS[seed-1]) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
