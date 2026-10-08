"""9198 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 9198
SAMPLE_IN = '{}[(){}]()\n'
SAMPLE_OUT = 'Yes\n'
REFERENCE_SOURCE = 'def is_beautiful_brackets(sequence):\n    stack = []\n    # 对应关系字典，键为右括号，值为对应的左括号\n    bracket_pairs = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}\n    \n    for bracket in sequence:\n        if bracket in bracket_pairs.values():\n            # 若是左括号，压入栈中\n            stack.append(bracket)\n        elif bracket in bracket_pairs:\n            # 若是右括号，检查栈顶元素是否匹配\n            if stack and stack[-1] == bracket_pairs[bracket]:\n                stack.pop()\n            else:\n                return "No"\n        else:\n            # 输入不合法的字符时，直接返回No\n            return "No"\n    # 栈为空表示括号序列美观\n    return "Yes" if not stack else "No"\n\n# 输入处理\nsequence = input().strip()\n\n# 输出结果\nprint(is_beautiful_brackets(sequence))\n'

def g9198(r):
    pairs = ["()", "[]", "{}"]
    text = "".join(r.choice(pairs) for _ in range(r.randint(2, 20)))
    if r.random() < .5: text = text[:-1] + r.choice(")]}{")
    return text + "\n"

def valid(text):
    """题面：一行括号序列，只含 ()[]{}，长度不超过 10000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    body = text[:-1]
    return len(body) <= 10000 and all(c in "()[]{}" for c in body)


def nested(r, pairs):
    """随机生成恰含 pairs 对括号的美观序列（随机嵌套 + 并列）。"""
    out, stack, opened = [], [], 0
    while opened < pairs or stack:
        if opened < pairs and (not stack or r.random() < .5):
            c = r.choice("([{")
            stack.append(c)
            out.append(c)
            opened += 1
        else:
            out.append({"(": ")", "[": "]", "{": "}"}[stack.pop()])
    return "".join(out)


def extra_cases():
    """2026-10 审计补充：原数据只有并列的 () [] {}，没有任何嵌套，
    只查相邻配对或只数各类括号个数的写法都能过；最长也只有约 40 字符。"""
    r = random.Random(91980)
    out = ["(", ")", "()", ")(", "([)]", "{[()]}", "{[(])}", "(((", ")))", "[(])",
           "((([[[{{{}}}]]])))", "{}{}{}{}{}{}{}{}{}{}(}"]
    out.append("(" * 5000 + ")" * 5000)                       # 深嵌套 Yes
    out.append("[" * 5000 + ")" * 5000)                       # 深嵌套类型全错 No
    out.append("{" * 4999 + "()" + "}" * 4999)                 # Yes
    for pairs in (50, 300, 2000, 5000, 5000):
        out.append(nested(r, pairs))                          # Yes
    for pairs in (50, 300, 2000, 5000):                       # 换掉一个括号的类型 No
        t = list(nested(r, pairs))
        k = r.randrange(len(t))
        t[k] = r.choice([c for c in "()[]{}" if c != t[k] and
                         (c in "([{") == (t[k] in "([{")])
        out.append("".join(t))
    t = nested(r, 4999)
    out.append(t + "(]")                                     # 只在末尾出错 No
    out.append(nested(r, 2500) + ")" + nested(r, 2499) + "(") # 个数平衡但次序错 No
    out.append(nested(r, 4999) + "(")                          # 奇数长度 No
    return [c + "\n" for c in out]


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g9198(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for c in extra_cases():
        if c not in cases:
            cases.append(c)
    assert all(valid(c) for c in cases), "题面：只含 ()[]{}，长度不超过 10000"
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
