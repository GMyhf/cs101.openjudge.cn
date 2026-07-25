import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def is_isomorphic(s, t):\n    if len(s) != len(t):\n        return "NO"\n    \n    # 创建两个映射表\n    s_to_t = {}\n    t_to_s = {}\n    \n    for i in range(len(s)):\n        char_s = s[i]\n        char_t = t[i]\n        \n        # 检查 s 到 t 的映射\n        if char_s in s_to_t:\n            if s_to_t[char_s] != char_t:\n                return "NO"\n        else:\n            s_to_t[char_s] = char_t\n        \n        # 检查 t 到 s 的映射\n        if char_t in t_to_s:\n            if t_to_s[char_t] != char_s:\n                return "NO"\n        else:\n            t_to_s[char_t] = char_s\n    \n    return "YES"\n\n# 输入\ns = input().strip()\nt = input().strip()\n\n# 输出结果\nprint(is_isomorphic(s, t))\n'
SAMPLE_IN = 'paper\ntitle\n'
def generate_case(r):
    alphabet = "abcdefg"
    first = r.sample(alphabet, 2)
    s = "".join(first) + "".join(r.choice(alphabet) for _ in range(r.randint(0, 28)))
    mapping = {}; available = list(alphabet); t = []
    for ch in s:
        if ch not in mapping: mapping[ch] = r.choice(available); available.remove(mapping[ch])
        t.append(mapping[ch])
    if r.random() < .5: t[1] = t[0]
    assert len(s) == len(t)
    return s + "\n" + "".join(t) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29455 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
