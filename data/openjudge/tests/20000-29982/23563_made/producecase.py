import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）\ns=input().split('+')\na=[]\nfor k in s:\n    a.append(list(k.split('n^')))\nn=len(a)\nmax_a=float('-inf')\nfor i in range(n):\n    if a[i][0]!='0':\n        max_a=max(max_a,int(a[i][1]))\nprint(f'n^{max_a}')\n"
SAMPLE_IN = '6n^2+5n^3\n'
SAMPLE_OUT = 'n^3\n'
import re
_TERM = re.compile(r"(\d*)n\^(\d+)")


def valid(text):
    """题面契约：一行；若干项以 + 连接、至少一项；每项形如 n^b 或 an^b，a、b 为非负整数且 <= 10^8。
    另加生成器自己的约定：至少有一项系数非 0（全 0 时题意不明，不出这种数据）。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    terms = text[:-1].split("+")
    nonzero = False
    for t in terms:
        m = _TERM.fullmatch(t)
        if not m:
            return False
        a = int(m.group(1)) if m.group(1) else 1
        b = int(m.group(2))
        if a > 10**8 or b > 10**8:
            return False
        nonzero |= a != 0
    return nonzero


def generate_case(r):
    # 2026-07-26 补强：原来只靠 randint(0,100) 撞 0 系数，且从不刻意让**首项**系数为 0。
    # 而这题的典型错法正是「用 `(?<!\+0)` 之类的负向后顾排除零项」——它排不掉首项，
    # 于是 `0n^8+7n^5+...` 会被错答成 n^8。20 组数据一次都没覆盖到这个形状，
    # 平台判 WA 而本地对拍全过。现在每三组安排一组「首项系数为 0 且指数最大」。
    count = r.randint(2, 6)
    terms = [f"{r.randint(0, 100)}n^{r.randint(0, 30)}" for _ in range(count)]
    if r.randint(0, 2) == 0:
        top = max(int(t.split("n^")[1]) for t in terms)
        terms.insert(0, f"0n^{top + r.randint(1, 5)}")     # 零系数、指数比谁都大
    if all(term.startswith("0n^") for term in terms):
        terms[-1] = "1n^0"
    assert all(term.count("n^") == 1 and term.replace("n^", "").isdigit() for term in terms)
    assert any(not term.startswith("0n^") for term in terms), "题面保证至少有一个非零项"
    return "+".join(terms) + "\n"


def generate_extra(r, kind):
    # 2026-10 补强：原 19 组系数全部显式写出（从没有样例 2 里 `n^9` 这种省略系数的项），
    # a、b 只到 100/35，答案从没出现 n^0，也没有单项式。末 6 组换成下面这些形状。
    if kind == "sample2":
        return "99n^10+n^9+0n^100\n"
    if kind == "const":          # 非零项指数全为 0，高次项系数为 0 → n^0
        terms = [f"{r.randint(1, 10**8)}n^0", f"0n^{r.randint(1, 10**8)}", "n^0", f"0n^{r.randint(1, 50)}"]
        r.shuffle(terms)
        return "+".join(terms) + "\n"
    if kind == "single":
        return f"n^{10**8}\n"
    if kind == "bare":           # 省略系数的项是最大项；还有 0 系数项指数更大
        terms = [f"{r.randint(2, 10**8)}n^{r.randint(0, 99)}" for _ in range(5)] + ["n^100", f"0n^{10**8}"]
        r.shuffle(terms)
        return "+".join(terms) + "\n"
    if kind == "big":            # a、b 到上限；按字符串比较指数会错（9xxxxxx > 1xxxxxxx）
        terms = [f"{r.randint(1, 10**8)}n^{r.choice([9999999, 99999999, 10**8 - 1, 10**7])}" for _ in range(3)]
        terms += [f"{10**8}n^{10**8}", f"0n^{r.randint(1, 10**8)}"]
        r.shuffle(terms)
        return "+".join(terms) + "\n"
    # long：两万项，混合省略系数与 0 系数
    terms = []
    for _ in range(20000):
        a = r.choice(["", "0", str(r.randint(1, 10**8))])
        terms.append(f"{a}n^{r.randint(0, 10**8)}")
    return "+".join(terms) + "\n"


EXTRA_KINDS = ["sample2", "const", "single", "bare", "big", "long"]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        first_extra = 20 - len(EXTRA_KINDS)     # 组数保持 20（catalog 显式列出），末 6 组换成补强组
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= first_extra:
                content = generate_extra(random.Random(23563 * 7 + index), EXTRA_KINDS[index - first_extra])
                assert content not in seen
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23563 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
