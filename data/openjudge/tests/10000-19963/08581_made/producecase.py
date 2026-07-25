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


def make(rng, depth):
    if depth == 0 or rng.random() < .25:
        return "."
    return rng.choice("ABCDEFGH") + make(rng, depth - 1) + make(rng, depth - 1)


def build_cases():
    cases = [SAMPLE_IN, ".\n", "A..\n"]
    for index in range(1, 60):
        if len(cases) >= 21:
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
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    for c in cases:
        body = c.strip()
        assert set(body) <= set("ABCDEFGH."), "题面：只由大写字母或 . 组成"
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
