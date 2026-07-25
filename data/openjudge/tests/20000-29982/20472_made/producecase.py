"""20472 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20472
SAMPLE_IN = 'GGLLGG\n'
SAMPLE_OUT = '1\n'
REFERENCE_SOURCE = "def is_robot_making_loop(commands):\n    # 初始位置和方向\n    x, y = 0, 0\n    direction = 'N'\n\n    # 方向变换的规则，用字典表示\n    left_turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}\n    right_turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}\n\n    # 模拟机器人的移动\n    for command in commands:\n        if command == 'G':\n            if direction == 'N':\n                y += 1\n            elif direction == 'S':\n                y -= 1\n            elif direction == 'E':\n                x += 1\n            elif direction == 'W':\n                x -= 1\n        elif command == 'L':\n            direction = left_turns[direction]\n        elif command == 'R':\n            direction = right_turns[direction]\n\n    # 如果机器人回到原点，或者不是面向北方（说明它会改变方向然后可能回到原点）\n    return (x == 0 and y == 0) or direction != 'N'\n\n# 读取输入并输出结果\ncommands = input().strip()\nprint(1 if is_robot_making_loop(commands) else 0)\n\n"

def g20472(r): return "".join(r.choice("GLR") for _ in range(r.randint(1,20)))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20472(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
