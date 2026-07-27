import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='from itertools import permutations\n\nt = int(input())\n\nfor _ in range(t):\n    s1, s2, s3 = input().split()\n\n    letters = sorted(set(s1 + s2 + s3))\n\n    # 需要非零的字母\n    lead = set()\n    if len(s1) > 1:\n        lead.add(s1[0])\n    if len(s2) > 1:\n        lead.add(s2[0])\n    if len(s3) > 1:\n        lead.add(s3[0])\n\n    found = False\n\n    def dfs(idx, mp, used):\n        global found\n\n        if idx == len(letters):\n            a = int("".join(str(mp[ch]) for ch in s1))\n            b = int("".join(str(mp[ch]) for ch in s2))\n            c = int("".join(str(mp[ch]) for ch in s3))\n\n            if a + b == c:\n                print(f"{a}+{b}={c}")\n                return True\n            return False\n\n        ch = letters[idx]\n\n        for d in range(10):\n            if d in used:\n                continue\n\n            if d == 0 and ch in lead:\n                continue\n\n            mp[ch] = d\n            used.add(d)\n\n            if dfs(idx + 1, mp, used):\n                return True\n\n            used.remove(d)\n            del mp[ch]\n\n        return False\n\n    found = dfs(0, {}, set())\n\n    if not found:\n        print("No Solution")'
SAMPLE='5\nA A B\nAA AA AAA\nAB ABC ACDD\nA A BC\nABCD BCD ACEA\n'
GENERATOR_NAME='g25139'
def g25139(r):
    letters = list("ABCDE")
    def word(): return "".join(r.choice(letters[:r.randint(2, 5)]) for _ in range(r.randint(1, 6)))
    a, b = word(), word(); c = word()
    known = r.choice(["A A BC", "ABCD BCD ACEA", "A A B"])
    return f"3\nA A BC\n{a} {b} {c}\n{known}\n"

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
