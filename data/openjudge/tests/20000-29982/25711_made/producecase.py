import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="N, M = map(int,input().split())\nresult = []\nfor _ in range(N):\n    line = input().split()\n    sum1 = 0\n    sum2 = 0\n    for i in range(1,len(line)-1,2):\n        if int(line[i])>=60:\n            gpa = 4-(3*((100-int(line[i]))**2)/1600)\n        else:\n            gpa = 0\n        sum1 += gpa * int(line[i+1])\n        sum2 += int(line[i+1])\n        aver = sum1/sum2\n\n    result.append([line[0],aver])\nresult = sorted(result,key=lambda x:x[1],reverse=True)[:M]\nname = []\nfor i in range(M):\n    name.append(result[i][0])\nprint(' '.join(name))"
SAMPLE='5 3\n2201111000 80 5 78 3 95 2\n2201111001 59 2 67 3 60 4 57 2\n2201111002 78 5 80 2\n2201111003 60 2 100 5\n2201111004 78 4 84 2\n'
GENERATOR_NAME='g25711'
def g25711(r):
    n = r.randint(2, 80); m = r.randint(1, n); rows = []
    for i in range(n):
        courses = r.randint(1, 5); vals = []
        for _ in range(courses): vals += [str(r.randint(60, 100)), str(r.randint(1, 6))]
        rows.append(f"{2201000000 + i} " + " ".join(vals))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
