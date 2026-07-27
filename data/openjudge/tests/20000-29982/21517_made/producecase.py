import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21517/\n# Accepted submission: 52740168\n# Source: http://cs101.openjudge.cn/practice/solution/52740168/\n# License: not declared on the submission page; no license is inferred.\n\ndef main():\n    import sys\n    from collections import defaultdict\n    input = sys.stdin.read().split()\n    ptr = 0\n    N = int(input[ptr])\n    ptr += 1\n    \n    strs = []\n    for _ in range(N):\n        M = int(input[ptr])\n        ptr += 1\n        a = list(map(int, input[ptr:ptr+M]))\n        ptr += M\n        # 生成差分序列\n        diff = []\n        for i in range(M-1):\n            diff.append(str(a[i+1] - a[i]))\n        strs.append(diff)\n    \n    # 二分最长长度\n    l = 0\n    r = max(len(s) for s in strs)\n    ans = 0\n    \n    while l <= r:\n        mid = (l + r) // 2\n        if mid == 0:\n            ans = max(ans, 0)\n            l = mid + 1\n            continue\n        \n        cnt = defaultdict(int)\n        ok = False\n        \n        # 处理第一个串\n        s = strs[0]\n        se = set()\n        for i in range(len(s) - mid + 1):\n            sub = \',\'.join(s[i:i+mid])\n            se.add(sub)\n        for k in se:\n            cnt[k] += 1\n        \n        # 处理其他串\n        for idx in range(1, N):\n            s = strs[idx]\n            se = set()\n            for i in range(len(s) - mid + 1):\n                sub = \',\'.join(s[i:i+mid])\n                se.add(sub)\n            for k in se:\n                cnt[k] += 1\n        \n        # 检查是否有全部串都出现的子串\n        if N in cnt.values():\n            ok = True\n        \n        if ok:\n            ans = mid\n            l = mid + 1\n        else:\n            r = mid - 1\n    \n    print(ans + 1)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='2\n2 1 2\n3 4 5 9\n'
GENERATOR_NAME='g21517'
def g21517(r):
    n = r.randint(40, 70)
    common = r.choice([[1, 3, 7, 12], [1, 4, 9], [2, 5]])
    rows = []
    for _ in range(n):
        values = [r.randint(0, 1864) for _ in range(r.randint(2, 9))]
        p = r.randint(0, len(values))
        values[p:p] = common
        rows.append(" ".join(map(str, [len(values)] + values)))
    return f"{n}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
