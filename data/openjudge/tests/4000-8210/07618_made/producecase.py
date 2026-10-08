import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n=int(input())\noldage=[]\nteens=[]\nfor _ in range(n):\n    name,age=input().split()\n    age=int(age)\n    if age>=60:\n        oldage.append((name,age))\n    else:\n        teens.append((name,age))\noldage.sort(reverse=True,key=lambda x:x[1])\nfor name, age in oldage:\n    print(name)\nfor name, age in teens:\n    print(name)'
SAMPLE='5\n021075 40\n004003 15\n010158 67\n021033 75\n102012 30\n'
GENERATOR_NAME='g7618'
def valid(text):
    """题面：第一行小于 100 的正整数 n；随后 n 行「ID 年龄」单空格分隔；ID 长度小于 10、只含数字和字母且互不相同；年龄为整数。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 0 < n < 100 or len(lines) != n + 1:
        return False
    ids = set()
    for line in lines[1:]:
        m = re.fullmatch(r"([0-9A-Za-z]{1,9}) (-?(?:0|[1-9][0-9]*))", line)
        if not m or m.group(1) in ids:
            return False
        ids.add(m.group(1))
    return True


ALNUM="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def g7618(r,seed):
    if seed<=3: n=seed                     # 最小规模
    elif seed%3==0: n=99                   # 题面：小于 100 的正整数
    else: n=r.randint(4,98)
    ids=[]
    style=seed%3
    while len(ids)<n:                      # ID 长度小于 10，只含数字和字母，互不相同
        L=r.randint(1,9)
        x="".join(r.choice("0123456789" if style==0 else ALNUM) for _ in range(L))
        if x not in ids: ids.append(x)
    mode=seed%6
    if mode==0:   pool=list(range(1,100))
    elif mode==1: pool=[59,60,61]                       # 60 岁边界与大量同龄老人
    elif mode==2: pool=list(range(60,101))              # 全是老年人
    elif mode==3: pool=list(range(1,60))                # 全是非老年人
    elif mode==4: pool=[60,60,60,75,75,30,59,10]        # 同龄老人须保持登记顺序
    else:         pool=[r.randint(0,120) for _ in range(5)]+[60]
    return f"{n}\n"+"\n".join(f"{x} {r.choice(pool)}" for x in ids)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7618(random.Random(seed),seed) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
