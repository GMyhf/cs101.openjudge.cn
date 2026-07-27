import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20196/\n# Accepted submission: 31921452\n# Source: http://cs101.openjudge.cn/practice/solution/31921452/\n# License: not declared on the submission page; no license is inferred.\n\nlt1=[31,29,31,30,31,30,31,31,30,31,30,31]\nlt=[31,28,31,30,31,30,31,31,30,31,30,31]\nimport math\ny,m,d=map(int,input().split())\ni_sl=365\nG=y\nif (y%4==0 and y%100!=0) or y%400==0:\n    used=lt1\n    i_sl=366\nelse:\n    used=lt\nG+=(sum(used[:m-1])+d-1)/i_sl\nH=(G-621.5774) / 0.970224\n\ny1=int(H)\nd1=H-y1\nlt2={2,5,7,10,13,16,18,21,24,26,29}\nis_sleap=354\nif y1%30 in lt2:\n    is_sleap=355\nd1*=is_sleap\n\nd1=math.ceil(d1)\n\nm1=0\nmut_year=[30,29,30,29,30,29,30,29,30,29,30,29]\nwhile m1<11 and d1>mut_year[m1]:\n    d1-=mut_year[m1]\n    m1+=1\nprint(y1,m1+1,d1)'
SAMPLE='2020 1 10\n'
GENERATOR_NAME='g20196'
def g20196(r):
    y = r.randint(1900, 2200)
    leap = y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
    m = r.randint(1, 12)
    days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return f"{y} {m} {r.randint(1, days[m - 1])}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
