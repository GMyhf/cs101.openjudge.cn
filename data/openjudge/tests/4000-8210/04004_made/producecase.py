import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); n,t=a[:2]; dp=[0]*(t+1); dp[0]=1\nfor x in a[2:2+n]:\n    for s in range(t,x-1,-1): dp[s]+=dp[s-x]\nprint(dp[t])'
SAMPLE_IN='5 5\n1 2 3 4 5\n'
def g4004(r):
    n = r.randint(1, 20)
    values = [r.randint(1, 80) for _ in range(n)]
    return f"{n} {r.randint(1, 1000)}\n" + " ".join(map(str, values)) + "\n"


def valid(text):
    """题面契约：第一行 n t（1<=n<=20，1<=t<=1000），第二行恰 n 个正整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    first = lines[0].split(" ")
    if len(first) != 2 or not all(x.isdigit() for x in first):
        return False
    n, t = map(int, first)
    if not (1 <= n <= 20 and 1 <= t <= 1000):
        return False
    vals = lines[1].split(" ")
    if len(vals) != n or not all(x.isdigit() and x[0] != "0" for x in vals):
        return False
    return True


def fmt(t, values):
    return f"{len(values)} {t}\n" + " ".join(map(str, values)) + "\n"


def extra_cases():
    """补强：t 取满 1000 且答案非零、组合数极大、n=1 命中/不命中、数大于 t、全相同。"""
    r = random.Random(40040)
    out = []
    out.append(fmt(10, [1] * 20))                       # C(20,10)=184756
    out.append(fmt(1000, [100] * 20))                   # C(20,10)，t 取上限
    out.append(fmt(1000, [r.randint(30, 70) for _ in range(20)]))
    out.append(fmt(1000, [r.randint(80, 120) for _ in range(20)]))
    out.append(fmt(1000, [1000] + [r.randint(1, 1000) for _ in range(19)]))
    out.append(fmt(1000, list(range(1, 21))))           # 总和 210<1000 → 0
    out.append(fmt(210, list(range(1, 21))))            # 恰好全选 → 1
    out.append(fmt(1, [1]))
    out.append(fmt(7, [8]))
    out.append(fmt(7, [7]))
    out.append(fmt(500, [r.randint(1, 100000) for _ in range(10)] + [r.randint(20, 60) for _ in range(10)]))
    out.append(fmt(105, [r.choice([5, 10, 15, 20, 25]) for _ in range(20)]))
    out.append(fmt(999, [r.randint(1, 1000) for _ in range(20)]))
    return out


def main():
 with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
  handle.write(REFERENCE_SOURCE);handle.flush()
  root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
  cases=[]
  for index in range(40):
   if index==0: content=SAMPLE_IN
   else:
    for attempt in range(100):
     content=g4004(random.Random(4004+index+attempt*1000))
     if content not in seen: break
    else: raise AssertionError("insufficient diversity")
   seen.append(content);cases.append(content)
  for content in extra_cases():
   assert content not in cases
   cases.append(content)
  for index,content in enumerate(cases):
   assert valid(content), index
   result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
   (root/f"{index}.in").write_text(content,encoding="utf-8")
   (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
