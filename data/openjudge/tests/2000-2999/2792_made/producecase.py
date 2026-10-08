import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面：第1行组数n；每组5行：s (1<=s<=10000)；a (1<=a<=10000)；a个不超过10000的正整数；b (1<=b<=10000)；b个不超过10000的正整数。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    def num(x):
        return x.isdigit() and x[0] != "0"
    if not lines or not num(lines[0]): return False
    n = int(lines[0])
    if len(lines) != 1 + 5 * n: return False
    for g in range(n):
        s_, a, pa, b, pb = lines[1 + 5 * g: 6 + 5 * g]
        if not (num(s_) and num(a) and num(b)): return False
        if not (int(s_) <= 10000 and int(a) <= 10000 and int(b) <= 10000): return False
        for cnt, row in ((int(a), pa), (int(b), pb)):
            t = row.split(" ")
            if len(t) != cnt or not all(num(x) and int(x) <= 10000 for x in t): return False
    return True

def extra_cases():
    """补充：a=b=10000 满规模（卡 O(ab) 双重循环）、值域/和取到 10000、s=1 恒为 0、全相等时答案 1e8 等边界。"""
    r = random.Random(2792)
    def grp(s_, A, B):
        return [str(s_), str(len(A)), " ".join(map(str, A)), str(len(B)), " ".join(map(str, B))]
    def fmt(gs):
        return str(len(gs)) + "\n" + "\n".join(x for g in gs for x in g) + "\n"
    N = 10000
    cases = []
    cases.append(fmt([grp(1, [1], [1]), grp(2, [1], [1]), grp(10000, [10000], [10000]), grp(10000, [9999], [1]), grp(10000, [5000, 5000], [5000])]))
    cases.append(fmt([grp(2, [1] * N, [1] * N)]))
    cases.append(fmt([grp(10000, [r.randint(1, 10000) for _ in range(N)], [r.randint(1, 10000) for _ in range(N)]) for _ in range(3)]))
    cases.append(fmt([grp(r.randint(1, 10000), [r.randint(1, 50) for _ in range(N)], [r.randint(1, 10000) for _ in range(N)]) for _ in range(2)] + [grp(1, [r.randint(1, 10000) for _ in range(N)], [r.randint(1, 10000) for _ in range(N)])]))
    gs = []
    for _ in range(5):
        s_ = r.randint(2, 10000); A = [r.randint(1, s_ - 1) if r.random() < .7 else r.randint(1, 10000) for _ in range(N)]
        B = [s_ - x if x < s_ and r.random() < .5 else r.randint(1, 10000) for x in (r.choice(A) for _ in range(N))]
        gs.append(grp(s_, A, B))
    cases.append(fmt(gs))
    return cases

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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 40)]+extra_cases()
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
