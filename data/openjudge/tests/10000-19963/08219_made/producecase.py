import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nif n > 0:\n    print(\'positive\')\nelif n < 0:\n    print(\'negative\')\nelse:\n    print("zero")'
SAMPLE='1\n'
GENERATOR_NAME='g8219'
def g8219(r):
    value=r.choice([-10**9,-1,0,1,10**9]) if r.random()<.25 else r.randint(-10**9,10**9)
    return f"{value}\n"

def valid(text):
    """题面契约：一行一个整数 N，-10^9 <= N <= 10^9（规范写法：无前导零、无 +、无 -0）。"""
    if not text.endswith("\n") or "\n" in text[:-1]:
        return False
    t=text[:-1]
    return re.fullmatch(r"0|-?[1-9][0-9]*",t) is not None and -10**9<=int(t)<=10**9

# 追加的边界组：原 40 组一个 0 都没有（zero 分支从未被测），且有 8 组重复
EXTRA=['0\n','2\n','-2\n','999999999\n','-999999999\n','10\n','-10\n']

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
        # 遇到与前面重复的组就换种子（seed+1000*attempt），不重复的组保持原样
        for attempt in range(100):
            c=globals()[GENERATOR_NAME](random.Random(seed+1000*attempt))
            if c not in cases and c not in EXTRA: break
        cases.append(c)
    cases.insert(1,EXTRA[0])
    cases+=EXTRA[1:]
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
