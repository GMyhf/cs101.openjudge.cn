import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def max_gpa_increase(h, courses):\n    # 总复习时间，扣除每门课的基础复习时间\n    total_time = 2 * h - 0.5 * len(courses)\n\n    # 计算每门课程的性价比：每增加一小时复习时间所能提高的分数乘以学分\n    for course in courses:\n        course.append(course[0] * course[1])  # 将性价比添加到每个课程的信息中\n\n    # 按性价比从高到低排序课程\n    courses.sort(key=lambda x: -x[2])\n\n    total_increase = 0  # 初始化总分提高\n    for course in courses:\n        if total_time <= 0:\n            break\n        # 计算当前课程最多可以分配的复习时间\n        max_time_for_course = min(5 / course[0], total_time)\n        total_time -= max_time_for_course\n        # 计算当前课程的分数提高并累加到总分提高\n        total_increase += max_time_for_course * course[0] * course[1]\n\n    return total_increase\n\n\n# 输入\nh = int(input())\nm = int(input())\ncourses = []\nfor _ in range(m):\n    s, c = map(float, input().split())\n    courses.append([s, c])\n\n# 输出\nprint(f"{max_gpa_increase(h, courses):.1f}")\n'
SAMPLE_IN = '10\n4\n1.000000 1.000000\n2.000000 1.000000\n2.500000 1.000000\n1.000000 1.000000\n'
SAMPLE_OUT = '20.0\n'
def generate_case(r):
    m = r.randint(1, 10); h = r.randint(6, 10); rows = [(r.uniform(.5, 3), r.randint(1, 5)) for _ in range(m)]
    assert 6 <= h <= 10 and 1 <= m <= 10 and all(s > 0 and c > 0 for s, c in rows)
    return f"{h}\n{m}\n" + "\n".join(f"{s:.6f} {c:.6f}" for s, c in rows) + "\n"

import re
_REAL = re.compile(r"\d+(\.\d+)?")


def valid(text):
    """题面：第一行正整数 h（6<=h<=10）；第二行正整数 m（1<=m<=10）；其余 m 行每行两个实数 s c，空格隔开。
    s 是每多复习一小时提高的分数、c 是学分，按语义取正数（s=0 时「提高 5 分」的上限无从谈起）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) < 2 or not all(x.isdigit() and x == str(int(x)) for x in lines[:2]):
        return False
    h, m = int(lines[0]), int(lines[1])
    if not (6 <= h <= 10 and 1 <= m <= 10) or len(lines) != m + 2:
        return False
    for line in lines[2:]:
        parts = line.split(" ")
        if len(parts) != 2 or not all(_REAL.fullmatch(t) and float(t) > 0 for t in parts):
            return False
    return True


def exact_answer(text):
    """用 Fraction 精确算贪心结果，供生成时避开 x.x5 这种舍入边界。"""
    from fractions import Fraction as F
    lines = text.split()
    h, m = int(lines[0]), int(lines[1])
    cs = [(F(lines[2 + 2 * i]), F(lines[3 + 2 * i])) for i in range(m)]
    t = 2 * h - F(m, 2); tot = F(0)
    for s, c in sorted(cs, key=lambda x: -x[0] * x[1]):
        use = min(F(5) / s, t)
        if use <= 0: break
        t -= use; tot += use * s * c
    return tot


def extra_case(k, r):
    """补充组：s、c 取更宽的实数范围；s 与 s*c 排序不一致；边界 h=6/10、m=1/10。"""
    for _ in range(1000):
        if k == 0:      # h=6, m=10, s 很小：时间完全不够，全部压在 s*c 最大的一门上
            h, m = 6, 10; rows = [(r.uniform(.1, .6), r.uniform(.5, 6)) for _ in range(m)]
        elif k == 1:    # h=10, m=1, s 大：时间富余，只能拿满 5 分
            h, m = 10, 1; rows = [(r.uniform(5, 12), r.uniform(1, 5))]
        elif k == 2:    # s 大的学分小、s 小的学分大：按 s 排序或按 c 排序都会错
            h, m = 6, 10
            rows = []
            for _ in range(m):
                s = r.uniform(.3, 1.5)
                rows.append((s, 6 / s * r.uniform(.6, 1.4)))
        elif k == 3:    # h=6, m=10, s 跨度大，部分课程饱和、部分只分到零头
            h, m = 6, 10; rows = [(r.choice([r.uniform(.2, .8), r.uniform(2, 6)]), r.uniform(.5, 5)) for _ in range(m)]
        elif k == 4:    # 学分为非整数实数
            h, m = r.randint(6, 10), r.randint(5, 10); rows = [(r.uniform(.5, 4), r.uniform(.5, 4.5)) for _ in range(m)]
        elif k == 5:    # 时间恰好介于两门课饱和之间
            h, m = 7, 10; rows = [(r.uniform(.7, 1.3), r.uniform(1, 4)) for _ in range(m)]
        elif k == 6:    # h=10, m=10 都较大
            h, m = 10, 10; rows = [(r.uniform(.3, 3), r.uniform(.5, 5)) for _ in range(m)]
        else:           # 随机宽范围
            h, m = r.randint(6, 10), r.randint(1, 10); rows = [(r.uniform(.1, 8), r.uniform(.5, 5)) for _ in range(m)]
        text = f"{h}\n{m}\n" + "\n".join(f"{s:.6f} {c:.6f}" for s, c in rows) + "\n"
        v = exact_answer(text) * 10
        frac = v - int(v)
        if abs(frac - 0.5) > 1e-4:   # 远离四舍五入边界
            return text
    raise AssertionError(k)


def main():
    assert SAMPLE_IN == '10\n4\n1.000000 1.000000\n2.000000 1.000000\n2.500000 1.000000\n1.000000 1.000000\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22491 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            cases.append(content)
        for k in range(10):
            content = extra_case(k, random.Random(22491 * 100 + k))
            assert content not in cases, k
            cases.append(content)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
