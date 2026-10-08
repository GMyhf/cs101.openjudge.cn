import random, subprocess, sys, tempfile
from pathlib import Path

def score(vals):
    solved = sum(1 for k in range(4) if vals[2 * k + 1] > 0)
    pen = sum(vals[2 * k + 1] + 20 * (vals[2 * k] - 1) for k in range(4) if vals[2 * k + 1] > 0)
    return solved, pen

def valid(text):
    # 题面：第 1 行 nTeams；随后 n 行：队名（不含空白）+ 4 题各「提交次数 解出时间」（整数）；
    # 未解出时间为 0；解出则提交次数至少 1；保证按罚时比较后不出现并列（冠军唯一）。
    lines = text.split("\n")
    if lines and lines[-1] == "": lines.pop()
    if not lines or not lines[0].strip().isdigit(): return False
    n = int(lines[0])
    if n < 1 or len(lines) != n + 1: return False
    scores = []
    for ln in lines[1:]:
        p = ln.split()
        if len(p) != 9 or not all(t.isdigit() for t in p[1:]): return False
        v = list(map(int, p[1:]))
        for k in range(4):
            if v[2 * k + 1] > 0 and v[2 * k] < 1: return False
        scores.append(score(v))
    best = max(scores, key=lambda s: (s[0], -s[1]))
    return scores.count(best) == 1

def team(r, solve_p, maxt=300, maxs=8):
    v = []
    for _ in range(4):
        if r.random() < solve_p:
            v += [r.randint(1, maxs), r.randint(1, maxt)]
        else:
            v += [r.choice([0, 0, r.randint(1, maxs)]), 0]
    return v

def names(r, n):
    out = {}  # 用 dict 保序去重；set 的遍历顺序受字符串哈希随机化影响，不可复现
    while len(out) < n:
        out.setdefault(r.choice(["Team", "", "Stars", "Rockets", "PKU_", "x"]) + "".join(
            r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-") for _ in range(r.randint(1, 10))), None)
    return list(out)

def contest(r, n, solve_p=0.5, maxt=300, maxs=8):
    # 冠军唯一
    while True:
        rows = [team(r, solve_p, maxt, maxs) for _ in range(n)]
        sc = [score(v) for v in rows]
        b = max(sc, key=lambda s: (s[0], -s[1]))
        if sc.count(b) == 1:
            break
    nm = names(r, n)
    return f"{n}\n" + "".join(f"{a} " + " ".join(map(str, v)) + "\n" for a, v in zip(nm, rows))

def tie_on_solved(r, n):
    # 至少还有一队与冠军解题数相同，只能靠罚时区分；其余队随机（含未解出却有提交的题）
    while True:
        k = r.randint(1, 4)
        rows = []
        for _ in range(n):
            v = team(r, 0.5)
            rows.append(v)
        top = []
        for _ in range(2):
            v = [0, 0] * 4
            for p in r.sample(range(4), k):
                v[2 * p] = r.randint(1, 6); v[2 * p + 1] = r.randint(1, 300)
            top.append(v)
        rows[r.randrange(n)] = top[0]; rows[r.randrange(n)] = top[1]
        sc = [score(v) for v in rows]
        b = max(sc, key=lambda s: (s[0], -s[1]))
        if sc.count(b) == 1 and sum(1 for s in sc if s[0] == b[0]) >= 2:
            break
    nm = names(r, n)
    return f"{n}\n" + "".join(f"{a} " + " ".join(map(str, v)) + "\n" for a, v in zip(nm, rows))

def build_cases():
    r = random.Random(1581)
    cases = []
    # n=1（含一题未解、提交次数非 0 也不计罚时）
    cases.append("1\nSolo 3 0 0 0 7 0 0 0\n")
    cases.append("1\nAlone 1 1 2 50 3 0 1 300\n")
    # 解题多但罚时高者胜；冠军在首/尾
    cases.append("3\nFast 1 5 1 6 0 0 9 0\nSlowButMore 5 290 4 280 3 270 0 0\nNone 0 0 0 0 0 0 0 0\n")
    cases.append("3\nA 2 10 0 0 0 0 0 0\nB 1 25 0 0 0 0 0 0\nC 1 31 0 0 0 0 0 0\n")
    # 只看时间不看错误提交会选错：A 时间和 30、错 2 次=70；B 时间和 60、错 0 次=60
    cases.append("2\nA 3 10 1 20 0 0 4 0\nB 1 30 1 30 2 0 0 0\n")
    # 题数相同：A=30+30=60 胜、B=65；若把未解出题的 9 次提交也计罚时，A 会输
    cases.append("3\nA 1 30 1 30 9 0 0 0\nB 1 35 1 30 0 0 0 0\nC 2 40 0 0 0 0 0 0\n")
    for _ in range(10):
        cases.append(contest(r, r.randint(2, 10), solve_p=r.choice([0.2, 0.5, 0.8])))
    for _ in range(10):
        cases.append(tie_on_solved(r, r.randint(2, 30)))
    for _ in range(5):
        cases.append(contest(r, r.randint(50, 300), solve_p=r.choice([0.3, 0.6, 0.9]), maxt=600, maxs=30))
    cases.append(tie_on_solved(r, 500))
    cases.append(contest(r, 1000, solve_p=0.9, maxt=1000, maxs=50))
    while len(cases) < 39:
        cases.append(tie_on_solved(r, r.randint(5, 100)))
    return cases

REFERENCE='// External reference: http://cs101.openjudge.cn/practice/01581/statistics/\n// Accepted submission: 51691711\n// Source: http://cs101.openjudge.cn/practice/solution/51691711/\n// License: not declared on the submission page; no license is inferred.\n\n#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int nTeams;\n    if (!(cin >> nTeams)) return 0;\n\n    string bestName;\n    int bestSolved = -1;\n    long long bestPenalty = (1LL<<60);\n\n    for (int t = 0; t < nTeams; ++t) {\n        string name;\n        cin >> name;\n\n        int solved = 0;\n        long long penalty = 0;\n\n        for (int i = 0; i < 4; ++i) {\n            long long sub, tim;\n            cin >> sub >> tim;\n            if (tim > 0) {\n                ++solved;\n                penalty += tim + 20LL * (sub - 1);\n            }\n        }\n\n        if (solved > bestSolved || (solved == bestSolved && penalty < bestPenalty)) {\n            bestSolved = solved;\n            bestPenalty = penalty;\n            bestName = name;\n        }\n    }\n\n    cout << bestName << \' \' << bestSolved << \' \' << bestPenalty << "\\n";\n    return 0;\n}\n'
LANGUAGE='G++'
SAMPLE='4\nStars 2 20 5 0 4 190 3 220\nRockets 5 180 1 0 2 0 3 100\nPenguins 1 15 3 120 1 300 4 0\nMarsupials 9 0 3 100 2 220 3 80\n'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
