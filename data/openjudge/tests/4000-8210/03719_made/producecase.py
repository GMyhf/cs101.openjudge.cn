"""3719 学生信息用qsort排序 测试数据生成器：固定种子，重跑可逐字节复现 data/。

题面约束（valid() 逐条核）：
  - 每个学生两行：名字（英文字母和空格，最长 18 个字符），"学号,性别 年龄"；
  - 学号是不超过 100000 的整数，性别 'M'/'F'，年龄不大于 100 的整数；
  - 末尾可能有若干个回车，也可能没有；学生不超过 100 个；
  - 不会出现两个学生的名字仅大小写有差别（生成时名字按小写也互不相同，排序结果唯一）。

2026-10 审计修正：原生成器给名字拼了 " 0"、" 1"… 数字后缀，39 组随机数据的名字
全部含数字，越出「由英文字母和空格构成」；学生数最多 8 个，名字只有 4 种前缀，
也没有「按 ASCII 排和按大小写无关排结果不同」的组。现在名字只用字母和空格，
混入小写开头、McDonald/Mcbride 这类内部大小写、Ann/Ann Lee/Anna 前缀关系，
学生数覆盖 1 和 100，学号覆盖 1 与 100000，末尾回车 0~3 个。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

REFERENCE_SOURCE = 'import sys\nlines=sys.stdin.read().splitlines()\nwhile lines and not lines[-1].strip(): lines.pop()\nn=len(lines)//2; rows=[]\nfor i in range(n):\n    name=lines[2*i]; a=lines[2*i+1].split()\n    ident,sex=a[0].split(","); age=a[1]\n    rows.append((name, i, ident, sex, age))\nfor x in sorted(rows,key=lambda z:z[0].lower()):\n    print(x[0]); print(f"{int(x[2]):08d},{x[3]} {x[4]}")\n'
SAMPLE_IN = 'Tom Hanks\n7863,M 18\nMary Lu\n18343,F 21\nSanta Fe\n27863,M 17\n'
SAMPLE_OUT = 'Mary Lu\n00018343,F 21\nSanta Fe\n00027863,M 17\nTom Hanks\n00007863,M 18\n'
NAME_RE = re.compile(r"[A-Za-z ]{1,18}")
INFO_RE = re.compile(r"(0|[1-9]\d*),([MF]) (0|[1-9]\d*)")


def valid(text):
    if "\r" in text:
        return False
    body = text.rstrip("\n")
    lines = body.split("\n")
    if body == "" or len(lines) % 2 or not 1 <= len(lines) // 2 <= 100:
        return False
    seen = set()
    for i in range(0, len(lines), 2):
        name, info = lines[i], lines[i + 1]
        if not NAME_RE.fullmatch(name) or not re.search(r"[A-Za-z]", name):
            return False
        if name.lower() in seen:
            return False
        seen.add(name.lower())
        m = INFO_RE.fullmatch(info)
        if not m or int(m.group(1)) > 100000 or int(m.group(3)) > 100:
            return False
    return True


WORDS = ["Tom", "Hanks", "Mary", "Lu", "Santa", "Fe", "Ann", "Anna", "Lee", "bob", "Bob", "alice",
         "Zoe", "zack", "McDonald", "Mcbride", "MacArthur", "de", "Van", "von", "Li", "Wang", "Xu",
         "a", "B", "Z", "y", "Eve", "eva", "Oscar", "oScar", "QQ", "John", "Smith", "jane", "Doe",
         "Kim", "Yu", "Abe", "abel", "Ab", "Jack", "Jackson"]


def make_name(r):
    while True:
        k = r.choice([1, 1, 2, 2, 2, 3])
        ws = []
        for _ in range(k):
            w = r.choice(WORDS)
            t = r.random()
            if t < .15:
                w = w.lower()
            elif t < .25:
                w = w.upper()
            ws.append(w)
        name = " ".join(ws)
        if len(name) <= 18:
            return name


def gen(r, n, tail):
    names, seen = [], set()
    # 前缀 / 内部大小写 / 小写开头这几类先放进去
    for fixed in r.sample(["Ann", "Ann Lee", "Anna", "McDonald", "Mcbride", "bob", "Alice", "Carl",
                           "a", "B", "Abcdefghijklmnopqr"], min(n, r.randint(0, 6))):
        names.append(fixed)
        seen.add(fixed.lower())
    while len(names) < n:
        name = make_name(r)
        if name.lower() not in seen:
            seen.add(name.lower())
            names.append(name)
    r.shuffle(names)
    rows = []
    for name in names:
        t = r.random()
        ident = 100000 if t < .05 else r.randint(0, 9) if t < .15 else r.randint(1, 100000)
        age = r.choice([0, 1, 100]) if r.random() < .1 else r.randint(5, 99)
        rows.append(f"{name}\n{ident},{r.choice('MF')} {age}")
    return "\n".join(rows) + "\n" * tail


def build_cases():
    cases = [SAMPLE_IN]
    specials = [(1, 0), (1, 1), (1, 3), (2, 1), (100, 1), (100, 0), (100, 3), (99, 2)]
    for k, (n, tail) in enumerate(specials):
        cases.append(gen(random.Random(37190 + k), n, tail))
    k = 0
    while len(cases) < 40:
        k += 1
        r = random.Random(3719 * 1000 + k)
        n = r.choice([r.randint(2, 10), r.randint(10, 40), r.randint(40, 100)])
        c = gen(r, n, r.choice([0, 1, 1, 1, 2, 3]))
        if c not in cases:
            cases.append(c)
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            if index == 0:
                assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
