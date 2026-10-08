import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import deque\n\n\ndef solve():\n    # 使用 sys.stdin.read 快速读取输入，适合处理 N = 10^5 的情况\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    N = int(input_data[0])\n    players = input_data[1:]\n\n    # 初始化存储结果的数组，未组队默认为 0\n    ans = [0] * N\n\n    # 定义三个队列存储不同职责玩家的索引\n    T_q = deque()\n    H_q = deque()\n    D_q = deque()\n\n    team_count = 0\n\n    for i in range(N):\n        role = players[i]\n        if role == "T":\n            T_q.append(i)\n        elif role == "H":\n            H_q.append(i)\n        elif role == "D":\n            D_q.append(i)\n\n        # 检查是否满足组队条件：1 T, 1 H, 3 D\n        if len(T_q) >= 1 and len(H_q) >= 1 and len(D_q) >= 3:\n            team_count += 1\n            # 取出最早进入队列的 5 名符合条件的玩家\n            t_idx = T_q.popleft()\n            h_idx = H_q.popleft()\n            d1_idx = D_q.popleft()\n            d2_idx = D_q.popleft()\n            d3_idx = D_q.popleft()\n\n            # 标记他们的队伍编号\n            ans[t_idx] = team_count\n            ans[h_idx] = team_count\n            ans[d1_idx] = team_count\n            ans[d2_idx] = team_count\n            ans[d3_idx] = team_count\n\n    # 输出结果，以空格分隔\n    print(*(ans))\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '10\nD D T D H T D D H D\n'
def generate_case(r):
    n = r.randint(5, 60); roles = ["T", "H"] + ["D"] * 3
    roles += [r.choice("DTH") for _ in range(n - 5)]; r.shuffle(roles)
    assert len(roles) == n and all(x in "DTH" for x in roles)
    return f"{n}\n" + " ".join(roles) + "\n"


def valid(text):
    """题面契约：第一行 N（1<=N<=1e5）；第二行 N 个字符，均为 T/H/D，用空格隔开。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    n = int(lines[0])
    toks = lines[1].split(" ")
    return 1 <= n <= 100000 and len(toks) == n and all(x in ("T", "H", "D") for x in toks)


def special_cases():
    """替换原第 30..39 组：原数据 n<=60 且每组必含一整队，缺 n<5、无人成队、大规模等情形。"""
    r = random.Random(308740)
    fmt = lambda a: f"{len(a)}\n" + " ".join(a) + "\n"
    N = 100000
    out = []
    out.append(fmt(["T"]))                                         # n=1，输出 0
    out.append(fmt(["T", "H", "D", "D"]))                          # n=4，凑不齐
    out.append(fmt(list("THDDDT")))                                # 题面样例 2
    out.append(fmt([r.choice("TDH") for _ in range(N)]))           # 满规模均匀随机
    out.append(fmt(["T"] * (N // 5) + ["H"] * (N // 5) + ["D"] * (N - 2 * (N // 5))))   # 前面长时间凑不齐，最后连成队
    a = ["D"] * (N * 3 // 5) + ["T"] * (N // 5) + ["H"] * (N // 5)
    out.append(fmt(a))                                             # H 最后才来，队伍编号与入队顺序错开
    a = [r.choice("TTTHHHD") for _ in range(N)]; out.append(fmt(a))  # D 稀缺，大量 T/H 剩下
    a = [r.choice("TDDDDDDH") for _ in range(N)]; out.append(fmt(a))  # D 过剩
    a = []
    while len(a) + 5 <= N:
        blk = list("THDDD"); r.shuffle(blk); a += blk
    out.append(fmt(a))                                             # 每 5 人恰好一队，答案最多
    out.append(fmt(["D"] * N))                                     # 全 0
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
                    content = generate_case(random.Random(30874 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and (index == 0 or content not in seen), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
