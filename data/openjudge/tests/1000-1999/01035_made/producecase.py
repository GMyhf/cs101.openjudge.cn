import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：词典每行一个单词、以 # 结束，单词互不相同、至多 10000 个；
    随后查询每行一个、以 # 结束，至多 50 个；单词均为 1..15 个小写字母。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    word = re.compile(r'[a-z]{1,15}$')
    if lines.count('#') != 2 or lines[-1] != '#':
        return False
    k = lines.index('#')
    dic, qs = lines[:k], lines[k + 1:-1]
    if len(dic) > 10000 or len(set(dic)) != len(dic) or len(qs) > 50:
        return False
    return all(word.match(w) for w in dic + qs)
def _word(r, alpha, lo=1, hi=15):
    return ''.join(r.choice(alpha) for _ in range(r.randint(lo, hi)))
def _edit(r, w, alpha):
    """对 w 做一次删除/替换/插入（结果长度保持在 1..15）。"""
    ops = []
    if len(w) > 1: ops.append('del')
    ops.append('rep')
    if len(w) < 15: ops.append('ins')
    op = r.choice(ops); i = r.randrange(len(w))
    if op == 'del':
        return w[:i] + w[i + 1:]
    if op == 'rep':
        return w[:i] + r.choice(alpha) + w[i + 1:]
    return w[:i] + r.choice(alpha) + w[i:]
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if seed == 1:
        dic = ['a']; qs = ['a', 'b', 'aa', 'ab', 'ba', 'aaa']
    elif seed == 2:
        dic = ['ab', 'ba', 'abc', 'acb', 'bac', 'b', 'a', 'abcd']
        qs = ['ab', 'ba', 'bca', 'abdc', 'cab', 'x', 'abc', 'abcde', 'ac']
    elif seed == 3:
        dic = [''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(15)) for _ in range(20)]
        dic = list(dict.fromkeys(dic))
        qs = [w for w in dic[:5]] + [w[:-1] for w in dic[5:10]] + [w[:7] + 'q' + w[8:] for w in dic[10:15]]
    elif seed == 4:
        # 稠密短词：全部 1、2 字母词 + 随机 3 字母词凑满 10000，查询的相似词成百上千
        L = 'abcdefghijklmnopqrstuvwxyz'
        dic = list(L) + [a + b for a in L for b in L]
        three = [a + b + c for a in L for b in L for c in L]; r.shuffle(three)
        dic += three[:10000 - len(dic)]; r.shuffle(dic)
        rest = three[10000 - 702:]
        qs = [r.choice(rest) for _ in range(30)] + [r.choice(dic) for _ in range(10)] + \
             [''.join(r.choice(L) for _ in range(4)) for _ in range(10)]
    else:
        big = seed >= 20
        alpha = r.choice(['ab', 'abc', 'abcde', 'abcdefghij', 'abcdefghijklmnopqrstuvwxyz'])
        target = 10000 if seed >= 30 else (r.randint(2000, 10000) if big else r.randint(5, 300))
        lo, hi = (1, 15)
        if alpha in ('ab', 'abc'):
            lo = 3 if alpha == 'abc' else 5        # 字母表太小时抬高最短长度，才凑得出足够多的不同单词
        seen = set(); dic = []
        tries = 0
        while len(dic) < target and tries < target * 20:
            tries += 1
            w = _word(r, alpha, lo, hi)
            if w not in seen:
                seen.add(w); dic.append(w)
        qn = 50 if seed % 4 else r.randint(1, 50)
        qs = []
        for _ in range(qn):
            kind = r.random()
            if kind < 0.2:
                qs.append(r.choice(dic))
            elif kind < 0.75:
                qs.append(_edit(r, r.choice(dic), alpha))
            elif kind < 0.85:
                qs.append(_word(r, 'abcdefghijklmnopqrstuvwxyz', 1, 15))
            elif kind < 0.92:
                w = r.choice(dic)
                if len(w) >= 2:
                    i = r.randrange(len(w) - 1); w = w[:i] + w[i + 1] + w[i] + w[i + 2:]   # 相邻对调：不算相似
                qs.append(w)
            else:
                qs.append(r.choice(qs) if qs else r.choice(dic))   # 重复查询
    return '\n'.join(dic + ['#'] + qs + ['#']) + '\n'
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1035: 拼写检查\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01035/\n# License: not declared in source collection; no license is inferred.\nimport sys\ndef is_correct(word, dictionary):\n    # 检查单词是否在字典中\n    return word in dictionary\n\ndef similar(word, dict_word):\n    # 检查word与dict_word是否相似，依据三种规则\n    len_word = len(word)\n    len_dict_word = len(dict_word)\n\n    # 1. 删除一个字母\n    if len_word - 1 == len_dict_word:\n        for i in range(len_word):\n            if word[:i] + word[i+1:] == dict_word:\n                return True\n\n    # 2. 替换一个字母\n    if len_word == len_dict_word:\n        diff_count = 0\n        for i in range(len_word):\n            if word[i] != dict_word[i]:\n                diff_count += 1\n            if diff_count > 1:\n                return False\n        if diff_count == 1:\n            return True\n\n    # 3. 插入一个字母\n    if len_word + 1 == len_dict_word:\n        for i in range(len_dict_word):\n            if word == dict_word[:i] + dict_word[i+1:]:\n                return True\n\n    return False\n\ndef check_words(dictionary, queries):\n    results = []\n\n    for word in queries:\n        if is_correct(word, dictionary):\n            results.append(f"{word} is correct")\n        else:\n            similar_words = []\n            for dict_word in dictionary:\n                if similar(word, dict_word):\n                    similar_words.append(dict_word)\n            if similar_words:\n                results.append(f"{word}: " + " ".join(similar_words))\n            else:\n                results.append(f"{word}:")\n\n    return results\n\ndef main():\n    # 读入词典部分\n    dictionary = []\n    while True:\n        word = input().strip()\n        if word == \'#\':\n            break\n        dictionary.append(word)\n\n    # 读入查询部分\n    queries = []\n    while True:\n        word = input().strip()\n        if word == \'#\':\n            break\n        queries.append(word)\n\n    # 检查单词\n    results = check_words(dictionary, queries)\n\n    # 输出结果\n    for result in results:\n        print(result)\n\nif __name__ == "__main__":\n    main()\n'
NUMBER=1035
SAMPLE='i\nis\nhas\nhave\nbe\nmy\nmore\ncontest\nme\ntoo\nif\naward\n#\nme\naware\nm\ncontest\nhav\noo\nor\ni\nfi\nmre\n#\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
