import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import sys\n\ndef solve():\n    # 一次性读取所有输入，提升读取效率\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    # 将发言数转换为整数列表\n    x = [int(v) for v in input_data[1:n+1]]\n    \n    # 将发言数量从大到小排序\n    x.sort(reverse=True)\n    \n    h_index = 0\n    # 遍历排序后的数组，寻找最大的满足条件的 k\n    for i in range(n):\n        if x[i] >= i + 1:\n            h_index = i + 1\n        else:\n            break\n            \n    print(h_index)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE_IN = '22\n262 128 210 223 62 70 104 61 80 44 40 6 63 94 42 18 1 13 0 0 0 0\n'
import re
_INT = re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    """题面约束：第一行 n（1<=n<=5*10^5）；下一行 n 个整数 xi（0<=xi<=10^9）。"""
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
    return all(int(t) <= 10**9 for t in tok)

def _fmt(xs):
    return f"{len(xs)}\n" + " ".join(map(str, xs)) + "\n"

def build_cases():
    r = random.Random(30930)
    cases = [SAMPLE_IN]
    # 最小规模与边界
    cases.append(_fmt([0]))
    cases.append(_fmt([1]))
    cases.append(_fmt([10**9]))
    cases.append(_fmt([0, 0, 0, 0, 0]))
    cases.append(_fmt([1, 1, 1, 1]))            # 答案 1
    cases.append(_fmt([5, 5, 5, 5, 5]))         # h = n
    cases.append(_fmt([3, 3, 3, 3, 3]))         # h < n，大量相等
    cases.append(_fmt([10, 8, 5, 2, 1]))        # 题面举例
    cases.append(_fmt([0, 10**9]))
    # 小规模随机（可暴力核对）
    for k in range(15):
        n = r.randint(1, 30)
        hi = [5, 30, 1000, 10**9][k % 4]
        cases.append(_fmt([r.randint(0, hi) for _ in range(n)]))
    # 中等规模
    for n in (500, 2000, 5000):
        cases.append(_fmt([r.randint(0, 2 * n) for _ in range(n)]))
    # 恰好在 h 附近堆积相等值（容易差一）
    xs = [700] * 700 + [699] * 300 + [r.randint(0, 698) for _ in range(1000)]
    r.shuffle(xs); cases.append(_fmt(xs))
    xs = [700] * 699 + [701] + [r.randint(0, 699) for _ in range(1300)]
    r.shuffle(xs); cases.append(_fmt(xs))
    # 大规模（单个文件 <= 1MB）
    cases.append(_fmt([r.randint(0, 10**9) for _ in range(90000)]))            # h 接近 n，卡 O(n^2)
    cases.append(_fmt(sorted(r.randint(10**8, 10**9) for _ in range(90000))))  # 升序，h = n
    cases.append(_fmt([r.randint(0, 200000) for _ in range(120000)]))
    xs = list(range(150000)); r.shuffle(xs); cases.append(_fmt(xs))             # 0..n-1 的排列
    cases.append(_fmt(list(range(150000, 0, -1))))                             # 降序 n..1，h = n/2
    cases.append(_fmt([r.randint(0, 9) for _ in range(500000)]))               # n 取上限，值很小
    cases.append(_fmt([0] * 499999 + [10**9]))                                 # n 取上限，答案 1
    cases.append(_fmt([0] * 500000))                                           # n 取上限，答案 0
    cases.append(_fmt([r.choice([0, 1, 2, 3, 99]) for _ in range(450000)]))
    xs = [60000] * 60000 + [r.randint(0, 59999) for _ in range(40000)]
    r.shuffle(xs); cases.append(_fmt(xs))
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
