import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#蒋子轩\ndef dfs(rem_sticks,rem_len,target):\n    if rem_sticks==0 and rem_len==0:\n        return True\n    if rem_len==0:\n        rem_len=target\n    for i in range(n):\n        if not used[i] and lens[i]<=rem_len:\n            used[i]=True\n            if dfs(rem_sticks-1,rem_len-lens[i],target):\n                return True\n            else:\n                used[i]=False\n                if lens[i]==rem_len or rem_len==target:\n                    return False\n    return False\nwhile True:\n    n=int(input())\n    if n==0:\n        break\n    lens=list(map(int,input().split()))\n    lens.sort(reverse=True)\n    total_len=sum(lens)\n    for l in range(lens[0],total_len//2+1):\n        if total_len%l!=0:\n            continue\n        used=[False]*n\n        if dfs(n,l,l):\n            print(l)\n            break\n    else:\n        print(total_len)\n'
SAMPLE_IN = '9\n5 2 1 5 2 1 5 2 1\n4\n1 2 3 4\n0\n'
SAMPLE_OUT = '6\n5\n'
def generate_case(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        target = r.randint(3, 18)
        pieces = []
        for _ in range(r.randint(2, 5)):
            remaining = target
            group = []
            while remaining > 0:
                part = r.randint(1, remaining)
                group.append(part); remaining -= part
            pieces.extend(group)
        r.shuffle(pieces)
        assert sum(pieces) % target == 0 and len(pieces) <= 64
        cases.extend([str(len(pieces)), " ".join(map(str, pieces))])
    return "\n".join(cases + ["0"]) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24375 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
