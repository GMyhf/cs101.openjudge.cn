# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2767: 简单密码
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02767/
# License: not declared; no license is inferred.
import sys
def decrypt_caesar_cipher(ciphertext):
    # 定义字母表
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # 创建一个映射字典：密文字母 -> 明文字母
    decrypt_map = {}
    shift = 5  # 密文向后移动5位
    for i in range(len(alphabet)):
        decrypt_map[alphabet[i]] = alphabet[(i - shift) % len(alphabet)]

    # 解密过程
    plaintext = []
    for char in ciphertext:
        if char in decrypt_map:  # 如果是大写字母，进行解密
            plaintext.append(decrypt_map[char])
        else:  # 非字母字符保持不变
            plaintext.append(char)

    return ''.join(plaintext)

# Input adapter: accept both this mirror's one-line form and the historical START/END wrapper.
lines = sys.stdin.read().splitlines()
if lines and lines[0] == "START":
    for line in lines[1:]:
        if line == "ENDOFINPUT": break
        if line not in ("START", "END"): print(decrypt_caesar_cipher(line))
elif lines:
    print(decrypt_caesar_cipher(lines[0]))
