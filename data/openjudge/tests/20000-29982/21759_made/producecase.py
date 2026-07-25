import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# gpt\ndef find_juanwang(n, x, y, grades, m, queries):\n    # 创建一个字典用于存储学生的课程和成绩\n    student_grades = {}\n\n    # 遍历成绩单，将学生的成绩添加到字典中\n    for i in range(n):\n        course, student, grade = grades[i]\n        if student not in student_grades:\n            student_grades[student] = []\n        student_grades[student].append(grade)\n\n    # 遍历查询列表，判断每个学生是否为卷王\n    results = []\n    for i in range(m):\n        student = queries[i]\n        if student in student_grades and len(student_grades[student]) >= x:\n            average_grade = sum(student_grades[student]) / len(student_grades[student])\n            if average_grade > y:\n                results.append("yes")\n            else:\n                results.append("no")\n        else:\n            results.append("no")\n\n    return results\n\n# 读取输入\nn, x, y = map(int, input().split())\ngrades = []\nfor _ in range(n):\n    course, student, grade = input().split()\n    grade = int(grade)\n    grades.append((course, student, grade))\n\nm = int(input())\nqueries = []\nfor _ in range(m):\n    query = input()\n    queries.append(query)\n\n# 调用函数进行查询\nresults = find_juanwang(n, x, y, grades, m, queries)\n\n# 输出结果\nfor result in results:\n    print(result)\n'
SAMPLE_IN = '7 3 90\nJiSuanGaiLunA XiaoWang 100\nJiSuanGaiLunA XiaoZhang 98\nGaoDengShuXue XiaoHong 90\nGaoDengShuXue XiaoWang 99\nMeiRenLiJieJiSuanJiXiTong XiaoWang 93\nPythonCongRuMengDaoFangQi XiaoHong 92\nJiSuanGaiLunA XiaoHong 88\n3\nXiaoWang\nXiaoHong\nXiaoZhang\n'
SAMPLE_OUT = 'yes\nno\nno\n'
def generate_case(r):
    students = ["A", "B", "C", "D"]; courses = ["Math", "CS", "Art", "Bio"]; rows = []
    for _ in range(r.randint(5, 25)): rows.append(f"{r.choice(courses)} {r.choice(students)} {r.randint(0, 100)}")
    q = r.sample(students, len(students)); assert rows and len(set(q)) == len(q)
    return f"{len(rows)} {r.randint(1, 4)} {r.randint(40, 90)}\n" + "\n".join(rows) + f"\n{len(q)}\n" + "\n".join(q) + "\n"

assert SAMPLE_IN == '7 3 90\nJiSuanGaiLunA XiaoWang 100\nJiSuanGaiLunA XiaoZhang 98\nGaoDengShuXue XiaoHong 90\nGaoDengShuXue XiaoWang 99\nMeiRenLiJieJiSuanJiXiTong XiaoWang 93\nPythonCongRuMengDaoFangQi XiaoHong 92\nJiSuanGaiLunA XiaoHong 88\n3\nXiaoWang\nXiaoHong\nXiaoZhang\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(21759 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
