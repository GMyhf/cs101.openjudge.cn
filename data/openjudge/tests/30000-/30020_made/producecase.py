import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import ceil\ndef fill(vacancy,goods):\n    filled = min(vacancy,goods)\n    vacancy -= filled\n    goods -= filled\n    return vacancy,goods\n\na,b,c,d,e = map(int,input().split())\ntotal = 0\n\n# carriers for pizza\ntotal += a\nvacancy,d = fill(a*5,d) #1*2 fit in space_11\nvacancy,e = fill(vacancy*2+a,e) # 1*1 fit in space 1\n\n# carriers for steak\ntotal += (b+1)//2\nvacancy = (b+1)//2*6 - b*2\nvacancy,c = fill(vacancy,c)\nvacancy,d = fill(vacancy*3,d)\nvacancy,e = fill(vacancy*2,e)\n\n# carriers for the remainder\ntotal += ceil((6*c+2*d+1*e)/36)\n\nprint(total)\n'
SAMPLE_IN = '783 943 34 682 39\n'
def generate_case(r):
    values = [r.randint(1, 1000) for _ in range(5)]
    return " ".join(map(str, values)) + "\n"



def valid(text):
    """题面契约：一行恰五个整数 pizza steak spaghetti chickenwings coke，每个都在 [1,1000]。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    tok = text[:-1].split(" ")
    if len(tok) != 5 or not all(t.isdigit() and t == str(int(t)) for t in tok):
        return False
    return all(1 <= int(t) <= 1000 for t in tok)


def extra_cases():
    """追加：原 40 组全是 [1,1000] 均匀随机，披萨/牛排占主导，鸡翅几乎总被披萨空隙吸收，
    「空隙装不下、溢出到新箱」的分支很少被走到。这里补：全 1 / 全 1000、
    大件极少而小件极多、牛排奇偶（单牛排箱能塞 4 份意面）、鸡翅恰好填满披萨空隙、
    剩余面积恰为 36 的倍数等，以及一批小规模组（另用 6x6 摆放枚举 + DP 的穷举 oracle 核过）。"""
    fixed = [
        (1, 1, 1, 1, 1), (1000, 1000, 1000, 1000, 1000), (1, 1, 1000, 1000, 1000),
        (1, 2, 1000, 1, 1), (1000, 1, 1, 1000, 1000), (1, 1, 1, 1000, 1),
        (1, 1, 1, 1, 1000), (1, 999, 1, 1, 1), (1, 1000, 1, 1, 1), (1, 1, 4, 1, 1),
        (1, 1, 5, 1, 1), (200, 1, 1, 1000, 1), (200, 1, 1, 1000, 200), (200, 1, 1, 999, 400),
        (1, 3, 1000, 1000, 1000), (1, 1000, 1000, 1, 1), (1, 999, 1000, 1000, 1000),
        (1, 2, 3, 15, 1), (3, 2, 4, 15, 3), (1, 1, 3, 9, 18), (2, 1, 1, 1, 36),
        (1, 1, 4, 5, 2), (1, 4, 2, 6, 1), (2, 3, 7, 13, 5), (1, 1, 1, 6, 1),
    ]
    r = random.Random(300200)
    while len(fixed) < 40:
        t = (r.randint(1, 3), r.randint(1, 4), r.randint(1, 6), r.randint(1, 13), r.randint(1, 13))
        if t not in fixed:
            fixed.append(t)
    return [" ".join(map(str, t)) + "\n" for t in fixed]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = list(range(40)) + extra_cases()
        for index, extra in enumerate(cases):
            if index == 0: content = SAMPLE_IN
            elif index >= 40: content = extra
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(30020 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:], content
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
