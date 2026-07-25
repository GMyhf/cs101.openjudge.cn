#!/usr/bin/env python3
"""机械判定 oracle 是不是参考解法的转写。

`t004_oracle_policy.py` 声明的是「不同算法族」，但它的三条断言里有两条走
`contract()` 时结构上不可能为假（`conceptual_bug_independence` 硬编码 True，
两个 family 由 `FAMILY_PAIRS` 保证不同），实际只校验了「理由非空」。
声明与代码之间没有任何连接——可以一边声明 dp_vs_enumeration，一边交两份
逐字符相同的 `bin(x^y).count("1")`。

这个模块补上一段机械连接：把两份源码的标识符全部抹平、只留 AST 结构，再比相似度。

**它是下限，不是判据。**首轮 10 对实测（人工阅读判定的 5 对转写标 ✗）：

    3263 ✗ 0.96   3712 ✗ 0.87   3421 ✗ 0.55   3710 ✗ 0.55   3714 ✓ 0.51
    3709 ~ 0.48   3711 ✓ 0.46   3708 ✗ 0.41   3527 ~ 0.34   3376 ✓ 0.21

0.80 阈值只抓到 5 对里的 2 对（3263、3712 是「照抄改变量名」）。
抓不到的两类：①同一计算换个写法（3708 的 for 循环 vs 生成器表达式）；
②同一算法换个函数拆分（3421）。而且 3421/3710 的 0.55 与真独立的 3714 的 0.51 已经重叠，
**不存在能干净分开两者的阈值**。

所以用法是：`--check` 挡住 0.80 以上的明显转写（零判断力即可执行），
排序靠前的几对仍然必须人工读一遍。**不要把它当成「独立性已验证」的证据。**

    python3 scripts/t004_oracle_similarity.py            # 打印首轮 10 对的得分排序
    python3 scripts/t004_oracle_similarity.py --check    # 超阈值即非零退出
"""
import ast
import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "data/openjudge/tests"
THRESHOLD = 0.80          # 只用于「照抄改名」这种明显情形；见模块 docstring：无法干净分开


class Skeleton(ast.NodeVisitor):
    """把 AST 压成「只有结构和运算符」的 token 序列，标识符/常量一律抹平。"""

    def __init__(self):
        self.tokens = []

    def generic_visit(self, node):
        self.tokens.append(type(node).__name__)
        super().generic_visit(node)

    def visit_Name(self, node):
        self.tokens.append("Name")

    def visit_Constant(self, node):
        self.tokens.append("Const:" + type(node.value).__name__)

    def visit_arg(self, node):
        self.tokens.append("arg")

    def visit_FunctionDef(self, node):
        self.tokens.append("FunctionDef")
        for item in node.args.args:
            self.visit(item)
        for item in node.body:
            self.visit(item)

    def visit_Attribute(self, node):
        self.tokens.append("Attribute:" + node.attr)   # 方法名保留：count/join 这类是算法指纹
        self.visit(node.value)


def skeleton(source):
    visitor = Skeleton()
    visitor.visit(ast.parse(source))
    return visitor.tokens


def similarity(left, right):
    return difflib.SequenceMatcher(None, skeleton(left), skeleton(right)).ratio()


def module_functions(tree):
    return {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}


def inline_helpers(source, functions, skip):
    """把分支里调用到的模块级辅助函数源码拼进来（传递闭包）。

    不这么做就会拿「两行的 return encode_spiral(...)」去比一份完整实现——
    3421 正是这样被我第一版漏掉的（得分 0.18，实际是逐行同构）。
    """
    seen, pending = {}, [source]
    while pending:
        chunk = pending.pop()
        for node in ast.walk(ast.parse(chunk)):
            if isinstance(node, ast.Name) and node.id in functions and node.id not in seen and node.id not in skip:
                seen[node.id] = functions[node.id]
                pending.append(ast.unparse(functions[node.id]))
    extra = "\n".join(ast.unparse(v) for _, v in sorted(seen.items()))
    return (extra + "\n" + source) if extra else source


def oracle_branches(path):
    """把 `oracle(number, content)` 拆成 {题号: 该分支源码}，最后的兜底归为 None。"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = module_functions(tree)
    func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "oracle")
    out, tail = {}, []
    for stmt in func.body:
        matched = None
        if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare):
            right = stmt.test.comparators[0]
            if isinstance(right, ast.Constant) and isinstance(right.value, int):
                matched = right.value
        if matched is None:
            tail.append(stmt)
        else:
            out[matched] = inline_helpers("\n".join(ast.unparse(x) for x in stmt.body), functions, {"oracle"})
    if tail:
        out[None] = inline_helpers("\n".join(ast.unparse(x) for x in tail), functions, {"oracle"})
    return out


def reference_source(number):
    directory = next(TESTS.glob(f"*/{number:05d}_made"), None)
    if directory is None:
        return None
    return (directory / "samplecode.py").read_text(encoding="utf-8")


def main():
    manifest = json.loads((ROOT / "collab/t004-round1-manifest.json").read_text(encoding="utf-8"))
    numbers = [x["local_number"] for x in manifest["entries"]]
    branches = oracle_branches(ROOT / "scripts/build_t004_round1.py")
    fallback = branches.get(None)
    rows, over = [], []
    for number in numbers:
        oracle_src = branches.get(number, fallback)
        ref_src = reference_source(number)
        if oracle_src is None or ref_src is None:
            print(f"  {number}: 取不到源码，失败")
            over.append(number)
            continue
        score = similarity(ref_src, oracle_src)
        rows.append((score, number))
        if score >= THRESHOLD:
            over.append(number)
    for score, number in sorted(rows, reverse=True):
        flag = "  <== 疑似转写" if score >= THRESHOLD else ""
        print(f"  {number}: 结构相似度 {score:.2f}{flag}")
    print(f"\n阈值 {THRESHOLD}：超阈值 {len(over)} 题 {over}")
    if "--check" in sys.argv and over:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
