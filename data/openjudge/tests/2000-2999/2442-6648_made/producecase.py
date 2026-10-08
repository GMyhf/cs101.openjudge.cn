import random, subprocess, sys, tempfile
from pathlib import Path
def g2442(r):
    out = [str(r.randint(1, 3))]
    for _ in range(int(out[0])):
        m, n = r.randint(2, 8), r.randint(1, 35); out.append(f"{m} {n}")
        out += [" ".join(str(r.randint(0, 10000)) for _ in range(n)) for _ in range(m)]
    return "\n".join(out) + "\n"
def valid(text):
    """02442 输入契约：首行 T；每组首行 "m n"（0<m<=100，0<n<=2000），随后 m 行各 n 个 0..10000 的整数。"""
    import re
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    num = re.compile(r"0|[1-9][0-9]*")
    def ints(line):
        tok = line.split(" ")
        if not all(num.fullmatch(x) for x in tok):
            return None
        return list(map(int, tok))
    h = ints(lines[0])
    if not h or len(h) != 1 or h[0] < 1:
        return False
    i = 1
    for _ in range(h[0]):
        if i >= len(lines):
            return False
        mn = ints(lines[i]); i += 1
        if not mn or len(mn) != 2:
            return False
        m, n = mn
        if not (0 < m <= 100 and 0 < n <= 2000) or i + m > len(lines):
            return False
        for _ in range(m):
            v = ints(lines[i]); i += 1
            if not v or len(v) != n or max(v) > 10000:
                return False
    return i == len(lines)
def g2442_v2(r, seed):
    def case(m, n, lo=0, hi=10000):
        rows = [" ".join(str(r.randint(lo, hi)) for _ in range(n)) for _ in range(m)]
        return [f"{m} {n}"] + rows
    if seed == 1:
        cases = [["1 1", "7"]]
    elif seed == 2:  # m=1：直接输出排序后的序列
        cases = [["1 6", "5 3 9 0 3 10000"], ["1 1", "0"]]
    elif seed == 3:  # n=1：唯一的和；m=100
        cases = [case(100, 1), case(100, 1, 10000, 10000)]
    elif seed == 4:  # 全 0、全 10000、大量相等
        cases = [case(5, 4, 0, 0), case(100, 3, 10000, 10000), case(7, 6, 0, 1)]
    elif seed <= 20:  # 小规模多组，可暴力核对
        cases = []
        for _ in range(r.randint(1, 10)):
            m = r.randint(1, 6); n = r.randint(1, 8 if m <= 4 else 4)
            hi = r.choice([1, 5, 30, 10000])
            cases.append(case(m, n, 0, hi))
    elif seed <= 28:  # 中等规模
        cases = []
        for _ in range(r.randint(1, 4)):
            cases.append(case(r.randint(10, 100), r.randint(50, 400), 0, r.choice([100, 10000])))
    elif seed <= 33:  # 满规模 m=100, n=2000（值域缩小以控制文件 ≤1MB）
        cases = [case(100, 2000, 0, r.choice([99, 999, 999]))]
    elif seed <= 36:  # n=2000，值域满 10000
        cases = [case(r.randint(70, 80), 2000, 0, 10000)]
    else:  # 多组中大规模
        cases = [case(r.randint(1, 100), r.randint(1, 2000), 0, 10000) for _ in range(r.randint(5, 12))]
        while sum(len(c) for c in cases) and len("\n".join("\n".join(c) for c in cases)) > 950_000:
            cases.pop()
    return "\n".join([str(len(cases))] + [x for c in cases for x in c]) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2442: Sequence\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02442/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport heapq\n\ndef get_ints():\n    """从标准输入流中逐词读取整数，节省内存。"""\n    for line in sys.stdin:\n        for word in line.split():\n            yield word\n\ndef solve():\n    ints_gen = get_ints()\n\n    try:\n        token = next(ints_gen)\n    except StopIteration:\n        return\n\n    # 测试用例数量\n    t_cases = int(token)\n\n    for _ in range(t_cases):\n        try:\n            m = int(next(ints_gen))\n            n = int(next(ints_gen))\n        except StopIteration:\n            break\n\n        # 读取第一个序列并排序\n        res = []\n        for i in range(n):\n            res.append(int(next(ints_gen)))\n        res.sort()\n\n        # 依次合并剩余的 m-1 个序列\n        for _ in range(m - 1):\n            row = []\n            for i in range(n):\n                row.append(int(next(ints_gen)))\n            row.sort()\n\n            # 使用最小堆合并当前结果 res 和新序列 row\n            # 堆中存储: (和, row序列的索引, res序列的值)\n            h = [(res[i] + row[0], 0, res[i]) for i in range(n)]\n            heapq.heapify(h)\n\n            new_res = [0] * n\n            for k in range(n):\n                curr_sum, row_idx, res_val = h[0]\n                new_res[k] = curr_sum\n\n                if row_idx + 1 < n:\n                    # 如果 row 序列还没到头，将该 res 值对应的下一个 row 值组合入堆\n                    heapq.heapreplace(h, (res_val + row[row_idx + 1], row_idx + 1, res_val))\n                # else:\n                #     # 如果 row 到头了，弹出堆顶\n                #     heapq.heappop(h)\n\n            # 更新 res 为合并后的前 n 个最小和\n            res = new_res\n\n        # 按照题目格式输出最小的 n 个和\n        sys.stdout.write(" ".join(map(str, res)) + "\\n")\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE='1\n2 3\n1 2 3\n2 2 3\n'
GENERATOR='g2442_v2'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
