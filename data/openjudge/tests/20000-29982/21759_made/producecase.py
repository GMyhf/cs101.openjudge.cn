import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# gpt\ndef find_juanwang(n, x, y, grades, m, queries):\n    # 创建一个字典用于存储学生的课程和成绩\n    student_grades = {}\n\n    # 遍历成绩单，将学生的成绩添加到字典中\n    for i in range(n):\n        course, student, grade = grades[i]\n        if student not in student_grades:\n            student_grades[student] = []\n        student_grades[student].append(grade)\n\n    # 遍历查询列表，判断每个学生是否为卷王\n    results = []\n    for i in range(m):\n        student = queries[i]\n        if student in student_grades and len(student_grades[student]) >= x:\n            average_grade = sum(student_grades[student]) / len(student_grades[student])\n            if average_grade > y:\n                results.append("yes")\n            else:\n                results.append("no")\n        else:\n            results.append("no")\n\n    return results\n\n# 读取输入\nn, x, y = map(int, input().split())\ngrades = []\nfor _ in range(n):\n    course, student, grade = input().split()\n    grade = int(grade)\n    grades.append((course, student, grade))\n\nm = int(input())\nqueries = []\nfor _ in range(m):\n    query = input()\n    queries.append(query)\n\n# 调用函数进行查询\nresults = find_juanwang(n, x, y, grades, m, queries)\n\n# 输出结果\nfor result in results:\n    print(result)\n'
SAMPLE_IN = '7 3 90\nJiSuanGaiLunA XiaoWang 100\nJiSuanGaiLunA XiaoZhang 98\nGaoDengShuXue XiaoHong 90\nGaoDengShuXue XiaoWang 99\nMeiRenLiJieJiSuanJiXiTong XiaoWang 93\nPythonCongRuMengDaoFangQi XiaoHong 92\nJiSuanGaiLunA XiaoHong 88\n3\nXiaoWang\nXiaoHong\nXiaoZhang\n'
SAMPLE_OUT = 'yes\nno\nno\n'
import re

