import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef main():\n    input = sys.stdin.read\n    data = input().split()\n    \n    n = int(data[0])\n    k = int(data[1])\n    times = [int(data[2 + i]) for i in range(n)]\n    \n    # 计算总炸制时间\n    total_time = sum(times)\n    \n    # 对炸制时间进行排序\n    times.sort()\n    \n    # 初始最大持续时间为总炸制时间除以 k\n    max_time = total_time / k\n    \n    # 如果最长的炸制时间大于或等于 max_time，则需要调整 k 的值\n    if times[-1] > max_time:\n        for i in range(n - 1, -1, -1):\n            if times[i] <= max_time:\n                break\n            total_time -= times[i]\n            k -= 1\n            max_time = total_time / k\n    \n    # 输出结果，保留三位小数\n    print(f"{max_time:.3f}")\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '4 2\n5 1 1 2\n'
def valid(text):
    """题面：第一行正整数 n、k，k<=n；第二行 n 个正整数 t[i]；保证 n<=1000，0<t[i]<=1000000。"""
    if not isinstance(text, str) or not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    def nums(line):
        toks = line.split(" ")
        if any(not x.isdigit() or (len(x) > 1 and x[0] == "0") for x in toks):
            return None
        return list(map(int, toks))
    head, ts = nums(lines[0]), nums(lines[1])
    if head is None or ts is None or len(head) != 2:
        return False
    n, k = head
    if not (1 <= k <= n <= 1000) or len(ts) != n:
        return False
    return all(0 < x <= 1000000 for x in ts)

def generate_case(r, index):
    if index < 16:          # 原有的小规模随机组
        n = r.randint(2, 25); k = r.randint(1, n - 1); times = [r.randint(1, 100) for _ in range(n)]
    elif index == 16:       # 最小规模
        n, k, times = 1, 1, [r.randint(1, 1000000)]
    elif index == 17:       # k = n：答案为最小值
        n = r.randint(2, 30); k = n; times = [r.randint(1, 1000) for _ in range(n)]
    elif index == 18:       # k = 1：答案为总和
        n = 1000; k = 1; times = [r.randint(1, 1000000) for _ in range(n)]
    elif index == 19:       # 全部相同
        n = 1000; k = r.randint(1, n); times = [1000000] * n
    elif index == 20:       # 满规模 k = n
        n = 1000; k = n; times = [r.randint(1, 1000000) for _ in range(n)]
    elif index < 28:        # 少量特大值 + 大量小值，迫使贪心多次剔除
        n = r.randint(200, 1000); k = r.randint(2, min(n, 60))
        big = r.randint(1, k - 1)
        times = [r.randint(900000, 1000000) for _ in range(big)] + [r.randint(1, 1000) for _ in range(n - big)]
        r.shuffle(times)
    elif index < 34:        # 满规模随机
        n = 1000; k = r.randint(1, n); times = [r.randint(1, 1000000) for _ in range(n)]
    else:                   # 中等规模、几何分布的时间
        n = r.randint(30, 1000); k = r.randint(1, n)
        times = [min(1000000, int(1.5 ** r.uniform(0, 34))) or 1 for _ in range(n)]
    assert 0 < k <= n and all(0 < x <= 1000000 for x in times)
    return f"{n} {k}\n" + " ".join(map(str, times)) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(28701 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
