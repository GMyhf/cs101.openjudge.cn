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

LOWER = "abcdefghijklmnopqrstuvwxyz"


def valid(text):
    """题面：第一行字符串 s，第二行字符串 t（未给长度与字符集上限）。只核：恰两行、非空、无空白字符。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    for line in lines:
        if not line or any(ch.isspace() for ch in line) or not line.isprintable():
            return False
    return True


def _iso_image(r, s, alphabet=LOWER):
    """把 s 按一个随机单射映射到 alphabet，返回同构的 t。"""
    chars = sorted(set(s))
    image = r.sample(alphabet, len(chars))
    mp = dict(zip(chars, image))
    return "".join(mp[c] for c in s)


def special_case(index):
    """第 25..39 组：补长串、两种方向的失配（s->t 一对多、t->s 多对一）以及最小规模。"""
    r = random.Random(294550 + index)
    k = index - 25
    if k == 0:
        s, t = "a", "z"                       # 最小规模 YES
    elif k == 1:
        s, t = "ab", "aa"                     # 多对一 -> NO
    elif k == 2:
        s, t = "aa", "ab"                     # 一对多 -> NO（只检查 t->s 的写法会错判）
    elif k == 3:
        s = LOWER * 40                        # 全字母表长串，映射成自身打乱 -> YES
        t = _iso_image(r, s)
    elif k in (4, 5, 6):
        # 长串 YES
        n = [1000, 3000, 5000][k - 4]
        sigma = r.sample(LOWER, r.randint(5, 26))
        s = "".join(r.choice(sigma) for _ in range(n))
        t = _iso_image(r, s)
    elif k in (7, 8, 9):
        # 长串，末尾附近制造 s 中同一字符对应 t 中两个不同字符（单向检查只看 t->s 会错）
        n = [800, 2500, 5000][k - 7]
        sigma = r.sample(LOWER, r.randint(4, 20))
        s = list("".join(r.choice(sigma) for _ in range(n)))
        t = list(_iso_image(r, "".join(s)))
        pos = n - 1 - r.randint(0, 5)
        c = s[pos]
        used = set(t)
        fresh = [x for x in LOWER if x not in used]
        # 让 t[pos] 换成一个 t 中从未出现的新字符：t->s 方向仍是单射，只有 s->t 方向失配
        t[pos] = fresh[0] if fresh else t[pos]
        if not fresh:
            raise AssertionError("need a fresh char")
        s, t = "".join(s), "".join(t)
    elif k in (10, 11, 12):
        # 长串，末尾附近制造 s 中两个不同字符对应 t 中同一字符（只检查 s->t 的写法会错）
        n = [800, 2500, 5000][k - 10]
        sigma = r.sample(LOWER, r.randint(4, 20))
        s = list("".join(r.choice(sigma) for _ in range(n)))
        pos = n - 1 - r.randint(0, 5)
        others = [x for x in LOWER if x not in set(s)]
        s[pos] = others[0]                    # s 在 pos 处出现一个只出现一次的新字符
        s = "".join(s)
        t = list(_iso_image(r, s))
        t[pos] = t[pos - 1] if s[pos - 1] != s[pos] else t[0]
        t = "".join(t)
    elif k == 13:
        s, t = "paper" * 600, "title" * 600   # 样例放大 -> YES
    else:
        s = "ab" * 2500
        t = "ab" * 2499 + "aa"                # 只在最后一位失配 -> NO
    assert len(s) == len(t)
    return s + "\n" + t + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 25: content = special_case(index)
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29455 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:], index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
