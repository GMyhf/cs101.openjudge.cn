import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 真不玩原\nfrom collections import defaultdict\n\nn = int(input())  # 学生数量\nm = int(input())  # 核酸检测信息数量\n\n# 学生基本信息，以及核酸检测信息\nstudent_info = [list(map(int, input().split())) for _ in range(n)]\ntest_info = [list(map(int, input().split())) for _ in range(m)]\n\n# 统计每名学生的核酸检测情况\ntest_record = defaultdict(list)\nfor day, student_id in test_info:\n    test_record[student_id].append(day)\n\n# 统计未按时完成核酸检测的学生数量\nlate_count = 0\ndepartment_uncompletion = defaultdict(int)\ndepartment_total_students = defaultdict(int)\n\nfor student in student_info:\n    student_id, department = student\n    sign = False\n    a = sorted(test_record[student_id])\n    if a[0] != 1 or max(a) < 7:\n        sign = True\n    for i in range(len(a)-1):\n        if a[i+1] - a[i] > 3:\n            sign = True\n            break\n    if sign:\n        late_count += 1\n        department_uncompletion[department] += 1\n    department_total_students[department] += 1\n\n# 计算每个院系未按时完成核酸检测的学生数量占比\ndepartment_ratio = {}\nfor department in department_uncompletion.keys():\n    ratio = department_uncompletion[department] / department_total_students[department]\n    department_ratio[department] = ratio\n\n# 输出结果\nworst_department = max(department_ratio, key=department_ratio.get)\n\nprint(late_count)\nprint(worst_department)\n'
SAMPLE_IN = '3\n10\n1001 101\n1003 101\n1004 102\n1 1001\n3 1001\n6 1001\n6 1003\n1 1003\n8 1003\n4 1003\n4 1004\n7 1004\n2 1004\n'
SAMPLE_OUT = '2\n102\n'
def valid(text):
    """题面：第一行 n（学生数），第二行 m（检测信息数）；接着 n 行“学生编号 院系编号”，
    再 m 行“检测日期 学生编号”，检测日期为 1～9。学生编号应互不相同、检测记录里的学生须已登记。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    def ints(line, k):
        t = line.split(" ")
        if len(t) != k or not all(x.isdigit() for x in t): return None
        return list(map(int, t))
    if len(lines) < 2: return False
    a, b = ints(lines[0], 1), ints(lines[1], 1)
    if a is None or b is None: return False
    n, m = a[0], b[0]
    if n < 1 or len(lines) != 2 + n + m: return False
    ids = set()
    for k in range(n):
        x = ints(lines[2 + k], 2)
        if x is None or x[0] in ids: return False
        ids.add(x[0])
    for k in range(m):
        x = ints(lines[2 + n + k], 2)
        if x is None or not (1 <= x[0] <= 9) or x[1] not in ids: return False
    return True

def judge_detail(text):
    """独立实现：返回 (未完成人数, 各院系未完成比例)。每个连续三天窗口都要有检测，第 1 天必须检测。"""
    from fractions import Fraction
    lines = text.split("\n"); n = int(lines[0]); m = int(lines[1])
    st = [tuple(map(int, lines[2 + k].split())) for k in range(n)]
    rec = {}
    for k in range(m):
        d, sid = map(int, lines[2 + n + k].split()); rec.setdefault(sid, set()).add(d)
    fail, tot, cnt = {}, {}, 0
    for sid, dp in st:
        days = rec.get(sid, set())
        ok = 1 in days and all(any(d in days for d in range(w, w + 3)) for w in range(1, 8))
        tot[dp] = tot.get(dp, 0) + 1
        if not ok: cnt += 1; fail[dp] = fail.get(dp, 0) + 1
    return cnt, {d: Fraction(fail.get(d, 0), tot[d]) for d in tot}

def well_defined(text):
    """至少一人未完成，且最差院系唯一（题面未给并列规则，数据必须避开并列）。"""
    cnt, r = judge_detail(text)
    mx = max(r.values())
    return cnt > 0 and sum(1 for v in r.values() if v == mx) == 1

def schedule(r, ok):
    """第 1 天必做（两种读法都一致）；ok=True 时每个三天窗口都覆盖。"""
    if ok:
        days, cur = {1}, 1
        while cur < 7:
            cur += r.randint(1, 3); days.add(cur)
        for _ in range(r.randint(0, 3)): days.add(r.randint(1, 9))
    else:
        kind = r.randint(0, 2)
        if kind == 0:    # 中间断档 4 天以上
            a = r.randint(1, 5); b = r.randint(a + 4, 9)
            days = {1} | {d for d in range(1, 10) if (d <= a or d >= b) and r.random() < 0.7} | {a}
            days = {d for d in days if not (a < d < b)}
        elif kind == 1:  # 最后一次早于第 7 天
            last = r.randint(1, 6)
            days = {1} | {d for d in range(1, last + 1) if r.random() < 0.6} | {last}
        else:            # 恰好差一天：间隔 4
            base = r.choice([[1, 5, 8], [1, 4, 8], [1, 3, 6], [1, 2, 6, 9]])
            days = set(base)
    assert (judge_detail_days(days)) == ok, (days, ok)
    return sorted(days)

def judge_detail_days(days):
    return 1 in days and all(any(d in days for d in range(w, w + 3)) for w in range(1, 8))

def generate_case(r, n, ndept, dup=0.1):
    while True:
        sids = r.sample(range(1000, 10 ** 6), n)
        depts = r.sample(range(100, 1000), ndept)
        stu = [(sid, depts[k % ndept] if k < ndept else r.choice(depts)) for k, sid in enumerate(sids)]
        rate = {d: r.random() for d in depts}
        tests = []
        for sid, dp in stu:
            for d in schedule(r, r.random() >= rate[dp]):
                tests.append((d, sid))
                if r.random() < dup: tests.append((d, sid))
        r.shuffle(tests)
        text = f"{n}\n{len(tests)}\n" + "\n".join(f"{a} {b}" for a, b in stu) + "\n" + "\n".join(f"{a} {b}" for a, b in tests) + "\n"
        if valid(text) and well_defined(text): return text

def cases():
    out = [SAMPLE_IN]
    # 小边界：单人单院系（必须未完成）、恰好每三天一次（1 4 7 通过）、差一天（1 5 8 不过）
    out.append("1\n1\n7 9\n1 7\n")
    out.append("3\n7\n11 1\n12 2\n13 2\n1 11\n4 11\n7 11\n1 12\n5 12\n8 12\n1 13\n")
    out.append("2\n6\n5 30\n6 40\n7 5\n1 5\n4 5\n1 6\n3 6\n6 6\n")
    r = random.Random(25655)
    specs = [(3, 2), (5, 2), (8, 3), (10, 4), (15, 3), (20, 5), (30, 6), (50, 4), (60, 7), (80, 8),
             (100, 10), (150, 12), (200, 6), (300, 20), (500, 30), (800, 25), (1000, 40), (1500, 50), (2000, 3), (2000, 60)]
    for n, k in specs: out.append(generate_case(r, n, k))
    return out

def main():
    data = cases()
    assert len(set(data)) == len(data)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(data):
            assert valid(content) and well_defined(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            cnt, ratio = judge_detail(content)
            assert result.stdout.split() == [str(cnt), str(max(ratio, key=ratio.get))], index
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
