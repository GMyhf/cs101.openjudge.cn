import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import gc\nimport heapq\nimport sys\n\n\ndef solve():\n    # 暂时禁用垃圾回收以提升执行速度\n    gc.disable()\n\n    # 以字节流形式读取输入，速度最快\n    input_bytes = sys.stdin.buffer.read().split()\n    if not input_bytes:\n        return\n\n    # 快速转换为整型列表\n    data = list(map(int, input_bytes))\n    N = data[0]\n    K = data[1]\n\n    # 利用高速 C 切片分离 A 轮和 B 轮数据\n    As = data[2::2]\n    Bs = data[3::2]\n\n    # 第一轮筛选：找出 As 中值最大的前 K 个索引\n    # 使用内置的 As.__getitem__ 替代 lambda 表达式，速度极快\n    if K < 1000:\n        top_k = heapq.nlargest(K, range(N), key=As.__getitem__)\n    else:\n        top_k = sorted(range(N), key=As.__getitem__, reverse=True)[:K]\n\n    # 第二轮筛选：在 top_k 索引中，找出使 Bs 值最大的索引\n    winner_idx = max(top_k, key=Bs.__getitem__)\n\n    # 输出 1 基准的牛编号\n    print(winner_idx + 1)\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '5 3\n3 10\n9 2\n5 6\n8 4\n6 5\n'
def generate_case(r):
    n = r.randint(2, 80); k = r.randint(1, n); avals = r.sample(range(1, 10**9), n); bvals = r.sample(range(1, 10**9), n)
    assert len(set(avals)) == n and len(set(bvals)) == n
    return f"{n} {k}\n" + "\n".join(f"{a} {b}" for a, b in zip(avals, bvals)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(31041 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
