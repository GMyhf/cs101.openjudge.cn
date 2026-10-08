import random
REFERENCE="# External reference: /practice/29946/statistics/\n# Accepted submission: 52733385\n# Source: http://cs101.openjudge.cn/practice/solution/52733385/\n# License: not declared on the submission page; no license is inferred.\n\ns = input().strip()\nk = int(input())\n\nstack = []\nfor c in s:\n    # 还能删，且栈顶比当前大，就删栈顶\n    while k > 0 and stack and stack[-1] > c:\n        stack.pop()\n        k -= 1\n    stack.append(c)\n\n# 如果还剩删除次数，从末尾删\nif k > 0:\n    stack = stack[:-k]\n\n# 去掉前导零\nres = ''.join(stack).lstrip('0')\n\n# 全零情况输出 0\nprint(res if res else '0')"
SAMPLE='175438 \n4\n'
GENERATOR_NAME='g29946'
def g29946(r):
    # 题面：k 是正整数 -> k >= 1（原来是 randint(0, n-1)，第 2、16、22 组 k=0 越界）；
    # 删 k 个后要剩下数字 -> k < 位数，所以一位数时补一位。
    n = r.randint(1, 100); s = str(r.randint(1, 9)) + "".join(str(r.randint(0, 9)) for _ in range(n - 1))
    if n == 1:
        s += str(r.randint(0, 9)); n = 2
    return f"{s}\n{r.randint(1, n - 1)}\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面契约：两行。第一行高精度正整数 n（不超过 250 位，无前导零）；第二行正整数 k，
    删去 k 个数字后要剩下数字 -> 1 <= k < n 的位数。题面样例第一行带一个行尾空格，
    所以行尾空格放行，其余格式严格。"""
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    if len(rows) != 2:
        return False
    n, k = rows[0].rstrip(" "), rows[1].rstrip(" ")
    if not (n.isdigit() and k.isdigit()) or n[0] == "0" or k != str(int(k)):
        return False
    return len(n) <= 250 and 1 <= int(k) < len(n)


def brute(text):
    """独立 oracle（短串）：枚举保留哪些位，取最小值。"""
    from itertools import combinations
    n, k = text.split()
    k = int(k)
    return str(min(int("".join(n[i] for i in keep)) for keep in combinations(range(len(n)), len(n) - k)))


def extra_cases():
    """追加：原数据最长 100 位、没有删完只剩 0 / 删出前导零 / 单调串要从尾部删的专门组。"""
    r = random.Random(299460)
    def rnd(m):
        return str(r.randint(1, 9)) + "".join(str(r.randint(0, 9)) for _ in range(m - 1))
    out = [
        "10\n1\n", "100000\n1\n", "1000000\n3\n", "10200\n1\n", "102030\n2\n",
        "123456789\n3\n", "987654321\n3\n", "11111\n4\n", "90909090\n4\n",
        "1" + "0" * 249 + "\n1\n",                    # 250 位，删 1 得 0
        "9" * 250 + "\n249\n",
        "123456789" * 27 + "1234567\n125\n",          # 250 位非降段 -> 尾删
        "".join(str(9 - i % 10) for i in range(250)) + "\n100\n",
        rnd(250) + "\n1\n", rnd(250) + "\n249\n", rnd(250) + "\n125\n",
        rnd(250) + "\n200\n", rnd(250) + "\n37\n",
        "5" + "".join(r.choice("05") for _ in range(249)) + "\n120\n",
        "1" + "".join(r.choice("0123") for _ in range(249)) + "\n60\n",
    ]
    return out
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
