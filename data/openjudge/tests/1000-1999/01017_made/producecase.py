import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：每行一个订单，六个非负整数以单个空格分隔；以六个 0 的一行结尾（且只在结尾出现）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'(0|[1-9][0-9]*)$')
    for k, line in enumerate(lines):
        toks = line.split(' ')
        if len(toks) != 6 or not all(num.match(t) for t in toks):
            return False
        last = all(t == '0' for t in toks)
        if last != (k == len(lines) - 1):
            return False
    return True
def generate(n, seed):
    r=random.Random(seed)
    # The original random-only batch missed the packing boundaries.  Keep
    # these deterministic cases first so regressions around each residual
    # capacity are always present, then continue with seeded random cases.
    corner_cases = [
        '1 9 0 0 0 0',       # reported failure: nine 2x2 do not fit in one box
        '9 1 0 0 0 0',
        '0 0 1 0 0 0', '0 0 4 0 0 0', '0 0 5 0 0 0',
        '0 0 0 1 0 0', '0 0 0 0 1 0', '0 0 0 0 0 1',
        '0 9 0 0 0 0', '0 10 0 0 0 0',
        '0 5 0 1 0 0', '0 6 0 1 0 0',
        '0 5 1 0 0 0', '0 6 1 0 0 0',
        '1 0 0 1 0 0', '37 0 0 1 0 0',
        '0 0 0 0 0 2', '0 0 0 0 2 0',
        '20 20 20 20 20 20', '0 0 3 1 0 0',
        '0 0 4 1 0 0', '0 0 7 1 0 0',
        '0 0 8 1 0 0', '1 5 0 0 0 1',
        '1 6 0 0 0 1', '35 0 0 0 0 1',
        '36 0 0 0 0 1', '37 0 0 0 0 1',
        '0 0 0 5 0 0', '0 0 0 0 5 0',
    ]
    if 1 <= seed <= len(corner_cases):
        return corner_cases[seed - 1] + '\n0 0 0 0 0 0\n'
    if seed == 31:
        # 每种 0..3 个的全部组合（去掉全 0），一次覆盖所有余数分支的交叉
        rows = [' '.join(map(str, (a, b, c, d, e, f)))
                for a in range(4) for b in range(4) for c in range(4)
                for d in range(4) for e in range(4) for f in range(4) if a + b + c + d + e + f]
        return '\n'.join(rows) + '\n0 0 0 0 0 0\n'
    if 32 <= seed <= 41:
        # 多订单文件：一部分小数量（贴着各类余量），一部分大数量
        rows = []
        for _ in range(r.randint(50, 2000)):
            hi = r.choice([3, 9, 40, 1000, 100000])
            row = [r.randint(0, hi) for _ in range(6)]
            if not any(row):
                row[r.randrange(6)] = 1
            rows.append(' '.join(map(str, row)))
        return '\n'.join(rows) + '\n0 0 0 0 0 0\n'
    return ' '.join(str(r.randint(0,20)) for _ in range(6))+'\n0 0 0 0 0 0\n'
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1017: 装箱问题\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01017/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport math\nrest = [0,5,3,1]\n\nwhile True:\n    a,b,c,d,e,f = map(int,input().split())\n    if a + b + c + d + e + f == 0:\n        break\n    boxes = d + e + f           #装4*4, 5*5, 6*6\n    boxes += math.ceil(c/4)     #填3*3\n    spaceforb = 5*d + rest[c%4] #能和4*4 3*3 一起放的2*2\n    if b > spaceforb:\n    \tboxes += math.ceil((b - spaceforb)/9)\n    spacefora = boxes*36 - (36*f + 25*e + 16*d + 9*c + 4*b)     #和其他箱子一起的填的1*1\n\n    if a > spacefora:\n        boxes += math.ceil((a - spacefora)/36)\n    print(boxes)\n'
NUMBER=1017
SAMPLE='0 0 4 0 0 1\n7 5 1 0 0 0\n0 0 0 0 0 0\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,51)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
