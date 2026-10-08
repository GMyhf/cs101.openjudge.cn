import random,subprocess,sys,tempfile
from pathlib import Path
import re
def _fences(n):
    # up[m][k]：m 根木棒、首根是其中第 k 短且下一根更高的方案数；down 同理
    if n == 1:
        return 1
    up = [[0] * (n + 2) for _ in range(n + 1)]; down = [[0] * (n + 2) for _ in range(n + 1)]
    up[1][1] = down[1][1] = 1
    for m in range(2, n + 1):
        for k in range(1, m + 1):
            up[m][k] = sum(down[m - 1][j] for j in range(k, m))
            down[m][k] = sum(up[m - 1][j] for j in range(1, k))
    return sum(up[n][k] + down[n][k] for k in range(1, n + 1))
def valid(text):
    """题面契约：首行 K（1..100），随后 K 行「N C」，1 ≤ N ≤ 20，1 ≤ C ≤ N 根木棒的美观栅栏总数。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'[1-9][0-9]*$')
    if not lines or not num.match(lines[0]):
        return False
    K = int(lines[0])
    if not 1 <= K <= 100 or len(lines) != K + 1:
        return False
    for line in lines[1:]:
        t = line.split(' ')
        if len(t) != 2 or not all(num.match(x) for x in t):
            return False
        n, c = map(int, t)
        if not 1 <= n <= 20 or not 1 <= c <= _fences(n):
            return False
    return True
def fence_counts(n):
    if n == 1:
        return 1
    count = [[[0, 0] for _ in range(n + 1)] for _ in range(n + 1)]
    count[1][1] = [1, 1]
    for size in range(2, n + 1):
        for first in range(1, size + 1):
            count[size][first][0] = sum(count[size - 1][second][1]
                                            for second in range(first, size))
            count[size][first][1] = sum(count[size - 1][second][0]
                                            for second in range(1, first))
    return sum(sum(count[n][first]) for first in range(1, n + 1))
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    total = {n: fence_counts(n) for n in range(1, 21)}
    if seed == 1:
        values = [(1, 1), (2, 1), (2, 2), (20, 1), (20, total[20]), (19, total[19]), (3, 1), (3, 4)]
    elif seed == 2:      # N=2..5 的全部栅栏按序列出
        values = [(n, c) for n in (2, 3, 4, 5) for c in range(1, total[n] + 1)]
    elif seed == 3:      # N=6 的前 100 个（共 122 个，K 不能超 100）
        values = [(6, c) for c in range(1, 101)]
    elif seed == 4:      # 每个 N 的首尾与正中
        values = []
        for n in range(1, 21):
            values += [(n, 1), (n, total[n]), (n, (total[n] + 1) // 2)]
        values = values[:100]
    else:
        K = 100 if seed % 3 else r.randint(1, 100)
        values = []
        for _ in range(K):
            n = r.randint(15, 20) if seed >= 20 else r.randint(1, 20)
            c = r.choice([1, total[n], r.randint(1, total[n]), r.randint(1, total[n]),
                          r.randint(max(1, total[n] // 2 - 5), min(total[n], total[n] // 2 + 5))])
            values.append((n, c))
    return str(len(values)) + "\n" + "".join(f"{n} {c}\n" for n, c in values)
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1037: A decorative fence\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01037/\n# License: not declared in source collection; no license is inferred.\nimport sys\n# http://cs101.openjudge.cn/practice/01037/\n#\n# https://blog.csdn.net/u014236804/article/details/38373729\n# POJ1037 A decorative fence by Guo Wei\n\nUP = 0\nDOWN = 1\nMAXN = 25\n\narr = lambda m,n,l : [ [ [0 for k in range(l)] for j in range(n)] for i in range(m) ]\n#m = arr(2,3,4)\n\n# C[i][k][DOWN] 是S(i)中以第k短的木棒打头的DOWN方案数,C[i][k][UP] 是S(i)中以第k短的木棒打头的UP方案数,第k短指i根中第k短\nC = arr(MAXN, MAXN, 2)\n\ndef Init(n: int):\n    C[1][1][UP] = C[1][1][DOWN] = 1\n    for i in range(2, n+1):\n        for k in range(1, i+1):         # 枚举第一根木棒的长度\n            for M in range(k, i):       # 枚举第二根木棒的长度\n                C[i][k][UP] += C[i-1][M][DOWN]\n            for N in range(1, k):       # 枚举第二根木棒的长度\n                C[i][k][DOWN] += C[i-1][N][UP]\n\n# 总方案数是 Sum{ C[n][k][DOWN] + C[n][k][UP] } k = 1.. n;\n\ndef Print(n: int, cc: int):\n    skipped = 0         #已经跳过的方案数\n    seq = [0]*MAXN      #最终要输出的答案\n    used = [False]*MAXN     #木棒是否用过\n\n    for i in range(1, n+1):     # 依次确定每一个位置i的木棒序号\n        oldVal = skipped\n        k = 0\n        No = 0      # k是剩下的木棒里的第No短的,No从1开始算\n        for k in range(1, n+1):     # 枚举位置i的木棒 ，其长度为k\n            oldVal = skipped\n            if used[k]==False:\n                No += 1      # k是剩下的木棒里的第No短的\n                if i == 1:\n                    skipped += C[n][No][UP] + C[n][No][DOWN]\n                else:\n                    if k > seq[i-1] and ( i <=2 or seq[i-2]>seq[i-1]): #合法放置\n                        skipped += C[n-i+1][No][DOWN]\n                    elif k < seq[i-1] and (i<=2 or seq[i-2]<seq[i-1]): #合法放置\n                        skipped += C[n-i+1][No][UP]\n\n                if skipped >= cc:\n                    break\n\n\n        used[k] = True\n        seq[i] = k\n        skipped = oldVal\n\n    print(\' \'.join(map(str, seq[1:n+1])))\n    \'\'\'\n    for i in range(1, n+1):\n        print("{}".format(seq[i]), end=\' \')\n    print()\n    \'\'\'\n\nInit(20);\nfor _ in range(int(input())):\n    n, c = map(int, input().split())\n\n    Print(n,c)\n'
NUMBER=1037
SAMPLE='2\n2 1\n3 3\n'
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
