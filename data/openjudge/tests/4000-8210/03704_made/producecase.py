import random,re,string,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfor line in sys.stdin.read().splitlines():\n    bad=[" "]*len(line); stack=[]\n    for i,ch in enumerate(line):\n        if ch=="(": stack.append(i)\n        elif ch==")":\n            if stack: stack.pop()\n            else: bad[i]="?"\n    for i in stack: bad[i]="$"\n    print(line); print("".join(bad).rstrip())'
SAMPLE_IN='((ABCD(x)\n)(rttyy())sss)(\n'
def g3704(r):
    lines=[]
    for _ in range(r.randint(1, 5)):
        s="".join(r.choice("()ABCxyz") for _ in range(r.randint(1, 40)))
        lines.append(s)
    return "\n".join(lines)+"\n"



def valid(text):
    """题面契约：多组数据，每组一行，只含左右括号和大小写字母，长度 1..100。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    return bool(lines) and all(re.fullmatch(r"[()A-Za-z]{1,100}", s) for s in lines)


LETTERS = string.ascii_letters


def g_big(r):
    """长度贴上限 100 的多行：随机、深嵌套、全左/全右、无括号、交错。"""
    lines = []
    lines.append("".join(r.choice("()" + LETTERS) for _ in range(100)))
    lines.append("".join(r.choice("()()" + LETTERS) for _ in range(99)))
    lines.append("(" * 50 + ")" * 50)
    lines.append("(" * 51 + ")" * 49)
    lines.append(")" * 49 + "(" * 51)
    lines.append("(" * 100)
    lines.append(")" * 100)
    lines.append("".join(r.choice(LETTERS) for _ in range(100)))   # 无括号：第二行全空
    lines.append(")(" * 50)
    lines.append("".join(r.choice("()") for _ in range(100)))
    r.shuffle(lines)
    return "\n".join(lines) + "\n"


def g_mix(r):
    lines = []
    for _ in range(r.randint(5, 30)):
        n = r.choice([1, 2, r.randint(1, 100), 100])
        lines.append("".join(r.choice("((()))" + LETTERS[r.randrange(52)]) for _ in range(n)))
    return "\n".join(lines) + "\n"


FIXED = "(\n)\nA\nz\n()\n)(\nAbCdEfGhIjKlMnOpQrStUvWxYz\n((a)b)c)d(e\n"


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(48):
            if index==0: content=SAMPLE_IN
            elif index<40:
                for attempt_no in range(100):
                    content=g3704(random.Random(3704+index+attempt_no*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            elif index==40: content=FIXED
            elif index<44: content=g_big(random.Random(3704000+index))
            else: content=g_mix(random.Random(3704000+index))
            assert valid(content), index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
