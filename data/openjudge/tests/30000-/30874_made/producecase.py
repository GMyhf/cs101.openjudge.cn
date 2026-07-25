import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import deque\n\n\ndef solve():\n    # 使用 sys.stdin.read 快速读取输入，适合处理 N = 10^5 的情况\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    N = int(input_data[0])\n    players = input_data[1:]\n\n    # 初始化存储结果的数组，未组队默认为 0\n    ans = [0] * N\n\n    # 定义三个队列存储不同职责玩家的索引\n    T_q = deque()\n    H_q = deque()\n    D_q = deque()\n\n    team_count = 0\n\n    for i in range(N):\n        role = players[i]\n        if role == "T":\n            T_q.append(i)\n        elif role == "H":\n            H_q.append(i)\n        elif role == "D":\n            D_q.append(i)\n\n        # 检查是否满足组队条件：1 T, 1 H, 3 D\n        if len(T_q) >= 1 and len(H_q) >= 1 and len(D_q) >= 3:\n            team_count += 1\n            # 取出最早进入队列的 5 名符合条件的玩家\n            t_idx = T_q.popleft()\n            h_idx = H_q.popleft()\n            d1_idx = D_q.popleft()\n            d2_idx = D_q.popleft()\n            d3_idx = D_q.popleft()\n\n            # 标记他们的队伍编号\n            ans[t_idx] = team_count\n            ans[h_idx] = team_count\n            ans[d1_idx] = team_count\n            ans[d2_idx] = team_count\n            ans[d3_idx] = team_count\n\n    # 输出结果，以空格分隔\n    print(*(ans))\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '10\nD D T D H T D D H D\n'
def generate_case(r):
    n = r.randint(5, 60); roles = ["T", "H"] + ["D"] * 3
    roles += [r.choice("DTH") for _ in range(n - 5)]; r.shuffle(roles)
    assert len(roles) == n and all(x in "DTH" for x in roles)
    return f"{n}\n" + " ".join(roles) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30874 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
