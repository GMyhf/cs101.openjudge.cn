import subprocess, tempfile
from pathlib import Path
CASES=['a\n1\n', 'bc\n5\n', 'c\n22\n', 'cbacb\n94\n', 'acbca\n32\n', 'cabba\n100\n', 'acaa\n88\n', 'acb\n65\n', 'cbbcb\n56\n', 'acca\n95\n', 'c\n11\n', 'aab\n14\n', 'bcac\n33\n', 'caac\n19\n', 'cabaa\n33\n', 'c\n55\n', 'a\n58\n', 'c\n23\n', 'a\n66\n', 'c\n3\n']
SOURCE='def str_to_num(s):\n    """将字符串s转换为对应的26进制数字（a->0, b->1, ...）"""\n    num = 0\n    for c in s:\n        num = num * 26 + (ord(c) - ord(\'a\'))\n    return num\n\ndef num_to_str(num, length):\n    """将数字num转换为固定长度length的26进制字符串"""\n    s = [\'a\'] * length\n    for i in range(length-1, -1, -1):\n        s[i] = chr((num % 26) + ord(\'a\'))\n        num //= 26\n    return "".join(s)\n\nif __name__ == \'__main__\':\n    a = input().strip()\n    k = int(input().strip())\n    num_a = str_to_num(a)\n    num_b = num_a + (k + 1)  # a 与 b 之间正好有 k 个字符串\n    b = num_to_str(num_b, len(a))\n    print(b)\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
