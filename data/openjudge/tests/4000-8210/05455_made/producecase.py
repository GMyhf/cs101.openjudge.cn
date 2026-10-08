def solve_text(text):
    values = list(dict.fromkeys(map(int, text.split())))
    if not values: return ""
    left, right = {}, {}
    for value in values[1:]:
        cur = values[0]
        while True:
            if value < cur:
                if cur not in left: left[cur] = value; break
                cur = left[cur]
            elif value > cur:
                if cur not in right: right[cur] = value; break
                cur = right[cur]
            else: break
    queue = [values[0]]; out = []
    while queue:
        cur = queue.pop(0); out.append(str(cur))
        if cur in left: queue.append(left[cur])
        if cur in right: queue.append(right[cur])
    return " ".join(out) + "\n"


# 题面：只有一行，若干个数字（整数），空格隔开，可能重复；未给个数与值域上限。
# 提示说输入最后不带空格和回车，这里只容许末尾一个换行（判题端按行读即可）。
def valid(text):
    if text.endswith("\n"):
        text = text[:-1]
    if not text or "\n" in text or "\r" in text:
        return False
    parts = text.split(" ")
    for t in parts:
        if not t:
            return False
        u = t[1:] if t[0] == "-" else t
        if not u.isdigit():
            return False
    return True


def generate_case(rng): return " ".join(map(str, rng.sample(range(1, 200), rng.randint(3, 30)) + [1, 1, 2])) + "\n"


def line(vals): return " ".join(map(str, vals)) + "\n"


def extra_cases(rng):
    cases = []
    cases.append(line([42]))                                   # 只有一个数
    cases.append(line([7] * 15))                               # 全部重复，只剩根
    cases.append(line(list(range(1, 401))))                    # 递增，退化成右链
    cases.append(line(list(range(400, 0, -1))))                # 递减，退化成左链
    zig = []
    lo, hi = 1, 300
    while lo <= hi:                                            # 之字形链
        zig.append(lo); lo += 1
        if lo <= hi:
            zig.append(hi); hi -= 1
    cases.append(line(zig))
    v = list(range(1, 128))                                    # 完全二叉树
    def build(a):
        if not a: return []
        m = len(a) // 2
        return [a[m]] + build(a[:m]) + build(a[m + 1:])
    cases.append(line(build(v)))
    for n, hi in [(3000, 10**4), (5000, 10**9), (4000, 500), (2000, 10**6)]:
        cases.append(line([rng.randint(1, hi) for _ in range(n)]))
    cases.append(line([rng.randint(0, 9) for _ in range(200)]))  # 值域极小、大量重复，含 0
    cases.append(line(rng.sample(range(1, 100000), 1000) * 2))   # 整串重复一遍
    return cases


def main():
    import random
    from pathlib import Path
    SAMPLE_IN = '51 45 59 86 45 4 15 76 60 20 61 77 62 30 2 37 13 82 19 74 2 79 79 97 33 90 11 7 29 14 50 1 96 59 91 39 34 6 72 7\n'
    SAMPLE_OUT = '51 45 59 4 50 86 2 15 76 97 1 13 20 60 77 90 11 14 19 30 61 82 96 7 29 37 62 79 91 6 33 39 74 34 72\n'
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(5455)
    root = Path(__file__).parent / "data"
    for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)] + extra_cases(rng)):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print("generated 32 cases for 05455")


if __name__ == "__main__":
    main()
