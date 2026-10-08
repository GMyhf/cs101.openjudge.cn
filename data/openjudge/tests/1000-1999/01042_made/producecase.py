import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：若干组，每组 n（2..25）、h（1..16）、n 个 fi ≥ 0、n 个 di ≥ 0、n-1 个 ti（0 < ti ≤ 192），
    各占一行；以 n = 0 的一行结束。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'(0|[1-9][0-9]*)$')
    def ints(line, cnt):
        t = line.split(' ')
        return list(map(int, t)) if len(t) == cnt and all(num.match(x) for x in t) else None
    i = 0; cases = 0
    while True:
        if i >= len(lines):
            return False
        v = ints(lines[i], 1)
        if v is None:
            return False
        n = v[0]; i += 1
        if n == 0:
            return i == len(lines) and cases >= 1
        if not 2 <= n <= 25 or i + 4 > len(lines):
            return False
        h = ints(lines[i], 1); f = ints(lines[i + 1], n); d = ints(lines[i + 2], n); t = ints(lines[i + 3], n - 1)
        if None in (h, f, d, t) or not 1 <= h[0] <= 16 or not all(1 <= x <= 192 for x in t):
            return False
        i += 4; cases += 1
def _case(r, n, h, style):
    if style == 'zero':                      # 一条鱼都没有：全部时间留在湖 1
        f = [0] * n; d = [r.randint(0, 5) for _ in range(n)]
    elif style == 'flat':                    # d=0、f 大量相等：考并列时的取舍
        v = r.randint(0, 20); f = [r.choice([v, v, r.randint(0, 20)]) for _ in range(n)]
        d = [r.choice([0, 0, r.randint(0, 3)]) for _ in range(n)]
    elif style == 'tie':                     # 小值域，制造大量同分方案
        f = [r.randint(0, 6) for _ in range(n)]; d = [r.randint(0, 3) for _ in range(n)]
    else:
        f = [r.randint(0, 1000) for _ in range(n)]; d = [r.randint(0, 100) for _ in range(n)]
    tmax = r.choice([1, 3, 12, 50, 192])
    t = [r.randint(1, tmax) for _ in range(n - 1)]
    return "\n".join((str(n), str(h), " ".join(map(str, f)), " ".join(map(str, d)), " ".join(map(str, t))))
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    cases = []
    if seed == 1:
        cases = ["2\n1\n0 0\n0 0\n1", "2\n1\n0 5\n0 0\n1", "2\n16\n1 1\n0 0\n192",
                 "2\n1\n5 5\n0 0\n12", "3\n1\n0 0 100\n0 0 0\n6 5", "3\n1\n0 0 100\n0 0 0\n6 6",
                 "25\n16\n" + " ".join(["1000"] * 25) + "\n" + " ".join(["0"] * 25) + "\n" + " ".join(["1"] * 24),
                 "25\n16\n" + " ".join(["0"] * 24 + ["1000"]) + "\n" + " ".join(["1"] * 25) + "\n" + " ".join(["8"] * 24)]
    else:
        big = seed >= 25
        for _ in range(r.randint(20, 60) if big else r.randint(1, 10)):
            n = r.randint(20, 25) if big else r.randint(2, 10)
            h = r.randint(12, 16) if big else r.randint(1, 6)
            style = r.choice(['random', 'random', 'tie', 'flat', 'zero'] if seed % 2 else ['random', 'tie', 'tie', 'flat'])
            cases.append(_case(r, n, h, style))
    return "\n".join(cases) + "\n0\n"
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1042: Gone Fishing\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01042/\n# License: not declared in source collection; no license is inferred.\nimport sys\n# 蒋子轩23工学院\nfrom heapq import heappush, heappop\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    h = int(input()) * 12\n    ans = -1 #最大钓鱼数量\n    res = [0] * n #每个湖上所花费的时间\n    f = list(map(int, input().split()))\n    d = list(map(int, input().split()))\n    t = [0] + (list(map(int, input().split())) if n > 1 else [])\n    #枚举第几个湖泊结束\n    #对于每种情况贪心算法，它在每个湖上都试图钓尽可能多的鱼，并始终优先考虑鱼的数量多的湖。\n    for i in range(n):\n        now = 0 #该情况钓鱼数量\n        q = []  #优先队列\n        lakes = [{\'id\': j, \'f\': f[j], \'d\': d[j]} for j in range(i + 1)]\n        for lake in lakes:\n            # 使得鱼的数量多的湖排在优先队列的前面（取负实现）。如果鱼的数量相同，那么ID小的湖会排在前面。\n            heappush(q, (-lake[\'f\'], lake[\'id\']))\n        tmp = [0] * n #该情况每个湖钓鱼时间\n        time_left = h - sum(t[:i + 1]) #湖上剩余的时间\n        while time_left > 0:\n            fish_count, idx = heappop(q)\n            fish_count = -fish_count #变回正数\n            tmp[idx] += 1\n            now += fish_count\n            lakes[idx][\'f\'] -= lakes[idx][\'d\']\n            if lakes[idx][\'f\'] < 0:\n                lakes[idx][\'f\'] = 0\n            heappush(q, (-lakes[idx][\'f\'], idx))\n            time_left -= 1\n        if now > ans:\n            ans = now\n            res = tmp.copy()\n    print(", ".join(str(val * 5) for val in res))\n    print("Number of fish expected:", ans)\n    print()\n'
NUMBER=1042
SAMPLE='2\n1\n10 1\n2 5\n2\n4\n4\n10 15 20 17\n0 3 4 3\n1 2 3\n4\n4\n10 15 50 30\n0 3 4 3\n1 2 3\n0\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
