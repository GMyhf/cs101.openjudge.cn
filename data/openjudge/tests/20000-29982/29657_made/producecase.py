import random
REFERENCE='# External reference: /practice/29657/statistics/\n# Accepted submission: 52733740\n# Source: http://cs101.openjudge.cn/practice/solution/52733740/\n# License: not declared on the submission page; no license is inferred.\n\nimport bisect\n\ndef main():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    n1 = int(input[ptr])\n    n2 = int(input[ptr+1])\n    n3 = int(input[ptr+2])\n    K = int(input[ptr+3])\n    ptr +=4\n    \n    A = list(map(int, input[ptr:ptr+n1]))\n    ptr +=n1\n    B = list(map(int, input[ptr:ptr+n2]))\n    ptr +=n2\n    C = list(map(int, input[ptr:ptr+n3]))\n    ptr +=n3\n    \n    A.sort()\n    B.sort()\n    C.sort()\n    \n    ans = 0\n    for b in B:\n        # 找 a < b 且 b - a <= K\n        left = b - K\n        l = bisect.bisect_left(A, left)\n        r = bisect.bisect_left(A, b)\n        cntA = r - l\n        \n        # 找 c > b 且 c - b <= K\n        lo = b + 1\n        hi = b + K\n        L = bisect.bisect_right(C, lo-1)\n        R = bisect.bisect_right(C, hi)\n        cntC = R - L\n        \n        ans += cntA * cntC\n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='2 2 3 25\n142 176\n160 145 \n160 170 180\n'
GENERATOR_NAME='g29657'
def g29657(r):
    n1, n2, n3 = (r.randint(1, 35) for _ in range(3)); k = r.randint(0, 50)
    arrays = [[r.randint(-100, 100) for _ in range(n)] for n in (n1, n2, n3)]
    return f"{n1} {n2} {n3} {k}\n" + "\n".join(" ".join(map(str, a)) for a in arrays) + "\n"

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
