import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import sys\nimport heapq\n\ndef solve():\n    # 快速读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    n = int(input_data[0])\n    x = [int(v) for v in input_data[1:n+1]]\n    \n    # 预分配数组\n    L = [0] * (n + 1)\n    D = [0] * (n + 1)\n    \n    heappush = heapq.heappush\n    heappop = heapq.heappop\n    \n    # 1. 计算前缀偏差和 L\n    left = []\n    right = []\n    sum_left = 0\n    sum_right = 0\n    \n    if n > 0:\n        val = x[0]\n        heappush(left, -val)\n        sum_left = val\n        L[1] = 0\n        \n    for i in range(1, n):\n        val = x[i]\n        if val <= -left[0]:\n            heappush(left, -val)\n            sum_left += val\n        else:\n            heappush(right, val)\n            sum_right += val\n            \n        len_l = len(left)\n        len_r = len(right)\n        if len_l > len_r + 1:\n            moved = -heappop(left)\n            sum_left -= moved\n            heappush(right, moved)\n            sum_right += moved\n            len_l -= 1\n            len_r += 1\n        elif len_r > len_l:\n            moved = heappop(right)\n            sum_right -= moved\n            heappush(left, -moved)\n            sum_left += moved\n            len_l += 1\n            len_r -= 1\n            \n        L[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)\n        \n    # 2. 计算后缀偏差和 D (对反转数组运行相同逻辑)\n    left = []\n    right = []\n    sum_left = 0\n    sum_right = 0\n    x_rev = x[::-1]\n    \n    if n > 0:\n        val = x_rev[0]\n        heappush(left, -val)\n        sum_left = val\n        D[1] = 0\n        \n    for i in range(1, n):\n        val = x_rev[i]\n        if val <= -left[0]:\n            heappush(left, -val)\n            sum_left += val\n        else:\n            heappush(right, val)\n            sum_right += val\n            \n        len_l = len(left)\n        len_r = len(right)\n        if len_l > len_r + 1:\n            moved = -heappop(left)\n            sum_left -= moved\n            heappush(right, moved)\n            sum_right += moved\n            len_l -= 1\n            len_r += 1\n        elif len_r > len_l:\n            moved = heappop(right)\n            sum_right -= moved\n            heappush(left, -moved)\n            sum_left += moved\n            len_l += 1\n            len_r -= 1\n            \n        D[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)\n        \n    # 3. 寻找最优分割点 t\n    min_dist = float('inf')\n    for t in range(n + 1):\n        val = L[t] + D[n - t]\n        if val < min_dist:\n            min_dist = val\n            \n    # 如果 OJ 要求的输出包含公式中的系数 2，则输出 2 * min_dist\n    # 如果 OJ 存在描述与数据不符的情况（即样例输出为 18），则此处改为 print(min_dist)\n    print(2 * min_dist)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE_IN = '9\n3 4 1 9 2 12 6 5 7\n'
import re
_INT = re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    """题面约束：第一行 n（1<=n<=5*10^5）；第二行 n 个两两不同的整数 xi（1<=xi<=10^9）。"""
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if len(lines) != 2 or not _INT.match(lines[0].strip()):
        return False
    n = int(lines[0])
    if not (1 <= n <= 5 * 10**5):
        return False
    tok = lines[1].split()
    if len(tok) != n or not all(_INT.match(t) for t in tok):
        return False
    xs = list(map(int, tok))
    return all(1 <= v <= 10**9 for v in xs) and len(set(xs)) == n

def _fmt(xs):
    return f"{len(xs)}\n" + " ".join(map(str, xs)) + "\n"

def _distinct(r, n, lo, hi):
    """从 [lo, hi] 里取 n 个互不相同的数，随机顺序。"""
    if hi - lo + 1 <= 4 * n:
        xs = r.sample(range(lo, hi + 1), n)
    else:
        s = set()
        while len(s) < n:
            s.add(r.randint(lo, hi))
        xs = list(s); r.shuffle(xs)
    return xs

def build_cases():
    r = random.Random(30919)
    cases = [SAMPLE_IN]
    # 最小规模与边界值
    cases.append(_fmt([1]))
    cases.append(_fmt([10**9]))
    cases.append(_fmt([1, 10**9]))
    cases.append(_fmt([10**9, 1, 2]))
    cases.append(_fmt([1, 10**9, 2, 999999999]))   # 交错：搬家不如不搬也要正确比较
    # 小规模随机（可暴力核对）
    for k in range(18):
        n = 3 + k % 10
        cases.append(_fmt(_distinct(r, n, 1, 3 * n if k % 2 else 10**9)))
    # 中等规模
    for n in (50, 120, 200, 300):
        cases.append(_fmt(_distinct(r, n, 1, 10**9)))
    # 两簇：前半在小端、后半在大端，必须在中间搬家
    a = _distinct(r, 300, 1, 10**9)
    a.sort(); half = a[:150]; rest = a[150:]; r.shuffle(half); r.shuffle(rest)
    cases.append(_fmt(half + rest))
    # 单调序列
    cases.append(_fmt(list(range(1, 1001))))
    cases.append(_fmt(list(range(10**9, 10**9 - 1000, -1))))
    # 交错的两簇：搬家收益很小
    xs = []
    for i in range(500):
        xs.append(i + 1 if i % 2 == 0 else 10**9 - i)
    cases.append(_fmt(xs))
    # 大规模（单个文件 <= 1MB）：答案远超 32 位整数
    cases.append(_fmt(_distinct(r, 90000, 1, 10**9)))
    lo = _distinct(r, 90000, 1, 10**9); lo.sort()
    first = lo[:45000]; second = lo[45000:]; r.shuffle(first); r.shuffle(second)
    cases.append(_fmt(second + first))
    lo = _distinct(r, 90000, 1, 10**9); lo.sort()
    cases.append(_fmt(lo[::2] + lo[1::2][::-1]))
    xs = list(range(1, 140001)); r.shuffle(xs)
    cases.append(_fmt(xs))
    cases.append(_fmt(list(range(1, 140001))))
    cases.append(_fmt(_distinct(r, 120000, 1, 999999)))
    # 前 1/3 在大端、后 2/3 在小端（最优搬家点不在正中）
    lo = _distinct(r, 90000, 1, 10**9); lo.sort()
    big = lo[60000:]; small = lo[:60000]; r.shuffle(big); r.shuffle(small)
    cases.append(_fmt(big + small))
    # 几乎有序加扰动
    xs = list(range(1, 90001)); xs = [v * 11000 for v in xs]
    for _ in range(2000):
        i, j = r.randrange(90000), r.randrange(90000); xs[i], xs[j] = xs[j], xs[i]
    cases.append(_fmt(xs))
    return cases

def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert len(set(cases)) == len(cases), "存在重复测试组"
    root = Path(__file__).parent / "data"
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        for index, content in enumerate(cases):
            assert valid(content), f"第 {index} 组不满足题面约束"
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=120, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
