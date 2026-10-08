import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    it = iter(data)\n    n, k = int(next(it)), int(next(it))\n    \n    counts = {}\n    last_owner = {}\n    for p_idx in range(n):\n        for _ in range(k):\n            val = int(next(it))\n            counts[val] = counts.get(val, 0) + 1\n            last_owner[val] = p_idx # 覆盖更新，由于 p_idx 递增，最后存的是最大编号\n\n    prob_weights = [0] * n\n    for val, c in counts.items():\n        prob_weights[last_owner[val]] += c\n        \n    total = n * k\n    for w in prob_weights:\n        print(f"{w/total:.9f}")\n\nsolve()\n'
SAMPLE_IN = '3 4\n1 2 3 4\n1 2 5 6\n3 4 7 8\n'
SAMPLE_OUT = '0.000000000\n0.500000000\n0.500000000\n'
def generate_case(r):
    n = r.randint(2, 6); k = r.randint(2, 6); boards = [[r.randint(1, 20) for _ in range(k)] for _ in range(n)]
    return f"{n} {k}\n" + "\n".join(" ".join(map(str, row)) for row in boards) + "\n"


def valid(text):
    """题面契约：首行 n k（1≤n≤100，1≤k≤1000），其后恰 n 行，每行 k 个 [1,10^9] 内的整数。"""
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    def ints(line):
        parts = line.split(" ")
        if any(not p.isdigit() or (len(p) > 1 and p[0] == "0") for p in parts):
            return None
        return [int(p) for p in parts]
    first = ints(lines[0])
    if first is None or len(first) != 2:
        return False
    n, k = first
    if not (1 <= n <= 100 and 1 <= k <= 1000) or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        row = ints(line)
        if row is None or len(row) != k or any(not 1 <= v <= 10 ** 9 for v in row):
            return False
    return True


def fmt(boards):
    return f"{len(boards)} {len(boards[0])}\n" + "\n".join(" ".join(map(str, row)) for row in boards) + "\n"


def extra_cases():
    """追加的规模/边界组。n*k 都取 10^6 的约数，保证概率是有限小数（见 terminating 的说明）。"""
    r = random.Random(287480)
    out = ["4 2\n1 2\n3 4\n10 5\n7 8\n"]                      # 题面第二组样例
    out.append("1 1\n1000000000\n")                              # 最小规模
    out.append(fmt([[r.randint(1, 10 ** 9) for _ in range(1000)]]))  # n=1，k 上限
    out.append(fmt([[7] * 10 for _ in range(100)]))             # 全部同值：最慢者必最后
    out.append(fmt([[r.choice([1, 10 ** 9]) for _ in range(1)] for _ in range(100)]))  # k=1，值域两端
    # n·k=62500，值取在 10^9 附近（含边界），大量跨玩家重复
    out.append(fmt([[10 ** 9 - r.randint(0, 3000) for _ in range(625)] for _ in range(100)]))
    # 满规模 n=100,k=1000：小值域（重复极多）
    out.append(fmt([[r.randint(1, 50) for _ in range(1000)] for _ in range(100)]))
    # 满规模：中等值域
    out.append(fmt([[r.randint(1, 30000) for _ in range(1000)] for _ in range(100)]))
    # 满规模：玩家 i 只用 [1000i, 1000i+999] 内的值，互不相交 → 每人 0.01
    out.append(fmt([[1000 * i + r.randint(0, 999) for _ in range(1000)] for i in range(1, 101)]))
    # 满规模：前快后慢重叠，后一半玩家与前一半共享值
    out.append(fmt([[r.randint(1, 2000) + (i % 50) * 1000 for _ in range(1000)] for i in range(100)]))
    # n·k=50000，相邻玩家部分共享
    out.append(fmt([[r.randint(i * 100, i * 100 + 300) for _ in range(1000)] for i in range(1, 51)]))
    # n·k=1000 的中规模
    out.append(fmt([[r.randint(1, 200) for _ in range(40)] for _ in range(25)]))
    return out


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        def terminating(stdout):
            """所有概率的小数位都要能终止（<=6 位），不能是循环小数四舍五入出来的。

            题面写的是「绝对误差不超过 10^-6，保留九位小数」——也就是说它**本来就该用容差判**。
            我们的判题器只有 token 精确比对（改它属红线 1，且会影响全部已交付数据），
            于是像 1/6 = 0.166666667 这种值，另一个同样正确、只是累加顺序不同的实现
            可能给出 0.166666666，在本站被误判成 Wrong Answer。

            从数据这头绕开：只留下概率能被 10^-6 精确表示的局面，歧义就不存在了。
            实测随机局面里约 72% 满足，过滤代价很小。
            """
            for value in stdout.split():
                if len(value.split(".")[1].rstrip("0")) > 6:
                    return False
            return True

        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
                result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            else:
                for attempt in range(400):
                    content = generate_case(random.Random(28748 + index + attempt * 1000))
                    if content in seen: continue
                    result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
                    if terminating(result.stdout): break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert content not in seen and valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            assert terminating(result.stdout), index
            seen.append(content)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        assert (root / "0.out").read_text(encoding="utf-8") == SAMPLE_OUT


if __name__ == "__main__":
    main()
