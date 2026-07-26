import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）\nn=int(input())\nfor _ in range(n):\n    s1,s2=input().split()\n    pos=[]\n    start=0\n    while True:\n        po=s1.find(s2,start)\n        if po==-1:\n            break\n        pos.append(po)\n        start=po+1\n    if pos:\n        for po in pos:\n            print(po,end=' ')\n        print('')\n    else:\n        print('no')\n"
SAMPLE_IN = '4\nababcdefgabdefab ab\naaaaaaaaa a\naaaaaaaaa aaa \n112123323 a\n'
SAMPLE_OUT = '0 2 9 14 \n0 1 2 3 4 5 6 7 8 \n0 1 2 3 4 5 6 \nno\n'
def generate_case(r):
    pairs = []
    for _ in range(r.randint(2, 6)):
        text = "".join(r.choice("abcd") for _ in range(r.randint(3, 35)))
        pattern = "".join(r.choice("abcd") for _ in range(r.randint(1, min(8, len(text)))))
        pairs.append((text, pattern))
    assert all(0 < len(p) <= len(t) < 2 * 10**7 for t, p in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{t} {p}" for t, p in pairs) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(26999 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
