import random, subprocess, sys, tempfile
from pathlib import Path
def g2766(r):
    n = r.randint(1, 18); values = [str(r.randint(-127, 127)) for _ in range(n*n)]
    return str(n) + "\n" + "\n".join(" ".join(values[i*n:(i+1)*n]) for i in range(n)) + "\n"

def valid(text):
    """题面契约：第一行 N (0<N<=100)；之后共 N*N 个 [-127,127] 的整数，以空白（空格或空行）分隔。"""
    import re
    if not text.endswith('\n'): return False
    first, _, rest = text.partition('\n')
    if not re.fullmatch(r'[1-9][0-9]*', first): return False
    n = int(first)
    if not 1 <= n <= 100: return False
    if re.search(r'[^0-9\- \n]', rest): return False
    toks = rest.split()
    if len(toks) != n * n: return False
    return all(re.fullmatch(r'-?(0|[1-9][0-9]*)', t) and t != '-0' and -127 <= int(t) <= 127 for t in toks)

def extra_cases():
    """补充覆盖：N=1（正/负）、N=100 满规模、全负（答案为最大元素）、全 127、全 -127、空白分隔多样（空行/多空格/任意换行）。"""
    r = random.Random(276600)
    def fmt(n, vals): return str(n) + '\n' + '\n'.join(' '.join(map(str, vals[i*n:(i+1)*n])) for i in range(n)) + '\n'
    def messy(n, vals):
        out = []
        for v in vals:
            out.append(str(v)); out.append(r.choice([' ', ' ', '  ', '\n', '\n\n', ' \n']))
        return str(n) + '\n' + ''.join(out[:-1]) + '\n'
    cases = [fmt(1, [5]), fmt(1, [-127]), fmt(2, [-3, -1, -2, -5])]
    for _ in range(2):
        cases.append(fmt(100, [r.randint(-127, 127) for _ in range(10000)]))
    cases.append(fmt(100, [r.randint(-127, -1) for _ in range(10000)]))
    cases.append(fmt(100, [127] * 10000))
    cases.append(fmt(100, [-127] * 10000))
    cases.append(fmt(100, [r.randint(-127, 20) for _ in range(10000)]))
    cases.append(messy(100, [r.randint(-127, 127) for _ in range(10000)]))
    cases.append(messy(37, [r.randint(-127, 127) for _ in range(37 * 37)]))
    cases.append(fmt(73, [r.randint(-127, 127) for _ in range(73 * 73)]))
    return cases

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2766: 最大子矩阵\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02766/\n# License: not declared in source collection; no license is inferred.\ndef kadane(s):\n    curr_max = total_max = s[0]\n    for x in s[1:]:\n        curr_max = max(x, curr_max + x)\n        total_max = max(total_max, curr_max)\n    return total_max\n\ndef max_sum_matrix(mat):\n    max_sum = -float('inf')\n    row, col = len(mat), len(mat[0])\n    for top in range(row):\n        col_sum = [0] * col\n        for bottom in range(top, row):\n            for c in range(col):\n                col_sum[c] += mat[bottom][c]\n            max_sum = max(max_sum, kadane(col_sum))\n    return max_sum\n\nn = int(input())\nnums = []\nwhile len(nums) < n**2:\n    nums.extend(input().split())\nmat = [list(map(int, nums[i*n:(i+1)*n])) for i in range(n)]\nprint(max_sum_matrix(mat))\n"
SAMPLE='4\n0 -2 -7 0 9 2 -6 2\n-4 1 -4  1 -1\n\n8  0 -2\n'
GENERATOR='g2766'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 40)]+extra_cases()
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