def valid(text):
    """题面：第 1 行 n x y（1<=n<=100000，x>=0，0<=y<=100）；
    接着 n 行「课程名 学生名 成绩」，名字只含字母，成绩为整数，同一学生同一课程不出现两次；
    然后一行 m（1<=m<=1000）；接着 m 行学生名，保证在前面出现过。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 3 or not all(re.fullmatch(r"0|[1-9]\d*", t) for t in head):
        return False
    n, x, y = map(int, head)
    if not (1 <= n <= 100000 and x >= 0 and 0 <= y <= 100):
        return False
    if len(lines) < n + 2:
        return False
    pairs = set(); students = set()
    for line in lines[1:n + 1]:
        toks = line.split(" ")
        if len(toks) != 3 or not re.fullmatch(r"[A-Za-z]+", toks[0]) or not re.fullmatch(r"[A-Za-z]+", toks[1]):
            return False
        if not re.fullmatch(r"-?(0|[1-9]\d*)", toks[2]) or toks[2] == "-0":
            return False
        if (toks[0], toks[1]) in pairs:
            return False
        pairs.add((toks[0], toks[1])); students.add(toks[1])
    if not re.fullmatch(r"[1-9]\d*", lines[n + 1]):
        return False
    m = int(lines[n + 1])
    if not 1 <= m <= 1000 or len(lines) != n + 2 + m:
        return False
    return all(q in students for q in lines[n + 2:])

def _name(r, lo, hi):
    return "".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(lo, hi)))

def _names(r, k, lo, hi):
    out = set()
    while len(out) < k:
        out.add(_name(r, lo, hi))
    return sorted(out)

def build(r, n_students, n_courses, n_rows, x, y, m, score=None, slen=(1, 10), clen=(2, 12)):
    """生成互不重复的 (课程, 学生) 对；查询只取出现过的学生。"""
    students = _names(r, n_students, *slen)
    courses = _names(r, n_courses, *clen)
    assert n_rows <= n_students * n_courses
    pairs = set()
    # 先保证每个学生至少一门
    for s in students[:n_rows]:
        pairs.add((r.choice(courses), s))
    while len(pairs) < n_rows:
        pairs.add((r.choice(courses), r.choice(students)))
    pairs = sorted(pairs); r.shuffle(pairs)   # 先排序：set 的遍历顺序受 hash 随机化影响
    score = score or (lambda: r.randint(0, 100))
    rows = [f"{c} {s} {score()}" for c, s in pairs]
    seen = sorted({s for _, s in pairs})
    q = [r.choice(seen) for _ in range(m)]
    return f"{len(rows)} {x} {y}\n" + "\n".join(rows) + f"\n{m}\n" + "\n".join(q) + "\n"

def generate_case(r):
    """小规模随机：4 名学生、4 门课，(课程,学生) 不重复，查询都是出现过的学生。"""
    students = ["A", "B", "C", "D"]; courses = ["Math", "CS", "Art", "Bio"]
    pairs = r.sample([(c, s) for c in courses for s in students], r.randint(5, 16))
    rows = [f"{c} {s} {r.randint(0, 100)}" for c, s in pairs]
    present = sorted({s for _, s in pairs})
    q = r.sample(present, len(present))
    return f"{len(rows)} {r.randint(1, 4)} {r.randint(40, 90)}\n" + "\n".join(rows) + f"\n{len(q)}\n" + "\n".join(q) + "\n"

def _boundary(r):
    """每个学生的课程数与平均分都卡在 x、y 附近：恰等于 x 门、平均分恰等于 y（应为 no）等。"""
    x = r.randint(2, 6); y = r.randint(60, 95)
    rows = []; names = _names(r, 400, 3, 8); courses = _names(r, 12, 3, 8)
    for s in names:
        cnt = x + r.choice([-1, 0, 0, 1])
        cnt = max(1, cnt)
        target = y * cnt + r.choice([-1, 0, 0, 1])   # 总分 = y*cnt-1 / y*cnt / y*cnt+1
        target = max(0, min(100 * cnt, target))
        sc = [target // cnt] * cnt
        for i in range(target - sum(sc)):
            sc[i] += 1
        for c, v in zip(r.sample(courses, cnt), sc):
            rows.append(f"{c} {s} {v}")
    r.shuffle(rows)
    q = [r.choice(names) for _ in range(1000)]
    return f"{len(rows)} {x} {y}\n" + "\n".join(rows) + "\n1000\n" + "\n".join(q) + "\n"

def extra_case(k):
    r = random.Random(217590 + k)
    if k == 0:   # 最小：n=1，m=1
        return "1 1 0\nA B 1\n1\nB\n"
    if k == 1:   # n=1，成绩恰等于 y（严格大于才算）
        return "1 1 100\nA B 100\n1\nB\n"
    if k == 2:   # x=0
        return build(r, 300, 10, 1500, 0, r.randint(30, 70), 1000)
    if k == 3:   # y=0，成绩含 0
        return build(r, 300, 10, 1500, 1, 0, 1000, score=lambda: r.choice([0, 0, 0, 1]))
    if k == 4:   # y=100，没人能是卷王
        return build(r, 300, 10, 1500, 0, 100, 1000)
    if k == 5:   # x 很大
        return build(r, 200, 50, 5000, 40, 50, 1000)
    if k in (6, 7, 8):
        return _boundary(r)
    if k == 9:   # 课程名与学生名有重叠、大小写不同的名字
        rows = []
        names = ["Ab", "aB", "AB", "ab", "Math"]
        courses = ["Math", "ab", "Cs", "cs"]
        for s in names:
            for c in courses:
                if r.random() < 0.8:
                    rows.append(f"{c} {s} {r.randint(50, 100)}")
        r.shuffle(rows)
        present = sorted({row.split()[1] for row in rows})
        q = [r.choice(present) for _ in range(30)]
        return f"{len(rows)} 3 75\n" + "\n".join(rows) + f"\n30\n" + "\n".join(q) + "\n"
    # 满规模 n=100000，m=1000（逐条扫描成绩单 O(nm) 会超时）。
    # 为把单组 .in 控制在 1MB 内，课程名取 1 个字母、学生名取 3 个字母。
    short = dict(slen=(3, 3), clen=(1, 1))
    kind = k % 3
    if kind == 0:
        return build(r, 20000, 30, 100000, r.randint(3, 7), r.randint(40, 70), 1000, **short)
    if kind == 1:
        return build(r, 2000, 52, 100000, r.randint(45, 55), r.randint(45, 55), 1000, **short)
    return build(r, 50000, 5, 100000, r.randint(1, 3), r.randint(50, 90), 1000,
                 score=lambda: r.choice([r.randint(0, 100), 100, 99]), **short)

def main():
    assert SAMPLE_IN == '7 3 90\nJiSuanGaiLunA XiaoWang 100\nJiSuanGaiLunA XiaoZhang 98\nGaoDengShuXue XiaoHong 90\nGaoDengShuXue XiaoWang 99\nMeiRenLiJieJiSuanJiXiTong XiaoWang 93\nPythonCongRuMengDaoFangQi XiaoHong 92\nJiSuanGaiLunA XiaoHong 88\n3\nXiaoWang\nXiaoHong\nXiaoZhang\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0:
                content = SAMPLE_IN
            elif index < 20:
                for attempt in range(100):
                    content = generate_case(random.Random(21759 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            else:
                content = extra_case(index - 20)
                assert content not in seen, index
            assert valid(content), index
            assert len(content.encode()) <= 1 << 20, index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
