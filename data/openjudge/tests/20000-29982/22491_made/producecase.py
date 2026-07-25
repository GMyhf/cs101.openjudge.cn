import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def max_gpa_increase(h, courses):\n    # 总复习时间，扣除每门课的基础复习时间\n    total_time = 2 * h - 0.5 * len(courses)\n\n    # 计算每门课程的性价比：每增加一小时复习时间所能提高的分数乘以学分\n    for course in courses:\n        course.append(course[0] * course[1])  # 将性价比添加到每个课程的信息中\n\n    # 按性价比从高到低排序课程\n    courses.sort(key=lambda x: -x[2])\n\n    total_increase = 0  # 初始化总分提高\n    for course in courses:\n        if total_time <= 0:\n            break\n        # 计算当前课程最多可以分配的复习时间\n        max_time_for_course = min(5 / course[0], total_time)\n        total_time -= max_time_for_course\n        # 计算当前课程的分数提高并累加到总分提高\n        total_increase += max_time_for_course * course[0] * course[1]\n\n    return total_increase\n\n\n# 输入\nh = int(input())\nm = int(input())\ncourses = []\nfor _ in range(m):\n    s, c = map(float, input().split())\n    courses.append([s, c])\n\n# 输出\nprint(f"{max_gpa_increase(h, courses):.1f}")\n'
SAMPLE_IN = '10\n4\n1.000000 1.000000\n2.000000 1.000000\n2.500000 1.000000\n1.000000 1.000000\n'
SAMPLE_OUT = '20.0\n'
def generate_case(r):
    m = r.randint(1, 10); h = r.randint(6, 10); rows = [(r.uniform(.5, 3), r.randint(1, 5)) for _ in range(m)]
    assert 6 <= h <= 10 and 1 <= m <= 10 and all(s > 0 and c > 0 for s, c in rows)
    return f"{h}\n{m}\n" + "\n".join(f"{s:.6f} {c:.6f}" for s, c in rows) + "\n"

assert SAMPLE_IN == '10\n4\n1.000000 1.000000\n2.000000 1.000000\n2.500000 1.000000\n1.000000 1.000000\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22491 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
