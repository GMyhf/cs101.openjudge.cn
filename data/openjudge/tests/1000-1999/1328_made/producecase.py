import random, subprocess, sys, tempfile
from pathlib import Path
def g1328(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n, d = r.randint(1, 25), r.randint(1, 30)
        points = [f"{r.randint(-80,80)} {r.randint(0,d + (5 if r.random()<.15 else 0))}" for _ in range(n)]
        blocks.append(f"{n} {d}\n" + "\n".join(points) + "\n\n")
    return "".join(blocks) + "0 0\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1328: Radar Installation\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01328/\n# License: not declared in source collection; no license is inferred.\nimport math\n\ndef solve(n, d, islands):\n    if d < 0:\n        return -1\n\n    ranges = []\n    for x, y in islands:\n        if y > d:\n            return -1\n        delta = math.sqrt(d * d - y * y)\n        ranges.append((x - delta, x + delta))\n\n    if not ranges:\n        return -1\n\n    ranges.sort(key=lambda x:x[1])\n\n    number = 1\n    r = ranges[0][1]\n    for start, end in ranges[1:]:\n        if r < start:\n            r = end\n            number += 1\n\n    return number\n\ncase_number = 0\nwhile True:\n    n, d = map(int, input().split())\n    if n == 0 and d == 0:\n        break\n\n    case_number += 1\n    islands = []\n    for _ in range(n):\n        islands.append(tuple(map(int, input().split())))\n\n    result = solve(n, d, islands)\n    print(f"Case {case_number}: {result}")\n    input()\n'
SAMPLE='3 2\n1 2\n-3 1\n2 1\n\n1 2\n0 2\n\n0 0\n'
GENERATOR='g1328'

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
