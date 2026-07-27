import random
REFERENCE="# External reference: /practice/30061/statistics/\n# Accepted submission: 52831600\n# Source: http://cs101.openjudge.cn/practice/solution/52831600/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    # 解析 N 和 M\n    N = int(input_data[0])\n    M = int(input_data[1])\n    \n    # 将报出的编号放入集合中，便于快速查找\n    reported_students = set(map(int, input_data[2:2+M]))\n    \n    # 找出未到达的同学编号\n    missing_students = []\n    for i in range(N):\n        if i not in reported_students:\n            missing_students.append(i)\n            \n    # 根据要求输出结果\n    if not missing_students:\n        print(N)\n    else:\n        print(*(missing_students))\n\nif __name__ == '__main__':\n    main()"
SAMPLE='3 3\n0 2 1\n'
GENERATOR_NAME='g30061'
def g30061(r):
    n = r.randint(1, 1000); m = r.randint(0, n); values = r.sample(range(n), m)
    return f"{n} {m}\n" + (" ".join(map(str, values)) + "\n" if values else "\n")

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
