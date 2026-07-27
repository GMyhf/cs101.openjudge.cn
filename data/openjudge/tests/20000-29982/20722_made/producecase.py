import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20722/\n# Accepted submission: 43080163\n# Source: http://cs101.openjudge.cn/practice/solution/43080163/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Mon Nov 13 16:59:14 2023\n\n@author: Lenovo\n"""\n\nimport re\nwhile True:\n    try:\n        s=input()\n        m="<([A-Za-z]{1,5})>(.*)</\\\\1>"\n        lst=re.findall(m,s)\n        v=0\n        if lst:\n            for i in lst:\n                s=i[1]\n                m=".<([A-Za-z]{1,5})>(.*?)</\\\\1>."\n                nlst=re.findall(m,s)\n                if nlst:\n                    for j in nlst:\n                        s=j[1]\n                        m="(\\d+)"\n                        result=re.findall(m,s)\n                        if result:\n                            for n in result:\n                                if n==\'0\' or (len(n)<5 and n[0]!=\'0\'):\n                                    print(n,end=" ")\n                                    v=1\n        if v==1:\n            print("")\n        else:\n            print("NONE")\n    except:\n        break'
SAMPLE='bac<x><a>bb123<c>aaa 292 bbb 384 j 67477 0 dd 04 05hd</c>c12c</a></y>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</x></y>k</x>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</y>k</x>def\nk<a>1<c>12 35</c>78</c></a></a><x>d<y>3 4</y></x>def\nk<a>1<c>12 35</c>78</c></a></a><abcdefg>d<y>3 4</y></abcdefg>def\nk<a>1<c>12 35</a>78</a></c></B><x>d<y>3 4</y></x>def\n'
GENERATOR_NAME='g20722'
def g20722(r):
    nums = [str(r.choice([0, r.randint(1, 9999)])) for _ in range(r.randint(1, 6))]
    good = "x<a>" + " ".join(nums) + "<b>" + str(r.randint(1, 9999)) + "</b>z</a>y"
    bad = "plain text" if r.random() < .35 else "<a>12 <b>345</b></a>"
    return good + "\n" + bad + "\n"

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
