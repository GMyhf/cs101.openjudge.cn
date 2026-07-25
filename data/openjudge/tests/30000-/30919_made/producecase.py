import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import sys\nimport heapq\n\ndef solve():\n    # 快速读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    n = int(input_data[0])\n    x = [int(v) for v in input_data[1:n+1]]\n    \n    # 预分配数组\n    L = [0] * (n + 1)\n    D = [0] * (n + 1)\n    \n    heappush = heapq.heappush\n    heappop = heapq.heappop\n    \n    # 1. 计算前缀偏差和 L\n    left = []\n    right = []\n    sum_left = 0\n    sum_right = 0\n    \n    if n > 0:\n        val = x[0]\n        heappush(left, -val)\n        sum_left = val\n        L[1] = 0\n        \n    for i in range(1, n):\n        val = x[i]\n        if val <= -left[0]:\n            heappush(left, -val)\n            sum_left += val\n        else:\n            heappush(right, val)\n            sum_right += val\n            \n        len_l = len(left)\n        len_r = len(right)\n        if len_l > len_r + 1:\n            moved = -heappop(left)\n            sum_left -= moved\n            heappush(right, moved)\n            sum_right += moved\n            len_l -= 1\n            len_r += 1\n        elif len_r > len_l:\n            moved = heappop(right)\n            sum_right -= moved\n            heappush(left, -moved)\n            sum_left += moved\n            len_l += 1\n            len_r -= 1\n            \n        L[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)\n        \n    # 2. 计算后缀偏差和 D (对反转数组运行相同逻辑)\n    left = []\n    right = []\n    sum_left = 0\n    sum_right = 0\n    x_rev = x[::-1]\n    \n    if n > 0:\n        val = x_rev[0]\n        heappush(left, -val)\n        sum_left = val\n        D[1] = 0\n        \n    for i in range(1, n):\n        val = x_rev[i]\n        if val <= -left[0]:\n            heappush(left, -val)\n            sum_left += val\n        else:\n            heappush(right, val)\n            sum_right += val\n            \n        len_l = len(left)\n        len_r = len(right)\n        if len_l > len_r + 1:\n            moved = -heappop(left)\n            sum_left -= moved\n            heappush(right, moved)\n            sum_right += moved\n            len_l -= 1\n            len_r += 1\n        elif len_r > len_l:\n            moved = heappop(right)\n            sum_right -= moved\n            heappush(left, -moved)\n            sum_left += moved\n            len_l += 1\n            len_r -= 1\n            \n        D[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)\n        \n    # 3. 寻找最优分割点 t\n    min_dist = float('inf')\n    for t in range(n + 1):\n        val = L[t] + D[n - t]\n        if val < min_dist:\n            min_dist = val\n            \n    # 如果 OJ 要求的输出包含公式中的系数 2，则输出 2 * min_dist\n    # 如果 OJ 存在描述与数据不符的情况（即样例输出为 18），则此处改为 print(min_dist)\n    print(2 * min_dist)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE_IN = '9\n3 4 1 9 2 12 6 5 7\n'
def generate_case(r):
    n = r.randint(1, 40); xs = r.sample(range(1, 1000), n)
    return f"{n}\n" + " ".join(map(str, xs)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30919 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
