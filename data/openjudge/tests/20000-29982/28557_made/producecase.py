import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nout=[]\nfor line in sys.stdin.read().splitlines()[1:]:\n    a,b=map(int,line.split()); carry=0; count=0\n    while a or b:\n        carry,a,b=(a%10+b%10+carry)//10,a//10,b//10\n        count += carry\n    out.append(str(count))\nprint("\\n".join(out))'
SAMPLE_IN='5\n1 9\n18 100\n8374 29\n999 1\n123 967\n'
def valid(text):
    """题面：第一行 t (1<=t<=10)；接下去 t 行，每行两个整数 a, b (1<=a,b<=1e9)。"""
    if not isinstance(text, str) or not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def num(tok, lo, hi):
        if not tok.isdigit() or (len(tok) > 1 and tok[0] == "0"):
            return None
        v = int(tok)
        return v if lo <= v <= hi else None
    if num(lines[0], 1, 10) is None:
        return False
    t = int(lines[0])
    if len(lines) != t + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != 2 or any(num(x, 1, 10**9) is None for x in toks):
            return False
    return True

SPECIAL = [(999999999, 1), (1, 999999999), (1000000000, 1000000000), (999999999, 999999999),
           (500000000, 500000000), (1000000000, 999999999), (9, 9), (1, 1), (5, 5), (4, 5),
           (99999, 1), (123456789, 987654321), (909090909, 90909091), (555555555, 444444445)]

def pair(r, mode):
    if mode == "small":          # 20% 子任务：1<=a,b<=9
        return r.randint(1, 9), r.randint(1, 9)
    if mode == "same":           # 40% 子任务：位数相同
        d = r.randint(1, 9)
        lo, hi = 10 ** (d - 1), 10 ** d - 1
        return r.randint(lo, hi), r.randint(lo, hi)
    if mode == "chain":          # 长连续进位：x 的各位与 y 的各位和为 9，再在末位补 1
        d = r.randint(2, 9)
        a = r.randint(10 ** (d - 1), 10 ** d - 1)
        b = 10 ** d - 1 - a + 1
        if not 1 <= b <= 10 ** 9:
            b = 1
        return (a, b) if r.random() < .5 else (b, a)
    if mode == "special":
        return r.choice(SPECIAL)
    # 任意位数
    return r.randint(1, 10 ** r.randint(1, 9)), r.randint(1, 10 ** r.randint(1, 9))

def g28557(r, index):
    if index <= 6:
        modes = ["small"]
    elif index <= 18:
        modes = ["same"]
    elif index <= 26:
        modes = ["chain", "special", "any"]
    else:
        modes = ["any", "same", "chain", "special", "small"]
    n = 1 if index in (1, 19) else (10 if index % 3 else r.randint(1, 10))
    return str(n) + "\n" + "\n".join("%d %d" % pair(r, r.choice(modes)) for _ in range(n)) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
     handle.write(REFERENCE_SOURCE);handle.flush()
     root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
     for index in range(40):
      if index==0: content=SAMPLE_IN
      else:
       for attempt in range(100):
        content=g28557(random.Random(28557+index+attempt*1000),index)
        if content not in seen: break
       else: raise AssertionError("insufficient diversity")
      assert valid(content), index
      seen.append(content)
      result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
      (root/f"{index}.in").write_text(content,encoding="utf-8")
      (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__ == "__main__":
    main()
