import random
REFERENCE='# External reference: /practice/29778/statistics/\n# Accepted submission: 52682233\n# Source: http://cs101.openjudge.cn/practice/solution/52682233/\n# License: not declared on the submission page; no license is inferred.\n\nc = 0\n\ndef sorting(l):\n    if len(l) == 1:\n        return l\n    global c\n    l1, l2 = sorting(l[:len(l)//2]), sorting(l[len(l)//2:])\n    n = []\n    while l1 or l2:\n        if l1 and l2:\n            if l1[-1] >= l2[-1]:\n                n.append(l1.pop())\n            else:\n                if not 2*l1[0] >= l2[-1]:\n                    l, r = 0, len(l1)\n                    while l < r:\n                        mid = (l + r)//2\n                        if 2*l1[mid] < l2[-1]:\n                            l = mid + 1\n                        else:\n                            r = mid\n                    c += l\n                n.append(l2.pop())\n        elif l1:\n            n.extend(l1[::-1])\n            l1.clear()\n        else:\n            n.extend(l2[::-1])\n            l2.clear()\n    return n[::-1]\n\nsorting([int(input()) for i in range(int(input()))])\nprint(c)'
SAMPLE='10\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n'
GENERATOR_NAME='g29778'
def g29778(r):
    n = r.randint(1, 2000); return f"{n}\n" + "\n".join(str(r.randint(0, 10**6)) for _ in range(n)) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
