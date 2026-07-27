import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/27378/\n# Accepted submission: 52739303\n# Source: http://cs101.openjudge.cn/practice/solution/52739303/\n# License: not declared on the submission page; no license is inferred.\n\nkey = input()\ns = input()\nans = []\n\nfor char in s:\n    if char != '.':\n        ans.append(char)\n\n    if char == '.':\n        ans.append(key)\n\nprint(''.join(ans))"
SAMPLE='i\nlook . f.nd a d.rty keyboard.\n'
EXTRA_CASE=None
GENERATOR_NAME='g27378'
def g27378(r):
    key = r.choice("abcdefghijklmnopqrstuvwxyz")
    alphabet = "".join(c for c in "abcdefghijklmnopqrstuvwxyz" if c != key) + " ."
    text = "".join(r.choice(alphabet) for _ in range(r.randint(1, 180)))
    text = text.rstrip() or "."
    return f"{key}\n{text}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
