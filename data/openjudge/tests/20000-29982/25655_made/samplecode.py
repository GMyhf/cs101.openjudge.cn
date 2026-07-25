# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 真不玩原
from collections import defaultdict

n = int(input())  # 学生数量
m = int(input())  # 核酸检测信息数量

# 学生基本信息，以及核酸检测信息
student_info = [list(map(int, input().split())) for _ in range(n)]
test_info = [list(map(int, input().split())) for _ in range(m)]

# 统计每名学生的核酸检测情况
test_record = defaultdict(list)
for day, student_id in test_info:
    test_record[student_id].append(day)

# 统计未按时完成核酸检测的学生数量
late_count = 0
department_uncompletion = defaultdict(int)
department_total_students = defaultdict(int)

for student in student_info:
    student_id, department = student
    sign = False
    a = sorted(test_record[student_id])
    if a[0] != 1 or max(a) < 7:
        sign = True
    for i in range(len(a)-1):
        if a[i+1] - a[i] > 3:
            sign = True
            break
    if sign:
        late_count += 1
        department_uncompletion[department] += 1
    department_total_students[department] += 1

# 计算每个院系未按时完成核酸检测的学生数量占比
department_ratio = {}
for department in department_uncompletion.keys():
    ratio = department_uncompletion[department] / department_total_students[department]
    department_ratio[department] = ratio

# 输出结果
worst_department = max(department_ratio, key=department_ratio.get)

print(late_count)
print(worst_department)
