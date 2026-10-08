import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：首行 t（1 ≤ t ≤ 10），随后 t 行各一个 i（1 ≤ i ≤ 2147483647）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'[1-9][0-9]*$')
    if not lines or not num.match(lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 10 or len(lines) != t + 1:
        return False
    return all(num.match(x) and 1 <= int(x) <= 2147483647 for x in lines[1:])
def _group_ends(limit=2147483647):
    """返回各组 S_k 末位在整串中的位置（累加），直到超过 limit。"""
    ends = []; s = ss = 0; k = 0
    while ss < limit:
        k += 1; s += len(str(k)); ss += s; ends.append(ss)
    return ends
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    ends = _group_ends(); M = 2147483647
    # 位数变化处：S_9→S_10、S_99→S_100、S_999→S_1000、S_9999→S_10000 的组首/组尾
    special = [1, 2, 3, 4, 5, 6, 10, 45, 46, 47, 55, 56, 57, 58, M, M - 1, M - 2]
    for k in (9, 10, 99, 100, 999, 1000, 9999, 10000, len(ends) - 1):
        e = ends[k - 1]
        special += [e - 2, e - 1, e, e + 1, e + 2]
    # 组内位数变化处：组 S_k（k 足够大）里数字 9|10、99|100、999|1000、9999|10000 的衔接
    for k in (50, 500, 5000, 20000, len(ends) - 1):
        base = ends[k - 2]
        for b in (9, 99, 999, 9999):
            if b < k:
                pos = base + sum(len(str(j)) for j in range(1, b + 1))
                special += [pos - 1, pos, pos + 1, pos + 2]
    special = sorted({x for x in special if 1 <= x <= M})
    if seed <= (len(special) + 9) // 10:
        vals = special[(seed - 1) * 10: seed * 10]
    elif seed % 4 == 0:
        vals = [r.randint(1, 10 ** r.randint(1, 6)) for _ in range(r.randint(1, 10))]
    else:
        vals = [r.randint(1, M) for _ in range(10 if seed % 3 else r.randint(1, 10))]
    return f"{len(vals)}\n" + "".join(f"{v}\n" for v in vals)
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1019: Number Sequence\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01019/\n# License: not declared; no license is inferred.\nimport sys\n# 23n2300017711(杜昌钰)\n# 生成递增的字符串序列\nsequence = ""\ns = 0\nss = 0\nsums = []\n\n\nfor j in range(1, 33000):\n    sequence += str(j)  # 将当前数字转换为字符串并追加到序列中\n    s += len(str(j))\n    ss += s  # 累加当前数字的长度\n    sums.append(ss)  # 将累加和添加到列表中\n\n#print(ss)\n\n# 处理测试用例\ntest_cases = int(input())\n\nfor _ in range(test_cases):\n    x = int(input())\n\n    if x == 1:\n        print(1)\n    else:\n        # 在累加和列表中查找第一个大于等于 x 的元素\n        for i in range(len(sums)):\n            if x <= sums[i]:\n                # 计算偏移量并从序列中输出数字\n                offset = x - sums[i-1] - 1\n                print(sequence[offset])\n                break\n'
NUMBER=1019
SAMPLE='2\n8\n3\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
