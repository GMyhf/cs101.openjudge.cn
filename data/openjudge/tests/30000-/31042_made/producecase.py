import random
REFERENCE="# External reference: /practice/31042/statistics/\n# Accepted submission: 52824909\n# Source: http://cs101.openjudge.cn/practice/solution/52824909/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # Read all lines from standard input\n    input_data = sys.stdin.read().splitlines()\n    if not input_data:\n        return\n    \n    # Safely parse N and the old file lines\n    idx = 0\n    while idx < len(input_data) and not input_data[idx].strip().isdigit():\n        idx += 1\n    if idx >= len(input_data):\n        return\n    N = int(input_data[idx])\n    idx += 1\n    old_file = input_data[idx : idx + N]\n    idx += N\n    \n    # Safely parse M and the new file lines\n    while idx < len(input_data) and not input_data[idx].strip().isdigit():\n        idx += 1\n    if idx >= len(input_data):\n        return\n    M = int(input_data[idx])\n    idx += 1\n    new_file = input_data[idx : idx + M]\n    \n    # suf[i][j] stores the LCS of old_file[i:] and new_file[j:]\n    suf = [[0] * (M + 1) for _ in range(N + 1)]\n    \n    # Fill the DP table backwards\n    for i in range(N - 1, -1, -1):\n        suf_i = suf[i]\n        suf_i1 = suf[i+1]\n        old_val = old_file[i]\n        for j in range(M - 1, -1, -1):\n            if old_val == new_file[j]:\n                suf_i[j] = suf_i1[j+1] + 1\n            else:\n                val1 = suf_i1[j]\n                val2 = suf_i[j+1]\n                suf_i[j] = val1 if val1 > val2 else val2\n                \n    # Reconstruct the optimal path lexicographically\n    i, j = 0, 0\n    ans = []\n    while i < N or j < M:\n        R = suf[i][j]\n        # Option 0: Match (' ') - Weight 0\n        if i < N and j < M and old_file[i] == new_file[j] and suf[i+1][j+1] == R - 1:\n            ans.append(' ' + old_file[i])\n            i += 1\n            j += 1\n        # Option 1: Delete ('-') - Weight 1\n        elif i < N and suf[i+1][j] == R:\n            ans.append('-' + old_file[i])\n            i += 1\n        # Option 2: Add ('+') - Weight 2\n        elif j < M and suf[i][j+1] == R:\n            ans.append('+' + new_file[j])\n            j += 1\n            \n    print('\\n'.join(ans))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE="3\ndef main():\n    print('Hello')\n    return True\n4\ndef main():\n    # 打印问候\n    print('Hello World')\n    return True\n"
GENERATOR='g31042'
def g31042(r):
    """Generate two related line-oriented files with changes and LCS ties."""
    alphabet = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    size = r.randint(2, 45)
    old = [f"    {r.choice(alphabet)}_{i % 9}" if r.random() < .2 else f"{r.choice(alphabet)}_{i % 9}" for i in range(size)]
    new = []
    for line in old:
        action = r.random()
        if action < .18:
            continue
        if action < .42:
            new.append(f"+generated_{r.randint(0, 20)}")
        new.append(line if r.random() < .78 else f"{r.choice(alphabet)}_{r.randint(0, 8)}")
    for _ in range(r.randint(0, 8)):
        new.insert(r.randint(0, len(new)), r.choice(alphabet) + "_inserted")
    if not new:
        new = ["replacement"]
    return f"{len(old)}\n" + "\n".join(old) + f"\n{len(new)}\n" + "\n".join(new) + "\n"

def valid(text):
    """题面契约：N、N 行旧文本、M、M 行新文本，行数与给出的整数严格一致，之后无多余内容。"""
    if not text.endswith("\n") or "\r" in text: return False
    lines = text[:-1].split("\n")
    def count(x):
        return int(x) if x.isdigit() and (x == "0" or x[0] != "0") else None
    if not lines: return False
    n = count(lines[0])
    if n is None or len(lines) < n + 2: return False
    m = count(lines[n + 1])
    if m is None: return False
    return len(lines) == n + m + 2

def _pack(old, new):
    return f"{len(old)}\n" + "\n".join(old) + f"\n{len(new)}\n" + "\n".join(new) + "\n"

def _mutate(r, old, p_del, p_rep, p_ins, pool):
    new = []
    for line in old:
        if r.random() < p_ins: new.append(r.choice(pool))
        x = r.random()
        if x < p_del: continue
        new.append(r.choice(pool) if x < p_del + p_rep else line)
    return new or [r.choice(pool)]

def special_case(i):
    """补充：完全相同、完全不同、单行、重复行大量平局、千行级规模（O(NM) DP 在时限内）、纯插入、整体反转、仅缩进不同。"""
    r = random.Random(310420 + i)
    code = ["def f(x):", "    return x", "    pass", "if x:", "else:", "    x += 1", "    print(x)", "for i in range(n):", "}", "{", "    # todo", "import sys"]
    if i == 30:
        old = [f"line_{k % 7}" for k in range(30)]; return _pack(old, list(old))
    if i == 31:
        return _pack([f"old_{k}" for k in range(20)], [f"new_{k}" for k in range(25)])
    if i == 32:
        return _pack(["same"], ["same"])
    if i == 33:
        return _pack(["a"], ["b"])
    if i == 34:
        return _pack(["a", "b", "a", "b", "a", "b", "a"], ["b", "a", "b", "a", "b", "a", "b", "b"])
    if i == 35:
        pool = [f"t{k}" for k in range(6)]
        old = [r.choice(pool) for _ in range(2500)]
        return _pack(old, _mutate(r, old, .15, .15, .15, pool))
    if i == 36:
        old = [r.choice(code) for _ in range(2000)]
        return _pack(old, _mutate(r, old, .1, .1, .1, code + ["    new_line()", "# added"]))
    if i == 37:
        old = [r.choice(code) for _ in range(300)]
        new = []
        for line in old:
            new.append(line)
            if r.random() < .6: new.append(r.choice(code))
        return _pack(old, new)
    if i == 38:
        old = [r.choice(code[:5]) for _ in range(400)]
        return _pack(old, old[::-1])
    if i == 39:
        old = ["x = 1", "  x = 1", "    x = 1", "y", "  y", "y"]
        return _pack(old, ["    x = 1", "x = 1", "y", "  y", "  y", "x = 1"])
    raise ValueError(i)

from pathlib import Path
import random, subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        path=Path(d)/'main.py'; path.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(path)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 30)]+[special_case(i) for i in range(30, 40)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(run(case))
if __name__=='__main__': main()
