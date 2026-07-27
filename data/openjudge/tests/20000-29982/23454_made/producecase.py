import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23454/\n# Accepted submission: 52297305\n# Source: http://cs101.openjudge.cn/practice/solution/52297305/\n# License: not declared on the submission page; no license is inferred.\n\ns=input()\nans=''\nfound=False\nfor i in range(len(s)):\n    if s[i]!=' ':\n        ans+=s[i]\n        if found==True:\n            found=False\n    elif found==False:\n        ans+=s[i]\n        found=True\nprint(ans)"
SAMPLE='Boy        next    door\n'
GENERATOR_NAME='g23454'
def g23454(r):
    words=["alpha","beta","gamma","delta"]
    return ((" "*r.randint(1,8)).join(words[:r.randint(2,4)])+"\n")

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
