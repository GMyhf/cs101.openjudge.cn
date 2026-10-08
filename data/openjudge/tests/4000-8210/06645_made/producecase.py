import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ns=sys.stdin.read().strip(); bits=[]\nwhile int(s):\n    q,rem=[],0\n    for ch in s:\n        rem=rem*10+ord(ch)-48\n        if q or rem>=2: q.append(str(rem//2)); rem%=2\n    s="".join(q) or "0"; bits.append(str(rem))\nprint("".join(bits[::-1]) or "0")'
SAMPLE_IN='123456789012345678901234567890\n'


def valid(text):
    """题面：只有一行，一个十进制数（数字长度小于 100）。按非负整数、无前导零处理。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not (1 <= len(s) < 100) or not s.isascii() or not s.isdigit():
        return False
    return s == "0" or s[0] != "0"


def g6645(r):
    if r.random() < .15:
        value = 0
    else:
        value = r.randrange(1, 10**40)
    return f"{value}\n"


# 追加组：最小值、2 的幂及其邻居、满 99 位的大数（卡掉只用定长整数的写法）
EXTRA = [
    lambda r: "1\n",
    lambda r: "2\n",
    lambda r: "3\n",
    lambda r: f"{2**63}\n",
    lambda r: f"{2**64 - 1}\n",
    lambda r: f"{2**64}\n",
    lambda r: f"{2**128 + 1}\n",
    lambda r: f"{2**328}\n",
    lambda r: f"{2**328 - 1}\n",
    lambda r: "9" * 99 + "\n",
    lambda r: "1" + "0" * 98 + "\n",
    lambda r: f"{r.randrange(10**98, 10**99)}\n",
    lambda r: f"{r.randrange(10**98, 10**99)}\n",
    lambda r: f"{r.randrange(10**98, 10**99)}\n",
    lambda r: f"{r.randrange(10**60, 10**80)}\n",
    lambda r: f"{r.randrange(10**80, 10**98)}\n",
]


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        contents=[]
        for index in range(40):
            if index==0: content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g6645(random.Random(6645+index+attempt*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            contents.append(content)
        for i, f in enumerate(EXTRA):
            content = f(random.Random(66450 + i))
            assert content not in seen, "追加组与已有组重复"
            seen.append(content)
            contents.append(content)
        assert all(valid(c) for c in contents)
        for index, content in enumerate(contents):
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
