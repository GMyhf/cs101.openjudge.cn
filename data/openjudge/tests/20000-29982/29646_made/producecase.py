import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\n\n\ndef bacteria_war(harmful: int, beneficial: int) -> int:\n    hours = 0\n    while harmful > 0:\n        # Step 1: 有益菌消灭有害菌\n        harmful = max(0, harmful - beneficial)\n\n        # Step 2: 有害菌繁殖（在消灭之后进行）\n        harmful *= 2\n        harmful = min(harmful, 1_000_000)\n\n        # Step 3: 有益菌繁殖\n        beneficial = math.floor(beneficial * 1.05)\n\n        # Step 4: 时间增加\n        hours += 1\n    return hours\n\n\n# 主程序部分\ndef main():\n    n = int(input())\n    results = []\n    for _ in range(n):\n        h, b = map(int, input().split())\n        results.append(bacteria_war(h, b))\n    for res in results:\n        print(res)\n\n\nif __name__ == "__main__":\n    main()\n\n'
SAMPLE_IN = '4\n364 78\n289 48\n952 40\n966 23\n'
def generate_case(r):
    rows = [(r.randint(1, 100), r.randint(50, 1000)) for _ in range(r.randint(2, 8))]
    return str(len(rows)) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29646 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
