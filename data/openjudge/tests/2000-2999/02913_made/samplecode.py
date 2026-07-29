# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2913: 加密技术
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02913/
# License: not declared; no license is inferred.
import sys
def encrypt(text):
    # 数字序列"4962873"
    pattern = "4962873"
    encrypted_text = []
    for i, char in enumerate(text):
        # ASCII码范围限制在32到122之间，超出范围进行模运算
        shift = int(pattern[i % len(pattern)])
        new_char = chr((ord(char) + shift - 32) % (122 - 32 + 1) + 32)
        encrypted_text.append(new_char)
    return ''.join(encrypted_text)

def decrypt(encrypted_text):
    # 数字序列"4962873"
    pattern = "4962873"
    decrypted_text = []
    for i, char in enumerate(encrypted_text):
        # 解密时反向操作
        shift = int(pattern[i % len(pattern)])
        new_char = chr((ord(char) - shift - 32) % (122 - 32 + 1) + 32)
        decrypted_text.append(new_char)
    return ''.join(decrypted_text)


text = input()

encrypted = encrypt(text)
print(encrypted)

decrypted = decrypt(encrypted)
print(decrypted)
