import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import heapq\nfrom collections import defaultdict\n\nout = defaultdict(int)\npigs_heap = []\npigs_stack = []\n\nwhile True:\n    try:\n        s = input()\n    except EOFError:\n        break\n\n    if s == "pop":\n        if pigs_stack:\n            out[pigs_stack.pop()] += 1\n    elif s == "min":\n        if pigs_stack:\n            while True:\n                x = heapq.heappop(pigs_heap)\n                if not out[x]:\n                    heapq.heappush(pigs_heap, x)\n                    print(x)\n                    break\n                out[x] -= 1\n    else:\n        y = int(s.split()[1])\n        pigs_stack.append(y)\n        heapq.heappush(pigs_heap, y)\n'
SAMPLE_IN = 'pop\nmin\npush 5\npush 2\npush 3\nmin\npush 4\nmin\n'
SAMPLE_OUT = '2\n2\n'
def generate_case(r):
    lines = []; size = 0
    for _ in range(r.randint(10, 50)):
        if not size or r.random() < .6: lines.append(f"push {r.randint(0, 20000)}"); size += 1
        elif r.random() < .5: lines.append("min")
        else: lines.append("pop"); size -= 1
    assert lines and size >= 0
    return "\n".join(lines) + "\n"

def valid(text):
    """题面：每行一条指令 push n（0<=n<=20000 的整数）/ pop / min；指令总数不超过 100000。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not 1 <= len(lines) <= 100000: return False
    for line in lines:
        if line in ("pop", "min"): continue
        t = line.split(" ")
        if len(t) != 2 or t[0] != "push" or not t[1].isdigit() or not 0 <= int(t[1]) <= 20000: return False
    return True

def extra_cases():
    """补充：满规模 1e5 条、空栈 pop/min、大量重复重量（追加在原 20 组之后）。"""
    r = random.Random(220670); out = []
    def emit(lines): return "\n".join(lines) + "\n"
    # 先压 50000 头递增重量，再 50000 次 min：卡 O(n) 求 min
    out.append(emit([f"push {i % 20001}" for i in range(50000)] + ["min"] * 50000))
    # 交替 push/min，重量递减（每次都更新最小值）
    L = []
    for i in range(50000): L += [f"push {20000 - (i * 20000) // 50000}", "min"]
    out.append(emit(L))
    # 随机 1e5 条，含空栈 pop/min
    def rnd(n, hi, pp):
        L = []; size = 0
        for _ in range(n):
            x = r.random()
            if x < pp: L.append(f"push {r.randint(0, hi)}"); size += 1
            elif x < (1 + pp) / 2: L.append("min")
            else: L.append("pop"); size = max(0, size - 1)
        return L
    out.append(emit(rnd(100000, 20000, 0.4)))
    out.append(emit(rnd(100000, 3, 0.5)))      # 大量重复重量
    out.append(emit(rnd(100000, 20000, 0.34)))  # 栈经常为空
    # 先压满再全部弹空，再在空栈上 min/pop，最后再压一头
    L = [f"push {r.randint(0, 20000)}" for _ in range(30000)] + ["min"] * 2000
    L += ["pop", "min"] * 30000 + ["pop", "min"] * 2000 + ["push 0", "min", "push 20000", "min", "pop", "min"]
    out.append(emit(L))
    # 小边界：只有一条 push+min；空栈上的操作；重量 0 与 20000
    out.append("push 20000\nmin\n")
    out.append("pop\npop\nmin\npush 0\nmin\npop\nmin\npush 7\nmin\n")
    out.append("push 3\npush 3\npush 3\npop\nmin\npop\nmin\npop\nmin\npush 2\nmin\n")
    return out

def main():
    assert SAMPLE_IN == 'pop\nmin\npush 5\npush 2\npush 3\nmin\npush 4\nmin\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22067 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert all(valid(c) for c in seen)

if __name__ == "__main__":
    main()
