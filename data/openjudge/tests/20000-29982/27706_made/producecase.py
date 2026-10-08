import random,re,string,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nprint(" ".join(sys.stdin.read().split()[::-1]))'
SAMPLE_IN="123? you can cage a swallow can't you but you can't swallow a cage can you\n"
# 题面：单词可能包含字母、数字和标点符号
WORD_CHARS = string.ascii_letters + string.digits + string.punctuation
WORD_RE = re.compile("[" + re.escape(WORD_CHARS) + "]{1,10}")


def valid(text):
    """题面：一行句子，单词数不超过 50，每个单词长度不超过 10，单词由字母、数字、标点组成，相邻单词之间恰好一个空格。"""
    if not text.endswith("\n"):
        return False
    line = text[:-1]
    if "\n" in line or "\r" in line:
        return False
    words = line.split(" ")
    if not 1 <= len(words) <= 50:
        return False
    return all(WORD_RE.fullmatch(w) for w in words)


def g27706(r):
    words = [r.choice(["alpha", "B2", "x!", "can't", "42", "node"]) for _ in range(r.randint(1, 20))]
    return " ".join(words) + "\n"


def rand_word(r, length):
    return "".join(r.choice(WORD_CHARS) for _ in range(length))


def g_extra(r, k):
    # 补充组：单词数/单词长度顶到题面上限（50 个、长度 10），以及 1 个单词、单字符等边界
    if k == 0:
        words = [rand_word(r, 10) for _ in range(50)]
    elif k == 1:
        words = [rand_word(r, r.randint(1, 10)) for _ in range(50)]
    elif k == 2:
        words = [rand_word(r, 10)]
    elif k == 3:
        words = [r.choice(string.punctuation)]
    elif k == 4:
        words = [r.choice(string.ascii_letters) for _ in range(50)]
    elif k == 5:
        words = [rand_word(r, 10), rand_word(r, 1)]
    elif k == 6:
        words = ["".join(r.choice(string.punctuation) for _ in range(r.randint(1, 10))) for _ in range(r.randint(30, 50))]
    elif k == 7:
        words = [str(r.randint(0, 10 ** 9)) for _ in range(49)]
    elif k == 8:
        words = [rand_word(r, r.randint(8, 10)) for _ in range(r.randint(45, 50))]
    else:
        words = [rand_word(r, r.randint(1, 10)) for _ in range(r.randint(2, 50))]
    return " ".join(words) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        cases=[]
        for index in range(40):
            if index==0: content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g27706(random.Random(27706+index+attempt*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content); cases.append(content)
        for k in range(10):
            content=g_extra(random.Random(277060+k),k)
            assert content not in seen
            seen.append(content); cases.append(content)
        for index,content in enumerate(cases):
            assert valid(content), index
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
