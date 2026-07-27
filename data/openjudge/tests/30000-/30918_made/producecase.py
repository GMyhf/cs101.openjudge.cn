import random
REFERENCE='# External reference: /practice/30918/statistics/\n# Accepted submission: 52760611\n# Source: http://cs101.openjudge.cn/practice/solution/52760611/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom array import array\n\n# 一次性读取所有输入并切分\ninput_data = sys.stdin.buffer.read().split()\nif not input_data:\n    sys.exit(0)\n\nn = int(input_data[0])\ntotal_elements = n * n\n\n# 预定义一个返回无穷大的常量（因为 array 不支持 float(\'inf\')，我们用一个大数代替）\nINF = 10**9 \n\ndef count_factor(x, p):\n    """计算 x 中包含质因数 p 的个数"""\n    if x == 0:\n        return INF  \n    cnt = 0\n    while x % p == 0:\n        cnt += 1\n        x //= p\n    return cnt\n\ndef solve_min_path(matrix_bytes, factor_type):\n    """\n    利用一维原生数组实现滚动 DP\n    matrix_bytes: 包含所有矩阵元素的一维字节流解析后的原生数组\n    factor_type: 2 或 5\n    """\n    # 使用 \'i\' (signed int) 创建紧凑的一维数组，极大节省内存\n    dp = array(\'i\', [INF] * n)\n    \n    # 初始化第一行第一个元素\n    first_val = int(matrix_bytes[0])\n    dp[0] = count_factor(first_val, factor_type)\n    \n    # 初始化第一行剩余元素\n    for j in range(1, n):\n        val = int(matrix_bytes[j])\n        dp[j] = dp[j-1] + count_factor(val, factor_type)\n        \n    # 逐行进行状态转移\n    row_idx = 1\n    while row_idx < n:\n        start_pos = row_idx * n\n        \n        # 处理每一行的第一个元素（第一列）\n        first_val = int(matrix_bytes[start_pos])\n        dp[0] = dp[0] + count_factor(first_val, factor_type)\n        \n        # 处理该行剩余的元素\n        for j in range(1, n):\n            val = int(matrix_bytes[start_pos + j])\n            # dp[j] 未更新前是上一行的值（正上方），dp[j-1] 是当前行已更新的值（正左方）\n            top = dp[j]\n            left = dp[j-1]\n            dp[j] = (top if top < left else left) + count_factor(val, factor_type)\n            \n        row_idx += 1\n        \n    return dp[n-1]\n\n# 将输入数据直接映射为紧凑的原生整数数组，避免 Python list 的巨大开销\nmatrix_flat = array(\'i\', (int(x) for x in input_data[1:1+total_elements]))\n\n# 检查是否存在 0\nhas_zero = any(val == 0 for val in matrix_flat)\n\n# 分别计算最少因子 2 和最少因子 5\nmin_2 = solve_min_path(matrix_flat, 2)\nmin_5 = solve_min_path(matrix_flat, 5)\n\nans = min_2 if min_2 < min_5 else min_5\n\n# 如果原矩阵中有 0，那么一定存在一条经过 0 的路径，其乘积为 0，末尾恰好有 1 个 0\nif has_zero:\n    ans = 1 if ans > 1 else ans\n\nprint(ans)'
SAMPLE='3\n1 2 3\n4 5 6\n7 8 9\n'
GENERATOR_NAME='g30918'
CPP=False
def g30918(r):
    n=r.randint(1,30); return f"{n}\n"+"\n".join(" ".join(str(r.randint(1,1000)) for _ in range(n)) for _ in range(n))+"\n"

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
