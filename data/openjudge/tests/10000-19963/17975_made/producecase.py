import subprocess, tempfile
from pathlib import Path
CASES=['5 11\n24 13 35 15 14\n', '3 23\n-40 36 48\n', '9 19\n88 -65 -80 65 -23 -88 -58 74 -9\n', '9 23\n-56 91 -21 -62 -62 -78 57 52 74\n', '2 19\n49 54\n', '6 19\n17 99 -16 59 7 -42\n', '3 19\n-8 90 53\n', '5 17\n8 -48 -75 73 3\n', '6 13\n-51 65 9 -66 -43 -49\n', '4 11\n93 57 -59 55\n', '5 11\n64 -21 -24 7 -87\n', '5 23\n-46 1 33 94 91\n', '9 19\n25 81 14 64 -52 -61 54 -38 -50\n', '4 11\n54 -30 -67 -35\n', '2 13\n3 -25\n', '9 19\n-48 -29 38 -35 -55 -87 40 -33 -43\n', '4 23\n31 82 46 -32\n', '4 11\n-19 20 -67 1\n', '6 19\n-100 -44 -68 43 79 32\n', '7 19\n48 -77 13 -9 36 52 -10\n']
SOURCE='def quadratic_probe_insert(keys, M):\n    table = [None] * M\n    result = []\n\n    for key in keys:\n        pos = key % M\n        if table[pos] is None or table[pos] == key:\n            table[pos] = key\n            result.append(pos)\n            continue\n\n        # 否则开始二次探查\n        i = 1\n        instered = False\n        while not instered:\n            for sign in [1, -1]:\n                new_pos = (pos + sign * (i ** 2)) % M\n                if table[new_pos] is None or table[new_pos] == key:\n                    table[new_pos] = key\n                    result.append(new_pos)\n                    instered = True\n                    break\n\n            i += 1  # 探查次数增加\n\n    return result\n\n\nimport sys\n\ninput = sys.stdin.read\ndata = input().split()\nN = int(data[0])\nM = int(data[1])\nkeys = list(map(int, data[2:2 + N]))\n\npositions = quadratic_probe_insert(keys, M)\nprint(*positions)\n\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
