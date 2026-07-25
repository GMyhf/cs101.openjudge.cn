import subprocess, tempfile
from pathlib import Path
CASES=['10101\n', '01011001101011\n', '0011011000\n', '111\n', '0010101100110100001110100110010010000101000\n', '110111101111010011110010001111110101100110001111\n', '001011010010111101\n', '101011010111111111100100011\n', '01010100000100011010010\n', '00101011000011000011000100100010100110011\n', '110100000110101100010110000010\n', '10010100000111011010001001011\n', '010100000101110000010010111\n', '00111100001001000000111010100111001011000110111\n', '0101110010001010110101111010110110010\n', '011100\n', '10111111010\n', '0011011110010101010000001010110011001011110010\n', '0011101010100000100000100011011111111111100111101\n', '11111001111001000110100\n']
SOURCE='def count_balanced_substrings(s):\n    # 初始化当前字符和前一个字符的计数器\n    curr_count = 1\n    prev_count = 0\n    result = 0\n\n    # 遍历字符串的每个字符\n    for i in range(1, len(s)):\n        # 如果当前字符和前一个字符相同，增加当前计数器\n        if s[i] == s[i - 1]:\n            curr_count += 1\n        else:\n            # 如果当前字符和前一个字符不同，那么我们可以创建\n            # min(curr_count, prev_count) 个子串\n            result += min(curr_count, prev_count)\n            # 将当前计数器值赋给前一个计数器，并重置当前计数器为1\n            prev_count = curr_count\n            curr_count = 1\n\n    # 出循环后，处理最后一组字符\n    result += min(curr_count, prev_count)\n\n    return result\n\n# 测试样例输入\n#print(count_balanced_substrings("10101"))  # 输出应该是4\n#print(count_balanced_substrings("00110011"))  # 输出应该是6\nprint(count_balanced_substrings(input()))\n'
with tempfile.NamedTemporaryFile('w',suffix='.py') as f:
 f.write(SOURCE); f.flush()
 root=Path(__file__).parent/'data'
 for i,c in enumerate(CASES):
  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout
  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)
