# External reference: statistics page /practice/27778/
# Accepted submission: 52735575
# Source: http://cs101.openjudge.cn/practice/solution/52735575/
# License: not declared on the submission page; no license is inferred.

import hashlib

def get_md5(s):
    # 创建md5对象
    md5 = hashlib.md5()
    # 必须编码为 bytes 才能加密
    md5.update(s.encode('utf-8'))
    # 返回32位小写十六进制字符串
    return md5.hexdigest()

T = int(input())
for _ in range(T):
    # 读取两行文本
    text1 = input()
    text2 = input()
    # 计算MD5并比较
    if get_md5(text1) == get_md5(text2):
        print("Yes")
    else:
        print("No")