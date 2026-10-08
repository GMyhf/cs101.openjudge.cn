import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）\nn=int(input())\nfor _ in range(n):\n    s1,s2=input().split()\n    pos=[]\n    start=0\n    while True:\n        po=s1.find(s2,start)\n        if po==-1:\n            break\n        pos.append(po)\n        start=po+1\n    if pos:\n        for po in pos:\n            print(po,end=' ')\n        print('')\n    else:\n        print('no')\n"
SAMPLE_IN = '4\nababcdefgabdefab ab\naaaaaaaaa a\naaaaaaaaa aaa \n112123323 a\n'
SAMPLE_OUT = '0 2 9 14 \n0 1 2 3 4 5 6 7 8 \n0 1 2 3 4 5 6 \nno\n'
def valid(text):
    """题面：首行整数 n；接下来 n 行，每行两个不带空格的字符串 txt pat，
    0 < len(pat) <= len(txt) < 2*10^7。题面样例第 3 行带行尾空格，故只容忍行尾空白。"""
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    if not lines or not lines[0].isdigit() or (len(lines[0]) > 1 and lines[0][0] == "0"):
        return False
    n = int(lines[0])
    if n < 1 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        body = line.rstrip(" ")
        parts = body.split(" ")
        if len(parts) != 2 or any(not p or any(c.isspace() for c in p) for p in parts):
            return False
        txt, pat = parts
        if not (0 < len(pat) <= len(txt) < 2 * 10**7):
            return False
    return True

def _rand(r, alpha, k):
    return "".join(r.choice(alpha) for _ in range(k))

def _small(r):
    pairs = []
    for _ in range(r.randint(2, 30)):
        alpha = r.choice(["ab", "abcd", "a", "0123456789"])
        txt = _rand(r, alpha, r.randint(1, 40))
        kind = r.random()
        if kind < 0.3:  # 取 txt 的子串，保证出现
            i = r.randrange(len(txt)); j = r.randint(i + 1, min(len(txt), i + 8))
            pat = txt[i:j]
        elif kind < 0.4:  # pat 与 txt 等长
            pat = txt if r.random() < 0.5 else _rand(r, alpha + "z", len(txt))
        else:
            pat = _rand(r, alpha + ("x" if r.random() < 0.2 else ""), r.randint(1, min(8, len(txt))))
        pairs.append((txt, pat))
    return pairs

def generate_case(r, index):
    if index <= 9:
        pairs = _small(r)
    elif index == 10:  # 最小：单字符
        pairs = [("a", "a"), ("a", "b"), ("ab", "b"), ("ba", "ab")]
    elif index == 11:  # 长全 a 串配长 pat 加一位不同：答案 no，卡 O(len(txt)*len(pat)) 朴素匹配
        pairs = [("a" * 600000, "a" * 350000 + "b")]
    elif index == 12:  # 同上，失配字符在开头
        pairs = [("a" * 600000, "b" + "a" * 350000)]
    elif index == 13:  # 周期串，大量重叠匹配（输出约 1MB）
        pairs = [("ab" * 150000, "ab" * 50)]
    elif index == 14:  # 长随机二元串，短 pat
        txt = _rand(r, "ab", 990000)
        pairs = [(txt, _rand(r, "ab", 12))]
    elif index == 15:  # pat 与 txt 等长且相同，以及只差末位
        txt = _rand(r, "abc", 240000)
        pairs = [(txt, txt), (txt, txt[:-1] + ("a" if txt[-1] != "a" else "b"))]
    elif index == 16:  # 匹配只在最后一个位置
        pairs = [("a" * 600000 + "b", "a" * 1000 + "b")]
    elif index == 17:  # 多行中等规模
        pairs = []
        for _ in range(200):
            txt = _rand(r, "ab", r.randint(1000, 4000))
            i = r.randrange(len(txt) - 20)
            pairs.append((txt, txt[i:i + r.randint(1, 20)]))
    elif index == 18:  # 1000 行小串
        pairs = [(_rand(r, "ab", r.randint(1, 30)), _rand(r, "ab", 1)) for _ in range(1000)]
    else:  # 长随机串 + 取自 txt 的长 pat
        txt = _rand(r, "abcdefghij", 850000)
        pairs = [(txt, txt[123456:123456 + 50000]), (txt[:40000], txt[39990:40000])]
    assert all(0 < len(p) <= len(t) < 2 * 10**7 for t, p in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{t} {p}" for t, p in pairs) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(26999 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
