import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#23n2300017735(夏天明BrightSummer)\nimport re\n\nfor i in range(int(input())):\n    s, p = input(), input().replace("?", ".{1}").replace("*", ".*") + "$"\n    print("yes" if re.match(p, s) else "no")\n'
SAMPLE_IN = '3\nabc\nabc\nabc\na*c\nabc\na??c\n'
SAMPLE_OUT = 'yes\nyes\nno\n'
def generate_case(r):
    pairs = []
    for _ in range(r.randint(3, 8)):
        s = "".join(r.choice("abcd") for _ in range(r.randint(1, 10)))
        mode = r.randrange(3)
        if mode == 0: p = s
        elif mode == 1: p = "*" + s[:r.randint(0, len(s))] + "*"
        else: p = "?" * len(s)
        if r.random() < .4: p += "z"
        pairs.extend([s, p])
    assert len(pairs) % 2 == 0 and all(0 < len(x) < 50 for x in pairs)
    return str(len(pairs) // 2) + "\n" + "\n".join(pairs) + "\n"


def valid(text):
    """题面：首行 n（n<=30），后 2n 行依次为 s 与 p；s 非空仅含 a-z，p 非空仅含 a-z、? 和 *，长度均小于 50。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not (1 <= n <= 30) or len(lines) != 2 * n + 1:
        return False
    lower = set("abcdefghijklmnopqrstuvwxyz")
    for i in range(n):
        a, b = lines[1 + 2 * i], lines[2 + 2 * i]
        if not (0 < len(a) < 50 and 0 < len(b) < 50):
            return False
        if not set(a) <= lower or not set(b) <= lower | {"?", "*"}:
            return False
    return True


def _pattern_from(r, s, alpha):
    """由 s 派生模式：字符随机保留 / 换成 ? / 一段换成 *，再随机插入 *，可能再改坏一个字符。"""
    p, i = [], 0
    while i < len(s):
        x = r.random()
        if x < .45: p.append(s[i]); i += 1
        elif x < .7: p.append("?"); i += 1
        elif x < .9:
            p.append("*"); i += r.randint(0, min(6, len(s) - i))
        else:
            p.append("*")
    if r.random() < .5:
        k = r.randrange(len(p) + 1); p.insert(k, r.choice(["*", r.choice(alpha), "?"]))
    p = "".join(p)[:49] or "*"
    return p


def _pairs_case(pairs):
    assert 1 <= len(pairs) <= 30
    return str(len(pairs)) + "\n" + "".join(a + "\n" + b + "\n" for a, b in pairs)


def extra_cases():
    r = random.Random(248340)
    cases = []
    # 满规模随机：n=30，长度到 49，混合 ? 与 *
    for alpha in ("ab", "abc", "abcdefghijklmnopqrstuvwxyz"):
        pairs = []
        for _ in range(30):
            s = "".join(r.choice(alpha) for _ in range(r.randint(30, 49)))
            pairs.append((s, _pattern_from(r, s, alpha)))
        cases.append(_pairs_case(pairs))
    # 多 * 模式：* 与字母交替，长串上需要回溯。强度刻意压在正则写法（参考解即是）能过的范围内：
    # "*a" 重复到 8 次以上时 re 回溯会超过 8 秒/对，会卡掉题库里已 AC 的正则解，是否加强留给人工决定。
    trap = []
    for k in range(2, 7):
        trap.append(("a" * 49, ("*a" * k) + "b"))
        trap.append(("a" * 48 + "b", ("*a" * k) + "*b"))
        trap.append(("a" * r.randint(30, 49), ("*a" * k) + "*"))
        trap.append(("b" + "a" * r.randint(30, 48), "?" + ("*a" * k)))
    cases.append(_pairs_case(trap))
    trap2 = []
    for k in range(30):
        s = "ab" * 24 + r.choice("ab")
        p = ("*ab" * r.randint(3, 8) + "*?") + r.choice(["c", "", "*", "b", "a"])
        trap2.append((s, p[:49]))
    cases.append(_pairs_case(trap2))
    # 边界：单字符、全 ?、单个 *、长度 49、* 匹配空串、? 不匹配空串、末尾多余字符
    edge = [("a", "*"), ("a", "?"), ("a", "a"), ("a", "b"), ("a", "??"), ("a", "**"),
            ("a" * 49, "?" * 49), ("a" * 49, "?" * 48), ("a" * 48, "?" * 49), ("z" * 49, "*" * 49),
            ("abc", "abc*"), ("abc", "*abc"), ("abc", "ab*c*"), ("abc", "a*b*c*d"), ("abcd", "a*?d"),
            ("acb", "a*c"), ("cac", "a*c"), ("ac", "a?c"), ("aaac", "a?c"), ("abdc", "a*c"),
            ("mississippi", "m??*ss*?i*pi"), ("mississippi", "m*issip*?"), ("ab", "*?*?*"), ("ab", "*?*?*?*"),
            ("x", "*x*"), ("xy", "y*"), ("abcabc", "*bc"), ("abcabc", "*ab"), ("q" * 49, "q*" * 24 + "q"),
            ("q" * 48, "q*" * 24 + "q")]
    cases.append(_pairs_case(edge))
    cases.append("1\nzzzz\nz*z?\n")
    return cases


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()
        for index in range(20 + len(extras)):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20:
                content = extras[index - 20]
                if content in seen: raise AssertionError("duplicate extra case")
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24834 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
