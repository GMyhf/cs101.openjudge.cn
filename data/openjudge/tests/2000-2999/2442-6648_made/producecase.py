import random, subprocess, sys, tempfile
from pathlib import Path
def g2442(r):
    out = [str(r.randint(1, 3))]
    for _ in range(int(out[0])):
        m, n = r.randint(2, 8), r.randint(1, 35); out.append(f"{m} {n}")
        out += [" ".join(str(r.randint(0, 10000)) for _ in range(n)) for _ in range(m)]
    return "\n".join(out) + "\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2442: Sequence\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02442/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport heapq\n\ndef get_ints():\n    """从标准输入流中逐词读取整数，节省内存。"""\n    for line in sys.stdin:\n        for word in line.split():\n            yield word\n\ndef solve():\n    ints_gen = get_ints()\n\n    try:\n        token = next(ints_gen)\n    except StopIteration:\n        return\n\n    # 测试用例数量\n    t_cases = int(token)\n\n    for _ in range(t_cases):\n        try:\n            m = int(next(ints_gen))\n            n = int(next(ints_gen))\n        except StopIteration:\n            break\n\n        # 读取第一个序列并排序\n        res = []\n        for i in range(n):\n            res.append(int(next(ints_gen)))\n        res.sort()\n\n        # 依次合并剩余的 m-1 个序列\n        for _ in range(m - 1):\n            row = []\n            for i in range(n):\n                row.append(int(next(ints_gen)))\n            row.sort()\n\n            # 使用最小堆合并当前结果 res 和新序列 row\n            # 堆中存储: (和, row序列的索引, res序列的值)\n            h = [(res[i] + row[0], 0, res[i]) for i in range(n)]\n            heapq.heapify(h)\n\n            new_res = [0] * n\n            for k in range(n):\n                curr_sum, row_idx, res_val = h[0]\n                new_res[k] = curr_sum\n\n                if row_idx + 1 < n:\n                    # 如果 row 序列还没到头，将该 res 值对应的下一个 row 值组合入堆\n                    heapq.heapreplace(h, (res_val + row[row_idx + 1], row_idx + 1, res_val))\n                # else:\n                #     # 如果 row 到头了，弹出堆顶\n                #     heapq.heappop(h)\n\n            # 更新 res 为合并后的前 n 个最小和\n            res = new_res\n\n        # 按照题目格式输出最小的 n 个和\n        sys.stdout.write(" ".join(map(str, res)) + "\\n")\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE='1\n2 3\n1 2 3\n2 2 3\n'
GENERATOR='g2442'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
