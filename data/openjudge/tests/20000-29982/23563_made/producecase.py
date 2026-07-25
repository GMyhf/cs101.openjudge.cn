import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 2022fall-cs101, 楼翔\nimport re\nintermedia = input()\nlisty = [int(x) for x in re.findall(r".(?<!\\+0)n\\^(\\d+)", intermedia)] + [0]\nprint("n^" + str(max(listy)))\n'
SAMPLE_IN = '6n^2+5n^3\n'
SAMPLE_OUT = 'n^3\n'
def generate_case(r):
    terms = []
    for _ in range(r.randint(2, 6)):
        terms.append(f"{r.randint(0, 100)}n^{r.randint(0, 30)}")
    if all(term.startswith("0n") for term in terms):
        terms[0] = "1n^0"
    assert all(term.count("n^") == 1 and term.replace("n^", "").isdigit() for term in terms)
    return "+".join(terms) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23563 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
