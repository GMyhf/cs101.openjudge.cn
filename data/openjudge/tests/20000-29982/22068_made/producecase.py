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
