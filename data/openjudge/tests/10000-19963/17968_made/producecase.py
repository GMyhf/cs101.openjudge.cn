import subprocess, tempfile
from pathlib import Path
CASES=['4 5\n24 13 66 77\n', '2 5\n95 85\n', '4 7\n-12 92 79 -60\n', '10 11\n96 -29 -44 47 -26 -85 59 31 -51 93\n', '5 5\n-45 47 -72 6 -34\n', '8 17\n11 96 24 -37 -35 -25 53 -38\n', '3 13\n-100 -65 22\n', '4 17\n40 -18 14 64\n', '3 17\n-40 36 48\n', '9 13\n88 -65 -80 65 -23 -88 -58 74 -9\n', '9 17\n-56 91 -21 -62 -62 -78 57 52 74\n', '2 13\n49 54\n', '6 13\n17 99 -16 59 7 -42\n', '3 13\n-8 90 53\n', '9 11\n8 -48 -75 73 3 -13 -10 -45 42\n', '6 7\n-51 65 9 -66 -43 -49\n', '4 5\n93 57 -59 55\n', '5 5\n64 -21 -24 7 -87\n', '5 17\n-46 1 33 94 91\n', '9 13\n25 81 14 64 -52 -61 54 -38 -50\n']
SOURCE='def insert_hash_table(keys, M):\n    table = [0.5] * M  # 用 0.5 表示空位\n    result = []\n\n    for key in keys:\n        index = key % M\n        i = index\n\n        while True:\n            if table[i] == 0.5 or table[i] == key:\n                result.append(i)\n                table[i] = key\n                break\n            i = (i + 1) % M\n\n    return result\n\n# 使用标准输入读取数据\nimport sys\ninput = sys.stdin.read\ndata = input().split()\n\nN = int(data[0])\nM = int(data[1])\nkeys = list(map(int, data[2:2 + N]))\n\npositions = insert_hash_table(keys, M)\nprint(*positions)\n\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
