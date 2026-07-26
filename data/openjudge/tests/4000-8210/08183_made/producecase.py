import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="a, b, c, d = input().split()\nheight, width = int(a), int(b)\nkind_1 = [c]*width\nkind_2 = [c]+[' ']*(width-2)+[c]\nif d == '0':\n    print(*kind_1, sep = '')\n    for _ in range(height-2):\n        print(*kind_2, sep = '')\n    print(*kind_1, sep = '')\nelif d == '1':\n    for _ in range(height):\n        print(*kind_1, sep = '')"
SAMPLE='7 7 @ 0\n'
GENERATOR_NAME='g8183'
def g8183(r):
    h,w=r.randint(3,10),r.randint(5,10); return f"{h} {w} {r.choice('@#*')} {r.randint(0,1)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
