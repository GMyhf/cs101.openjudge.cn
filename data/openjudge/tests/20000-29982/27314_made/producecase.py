import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/27314/\n# Accepted submission: 52736038\n# Source: http://cs101.openjudge.cn/practice/solution/52736038/\n# License: not declared on the submission page; no license is inferred.\n\nimport re\n\n# 读取输入\ntext = input().strip()\nold_word, new_word = input().strip().split()\n\n# 统一小写用于匹配\ntarget_old = old_word.lower()\ntarget_new = new_word.lower()\n\n# 第一步：遍历每个字符，标记哪些字母是需要被替换的单词\nresult = []\nn = len(text)\ni = 0\ncapitalize_next = True  # 句子开头需要大写\n\nwhile i < n:\n    # 如果不是字母，直接添加\n    if not text[i].isalpha():\n        result.append(text[i])\n        # 遇到句号，下一个字母要大写\n        if text[i] == '.':\n            capitalize_next = True\n        i += 1\n        continue\n\n    # 提取连续字母（单词）\n    word_start = i\n    while i < n and text[i].isalpha():\n        i += 1\n    original_word = text[word_start:i]\n    lower_word = original_word.lower()\n\n    # 判断是否需要替换\n    if lower_word == target_old:\n        use_word = target_new\n    else:\n        use_word = lower_word\n\n    # 处理大小写：仅句子首字母大写，其余小写\n    if capitalize_next and use_word:\n        use_word = use_word[0].upper() + use_word[1:]\n        capitalize_next = False\n\n    result.append(use_word)\n\n# 拼接结果\nprint(''.join(result))"
SAMPLE='Given a text that contains only English letters and punctuation, replace a specific word in it with a given target word. Words are considered the same if they are identical in lowercase form. After replacement, in the modified text, only the first letter of each sentence should be capitalized, with all other letters in lowercase.\nword Woorrd\n'
EXTRA_CASE=None
GENERATOR_NAME='g27314'
def g27314(r):
    words = ["Alpha", "beta", "Gamma", "delta", "word", "TARGET"]
    old, new = r.choice(words), r.choice(words)
    parts = []
    for _ in range(r.randint(2, 12)):
        parts.append(" ".join(r.choice(words) for _ in range(r.randint(2, 7))) + ".")
    return " ".join(parts) + "\n" + f"{old} {new}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
