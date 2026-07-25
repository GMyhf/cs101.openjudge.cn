import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/\n# Naive Pattern Searching algorithm\ndef search(pat, txt):\n    M = len(pat)\n    N = len(txt)\n\n    res = []\n    # A loop to slide pat[] one by one */\n    for i in range(N - M + 1):\n    #i = 0\n    #while i < N - M + 1:\n        j = 0\n\n        # For current index i, check\n        # for pattern match */\n        while(j < M):\n            if (txt[i + j] != pat[j]):\n                #i = i+j + 1\n                break\n            j += 1\n\n        if (j == M):\n            res.append(str(i))\n            #i += M\n\n    return res\n\n\nn = int(input())\nfor _ in range(n):\n    txt, pat = input().split()\n    ans = search(pat, txt)\n    if ans:\n        print(' '.join(ans))\n    else:\n        print('no')\n"
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
