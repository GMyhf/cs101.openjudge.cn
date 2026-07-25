import subprocess, tempfile
from pathlib import Path
CASES=['4\n', '17\n', '28\n', '3\n', '8\n', '21\n', '19\n', '25\n', '23\n', '24\n', '29\n', '18\n', '27\n', '2\n', '13\n', '6\n', '9\n', '10\n', '1\n', '14\n']
SOURCE='def tribonacci(n):\n    if n == 0:\n        return 0\n    elif n <= 2:\n        return 1\n    trib = [0, 1, 1] + [0] * (n - 2)\n    for i in range(3, n + 1):\n        trib[i] = trib[i - 1] + trib[i - 2] + trib[i - 3]\n    return trib[n]\n\n# 读取输入并处理\nn = int(input())\nprint(tribonacci(n))\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
