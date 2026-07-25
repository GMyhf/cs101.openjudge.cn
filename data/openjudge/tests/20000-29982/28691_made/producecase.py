import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def main():\n    import sys\n    input = sys.stdin.read\n    data = input().strip().split()\n\n    num1 = int(data[0][:2])\n    num2 = int(data[1][:2])\n\n    result = num1 + num2\n    print(result)\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '12B 34D\n'
SAMPLE_OUT = '46\n'
def generate_case(r):
    a, b = r.randint(0, 99), r.randint(0, 99)
    return f"{a:02d}{r.choice('ABCD')} {b:02d}{r.choice('WXYZ')}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28691 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
