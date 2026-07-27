import random
REFERENCE='# External reference: /practice/30110/statistics/\n# Accepted submission: 52825154\n# Source: http://cs101.openjudge.cn/practice/solution/52825154/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\n\ndef solve():\n    # Read all input from standard input\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    s = input_data[0]\n\n    # Count frequencies of each digit \'0\'-\'9\'\n    digit_counts = [0] * 10\n    for char in s:\n        if "0" <= char <= "9":\n            digit_counts[int(char)] += 1\n\n    # Construct the largest number by appending digits from 9 down to 0\n    result_parts = []\n    for digit in range(9, -1, -1):\n        if digit_counts[digit] > 0:\n            result_parts.append(str(digit) * digit_counts[digit])\n\n    # Print the final reconstructed maximum integer\n    print("".join(result_parts))\n\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='5\n'
GENERATOR_NAME='g30110'
CPP=False
def g30110(r): return f"{r.randint(1, 10**9)}\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
