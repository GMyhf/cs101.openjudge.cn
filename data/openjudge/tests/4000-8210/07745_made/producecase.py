import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split()))\nodd=sorted((x for x in a if x%2),reverse=True)\neven=sorted(x for x in a if not x%2)\nprint(" ".join(map(str,odd+even)))'
SAMPLE_IN='4 7 3 13 11 12 0 47 34 98\n'


def valid(text):
    """题面契约：一行恰 10 个整数，单空格分隔，每个 0 <= x <= 100。"""
    if not text.endswith("\n") or "\n" in text[:-1]:
        return False
    tokens = text[:-1].split(" ")
    return len(tokens) == 10 and all(re.fullmatch(r"0|[1-9][0-9]*", t) and int(t) <= 100 for t in tokens)


def g7745(r):
    return " ".join(str(r.randint(0, 100)) for _ in range(10)) + "\n"


# 追加的边界组（原 40 组随机，没有全奇、全偶、大量重复、全相同的情形）
EXTRA_CASES = [
    "1 3 5 7 9 99 97 95 93 91\n",          # 全奇
    "0 2 4 100 98 96 6 8 10 50\n",        # 全偶，含 0 与 100
    "0 0 0 0 0 0 0 0 0 0\n",              # 全 0
    "100 100 100 100 100 100 100 100 100 100\n",
    "7 7 7 2 2 2 7 2 0 100\n",            # 大量重复
    "1 2 3 4 5 6 7 8 9 10\n",             # 已升序
    "99 1 100 0 51 50 49 48 1 0\n",       # 端点混合 + 重复
    "100 99 98 97 96 95 94 93 92 91\n",   # 已降序
]


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40+len(EXTRA_CASES)):
            if index==0: content=SAMPLE_IN
            elif index>=40: content=EXTRA_CASES[index-40]
            else:
                for attempt in range(100):
                    content=g7745(random.Random(7745+index+attempt*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and (index==0 or content not in seen), content
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
