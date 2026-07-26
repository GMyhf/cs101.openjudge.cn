import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）\ns=input().split('+')\na=[]\nfor k in s:\n    a.append(list(k.split('n^')))\nn=len(a)\nmax_a=float('-inf')\nfor i in range(n):\n    if a[i][0]!='0':\n        max_a=max(max_a,int(a[i][1]))\nprint(f'n^{max_a}')\n"
SAMPLE_IN = '6n^2+5n^3\n'
SAMPLE_OUT = 'n^3\n'
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

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23563 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
