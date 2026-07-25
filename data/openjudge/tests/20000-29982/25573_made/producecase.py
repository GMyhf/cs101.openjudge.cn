import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '\'\'\'\ngreedy，从后往前遍历，看当前这个和他的前面那个，如果这两个相同，并且都需要变化，那就使用一次魔法2，\n用magic来记录当前这个位置使用过的魔法2，方便后续判断；\n如果这两个不同，也就是当前这个需要被改变，而前面那个不需要，那么就是用魔法1，改变当前这一个\n\'\'\'\n\ndef judge(c,m):\n    if c=="B":\n        return m==1\n    if c=="R":\n        return m==0\n\ns=input()\nL=len(s)\ncnt=0\nmagic=0\n\nfor i in range(L-1,-1,-1):\n    if judge(s[i],magic)==True:\n        continue\n    if i>0 and s[i]==s[i-1]:\n        magic = 1 - magic\n    cnt += 1\nprint(cnt)\n'
SAMPLE_IN = 'RRRRRBR\n'
SAMPLE_OUT = '1\n'
def generate_case(r):
    value = "".join(r.choice("RB") for _ in range(r.randint(1, 80)))
    assert set(value) <= set("RB") and value
    return value + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25573 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
