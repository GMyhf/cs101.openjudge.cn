import random, re, string, subprocess, sys, tempfile
from fractions import Fraction
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/27442/\n# Accepted submission: 52825161\n# Source: http://cs101.openjudge.cn/practice/solution/52825161/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    m = int(input_data[0])\n    n = int(input_data[1])\n\n    # 记录课程权重\n    weights = {}\n    idx = 2\n    for _ in range(m):\n        course = input_data[idx]\n        weight = float(input_data[idx+1])\n        weights[course] = weight\n        idx += 2\n\n    # 计算每个学生的综合成绩\n    student_scores = {}\n    for _ in range(n):\n        student = input_data[idx]\n        course = input_data[idx+1]\n        grade = int(input_data[idx+2])\n        idx += 3\n\n        # 获取课程权重并累加成绩\n        weight = weights.get(course, 0.0)\n        score_contrib = grade * weight\n        student_scores[student] = student_scores.get(student, 0.0) + score_contrib\n\n    # 排序：\n    # 第一关键字：成绩（降序，即 -x[1]）\n    # 第二关键字：姓名（升序，即 x[0]）\n    sorted_students = sorted(student_scores.items(), key=lambda x: (-x[1], x[0]))\n\n    # 输出结果\n    for student, _ in sorted_students:\n        print(student)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3 6\njisuangailun 0.6\ngailvlun 0.3\ngaodengshuxue 0.7\nxiaoming jisuangailun 72\nxiaoming gailvlun 80\nxiaoming gaodengshuxue 60\nxiaohong jisuangailun 0\nxiaohong gailvlun 60\nxiaohong gaodengshuxue 60\n'
EXTRA_CASE=None
GENERATOR_NAME='g27442'
def g27442(r):
    # 题面“每个同学选了m个课程”：每位同学恰有 m 条记录、m 门课各一条，故 n = 人数 * m
    # （旧版每人只有一条记录，违背题面）。名字 S{i} 自带 S1/S10 这类前缀字典序陷阱。
    m, n_stu = r.randint(1, 12), r.randint(1, 30)
    courses = [f"C{i}" for i in range(m)]
    lines = [f"{c} {r.uniform(0.1, 5):.2f}" for c in courses]
    rows = []
    for i in range(n_stu):
        order = courses[:]; r.shuffle(order)
        rows += [f"S{i} {c} {r.randint(0, 100)}" for c in order]
    return f"{m} {len(rows)}\n" + "\n".join(lines + rows) + "\n"


def float_safe(text):
    """各学生综合成绩精确值：相等的只允许 m=1（单个乘积，浮点结果必然相同），否则两两差 >= 1e-6。"""
    t = text.split("\n"); m, n = map(int, t[0].split())
    w = {c: Fraction(x) for c, x in (l.split() for l in t[1:1 + m])}
    tot = {}
    for l in t[1 + m:1 + m + n]:
        a, c, sc = l.split(); tot[a] = tot.get(a, 0) + w[c] * int(sc)
    vals = sorted(tot.values())
    return all(b == a and m == 1 or b - a >= Fraction(1, 10 ** 6) for a, b in zip(vals, vals[1:]))


def base_case(s):
    for attempt in range(1000):
        c = g27442(random.Random(s if attempt == 0 else s * 1000 + attempt))
        if float_safe(c):
            return c
    raise AssertionError("no float-safe base case")

NAME_RE = re.compile(r"\S+")
WEIGHT_RE = re.compile(r"[0-9]+(\.[0-9]+)?|\.[0-9]+")
SCORE_RE = re.compile(r"-?[0-9]+")


