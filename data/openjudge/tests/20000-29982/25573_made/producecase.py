import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '\'\'\'\ngreedy，从后往前遍历，看当前这个和他的前面那个，如果这两个相同，并且都需要变化，那就使用一次魔法2，\n用magic来记录当前这个位置使用过的魔法2，方便后续判断；\n如果这两个不同，也就是当前这个需要被改变，而前面那个不需要，那么就是用魔法1，改变当前这一个\n\'\'\'\n\ndef judge(c,m):\n    if c=="B":\n        return m==1\n    if c=="R":\n        return m==0\n\ns=input()\nL=len(s)\ncnt=0\nmagic=0\n\nfor i in range(L-1,-1,-1):\n    if judge(s[i],magic)==True:\n        continue\n    if i>0 and s[i]==s[i-1]:\n        magic = 1 - magic\n    cnt += 1\nprint(cnt)\n'
SAMPLE_IN = 'RRRRRBR\n'
SAMPLE_OUT = '1\n'
def valid(text):
    """题面：一个字符串，由 R 和 B 组成；n < 500000。"""
    if not text.endswith("\n"): return False
    body = text[:-1]
    if "\n" in body or not body: return False
    return set(body) <= set("RB") and len(body) < 500000

def extra_cases():
    """规模与边界组：n=1、全 R（答案 0）、全 B、交替、长块、满规模随机。"""
    r = random.Random(255730)
    N = 499999
    out = ["R\n", "B\n", "BB\n", "RB\n", "BR\n",
           "R" * N + "\n", "B" * N + "\n", ("RB" * N)[:N] + "\n", ("BR" * N)[:N] + "\n",
           "".join(r.choice("RB") for _ in range(N)) + "\n"]
    blk = []
    while len(blk) < N:
        blk.extend(r.choice("RB") * r.randint(1, 50))
    out.append("".join(blk[:N]) + "\n")
    # 大多是 R、零星 B：卡只用魔法2 的写法
    t = ["R"] * N
    for i in r.sample(range(N), 2000): t[i] = "B"
    out.append("".join(t) + "\n")
    # 中等随机，用来和暴力 DP 交叉
    for k in range(8):
        n = r.randint(1000, 5000)
        out.append("".join(r.choice("RB" if k % 2 else "RRRB") for _ in range(n)) + "\n")
    return out

def generate_case(r):
    value = "".join(r.choice("RB") for _ in range(r.randint(1, 80)))
    assert set(value) <= set("RB") and value
    return value + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(25573 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            assert valid(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
