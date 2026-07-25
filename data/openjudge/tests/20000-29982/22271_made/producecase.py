import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import Counter\n\ndef main():\n    # 读取输入\n    input_data = sys.stdin.read().strip().split(\'\\n\')\n    N = int(input_data[0])  # 树的总数\n    tree_names = input_data[1:]  # 每棵树的种类名称\n\n    # 统计每种树的数量\n    tree_counter = Counter(tree_names)\n\n    # 按字典序排序\n    sorted_trees = sorted(tree_counter.items())\n\n    # 输出结果\n    for tree, count in sorted_trees:\n        percentage = (count / N) * 100\n        print(f"{tree} {percentage:.4f}%")\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '4\nApple\nCherry\nPear\nPeach\n'
SAMPLE_OUT = 'Apple 25.0000% \nCherry 25.0000%\nPeach 25.0000%\nPear 25.0000%\n'
def generate_case(r):
    names = ["Oak", "Pine", "Birch", "Maple", "Cedar", "Elm"]; n = r.randint(5, 30); values = [r.choice(names) for _ in range(n)]
    return str(n) + "\n" + "\n".join(values) + "\n"

assert SAMPLE_IN == '4\nApple\nCherry\nPear\nPeach\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22271 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
