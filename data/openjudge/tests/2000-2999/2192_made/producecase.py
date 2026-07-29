import random, subprocess, sys, tempfile
from pathlib import Path
def g2192(r):
    rows = []
    for _ in range(r.randint(1, 12)):
        a = "".join(r.choice("abcde") for _ in range(r.randint(1, 18)))
        b = "".join(r.choice("abcde") for _ in range(r.randint(1, 18)))
        aa, bb, c = list(a), list(b), []
        while aa or bb:
            src = aa if not bb or (aa and r.random() < .5) else bb; c.append(src.pop(0))
        if r.random() < .35: c[r.randrange(len(c))] = "z"
        rows.append(f"{a} {b} {''.join(c)}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2192: Zipper\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02192/\n# License: not declared in source collection; no license is inferred.\n# 袁籁2300010728\nfrom functools import lru_cache\n\n\n@lru_cache\ndef f(a, b, c):\n    if len(c) == 0:\n        return True\n    else:\n        if len(a) and c[0] == a[0] and f(a[1:], b, c[1:]):\n            return True\n        elif len(b) and c[0] == b[0] and f(a, b[1:], c[1:]):\n            return True\n        else:\n            return False\n\n\nn = int(input())\nfor _ in range(n):\n    a, b, c = input().split()\n    x = len(c)\n    if f(a, b, c):\n        print('Data set %d: yes' % (_ + 1))\n    else:\n        print('Data set %d: no' % (_ + 1))\n"
SAMPLE='3\ncat tree tcraete\ncat tree catrtee\ncat tree cttaree\n'
GENERATOR='g2192'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
