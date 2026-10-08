import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nDilworth定理:\nDilworth定理表明，任何一个有限偏序集的最长反链(即最长下降子序列)的长度，\n等于将该偏序集划分为尽量少的链(即上升子序列)的最小数量。\n因此，计算序列的最长下降子序列长度，即可得出最少需要多少台测试仪。\n"""\n\nfrom bisect import bisect_left\n\ndef min_testers_needed(scores):\n    scores.reverse()  # 反转序列以找到最长下降子序列的长度\n    lis = []  # 用于存储最长上升子序列\n\n    for score in scores:\n        pos = bisect_left(lis, score)\n        if pos < len(lis):\n            lis[pos] = score\n        else:\n            lis.append(score)\n\n    return len(lis)\n\n\nN = int(input())\nscores = list(map(int, input().split()))\n\nresult = min_testers_needed(scores)\nprint(result)\n'
SAMPLE_IN = '5\n1 7 3 5 2\n'
SAMPLE_OUT = '3\n'
def valid(text):
    """题面契约：两行；第一行 N（1<=N<=100000）；第二行恰 N 个整数，取值 0..10000。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    first = lines[0].split()
    if len(first) != 1 or not first[0].isdigit():
        return False
    n = int(first[0])
    if not 1 <= n <= 100000:
        return False
    toks = lines[1].split()
    if len(toks) != n or lines[1] != " ".join(toks):
        return False
    for t in toks:
        if not t.isdigit() or (len(t) > 1 and t[0] == "0"):
            return False
        if not 0 <= int(t) <= 10000:
            return False
    return True


def generate_case(r):
    values = [r.randint(0, 10000) for _ in range(r.randint(2, 45))]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n"


def fmt(values):
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n"


def special_cases():
    """第 11 组起：边界与满规模。"""
    r = random.Random(283890)
    cases = []
    cases.append(fmt([0]))                                   # N=1，成绩为 0
    cases.append(fmt([10000] * 7 + [0] * 5))                  # 大量相等：相等可共用一台
    cases.append(fmt(list(range(30, 0, -1))))                 # 严格下降：每人一台
    cases.append(fmt([r.choice([0, 1, 2, 10000]) for _ in range(3000)]))  # 极少取值、大量重复
    cases.append(fmt([r.randint(0, 10000) for _ in range(100000)]))       # 满规模随机
    cases.append(fmt(sorted((r.randint(0, 10000) for _ in range(100000)))))  # 满规模非降：答案 1
    # 满规模、答案约 10001：卡掉逐台线性扫描的 O(N*答案) 写法
    vals = list(range(10000, -1, -1))
    while len(vals) < 100000:
        vals.append(r.randint(0, 10000))
    pos = sorted(r.sample(range(100000), 10001))
    big = [0] * 100000
    rest_iter = iter(vals[10001:])
    k = 0
    for i in range(100000):
        if k < 10001 and i == pos[k]:
            big[i] = vals[k]; k += 1
        else:
            big[i] = next(rest_iter)
    cases.append(fmt(big))
    # 满规模、非增加序列（大量相等相邻）：bisect_left/right 用错会多算
    cases.append(fmt(sorted((r.randint(0, 10000) for _ in range(100000)), reverse=True)))
    # 满规模、锯齿：若干段严格下降拼接
    saw = []
    while len(saw) < 100000:
        top = r.randint(500, 10000)
        saw.extend(range(top, max(-1, top - r.randint(50, 500)), -1))
    cases.append(fmt(saw[:100000]))
    return cases


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        specials = special_cases()
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            elif index <= 10:
                for attempt in range(100):
                    content = generate_case(random.Random(28389 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            else:
                content = specials[index - 11]
            assert valid(content), index
            assert index == 0 or content not in seen, index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
