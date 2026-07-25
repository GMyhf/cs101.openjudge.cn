import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import ceil\ndef fill(vacancy,goods):\n    filled = min(vacancy,goods)\n    vacancy -= filled\n    goods -= filled\n    return vacancy,goods\n\na,b,c,d,e = map(int,input().split())\ntotal = 0\n\n# carriers for pizza\ntotal += a\nvacancy,d = fill(a*5,d) #1*2 fit in space_11\nvacancy,e = fill(vacancy*2+a,e) # 1*1 fit in space 1\n\n# carriers for steak\ntotal += (b+1)//2\nvacancy = (b+1)//2*6 - b*2\nvacancy,c = fill(vacancy,c)\nvacancy,d = fill(vacancy*3,d)\nvacancy,e = fill(vacancy*2,e)\n\n# carriers for the remainder\ntotal += ceil((6*c+2*d+1*e)/36)\n\nprint(total)\n'
SAMPLE_IN = '783 943 34 682 39\n'
def generate_case(r):
    values = [r.randint(1, 1000) for _ in range(5)]
    return " ".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30020 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
