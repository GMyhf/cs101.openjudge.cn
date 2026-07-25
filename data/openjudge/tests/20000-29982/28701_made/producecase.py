import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef main():\n    input = sys.stdin.read\n    data = input().split()\n    \n    n = int(data[0])\n    k = int(data[1])\n    times = [int(data[2 + i]) for i in range(n)]\n    \n    # 计算总炸制时间\n    total_time = sum(times)\n    \n    # 对炸制时间进行排序\n    times.sort()\n    \n    # 初始最大持续时间为总炸制时间除以 k\n    max_time = total_time / k\n    \n    # 如果最长的炸制时间大于或等于 max_time，则需要调整 k 的值\n    if times[-1] > max_time:\n        for i in range(n - 1, -1, -1):\n            if times[i] <= max_time:\n                break\n            total_time -= times[i]\n            k -= 1\n            max_time = total_time / k\n    \n    # 输出结果，保留三位小数\n    print(f"{max_time:.3f}")\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '4 2\n5 1 1 2\n'
def generate_case(r):
    n = r.randint(2, 25); k = r.randint(1, n - 1); times = [r.randint(1, 100) for _ in range(n)]
    assert 0 < k <= n and all(0 < x <= 1000000 for x in times)
    return f"{n} {k}\n" + " ".join(map(str, times)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28701 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
