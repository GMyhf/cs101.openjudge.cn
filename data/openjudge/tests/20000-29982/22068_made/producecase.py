import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def is_valid_pop_sequence(origin, output):\n    if len(origin) != len(output):\n        return False  # 长度不同，直接返回False\n\n    stack = []\n    bank = list(origin)\n    \n    for char in output:\n        # 如果当前字符不在栈顶，且bank中还有字符，则继续入栈\n        while (not stack or stack[-1] != char) and bank:\n            stack.append(bank.pop(0))\n        \n        # 如果栈为空，或栈顶字符不匹配，则不是合法的出栈序列\n        if not stack or stack[-1] != char:\n            return False\n        \n        stack.pop()  # 匹配成功，弹出栈顶元素\n    \n    return True  # 所有字符都匹配成功\n\n# 读取原始字符串\norigin = input().strip()\n\n# 循环读取每一行输出序列并判断\nwhile True:\n    try:\n        output = input().strip()\n        if is_valid_pop_sequence(origin, output):\n            print('YES')\n        else:\n            print('NO')\n    except EOFError:\n        break\n\n"
SAMPLE_IN = 'abc\nabc\nbca\ncab\n'
SAMPLE_OUT = 'YES\nYES\nNO\n'
def generate_case(r):
    origin = "".join(r.sample("abcXYZ0123456789", r.randint(3, 10))); queries = []
    for _ in range(r.randint(5, 15)):
        q = list(origin); r.shuffle(q); queries.append("".join(q))
    assert len(set(origin)) == len(origin) and all(sorted(q) == sorted(origin) for q in queries)
    return origin + "\n" + "\n".join(queries) + "\n"

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def valid(text):
    """题面：首行 x 由大小写字母和数字构成、无重复字符、长度不超过 62；其后不超过 50 行，每行一个长度不超过 100 的字符串。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    x, qs = lines[0], lines[1:]
    if not (1 <= len(x) <= 62 and all(c in ALPHABET for c in x) and len(set(x)) == len(x)): return False
    if not 1 <= len(qs) <= 50: return False
    return all(1 <= len(q) <= 100 and q.isprintable() and not any(c.isspace() for c in q) for q in qs)

def extra_cases():
    """补充：x 长到 62、50 行询问；合法出栈序列（YES）与各类 NO（乱序、长度不符、混入 x 外字符、重复字符）。"""
    r = random.Random(220680); out = []
    def legal(x):
        st, res, i = [], [], 0
        while len(res) < len(x):
            if i < len(x) and (not st or r.random() < 0.5): st.append(x[i]); i += 1
            else: res.append(st.pop())
        return "".join(res)
    def near(x):          # 合法序列里交换两个位置，多半变非法
        q = list(legal(x)); a, b = r.sample(range(len(q)), 2); q[a], q[b] = q[b], q[a]; return "".join(q)
    def query(x):
        k = r.random()
        if k < 0.35: return legal(x)
        if k < 0.55: return near(x) if len(x) > 1 else x + x
        if k < 0.65: q = list(x); r.shuffle(q); return "".join(q)
        if k < 0.75:      # 长度不符：截短或加长（最长 100）
            q = legal(x)
            return q[:r.randint(1, len(q) - 1)] if len(q) > 1 and r.random() < 0.5 else (q + "".join(r.choice(ALPHABET) for _ in range(r.randint(1, 100 - len(q)))))
        if k < 0.87:      # 等长但混入 x 以外的字符
            others = [c for c in ALPHABET if c not in x]
            if not others: return legal(x)[:-1]
            q = list(legal(x)); q[r.randrange(len(q))] = r.choice(others); return "".join(q)
        q = list(legal(x))   # 等长但有重复字符
        if len(q) > 1: a, b = r.sample(range(len(q)), 2); q[a] = q[b]
        else: q = q * 2
        return "".join(q)
    for size in [62, 62, 62, 50, 40, 30, 20, 10, 5, 2]:
        x = "".join(r.sample(ALPHABET, size))
        qs = [x, x[::-1]] + [query(x) for _ in range(48)]
        out.append(x + "\n" + "\n".join(qs) + "\n")
    out.append("a\na\nb\naa\nA\n")
    out.append("Z9\nZ9\n9Z\nZ\nZ9Z\n99\n")
    return out

def main():
    assert SAMPLE_IN == 'abc\nabc\nbca\ncab\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22068 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert all(valid(c) for c in seen)

if __name__ == "__main__":
    main()
