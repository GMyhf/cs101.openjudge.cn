import random
REFERENCE='# External reference: /practice/30044/statistics/\n# Accepted submission: 52732985\n# Source: http://cs101.openjudge.cn/practice/solution/52732985/\n# License: not declared on the submission page; no license is inferred.\n\ndef is_prime(n):\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    i = 3\n    while i*i <= n:\n        if n % i == 0:\n            return False\n        i += 2\n    return True\n\ndef reverse_bin(num):\n    s = bin(num)[2:]       # 转二进制，去掉0b\n    rev = s[::-1]\n    return int(rev, 2)\n\npairs_set = set()\nres_list = []\nnum = 3\n\nwhile len(res_list) <= 1000:\n    if is_prime(num):\n        rev_num = reverse_bin(num)\n        if is_prime(rev_num):\n            a = min(num, rev_num)\n            b = max(num, rev_num)\n            if (a,b) not in pairs_set:\n                pairs_set.add((a,b))\n                res_list.append((a,b))\n    num += 1\n\nx = int(input())\nprint(res_list[x][0], res_list[x][1])'
SAMPLE='5\n'
GENERATOR_NAME='g30044'
def g30044(r): return f"{r.randint(0, 1000)}\n"

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
