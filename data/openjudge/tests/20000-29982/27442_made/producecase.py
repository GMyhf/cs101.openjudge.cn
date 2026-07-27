import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/27442/\n# Accepted submission: 52825161\n# Source: http://cs101.openjudge.cn/practice/solution/52825161/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    m = int(input_data[0])\n    n = int(input_data[1])\n\n    # 记录课程权重\n    weights = {}\n    idx = 2\n    for _ in range(m):\n        course = input_data[idx]\n        weight = float(input_data[idx+1])\n        weights[course] = weight\n        idx += 2\n\n    # 计算每个学生的综合成绩\n    student_scores = {}\n    for _ in range(n):\n        student = input_data[idx]\n        course = input_data[idx+1]\n        grade = int(input_data[idx+2])\n        idx += 3\n\n        # 获取课程权重并累加成绩\n        weight = weights.get(course, 0.0)\n        score_contrib = grade * weight\n        student_scores[student] = student_scores.get(student, 0.0) + score_contrib\n\n    # 排序：\n    # 第一关键字：成绩（降序，即 -x[1]）\n    # 第二关键字：姓名（升序，即 x[0]）\n    sorted_students = sorted(student_scores.items(), key=lambda x: (-x[1], x[0]))\n\n    # 输出结果\n    for student, _ in sorted_students:\n        print(student)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3 6\njisuangailun 0.6\ngailvlun 0.3\ngaodengshuxue 0.7\nxiaoming jisuangailun 72\nxiaoming gailvlun 80\nxiaoming gaodengshuxue 60\nxiaohong jisuangailun 0\nxiaohong gailvlun 60\nxiaohong gaodengshuxue 60\n'
EXTRA_CASE=None
GENERATOR_NAME='g27442'
def g27442(r):
    m, n = r.randint(1, 12), r.randint(1, 80)
    courses = [f"C{i}" for i in range(m)]
    lines = [f"{c} {r.uniform(0.1, 5):.2f}" for c in courses]
    rows = [f"S{i} {r.choice(courses)} {r.randint(0, 100)}" for i in range(n)]
    return f"{m} {n}\n" + "\n".join(lines + rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
