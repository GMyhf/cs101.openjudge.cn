import random, subprocess, sys, tempfile
from pathlib import Path
def g2707(r):
    rows = []
    for _ in range(r.randint(3, 15)):
        a = r.choice([x for x in range(-20, 21) if x]); b = r.randint(-30, 30); c = r.randint(-30, 30)
        rows.append(f"{a} {b} {c}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2707: 求一元二次方程的根\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/routine/02707/\n# License: not declared in source collection; no license is inferred.\nimport math\nn = int(input())\nfor i in range(n):\n    a, b, c = map(float, input().split())\n    if b == 0:\n        b = -b\n    delta = b ** 2 - 4 * a * c\n    if delta > 0:\n        x1 = (-b + math.sqrt(delta)) / (2 * a)\n        x2 = (-b - math.sqrt(delta)) / (2 * a)\n        print(f"x1={x1:.5f};x2={x2:.5f}")\n    elif delta == 0:\n        t = (-b) / (2 * a)\n        print(f"x1=x2={t:.5f}")\n    else:\n        d = math.sqrt(-delta) / (2 * a)\n        re = (-b) / (2 * a)\n        print(f"x1={re:.5f}+{d:.5f}i;x2={re:.5f}-{d:.5f}i")\n'
SAMPLE='3\n1.0 3.0 1.0\n2.0 -4.0 2.0\n1.0 2.0 8.0\n'
GENERATOR='g2707'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
