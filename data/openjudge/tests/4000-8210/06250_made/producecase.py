import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = 'abcd123ab888efghij45ef67kl,ab,ef\n'
SAMPLE_OUT = '18\n'
CASES = ['abcd123ab888efghij45ef67kl,ab,ef\n', 'i807iagb1efxxy5e8a9chg8f72f9vd7i,xxy,v\n', 'aeabbj03wvw1fggbayy305b50g929,yy,wvw\n', '4igb13he8i1ehd4yxjc9haa22dj0a08vw1j7d0b,yx,vw\n', 'dcd4f2j2g9dc7yyybh75853fdg13976wvv8ac5dh6,yyy,wvv\n', '5430ede4xgc416e0w804fh03b622e,x,w\n', 'g5h2g3ee9jjayd27fg3hvjb70bc39i15g17,y,v\n', 'a8b558dd7y6bb0ejwwhffc7b2824hb862,y,ww\n', 'd6j8x208956gb9a8fwwvdb21ia,x,wwv\n', 'biffi0g9558cvv7ha63f16a1f7by54a8c5ibbf62,y,vv\n', '6e4d002gv8h3cxxdf370g8,xx,v\n', 'bf94avagi83yyx1521hb,yyx,v\n', 'd6j9779c732e1xfh4b60whg9,x,w\n', 'c6i9569jb74af1ayx4afa5b71a41dvwv6g78dh9061ig6a,yx,vwv\n', '965j6ggyyx161b6hb9ffh30vv4ifd151b39,yyx,vv\n', '4153ixx41692d6j81wvd2d2,xx,wv\n', '4jb7ib9i6ay398g37iwwfb4,y,ww\n', 'df6x3gd9w4j70fa6cd232g,x,w\n', 'b79d0axxyihijdj4vv9i4475ae6dj,xxy,vv\n', 'i6j215gi2i0f5wv9eb39a2bi37ebdxy9728igf4,xy,wv\n']
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
