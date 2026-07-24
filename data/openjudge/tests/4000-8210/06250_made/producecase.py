import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = 'abcd123ab888efghij45ef67kl,ab,ef\n'
SAMPLE_OUT = '18\n'
CASES = ['abcd123ab888efghij45ef67kl,ab,ef\n', '7oe0fuc7qv8qamdajl4iafpnbl8ykch9qbifl,a,b\n', 'z9unqbruaaacdsubmwknndb41,a,b\n', 'un47xfz3qamdx0pjqwjog2sebobazzhsvbunw,a,b\n', '044nqzheg2kzaynhe8dpb540kgnx087q,a,b\n', 'cphxa421uigi3bme2w7iv,a,b\n', '0m3n5pam0iissbtgb8ln1otc8u,a,b\n', 'r0ojwyaac45hh9n6bddvjsplke9czz,a,b\n', 'oifa08fg6tzu46mcakbhdzxqb,a,b\n', '4229aqsncqklrvm54e9ba61lw6,a,b\n', 'eigzq4xaj3gvuzmfo1ebgl19vm1,a,b\n', '615dmznkdk3blbar1mx5ybpds80b3r,a,b\n', 'lncag6t88f8bzjwmko2c7,a,b\n', '1h4lttoear46sc82alwab2bla4c8xa3xh,a,b\n', '0vf035hs65tanmw6xd6pcklbp0v32qlgw4wc1,a,b\n', 'gaqnv3ua2x50qb3x7zh7txeg,a,b\n', 'zroa8p43td8rdr6arbn19rakc24,a,b\n', 'jhj5scagl6e0nh3s9vkabfhy1zm036bn,a,b\n', 'fi240u1pd9hvatqobths28r3,a,b\n', 'bxuo3nhq7ayx5nqzqbul4id0azcr08i,a,b\n']
REFERENCE_SOURCE = "# 23n2300017735(夏天明BrightSummer)\ndef find(s, pat):\n    nex = [0]\n    for i, p in enumerate(pat[1:], 1):\n        tmp = nex[i-1]\n        while True:\n            if p == pat[tmp]:\n                nex.append(tmp+1)\n                break\n            elif tmp:\n                tmp = nex[tmp-1]\n            else:\n                nex.append(0)\n                break\n    j = 0\n    for i, char in enumerate(s):\n        while True:\n            if char == pat[j]:\n                j += 1\n                if j == len(pat):\n                    return i\n                break\n            elif j:\n                j -= nex[j]\n            else:\n                break\n\ns, p1, p2 = input().split(',')\ntry:\n    assert((ans := len(s)-find(s, p1)-find(s[::-1], p2[::-1])-2) >= 0)\n    print(ans)\nexcept (TypeError, AssertionError):\n    print(-1)\n"
assert CASES[0] == SAMPLE_IN
random.seed(6250)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
