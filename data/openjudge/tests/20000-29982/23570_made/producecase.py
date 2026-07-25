import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nthe toggle function is used to flip the bit, which simplifies the flip function. \nusing a for-loop to iterate over the two cases: pressing the first button or not. \n"""\ndef toggle(bit):\n    return \'0\' if bit == \'1\' else \'1\'\n\ndef flip(lock, i):\n    if i > 0:\n        lock[i-1] = toggle(lock[i-1])\n    lock[i] = toggle(lock[i])\n    if i + 1 < len(lock):\n        lock[i+1] = toggle(lock[i+1])\n\ndef main():\n    s = input()\n    fin = input()\n    n = len(s)\n    ans = float(\'inf\')\n\n    for press_first in [False, True]:\n        tmp = 0\n        lock = list(s)\n        if press_first:\n            flip(lock, 0)\n            tmp += 1\n        for i in range(1, n):\n            if lock[i-1] != fin[i-1]:\n                flip(lock, i)\n                tmp += 1\n        if lock[n-1] == fin[n-1]:\n            ans = min(ans, tmp)\n\n    if ans == float(\'inf\'):\n        print("impossible")\n    else:\n        print(ans)\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '011\n000\n'
SAMPLE_OUT = '1\n'
def generate_case(r):
    n = r.randint(1, 30)
    start = "".join(r.choice("01") for _ in range(n))
    target = "".join(r.choice("01") for _ in range(n))
    assert len(start) == len(target) == n and set(start + target) <= set("01")
    return start + "\n" + target + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23570 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
