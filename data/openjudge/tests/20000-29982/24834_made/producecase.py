import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#23n2300017735(夏天明BrightSummer)\nimport re\n\nfor i in range(int(input())):\n    s, p = input(), input().replace("?", ".{1}").replace("*", ".*") + "$"\n    print("yes" if re.match(p, s) else "no")\n'
SAMPLE_IN = '3\nabc\nabc\nabc\na*c\nabc\na??c\n'
SAMPLE_OUT = 'yes\nyes\nno\n'
def generate_case(r):
    pairs = []
    for _ in range(r.randint(3, 8)):
        s = "".join(r.choice("abcd") for _ in range(r.randint(1, 10)))
        mode = r.randrange(3)
        if mode == 0: p = s
        elif mode == 1: p = "*" + s[:r.randint(0, len(s))] + "*"
        else: p = "?" * len(s)
        if r.random() < .4: p += "z"
        pairs.extend([s, p])
    assert len(pairs) % 2 == 0 and all(0 < len(x) < 50 for x in pairs)
    return str(len(pairs) // 2) + "\n" + "\n".join(pairs) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24834 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
