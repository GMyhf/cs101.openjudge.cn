import random
REFERENCE='# External reference: /practice/30918/statistics/\n# Accepted submission: 52760611\n# Source: http://cs101.openjudge.cn/practice/solution/52760611/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom array import array\n\n# 一次性读取所有输入并切分\ninput_data = sys.stdin.buffer.read().split()\nif not input_data:\n    sys.exit(0)\n\nn = int(input_data[0])\ntotal_elements = n * n\n\n# 预定义一个返回无穷大的常量（因为 array 不支持 float(\'inf\')，我们用一个大数代替）\nINF = 10**9 \n\ndef count_factor(x, p):\n    """计算 x 中包含质因数 p 的个数"""\n    if x == 0:\n        # 修正：原提交返回 INF，多个 0 累加会溢出 32 位有符号数组；0 按 10 处理（2、5 各计 1 个），最后再与 1 取 min\n        return 1\n    cnt = 0\n    while x % p == 0:\n        cnt += 1\n        x //= p\n    return cnt\n\ndef solve_min_path(matrix_bytes, factor_type):\n    """\n    利用一维原生数组实现滚动 DP\n    matrix_bytes: 包含所有矩阵元素的一维字节流解析后的原生数组\n    factor_type: 2 或 5\n    """\n    # 使用 \'i\' (signed int) 创建紧凑的一维数组，极大节省内存\n    dp = array(\'i\', [INF] * n)\n    \n    # 初始化第一行第一个元素\n    first_val = int(matrix_bytes[0])\n    dp[0] = count_factor(first_val, factor_type)\n    \n    # 初始化第一行剩余元素\n    for j in range(1, n):\n        val = int(matrix_bytes[j])\n        dp[j] = dp[j-1] + count_factor(val, factor_type)\n        \n    # 逐行进行状态转移\n    row_idx = 1\n    while row_idx < n:\n        start_pos = row_idx * n\n        \n        # 处理每一行的第一个元素（第一列）\n        first_val = int(matrix_bytes[start_pos])\n        dp[0] = dp[0] + count_factor(first_val, factor_type)\n        \n        # 处理该行剩余的元素\n        for j in range(1, n):\n            val = int(matrix_bytes[start_pos + j])\n            # dp[j] 未更新前是上一行的值（正上方），dp[j-1] 是当前行已更新的值（正左方）\n            top = dp[j]\n            left = dp[j-1]\n            dp[j] = (top if top < left else left) + count_factor(val, factor_type)\n            \n        row_idx += 1\n        \n    return dp[n-1]\n\n# 将输入数据直接映射为紧凑的原生整数数组，避免 Python list 的巨大开销\nmatrix_flat = array(\'i\', (int(x) for x in input_data[1:1+total_elements]))\n\n# 检查是否存在 0\nhas_zero = any(val == 0 for val in matrix_flat)\n\n# 分别计算最少因子 2 和最少因子 5\nmin_2 = solve_min_path(matrix_flat, 2)\nmin_5 = solve_min_path(matrix_flat, 5)\n\nans = min_2 if min_2 < min_5 else min_5\n\n# 如果原矩阵中有 0，那么一定存在一条经过 0 的路径，其乘积为 0，末尾恰好有 1 个 0\nif has_zero:\n    ans = 1 if ans > 1 else ans\n\nprint(ans)'
SAMPLE='3\n1 2 3\n4 5 6\n7 8 9\n'
GENERATOR_NAME='g30918'
CPP=False
import re
_INT = re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    """题面约束：第一行 n（2<=n<=1000）；接下来 n 行，每行 n 个不超过 10^9 的非负整数。"""
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if not lines or not _INT.match(lines[0].strip()):
        return False
    n = int(lines[0])
    if not (2 <= n <= 1000) or len(lines) != n + 1:
        return False
    for row in lines[1:]:
        tok = row.split()
        if len(tok) != n:
            return False
        for t in tok:
            if not _INT.match(t) or int(t) > 10**9:
                return False
    return True

def _fmt(m):
    return f"{len(m)}\n" + "\n".join(" ".join(map(str, row)) for row in m) + "\n"

def g30918(r, n, pool, zero_p=0.0):
    m = [[(0 if r.random() < zero_p else r.choice(pool)) for _ in range(n)] for _ in range(n)]
    return _fmt(m)

def build_cases():
    r = random.Random(30918)
    small = [2, 3, 4, 5, 6, 7, 8]
    rich = [1, 2, 4, 5, 8, 10, 16, 20, 25, 25, 40, 50, 100, 125, 3, 7, 9]
    cases = [SAMPLE]
    # 最小规模
    cases.append("2\n1 1\n1 1\n")
    cases.append("2\n0 0\n0 0\n")
    cases.append("2\n1000000000 1000000000\n1000000000 1000000000\n")
    cases.append("2\n2 5\n5 2\n")
    # 有 0：经过 0 的路径更优（答案 1），非零路径都 >=2
    cases.append("3\n10 10 10\n10 0 10\n10 10 10\n")
    # 有 0 但存在 0 个末尾零的路径（答案 0，不能直接输出 1）
    cases.append("3\n1 0 0\n1 0 0\n1 1 1\n")
    # 只看 2 或 5 单独最优、不能按乘积贪心：2 少的路 5 多、5 少的路 2 多
    cases.append("3\n1 2 1\n5 4 2\n25 5 1\n")
    # 小规模随机（含 0 / 不含 0），可暴力核对
    for k in range(20):
        n = small[k % len(small)]
        cases.append(g30918(r, n, rich, zero_p=(0.15 if k % 3 == 0 else 0.0)))
    # 中等规模
    for n, zp in ((30, 0.0), (50, 0.002), (100, 0.0), (150, 0.0005)):
        cases.append(g30918(r, n, rich, zp))
    # 大数值：接近 10^9 的 2、5 的高次幂与 10^9 本身
    big = [10**9, 2**29, 5**12, 2**6 * 5**8, 999999999, 2**9 * 5**9 // 10, 5**5 * 2**15, 999999937]
    cases.append(g30918(r, 300, big))
    cases.append(_fmt([[10**9] * 300 for _ in range(300)]))
    cases.append(g30918(r, 300, big + [r.randint(1, 10**9) for _ in range(20)], 0.0001))
    # 文件 <=1MB 下的最大规模：一位数元素，n=700
    digits = [1, 2, 4, 5, 8, 3, 6, 7, 9]
    cases.append(g30918(r, 700, digits))
    cases.append(g30918(r, 450, [2, 4, 8, 5, 25, 10, 20, 50, 16, 40]))
    m = [[10] * 580 for _ in range(580)]
    m[579][0] = 0  # 唯一的 0 在左下角，其余全是 10：非零路径末尾零 1159 个 -> 答案 1
    cases.append(_fmt(m))
    m = [[r.choice([10, 5, 25, 50]) for _ in range(500)] for _ in range(500)]
    for i in range(500):
        m[i][0] = 2; m[499][i] = 2
    m[250][250] = 0  # 有 0，但沿左边和下边全 2 的路径末尾零为 0 -> 答案 0
    cases.append(_fmt(m))
    cases.append(g30918(r, 700, [1, 2, 3, 5, 0], 0.0))
    return cases

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
    cases=build_cases()
    assert cases[0]==SAMPLE
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
