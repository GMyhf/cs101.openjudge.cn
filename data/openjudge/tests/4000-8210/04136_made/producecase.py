import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'r=int(input())\nn=int(input())\nrects=[]\narea=0\nfor _ in range(n):\n    l,t,w,h=[int(i) for i in input().split()]\n    rects.append((l,l+w,h))\n    area+=w*h\nleft=0\nright=r\nwhile True:\n    if right-left<=1:\n        ans=right\n        break\n    mid=left+(right-left)//2\n    half=0\n    for le,ri,we in rects:\n        if ri<=mid:\n            half+=(ri-le)*we\n        elif ri>mid and le<mid:\n            half+=(mid-le)*we\n    if half*2>=area:\n        right=mid\n    else:\n        left=mid\nleft=ans\nright=r+1\nwhile True:\n\n    if right-left<=1:\n        fans=left\n        break\n    mid=left+(right-left)//2\n    ahalf=0\n    for le,ri,we in rects:\n        if ri<=ans:\n            pass\n        elif ri<=mid:\n            ahalf+=(ri-le)*we\n        elif ri>mid and le<mid:\n            ahalf+=(mid-le)*we\n    if ahalf==0:\n        left=mid\n    else:\n        right=mid\n    \nprint(fans)'
SAMPLE = '1000\n2\n1 1 2 1\n5 1 2 1\n'
GENERATOR_NAME = 'g4136'
def g4136(r):
    size=r.randint(8,40); cuts=sorted(r.sample(range(1,size),r.randint(1,min(6,size-1))))
    b=[0]+cuts+[size]
    z=[(b[i],r.randint(1,size-1),b[i+1]-b[i],r.randint(1,size-1)) for i in range(len(b)-1)]
    return f"{size}\n{len(z)}\n"+"\n".join(f"{x} {y} {w} {h}" for x,y,w,h in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
