"""8581 测试数据生成器：按深度分档生成互不相同的扩展二叉树，重跑可逐字节复现 data/。

出处：build_001a —— 2026-07-25 回归扫描修正。
原生成器固定 `make(5)` 抽 19 次、且不去重，20 组去重后只剩 13 组。
现改为按下标切换深度（2..7）并带去重重试，另外显式带上两个边界形状：
单结点 "A.." 与空树 "."。

题面保证「全部由大写字母或 . 组成」-> 生成器内断言逐组验证；
另断言每串都是一棵合法的扩展先序序列（恰好消费完、不多不少）。
"""
import random
from pathlib import Path

SAMPLE_IN = 'ABD..EF..G..C..\n'
SAMPLE_OUT = 'DBFEGAC\nDFGEBCA\n'


def solve_text(text):
    preorder = text.strip()
    pos = 0
    inorder, postorder = [], []

    def visit():
        nonlocal pos
        char = preorder[pos]
        pos += 1
        if char == ".":
            return
        visit()
        inorder.append(char)
        visit()
        postorder.append(char)

    visit()
    return "".join(inorder) + "\n" + "".join(postorder) + "\n"


def well_formed(s):
    """恰好是一棵扩展二叉树的先序序列：一次遍历用完全部字符。"""
    pos = 0

    def walk():
        nonlocal pos
        if pos >= len(s):
            raise ValueError
        c = s[pos]
        pos += 1
        if c == ".":
            return
        walk()
        walk()

    try:
        walk()
    except (ValueError, RecursionError):
        return False
    return pos == len(s)


def valid(text):
    """题面：一行扩展二叉树的先序序列，全部由大写字母或 . 组成，且恰为一棵扩展树。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    body = text[:-1]
    if not body or any(not ("A" <= c <= "Z" or c == ".") for c in body):
        return False
    # 计数法判合法：初始需 1 个槽位，字母 +1，点 -1，中途不能归零
    need = 1
    for i, c in enumerate(body):
        if need == 0:
            return False
        need += 1 if c != "." else -1
    return need == 0


def chain(letters, length, side):
    """退化链：side='L' 只挂左孩子，'R' 只挂右孩子，'Z' 左右交替。"""
    def build(i):
        if i == length:
            return "."
        c = letters[i % len(letters)]
        s = side if side != "Z" else "LR"[i % 2]
        return c + (build(i + 1) + "." if s == "L" else "." + build(i + 1))
    return build(0)


def full(letters, depth, k=[0]):
    if depth == 0:
        return "."
    c = letters[k[0] % len(letters)]
    k[0] += 1
    return c + full(letters, depth - 1, k) + full(letters, depth - 1, k)


def make_big(rng, nodes):
    """随机插入法造一棵 nodes 个结点、字母取 A..Z 的树，非递归转先序串。"""
    left, right = [-1] * nodes, [-1] * nodes
    for v in range(1, nodes):
        u = 0
        while True:
            if rng.random() < .5:
                if left[u] < 0:
                    left[u] = v
                    break
                u = left[u]
            else:
                if right[u] < 0:
                    right[u] = v
                    break
                u = right[u]
    labels = [rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(nodes)]
    out, stack = [], [0]
    while stack:
        u = stack.pop()
        if u < 0:
            out.append(".")
            continue
        out.append(labels[u])
        stack.append(right[u])
        stack.append(left[u])
    return "".join(out)


def make(rng, depth):
    if depth == 0 or rng.random() < .25:
        return "."
    return rng.choice("ABCDEFGH") + make(rng, depth - 1) + make(rng, depth - 1)


def build_cases():
    cases = [SAMPLE_IN, ".\n", "A..\n"]
    for index in range(1, 60):
        if len(cases) >= 40:
            break
        depth = 2 + index % 6
        for attempt in range(200):
            body = make(random.Random(8581 + index * 977 + attempt), depth)
            content = body + "\n"
            if content not in cases:
                cases.append(content)
                break
        else:
            raise AssertionError(f"第 {index} 组凑不出新形状")
    # 2026-10 审计补充：原数据字母只用 A..H、最长约 250 字符、没有退化链。
    # 补 Z 等全字母、左/右/之字退化链（深度 300，低于 Python 默认递归上限）、
    # 满二叉树和约 2000 结点的随机树。
    az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    extra = [chain(az, 300, "L"), chain(az[::-1], 300, "R"), chain(az, 299, "Z"),
             full(az, 9), make_big(random.Random(85810), 2000),
             make_big(random.Random(85811), 3000), "Z.Y..", "AB..."]
    for body in extra:
        content = body + "\n"
        assert content not in cases
        cases.append(content)
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    for c in cases:
        body = c.strip()
        assert valid(c), "题面：只由大写字母或 . 组成且为合法扩展先序"
        assert well_formed(body), f"不是合法的扩展先序序列: {body[:40]}"
    assert max(len(c.strip()) for c in cases) >= 40, "要有规模大一些的树"
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "参考解法跑不出样例输出"
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 08581")


if __name__ == "__main__":
    main()
