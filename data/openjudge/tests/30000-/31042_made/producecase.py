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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(run(case))
if __name__=='__main__': main()
