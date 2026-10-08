import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef solve():\n    # 读取所有输入并按空格切分\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    # 第一行是 n，后面是 n 个整数\n    n = int(input_data[0])\n    # 将数组元素转为整数并放入集合中\n    nums = set(map(int, input_data[1:n+1]))\n    \n    # 从最小的正整数 1 开始查找\n    res = 1\n    while res in nums:\n        res += 1\n    \n    # 输出结果\n    print(res)\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '3\n1 2 0\n'
def generate_case(r):
    n = r.randint(1, 100); a = [r.randint(-100, 100) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a)) + "\n"


def valid(text):
    """题面契约：第一行 n（1<=n<=100）；第二行 n 个整数，-2^31<=nums[i]<=2^31-1。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    n = int(lines[0])
    if not 1 <= n <= 100:
        return False
    toks = lines[1].split(" ")
    if len(toks) != n:
        return False
    for t in toks:
        try:
            x = int(t)
        except ValueError:
            return False
        if str(x) != t or not -2**31 <= x <= 2**31 - 1:
            return False
    return True


def special_cases():
    """边界组：替换原第 30..39 组（原数据值域只有 [-100,100]，答案从未是 n+1）。"""
    r = random.Random(306460)
    fmt = lambda a: f"{len(a)}\n" + " ".join(map(str, a)) + "\n"
    lo, hi = -2**31, 2**31 - 1
    out = []
    out.append(fmt([1]))                                   # n=1，答案 2
    out.append(fmt([hi]))                                  # n=1，答案 1
    out.append(fmt([lo]))                                  # n=1，负数下界
    a = list(range(1, 101)); r.shuffle(a); out.append(fmt(a))          # 1..100 全排列，答案 101
    a = list(range(1, 100)) + [hi]; r.shuffle(a); out.append(fmt(a))   # 答案 100，含上界
    a = [r.choice([lo, hi, -1, 0, 2**31 - 2, 101, 102]) for _ in range(100)]; out.append(fmt(a))  # 无 1，答案 1
    a = [r.randint(1, 50) for _ in range(100)]; out.append(fmt(a))     # 大量重复
    a = list(range(1, 60)); a.remove(37); a += [lo] * 20 + [hi] * 22; r.shuffle(a); out.append(fmt(a))  # 答案 37
    a = [r.randint(lo, hi) for _ in range(100)]; out.append(fmt(a))    # 满值域随机
    a = [x for x in range(100, 0, -1)]; a[0] = 0; out.append(fmt(a))   # 逆序 0,99..1，答案 100
    return out


def main():
    specials = special_cases()
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 30: content = specials[index - 30]
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(30646 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and (index == 0 or content not in seen)
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
