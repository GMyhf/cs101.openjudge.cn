#!/usr/bin/env python3
"""Build T-002 batch 001a: twenty solution-backed, custom-generated packages."""
import json
import random
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab" / "t002-batch-001-manifest.json"
TESTS = ROOT / "data" / "openjudge" / "tests"
IDS = [3406, 3441, 3447, 3532, 3720, 4005, 4036, 4075, 4077, 4078, 4079, 4080, 4081, 4082, 4084, 4089, 4093, 4103, 4109, 4141]


def bucket(n):
    if n < 2000: return "1000-1999"
    if n < 3000: return "2000-2999"
    if n <= 3682: return "3000-3682"
    if n <= 8210: return "4000-8210"
    if n <= 19963: return "10000-19963"
    if n <= 29982: return "20000-29982"
    return "30000-"


def get_section(source, number):
    lines = Path(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+0*{number}[:：]", lines[start]):
            end = starts[i + 1] if i + 1 < len(starts) else len(lines)
            return "\n".join(lines[start:end])
    raise ValueError(number)


def fence_blocks(body):
    fence = r"\x60\x60\x60"
    return re.findall(fence + r"(?:python|py)?\s*\n(.*?)" + fence, body, re.S | re.I)


def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"


def g3406(r):
    n = r.randint(1, 30); heights = [r.randint(1, 100) for _ in range(n)]
    return f"{n} {r.randint(max(1, n), sum(heights))}\n" + "\n".join(map(str, heights)) + "\n"


def g3441(r):
    n = r.choice([2, 4, 8, 12]); rows = [[r.randint(-20, 20) for _ in range(4)] for _ in range(n)]
    return str(n) + "\n" + "\n".join(" ".join(map(str, x)) for x in rows) + "\n"


def g3532(r):
    n = r.randint(1, 100); a = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a)) + "\n"


def g3720(r):
    return "1\nA\n-B\n--*\n--C\n0\n"


def g4005(r):
    lines = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 12)
        lines += [str(n), " ".join(str(r.randint(1, 100)) for _ in range(n)), " ".join(str(r.randint(1, 100)) for _ in range(n))]
    return "\n".join(lines + ["0"]) + "\n"


def g4036(r):
    a, b, k = r.randint(0, 100), r.randint(0, 100), r.randint(0, 20)
    n = r.randint(0, k); return f"{a} {b} {k} {n} {k-n}\n"


def g4075(r):
    cases = r.randint(1, 4); lines = [str(cases)]
    for _ in range(cases):
        n = r.randint(1, 8); lines.append(str(n))
        lines += [" ".join(str(r.randint(-9, 9)) for _ in range(n)) for _ in range(n)]
    return "\n".join(lines) + "\n"


def g4077(r): return f"{r.randint(1, 12)}\n"


def g4078(r):
    ops = []
    size = 0
    for _ in range(r.randint(10, 60)):
        if size == 0 or r.random() < .7:
            ops.append(f"1 {r.randint(-100, 100)}"); size += 1
        else:
            ops.append("2"); size -= 1
    return str(len(ops)) + "\n" + "\n".join(ops) + "\n"


def g4079(r):
    vals = r.sample(range(1, 1000), r.randint(3, 40))
    return " ".join(map(str, vals)) + "\n"


def g4080(r):
    n = r.randint(1, 30); return f"{n}\n" + " ".join(str(r.randint(1, 1000)) for _ in range(n)) + "\n"


def g4081(r): return r.choice(["dudduduudu", "ddduuu", "dududu", "dduduu"]) + "\n"


def g4082(r): return "9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n"


def g4084(r):
    n = r.randint(2, 20); edges = [(i, i + 1) for i in range(1, n)]
    for _ in range(r.randint(0, n)):
        a, b = sorted(r.sample(range(1, n + 1), 2))
        if a != b and (a, b) not in edges: edges.append((a, b))
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"


def g4089(r):
    t = r.randint(2, 6); lines = [str(t)]
    for _ in range(t):
        nums = [str(r.randint(100, 999999)) for _ in range(r.randint(2, 12))]
        lines += [str(len(nums))] + nums
    return "\n".join(lines) + "\n"


def g4093(r):
    n = r.randint(1, 5); m = r.randint(1, 8); lines = [str(n)]
    for _ in range(n):
        docs = sorted(r.sample(range(1, 10), r.randint(0, 5)))
        lines.append(" ".join([str(len(docs))] + list(map(str, docs))))
    lines.append(str(m))
    for _ in range(m): lines.append(" ".join(str(r.choice([-1, 0, 1])) for _ in range(n)))
    return "\n".join(lines) + "\n"


def g4103(r): return f"{r.randint(1, 15)}\n"


def g4109(r):
    n = r.randint(2, 20); edges = [(i, i + 1) for i in range(1, n)]
    queries = [tuple(r.sample(range(1, n + 1), 2)) for _ in range(r.randint(1, 8))]
    lines = [f"1", f"{n} {len(edges)} {len(queries)}"]
    lines += [f"{a} {b}" for a, b in edges] + [f"{a} {b}" for a, b in queries]
    return "\n".join(lines) + "\n"


def g4141(r):
    return " ".join(str(r.randint(0, 4)) for _ in range(6)) + "\n"


GENERATORS = dict(zip(IDS, [g3406, g3441, None, g3532, g3720, g4005, g4036, g4075, g4077, g4078, g4079, g4080, g4081, g4082, g4084, g4089, g4093, g4103, g4109, g4141]))


def run(code, text):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        p = subprocess.run(["python3", f.name], input=text, text=True, capture_output=True, timeout=5)
    if p.returncode: raise RuntimeError(p.stderr[-1000:])
    return p.stdout


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {x["local_number"]: x for x in manifest["entries"]}
    report = []
    for number in IDS:
        print("building", number, flush=True)
        entry = by_id[number]; body = get_section(entry["source"], number)
        code = next(c for c in fence_blocks(body) if "import " in c or "def " in c)
        sample_in, sample_out = sample(body, "样例输入"), sample(body, "样例输出")
        assert run(code, sample_in).split() == sample_out.split(), number
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"
        data.mkdir(parents=True, exist_ok=True)
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        generator = GENERATORS[number]
        if generator is None: generator = lambda r, value=sample_in: value
        cases = [sample_in] + [generator(random.Random(number + i)) for i in range(1, 20)]
        outputs = [run(code, value) for value in cases]
        produce = f'''import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = {sample_in!r}
SAMPLE_OUT = {sample_out!r}
CASES = {cases!r}
REFERENCE_SOURCE = {code!r}
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed({number})
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{{index}}.in").write_text(content, encoding="utf-8")
    (root / f"{{index}}.out").write_text(solve_reference(content), encoding="utf-8")
'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (value, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(value, encoding="utf-8")
            (data / f"{i}.out").write_text(output, encoding="utf-8")
        report.append({"local_number": number, "status": "generated", "source": entry["source"], "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "output_reference": "embedded solution source", "test_cases": 20})
    (ROOT / "collab" / "t002-001a-report.json").write_text(json.dumps({"batch": "001a", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
