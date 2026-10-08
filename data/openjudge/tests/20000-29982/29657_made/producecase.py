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


def _is_int(tok):
    t = tok[1:] if tok[:1] == "-" else tok
    return t.isdigit() and (t == "0" or t[0] != "0") and tok != "-0"


def valid(text):
    """题面：输入四行；第一行 N1 N2 N3 K（1<=N1,N2,N3<=50000）；接下来三行分别有 N1、N2、N3 个整数（身高），空格分隔。
    题面未给 K 与身高的取值范围，只核为整数（样例第三行末尾带一个空格，行末空格放行）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 4:
        return False
    head = lines[0].split()
    if len(head) != 4 or not all(_is_int(t) for t in head):
        return False
    ns = list(map(int, head[:3]))
    if not all(1 <= x <= 50000 for x in ns):
        return False
    for n, line in zip(ns, lines[1:]):
        toks = line.rstrip(" ").split(" ")
        if len(toks) != n or not all(_is_int(t) for t in toks):
            return False
    return True


def _case(n1, n2, n3, k, arrays):
    return f"{n1} {n2} {n3} {k}\n" + "\n".join(" ".join(map(str, a)) for a in arrays) + "\n"


def special_case(index):
    """第 25..39 组：补 N=1、K=0、全相等、满规模（答案超 2^32）、大值域、组规模悬殊等。"""
    r = random.Random(296570 + index)
    k = index - 25
    M = 50000
    if k == 0:
        return _case(1, 1, 1, 10, [[150], [155], [160]])        # 恰好 1 种
    if k == 1:
        return _case(1, 1, 1, 4, [[150], [155], [160]])         # 差距超 K，0 种
    if k == 2:
        return _case(1, 1, 1, 5, [[150], [150], [151]])         # 需严格递增，0 种
    if k == 3:
        return _case(3, 3, 3, 0, [[1, 2, 3], [2, 3, 4], [3, 4, 5]])   # K=0
    if k == 4:                                                  # 满规模全相等 -> 0
        return _case(M, M, M, 1000, [[170] * M] * 3)
    if k == 5:                                                  # 满规模，K 覆盖全部值域：答案为严格递增三元组数
        arr = [[r.randint(100, 300) for _ in range(M)] for _ in range(3)]
        return _case(M, M, M, 1000, arr)
    if k in (6, 7, 8):                                          # 满规模，大量重复，K 适中
        kk = [1, 15, 60][k - 6]
        arr = [[r.randint(100, 300) for _ in range(M)] for _ in range(3)]
        return _case(M, M, M, kk, arr)
    if k == 9:                                                  # 三组分层：一组矮、二组中、三组高
        arr = [[r.randint(100, 180) for _ in range(M)], [r.randint(150, 230) for _ in range(M)],
               [r.randint(200, 280) for _ in range(M)]]
        return _case(M, M, M, 50, arr)
    if k == 10:                                                 # 规模悬殊
        arr = [[r.randint(140, 160)], [r.randint(100, 300) for _ in range(M)], [r.randint(100, 300) for _ in range(M)]]
        return _case(1, M, M, 40, arr)
    if k == 11:
        arr = [[r.randint(100, 300) for _ in range(M)], [r.randint(100, 300) for _ in range(M)], [r.randint(140, 160)]]
        return _case(M, M, 1, 40, arr)
    if k == 12:                                                 # 大值域（受 1MB 输入限制，每组 25000 人）
        h = 25000
        arr = [[r.randint(1, 10**9) for _ in range(h)] for _ in range(3)]
        return _case(h, h, h, 10**7, arr)
    if k == 13:                                                 # 中等规模随机
        n1, n2, n3 = (r.randint(100, 5000) for _ in range(3))
        arr = [[r.randint(100, 250) for _ in range(n)] for n in (n1, n2, n3)]
        return _case(n1, n2, n3, r.randint(5, 40), arr)
    arr = [[r.randint(120, 220) for _ in range(M)] for _ in range(3)]   # 恰好差 K 的边界大量出现
    return _case(M, M, M, 10, arr)

REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) if seed < 25 else special_case(seed) for seed in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
