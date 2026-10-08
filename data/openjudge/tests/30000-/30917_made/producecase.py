import random
REFERENCE='# External reference: /practice/30917/statistics/\n# Accepted submission: 52760585\n# Source: http://cs101.openjudge.cn/practice/solution/52760585/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 使用 sys.stdin 读取输入，处理大数据量时比 input() 更快\n    input_data = sys.stdin.read().splitlines()\n    if not input_data:\n        return\n    \n    T = int(input_data[0])\n    results = []\n    \n    for i in range(1, T + 1):\n        s = input_data[i].strip()\n        n = len(s)\n        \n        # 记录每个字符最后一次出现的下标\n        last_pos = [-1] * 26\n        for idx, char in enumerate(s):\n            last_pos[ord(char) - ord(\'a\')] = idx\n            \n        t = []               # 用列表模拟栈，方便尾部追加和弹出\n        in_t = [False] * 26  # 记录字符是否已经在结果中\n        \n        for idx, char in enumerate(s):\n            char_idx = ord(char) - ord(\'a\')\n            \n            # 如果当前字符已经在结果中，直接跳过\n            if in_t[char_idx]:\n                continue\n                \n            # 贪心策略：如果栈顶元素小于当前字符，且栈顶元素在后面还会出现，则弹出\n            while t and t[-1] < char and last_pos[ord(t[-1]) - ord(\'a\')] > idx:\n                removed_char_idx = ord(t.pop()) - ord(\'a\')\n                in_t[removed_char_idx] = False\n                \n            # 将当前字符加入结果并标记为已存在\n            t.append(char)\n            in_t[char_idx] = True\n            \n        results.append("".join(t))\n        \n    # 统一输出所有结果\n    print("\\n".join(results))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='5\naezakmi\nabacaba\nconvexhull\nswflldjgpaxs\nmyneeocktxpqjpz\n'
GENERATOR_NAME='g30917'
CPP=False
def g30917(r):
    t=r.randint(1,20); return str(t)+"\n"+"\n".join("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,40))) for _ in range(t))+"\n"


def valid(text):
    """题面契约：第一行 T（1<=T<=1e4）；接下来 T 行，每行一个由小写字母组成的（非空）字符串，长度和<=2e5。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    t = int(lines[0])
    if not 1 <= t <= 10**4 or len(lines) != t + 1:
        return False
    total = 0
    for s in lines[1:]:
        if not s or any(not ("a" <= c <= "z") for c in s):
            return False
        total += len(s)
    return total <= 2 * 10**5


def special_cases():
    """替换原第 30..39 组：原数据 T<=20、|s|<=40，规模与 T 上限都没碰到。"""
    r = random.Random(309170)
    A = "abcdefghijklmnopqrstuvwxyz"
    rnd = lambda k, al=A: "".join(r.choice(al) for _ in range(k))
    fmt = lambda ss: f"{len(ss)}\n" + "\n".join(ss) + "\n"
    out = []
    out.append(fmt(["a"]))                                            # 最小
    out.append(fmt([rnd(200000)]))                                    # 单串满长
    out.append(fmt([A * (200000 // 26)]))                             # 升序循环：栈反复弹出
    out.append(fmt(["zyxwvutsrqponmlkjihgfedcba" * (200000 // 26)]))  # 降序循环：一次成型
    out.append(fmt([rnd(200000, "ab")]))                              # 小字母表
    out.append(fmt([rnd(20) for _ in range(10000)]))                  # T 满、每串 20
    out.append(fmt([r.choice(A) for _ in range(10000)]))             # T 满、每串 1 个字符
    lens = [r.randint(1, 60) for _ in range(5000)]
    out.append(fmt([rnd(k) for k in lens]))                           # 混合长度
    s = rnd(199974, "abcdefghijklm") + A                              # 每个字母的最后一次都挤在末尾
    out.append(fmt([s]))
    ss = [rnd(r.randint(1, 3000), A[: r.randint(1, 26)]) for _ in range(120)]
    while sum(map(len, ss)) > 200000: ss.pop()
    out.append(fmt(ss))
    return out

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 30)]+special_cases()
    assert len(cases)==40 and all(valid(c) for c in cases) and len(set(cases))==40
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
