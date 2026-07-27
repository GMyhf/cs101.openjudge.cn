# External reference: statistics page /practice/27442/
# Accepted submission: 52825161
# Source: http://cs101.openjudge.cn/practice/solution/52825161/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    m = int(input_data[0])
    n = int(input_data[1])

    # 记录课程权重
    weights = {}
    idx = 2
    for _ in range(m):
        course = input_data[idx]
        weight = float(input_data[idx+1])
        weights[course] = weight
        idx += 2

    # 计算每个学生的综合成绩
    student_scores = {}
    for _ in range(n):
        student = input_data[idx]
        course = input_data[idx+1]
        grade = int(input_data[idx+2])
        idx += 3

        # 获取课程权重并累加成绩
        weight = weights.get(course, 0.0)
        score_contrib = grade * weight
        student_scores[student] = student_scores.get(student, 0.0) + score_contrib

    # 排序：
    # 第一关键字：成绩（降序，即 -x[1]）
    # 第二关键字：姓名（升序，即 x[0]）
    sorted_students = sorted(student_scores.items(), key=lambda x: (-x[1], x[0]))

    # 输出结果
    for student, _ in sorted_students:
        print(student)

if __name__ == '__main__':
    solve()