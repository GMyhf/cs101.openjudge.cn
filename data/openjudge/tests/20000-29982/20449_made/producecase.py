import subprocess, tempfile
from pathlib import Path
CASES=['011\n', '000101\n', '10011110001010000000101\n', '100111000110101101011\n', '0010100110\n', '1101000110010000101\n', '1\n', '110000010000100001111\n', '0100001010000010111100001010\n', '111111010000\n', '10001101000110110\n', '01011001011100010111001\n', '10110001000011111100100111\n', '10010001110100001\n', '1001\n', '01111100\n', '101100\n', '111110110001001010110110011\n', '00100010100001011100\n', '10101011011100000110100011\n']
SOURCE="def binary_divisible_by_five(binary_string):\n    result = ''\n    num = 0\n    for bit in binary_string:\n        num = (num * 2 + int(bit)) % 5\n        if num == 0:\n            result += '1'\n        else:\n            result += '0'\n    return result\n\nbinary_string = input().strip()\nprint(binary_divisible_by_five(binary_string))\n"
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
