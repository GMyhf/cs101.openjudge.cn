# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def max_gpa_increase(h, courses):
    # 总复习时间，扣除每门课的基础复习时间
    total_time = 2 * h - 0.5 * len(courses)

    # 计算每门课程的性价比：每增加一小时复习时间所能提高的分数乘以学分
    for course in courses:
        course.append(course[0] * course[1])  # 将性价比添加到每个课程的信息中

    # 按性价比从高到低排序课程
    courses.sort(key=lambda x: -x[2])

    total_increase = 0  # 初始化总分提高
    for course in courses:
        if total_time <= 0:
            break
        # 计算当前课程最多可以分配的复习时间
        max_time_for_course = min(5 / course[0], total_time)
        total_time -= max_time_for_course
        # 计算当前课程的分数提高并累加到总分提高
        total_increase += max_time_for_course * course[0] * course[1]

    return total_increase


# 输入
h = int(input())
m = int(input())
courses = []
for _ in range(m):
    s, c = map(float, input().split())
    courses.append([s, c])

# 输出
print(f"{max_gpa_increase(h, courses):.1f}")
