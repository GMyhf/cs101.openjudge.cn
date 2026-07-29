import random, subprocess, sys, tempfile
from pathlib import Path
def g2792(r):
    out = [str(r.randint(1, 6))]
    for _ in range(int(out[0])):
        p, q = r.randint(1, 40), r.randint(1, 40)
        out += [str(r.randint(1, 200)), str(p), " ".join(str(r.randint(1,100)) for _ in range(p)), str(q), " ".join(str(r.randint(1,100)) for _ in range(q))]
    return "\n".join(out) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2792: 集合加法\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02792/\n# License: not declared in source collection; no license is inferred.\nfrom collections import Counter\n\ndef calculate_pairs(arr1, arr2, target_sum):\n    counter1 = Counter(arr1)\n    counter2 = Counter(arr2)\n\n    ans = 0\n    for item in counter1:\n        if target_sum - item in counter2:\n            ans += counter1[item] * counter2[target_sum - item]\n\n    return ans\n\n\nfor _ in range(int(input())):\n    s = int(input())\n    input()\n    l1 = list(map(int, input().split()))\n    input()\n    l2 = list(map(int, input().split()))\n\n    ans = calculate_pairs(l1, l2, s)\n    print(ans)\n'
SAMPLE='2\n99\n2\n49 49\n2\n50 50\n11\n9\n1 2 3 4 5 6 7 8 9\n10\n10 9 8 7 6 5 4 3 2 1\n'
GENERATOR='g2792'

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
