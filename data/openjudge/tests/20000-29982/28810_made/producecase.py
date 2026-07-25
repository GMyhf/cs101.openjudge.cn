import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef insert(root, val):\n    if not root:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert(root.left, val)\n    else:\n        root.right = insert(root.right, val)\n    return root\n\ndef build_bst(sequence):\n    root = None\n    for num in sequence:\n        root = insert(root, num)\n    return root\n\ndef is_same_tree(t1, t2):\n    if not t1 and not t2:\n        return True\n    if not t1 or not t2:\n        return False\n    if t1.val != t2.val:\n        return False\n    return is_same_tree(t1.left, t2.left) and is_same_tree(t1.right, t2.right)\n\n# 主程序\ndef main():\n    while True:\n        try:\n            N, L = map(int, input().split())\n            if N == 0:\n                break\n            base_seq = list(map(int, input().split()))\n            base_tree = build_bst(base_seq)\n\n            for _ in range(L):\n                check_seq = list(map(int, input().split()))\n                check_tree = build_bst(check_seq)\n                print("Yes" if is_same_tree(base_tree, check_tree) else "No")\n        except EOFError:\n            break\n\n# 示例输入运行\nif __name__ == "__main__":\n    main()\n\n'
SAMPLE_IN = '4 2\n3 1 4 2\n3 4 1 2\n3 2 4 1\n'
SAMPLE_OUT = 'Yes\nNo\n'
def generate_case(r):
    n = r.randint(2, 8); base = r.sample(range(1, 100), n); queries = []
    for _ in range(r.randint(2, 7)):
        q = base[:]; r.shuffle(q); queries.append(q)
    return f"{n} {len(queries)}\n" + " ".join(map(str, base)) + "\n" + "\n".join(" ".join(map(str, q)) for q in queries) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28810 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
