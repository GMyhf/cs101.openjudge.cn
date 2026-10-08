import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\ntable = []\nfor _ in range(n):\n    a, b = input().split()\n    table.append((a, int(b)))\ntable.sort(key = lambda x: (-x[1], x[0]))\nfor i in table:\n    print(*i)'
SAMPLE='4\nKitty 80\nHanmeimei 90\nJoey 92\nTim 28\n'
GENERATOR_NAME='g7615'
def valid(text):
    """题面：n（0<n<20）；n 行「名字 成绩」，单个空格分隔；名字只含字母、长度≤20；成绩为不大于 100 的非负整数。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 0 < n < 20 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        m = re.fullmatch(r"([A-Za-z]{1,20}) (0|[1-9][0-9]*)", line)
        if not m or int(m.group(2)) > 100:
            return False
    return True


def make_name(r,style,length):
    s="".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length))
    # 同一组内名字大小写风格一致，避免「字典序」是否区分大小写的歧义
    return {"cap":s.capitalize(),"lower":s,"upper":s.upper()}[style]

def g7615(r,seed):
    n=19 if seed%4==0 else (1 if seed in (1,2) else r.randint(2,19))   # 题面：0 < n < 20
    style=r.choice(["cap","cap","lower","upper"])
    names=[]
    while len(names)<n:
        if names and r.random()<.3:          # 前缀关系：Tom / Tomas
            b=r.choice(names); x=make_name(r,style,r.randint(1,4))
            x=b+(x.lower() if style!="upper" else x)
            x=x[:20]
        else:
            x=make_name(r,style,r.choice([1,2,3,r.randint(1,20),20]))
        if x not in names: names.append(x)
    mode=seed%5
    if mode==0: pool=[0,100]                   # 只有两端分数，大量并列
    elif mode==1: pool=[r.randint(0,100) for _ in range(3)]
    elif mode==2: pool=list(range(0,101))
    elif mode==3: pool=[r.randint(55,65)]*2+[100,0,9,10]   # 9 与 10、100：字符串比较会错
    else: pool=[r.randint(0,100)]               # 全部同分，只按名字排
    return f"{n}\n"+"\n".join(f"{x} {r.choice(pool)}" for x in names)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7615(random.Random(seed),seed) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
