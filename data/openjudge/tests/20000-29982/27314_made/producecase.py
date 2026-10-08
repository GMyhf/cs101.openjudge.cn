import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/27314/\n# Accepted submission: 52736038\n# Source: http://cs101.openjudge.cn/practice/solution/52736038/\n# License: not declared on the submission page; no license is inferred.\n\nimport re\n\n# 读取输入\ntext = input().strip()\nold_word, new_word = input().strip().split()\n\n# 统一小写用于匹配\ntarget_old = old_word.lower()\ntarget_new = new_word.lower()\n\n# 第一步：遍历每个字符，标记哪些字母是需要被替换的单词\nresult = []\nn = len(text)\ni = 0\ncapitalize_next = True  # 句子开头需要大写\n\nwhile i < n:\n    # 如果不是字母，直接添加\n    if not text[i].isalpha():\n        result.append(text[i])\n        # 遇到句号，下一个字母要大写\n        if text[i] == '.':\n            capitalize_next = True\n        i += 1\n        continue\n\n    # 提取连续字母（单词）\n    word_start = i\n    while i < n and text[i].isalpha():\n        i += 1\n    original_word = text[word_start:i]\n    lower_word = original_word.lower()\n\n    # 判断是否需要替换\n    if lower_word == target_old:\n        use_word = target_new\n    else:\n        use_word = lower_word\n\n    # 处理大小写：仅句子首字母大写，其余小写\n    if capitalize_next and use_word:\n        use_word = use_word[0].upper() + use_word[1:]\n        capitalize_next = False\n\n    result.append(use_word)\n\n# 拼接结果\nprint(''.join(result))"
SAMPLE='Given a text that contains only English letters and punctuation, replace a specific word in it with a given target word. Words are considered the same if they are identical in lowercase form. After replacement, in the modified text, only the first letter of each sentence should be capitalized, with all other letters in lowercase.\nword Woorrd\n'
EXTRA_CASE=None
GENERATOR_NAME='g27314'
LINE1_RE = re.compile(r'[A-Za-z :,.]+')
LINE2_RE = re.compile(r'[A-Za-z]+ [A-Za-z]+')

def valid(text):
    """题面：两行；第一行仅含英文字母、空格与标点 ':' ',' '.'；第二行为两个单词（连续英文字母）。"""
    lines = text.split('\n')
    if len(lines) != 3 or lines[2] != '':
        return False
    if not LINE1_RE.fullmatch(lines[0]) or not re.search(r'[A-Za-z]', lines[0]):
        return False
    return bool(LINE2_RE.fullmatch(lines[1]))

def rand_case(r, w):
    k = r.random()
    if k < 0.15: return w.upper()
    if k < 0.3: return w.capitalize()
    if k < 0.4: return ''.join(c.upper() if r.random() < .5 else c for c in w)
    return w

def g27314(r):
    base = ["alpha", "beta", "gamma", "delta", "word", "target", "a", "an", "the", "is", "of"]
    old = r.choice(["word", "target", "a", "the", "is", "beta"])
    # 含 old 作为子串的“陷阱词”，str.replace 式写法会误改
    traps = [old + "s", "s" + old, old + old, "x" + old + "y"]
    new = rand_case(r, r.choice(["Woorrd", "replaced", "X", "TheNew", "alpha", old, "punc"]))
    vocab = base + traps + [old] * 3
    if r.random() < 0.1:
        vocab = [w for w in vocab if w != old]   # 原单词不出现
    sents = []
    for _ in range(r.randint(1, 14)):
        ws = [rand_case(r, r.choice(vocab)) for _ in range(r.randint(1, 10))]
        s = ws[0]
        for w in ws[1:]:
            sep = r.choice([" ", " ", " ", ", ", ": ", "  ", ","])
            s += sep + w
        sents.append(s)
    text = sents[0]
    for s in sents[1:]:
        text += "." + r.choice([" ", " ", "  "]) + s
    if r.random() < 0.7:
        text += "."
    return text + "\n" + f"{rand_case(r, old)} {new}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else []); s=0
    while len(cases)<40:
        s+=1; c=globals()[GENERATOR_NAME](random.Random(s))
        if c not in cases: cases.append(c)
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
