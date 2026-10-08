import random
REFERENCE='# External reference: /practice/30110/statistics/\n# Accepted submission: 52825154\n# Source: http://cs101.openjudge.cn/practice/solution/52825154/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\n\ndef solve():\n    # Read all input from standard input\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    s = input_data[0]\n\n    # Count frequencies of each digit \'0\'-\'9\'\n    digit_counts = [0] * 10\n    for char in s:\n        if "0" <= char <= "9":\n            digit_counts[int(char)] += 1\n\n    # Construct the largest number by appending digits from 9 down to 0\n    result_parts = []\n    for digit in range(9, -1, -1):\n        if digit_counts[digit] > 0:\n            result_parts.append(str(digit) * digit_counts[digit])\n\n    # Print the final reconstructed maximum integer\n    print("".join(result_parts))\n\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='5\n'
GENERATOR_NAME='g30110'
CPP=False
def valid(text):
    # 题面：一行字符串 s，1<=|s|<=1e6，仅含小写字母与数字，且至少含一个 1~9 的数字
    if not text.endswith('\n') or text.count('\n') != 1: return False
    s = text[:-1]
    if not (1 <= len(s) <= 10**6): return False
    if any(not ('a' <= c <= 'z' or '0' <= c <= '9') for c in s): return False
    return any('1' <= c <= '9' for c in s)

def g30110(r): return f"{r.randint(1, 10**9)}\n"

LET = 'abcdefghijklmnopqrstuvwxyz'
def mixed(r, n, pd, digits='0123456789'):
    # 长度 n，每个字符以概率 pd 为数字
    s = [r.choice(digits) if r.random() < pd else r.choice(LET) for _ in range(n)]
    if not any('1' <= c <= '9' for c in s): s[r.randrange(n)] = r.choice('123456789')
    return ''.join(s)

def extra_cases():
    r = random.Random(30110)
    N = 10**6
    out = ['290es1q0', '1', 'a1', '1z', 'q0w0e0r1t0y', '0000000001', '9876543210', 'abc0def0ghi5']
    out.append(''.join(r.choice('0123456789') for _ in range(N - 1)) + '7')   # 性质 A 满规模
    out.append('0' * (N - 1) + '1')                                         # 前导零，答案 1 后跟 999999 个 0
    z = ['z'] * N; z[N // 2] = '3'; out.append(''.join(z))                   # 全是字母只有一个数字
    s = list(mixed(r, N, 0.0005)); out.append(''.join(s))                    # 性质 B：约 500 个数字
    M = 2 * 10**5                                                            # 体积控制：以下大组取 2e5，满 1e6 的只留上面 4 组
    out.append(mixed(r, M, 0.5))                                             # 一般情形
    out.append(mixed(r, M, 0.9, '019'))
    out.append(mixed(r, M, 0.3, '05'))
    out.append(''.join(r.choice(LET) for _ in range(999)) + '1' + '0' * 1000)
    for _ in range(6): out.append(mixed(r, r.randint(1, 2000), r.random()))
    for _ in range(4): out.append(mixed(r, r.randint(2 * 10**4, M), r.random()))
    return [x + '\n' for x in out]

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
