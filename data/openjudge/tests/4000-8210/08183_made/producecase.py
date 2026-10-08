import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="a, b, c, d = input().split()\nheight, width = int(a), int(b)\nkind_1 = [c]*width\nkind_2 = [c]+[' ']*(width-2)+[c]\nif d == '0':\n    print(*kind_1, sep = '')\n    for _ in range(height-2):\n        print(*kind_2, sep = '')\n    print(*kind_1, sep = '')\nelif d == '1':\n    for _ in range(height):\n        print(*kind_1, sep = '')"
SAMPLE='7 7 @ 0\n'
GENERATOR_NAME='g8183'
def g8183(r):
    h,w=r.randint(3,10),r.randint(5,10); return f"{h} {w} {r.choice('@#*')} {r.randint(0,1)}\n"

def valid(text):
    """题面契约：一行四个参数，单空格分隔：高 3..10、宽 5..10 的整数，一个画图字符（单个非空白字符），0 或 1。"""
    if not text.endswith("\n") or "\n" in text[:-1]:
        return False
    t=text[:-1].split(" ")
    if len(t)!=4 or not all(x.isdigit() and x[0]!="0" for x in t[:2]):
        return False
    h,w=int(t[0]),int(t[1])
    return 3<=h<=10 and 5<=w<=10 and len(t[2])==1 and not t[2].isspace() and t[3] in ("0","1")

# 追加的边界组：原数据没有最小/最大的空心矩形（3x5、10x10、3x10、10x5 空心），画图字符只有 @#*
EXTRA=['3 5 * 0\n','3 5 # 1\n','10 10 @ 0\n','10 10 * 1\n','3 10 + 0\n','10 5 A 0\n','4 5 $ 0\n','3 6 . 0\n',
       '10 6 % 1\n','5 10 X 0\n']

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]
    for seed in range(1, 40):
        # 原生成器有 3 组与前面重复：遇到重复就换种子（seed+1000*attempt），不重复的组保持原样
        for attempt in range(100):
            c=globals()[GENERATOR_NAME](random.Random(seed+1000*attempt))
            if c not in cases and c not in EXTRA: break
        cases.append(c)
    cases+=EXTRA
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