def valid(text):
    """题面没有给数据范围，只核格式：第一行 m n；接着 m 行“课程名 权重”（课程名互异，权重为小数）；
    再 n 行“学生姓名 课程名 成绩”（课程名必须在前面出现过，成绩为整数）；
    “每个同学选了m个课程”：每位同学恰好 m 条记录，m 门课各一条。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(re.fullmatch(r"[1-9][0-9]*", x) for x in head):
        return False
    m, n = map(int, head)
    if len(lines) != 1 + m + n:
        return False
    courses = set()
    for line in lines[1:1 + m]:
        parts = line.split(" ")
        if len(parts) != 2 or not NAME_RE.fullmatch(parts[0]) or not WEIGHT_RE.fullmatch(parts[1]):
            return False
        if parts[0] in courses:
            return False
        courses.add(parts[0])
    taken = {}
    for line in lines[1 + m:]:
        parts = line.split(" ")
        if len(parts) != 3 or not NAME_RE.fullmatch(parts[0]) or parts[1] not in courses or not SCORE_RE.fullmatch(parts[2]):
            return False
        got = taken.setdefault(parts[0], set())
        if parts[1] in got:
            return False
        got.add(parts[1])
    # 题面“每个同学选了m个课程”：每位同学 m 门课各恰好一条记录
    return all(len(v) == m for v in taken.values())


def fmt_weight(w):
    s = f"{float(w):.4f}".rstrip("0").rstrip(".")
    assert Fraction(s) == w
    return s


def g_multi(r, k):
    """补充组：每个学生选全部 m 门课（题面要求），记录打乱交错，测“累加”。
    浮点安全：偶数组用 k/4 这类二进制精确的权重，允许真并列（各种求和顺序都精确）；
    奇数组用任意四位小数权重，要求不同学生的综合成绩精确值互不相同且差 >= 1e-6。"""
    dyadic = k % 2 == 0
    m = r.randint(2, 15) if k < 8 else 12
    n_stu = r.randint(5, 60) if k < 8 else 1500
    courses = []
    while len(courses) < m:
        c = "".join(r.choice(string.ascii_lowercase) for _ in range(r.randint(3, 12)))
        if c not in courses:
            courses.append(c)
    if dyadic:
        weights = [Fraction(r.randint(1, 8), 4) for _ in courses]
    else:
        weights = [Fraction(r.randint(1, 30000), 10000) for _ in courses]   # 四位小数，减少大组里的精确并列
    names = set()
    base = ["".join(r.choice(string.ascii_lowercase) for _ in range(r.randint(1, 6))) for _ in range(max(2, n_stu // 4))]
    while len(names) < n_stu:
        b = r.choice(base)
        # 刻意制造前缀关系（如 ab / abc）和相近名字，考字典序
        names.add(b + ("" if r.random() < .3 else "".join(r.choice(string.ascii_lowercase) for _ in range(r.randint(1, 4)))))
    names = sorted(names); r.shuffle(names)
    rows = []
    total = {}
    pool = [0, 100] + list(range(0, 101, 5)) if dyadic else list(range(0, 101))
    for idx, name in enumerate(names):
        take = r.sample(range(m), m)
        if dyadic and idx % 3 == 1 and rows:
            # 与前一位同学选同样的课、同样的成绩，制造并列
            prev = [x for x in rows if x[0] == names[idx - 1]]
            for _, c, sc in prev:
                rows.append((name, c, sc))
            total[name] = total[names[idx - 1]]
            continue
        acc = Fraction(0)
        for c in take:
            sc = r.choice(pool)
            rows.append((name, c, sc)); acc += weights[c] * sc
        total[name] = acc
    if not dyadic:
        vals = sorted(total.values())
        if any(b - a < Fraction(1, 10 ** 6) for a, b in zip(vals, vals[1:])):
            return None
    r.shuffle(rows)
    head = [f"{len(courses)} {len(rows)}"] + [f"{c} {fmt_weight(w)}" for c, w in zip(courses, weights)]
    return "\n".join(head + [f"{a} {courses[c]} {sc}" for a, c, sc in rows]) + "\n"


def exact_answer(text):
    t = text.split("\n"); m, n = map(int, t[0].split())
    w = {c: Fraction(x) for c, x in (l.split() for l in t[1:1 + m])}
    tot = {}
    for l in t[1 + m:1 + m + n]:
        a, c, sc = l.split(); tot[a] = tot.get(a, 0) + w[c] * int(sc)
    return "".join(a + "\n" for a in sorted(tot, key=lambda a: (-tot[a], a)))


def extra_cases():
    out = []
    for k in range(10):
        for attempt in range(200):
            c = g_multi(random.Random(274420 + k * 1000 + attempt), k)
            if c is not None:
                break
        else:
            raise AssertionError("no float-safe case")
        out.append(c)
    return out


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[base_case(s) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases):
        (d/f'{i}.in').write_text(c)
        o=run(c); assert o==exact_answer(c), i
        (d/f'{i}.out').write_text(o)
if __name__=='__main__': main()
