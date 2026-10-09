#!/usr/bin/env python3
"""31378 KMP 字符比较次数（nextval）—— 生成器、输入契约与数据构建。

这道题先作为私有题 1000000 出好（`tests/private/1000000_made/`，只有 GMyhf 看得到），再用
oj-problem-tools 发到平台成为 practice/31378，平台上传的就是 1000000 那份数据。所以这里的
随机种子沿用 1000000（`SEED_NUMBER`），产出与私有版、与平台**逐字节相同** —— 改了种子，
本站与平台就是两套数据。两份目录要改一起改，`tests/test_private_1000000.py` 盯着两边一致。
第 0 组是题面样例（答案 31 19，构建时逐字比对）。形状按错法排：

  · `chain`    —— 模式串里 p[j] == p[next[j]] 成串出现（AAAA…B、ABABAB…C）：
                  用普通 next 而不是 nextval 的写法在这里多比很多次。
  · `minus`    —— nextval 里有大量 -1（模式串首字母反复出现）：把「j == -1 后移」
                  也计成一次比较的写法在这里挂。
  · `end`      —— 唯一一次匹配在主串末尾；`start` —— 主串开头就匹配：
                  匹配后不停、继续数下去的写法挂在 start，下标差一挂在两头。
  · `none`     —— 主串里没有模式串：位置应为 -1，比较次数一直数到主串扫完。
  · `equal`    —— |p| = |t|；`single` —— |p| = 1。
  · `random` / `big` —— 小字母表随机、题面上界 |t| = 10^5。
"""
import random

NUMBER = 31378
SEED_NUMBER = 1000000          # 见文件开头：与私有版 1000000、平台 31378 同一份数据
INPUT_DOMAIN = "第一行是模式串 p，第二行是主串 t，均只含大写英文字母，1 <= |p| <= |t| <= 100000"
SAMPLES = [
    ("BAAABBBAA\nBAAABBBCDDDCCHHHHBBBAAABBBAADD\n", "31 19\n"),
]
MAX_LEN = 10 ** 5
SHAPES = ("chain", "minus", "end", "start", "none", "equal", "single", "random", "big", "chain")


def word(rng, length, alphabet="AB"):
    return "".join(rng.choice(alphabet) for _ in range(length))


def render(p, t):
    return f"{p}\n{t}\n"


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "chain":
        # 主串由「模式串去掉最后一个字符 + 一个失配字符」反复拼成，每段都在末位失配后沿链回退
        unit = rng.choice(("A", "AB", "ABA", "AAB"))
        body = (unit * (rng.randint(2, 400) // len(unit) + 1))[:rng.randint(2, 400)]
        p = body + "C"
        n = rng.randint(len(p) * 5, 20000 if seed < 10 else MAX_LEN)
        parts = []
        while sum(map(len, parts)) < n:
            parts.append(body[:rng.randint(1, len(body))] + rng.choice("ABD"))
        t = "".join(parts)[:n - len(p)] + p if seed % 2 else "".join(parts)[:n]
        return render(p, t)
    if shape == "minus":
        head = rng.choice("ABC")
        p = "".join(head if rng.random() < 0.5 else rng.choice("ABCD".replace(head, ""))
                    for _ in range(rng.randint(5, 60)))
        p = head + p
        t = word(rng, rng.randint(len(p), 30000), "ABCD")
        return render(p, t)
    if shape == "end":
        p = word(rng, rng.randint(3, 50), "ABC") + "D"
        t = word(rng, rng.randint(1, 40000), "ABC") + p   # D 只在末尾出现，匹配唯一
        return render(p, t)
    if shape == "start":
        p = word(rng, rng.randint(1, 50))
        t = p + word(rng, rng.randint(0, 40000))
        return render(p, t)
    if shape == "none":
        p = word(rng, rng.randint(2, 200)) + "Z"
        t = word(rng, rng.randint(len(p), 60000))
        return render(p, t)
    if shape == "equal":
        p = word(rng, rng.randint(1, 5000))
        t = p if seed < 10 else p[:-1] + ("B" if p[-1] == "A" else "A")
        return render(p, t)
    if shape == "single":
        p = rng.choice("ABCXYZ")
        t = word(rng, rng.randint(1, 50000), "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace(p, "")) + p
        return render(p, t)
    if shape == "big":
        p = word(rng, rng.randint(10, 30)) if seed < 10 else ("AB" * 5000)[:rng.randint(1000, 9999)] + "A"
        return render(p, word(rng, MAX_LEN) if seed < 10 else ("AB" * MAX_LEN)[:MAX_LEN - 1] + "B")
    p = word(rng, rng.randint(1, 12), "ABC"[:rng.randint(2, 3)])
    return render(p, word(rng, rng.randint(len(p), 20000), "ABC"[:rng.randint(2, 3)]))


def valid(text):
    """照题面：恰两行，各为非空大写字母串，1 <= |p| <= |t| <= 10^5。"""
    if not text.endswith("\n") or "\r" in text:
        return "应以换行结尾且不含 \\r"
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return "应为 2 行"
    p, t = lines
    for name, s in (("p", p), ("t", t)):
        if not s or not all("A" <= c <= "Z" for c in s):
            return f"{name} 不是非空大写字母串"
    if not 1 <= len(p) <= len(t) <= MAX_LEN:
        return f"|p|={len(p)} |t|={len(t)} 越界"
    return True


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
TOTAL = 21


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [text for text, _answer in SAMPLES]
    cases += [generate(SEED_NUMBER, seed) for seed in range(1, TOTAL - len(SAMPLES) + 1)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if valid(case) is not True:
            raise SystemExit(f"case {index} violates the input contract: {valid(case)}")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=120, check=True)
        if index < len(SAMPLES) and result.stdout != SAMPLES[index][1]:
            raise SystemExit(f"第 {index} 组与题面样例输出不符：{result.stdout!r} != {SAMPLES[index][1]!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()
