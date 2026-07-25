# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# gpt
def find_juanwang(n, x, y, grades, m, queries):
    # 创建一个字典用于存储学生的课程和成绩
    student_grades = {}

    # 遍历成绩单，将学生的成绩添加到字典中
    for i in range(n):
        course, student, grade = grades[i]
        if student not in student_grades:
            student_grades[student] = []
        student_grades[student].append(grade)

    # 遍历查询列表，判断每个学生是否为卷王
    results = []
    for i in range(m):
        student = queries[i]
        if student in student_grades and len(student_grades[student]) >= x:
            average_grade = sum(student_grades[student]) / len(student_grades[student])
            if average_grade > y:
                results.append("yes")
            else:
                results.append("no")
        else:
            results.append("no")

    return results

# 读取输入
n, x, y = map(int, input().split())
grades = []
for _ in range(n):
    course, student, grade = input().split()
    grade = int(grade)
    grades.append((course, student, grade))

m = int(input())
queries = []
for _ in range(m):
    query = input()
    queries.append(query)

# 调用函数进行查询
results = find_juanwang(n, x, y, grades, m, queries)

# 输出结果
for result in results:
    print(result)
