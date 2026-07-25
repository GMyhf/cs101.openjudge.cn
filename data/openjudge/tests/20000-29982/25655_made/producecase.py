import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 真不玩原\nfrom collections import defaultdict\n\nn = int(input())  # 学生数量\nm = int(input())  # 核酸检测信息数量\n\n# 学生基本信息，以及核酸检测信息\nstudent_info = [list(map(int, input().split())) for _ in range(n)]\ntest_info = [list(map(int, input().split())) for _ in range(m)]\n\n# 统计每名学生的核酸检测情况\ntest_record = defaultdict(list)\nfor day, student_id in test_info:\n    test_record[student_id].append(day)\n\n# 统计未按时完成核酸检测的学生数量\nlate_count = 0\ndepartment_uncompletion = defaultdict(int)\ndepartment_total_students = defaultdict(int)\n\nfor student in student_info:\n    student_id, department = student\n    sign = False\n    a = sorted(test_record[student_id])\n    if a[0] != 1 or max(a) < 7:\n        sign = True\n    for i in range(len(a)-1):\n        if a[i+1] - a[i] > 3:\n            sign = True\n            break\n    if sign:\n        late_count += 1\n        department_uncompletion[department] += 1\n    department_total_students[department] += 1\n\n# 计算每个院系未按时完成核酸检测的学生数量占比\ndepartment_ratio = {}\nfor department in department_uncompletion.keys():\n    ratio = department_uncompletion[department] / department_total_students[department]\n    department_ratio[department] = ratio\n\n# 输出结果\nworst_department = max(department_ratio, key=department_ratio.get)\n\nprint(late_count)\nprint(worst_department)\n'
SAMPLE_IN = '3\n10\n1001 101\n1003 101\n1004 102\n1 1001\n3 1001\n6 1001\n6 1003\n1 1003\n8 1003\n4 1003\n4 1004\n7 1004\n2 1004\n'
SAMPLE_OUT = '2\n102\n'
def generate_case(r):
    n = r.randint(3, 20); students = [(1000 + i, 101 + (i % 4)) for i in range(n)]
    tests = [(1, sid) for sid, _ in students]
    tests += [(r.randint(2, 9), r.choice(students[1:])[0]) for _ in range(r.randint(n, 4 * n))]
    assert len(tests) >= n and all(1 <= day <= 9 for day, _ in tests)
    return f"{n}\n{len(tests)}\n" + "\n".join(f"{sid} {dept}" for sid, dept in students) + "\n" + "\n".join(f"{day} {sid}" for day, sid in tests) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25655 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
