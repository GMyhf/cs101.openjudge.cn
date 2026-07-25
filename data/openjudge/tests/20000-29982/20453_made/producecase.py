import subprocess, tempfile
from pathlib import Path
CASES=['1 1 1\n2\n', '7 8 4 8 0 2 -2 2 8 -4 3 -3 4 5 -2 8 2 -1 4 -5\n12\n', '2 6\n14\n', '3 3 1 -2 3 7 -2 -3 7 -5 -2\n14\n', '-1 -2 -4 -5\n-8\n', '2 5 2 8 3 -1 -1 0 5 6 0 -4 2\n-2\n', '2 8 8 6 3 -3 -2 7 -2 6 7 6 4 2 -1 3 -3 5\n3\n', '2 -5 -1 7\n14\n', '-5 -1 2 -4 -2 -2 2 8 -2 -2 -4 -2 4 -1 6 6\n0\n', '0 6 -3 -5 -1 3 7 6 -4 8 4 -3 -3 0 4 0 0 -5\n3\n', '0 4 -4 6 4\n8\n', '-2 0 1 0 -1 6 -1 7 6\n15\n', '-1 -3 1 -1 -3 5 6\n-8\n', '1 6 -1 3 8 -1 2 -2 4 2 5\n4\n', '4 -3 1\n-8\n', '-4 0 -5 3 2 -2 1 2 -3 1\n15\n', '0 -1 3 3 -3 -1 -2 4 0 5 2\n-3\n', '3 2 4 -2 -4 -2 -3 -1 8 -5 -4 2 -4 -5 5 4 3 6 5 -3\n13\n', '6 4 3 3 5 0 2 4 1 -4 3 -3 -4 5 3 3\n3\n', '0 -4 1\n4\n']
SOURCE='def subarray_sum(nums, k):\n    count = 0\n    sums = 0\n    d = dict()\n    d[0] = 1\n\n    for i in range(len(nums)):\n        sums += nums[i]\n        count += d.get(sums - k, 0)\n        d[sums] = d.get(sums, 0) + 1\n\n    return count\n\nnums = list(map(int, input().split()))\nk = int(input().strip())\nprint(subarray_sum(nums, k))\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
