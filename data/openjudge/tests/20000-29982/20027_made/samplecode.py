# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def str_to_num(s):
    """将字符串s转换为对应的26进制数字（a->0, b->1, ...）"""
    num = 0
    for c in s:
        num = num * 26 + (ord(c) - ord('a'))
    return num

def num_to_str(num, length):
    """将数字num转换为固定长度length的26进制字符串"""
    s = ['a'] * length
    for i in range(length-1, -1, -1):
        s[i] = chr((num % 26) + ord('a'))
        num //= 26
    return "".join(s)

if __name__ == '__main__':
    a = input().strip()
    k = int(input().strip())
    num_a = str_to_num(a)
    num_b = num_a + (k + 1)  # a 与 b 之间正好有 k 个字符串
    b = num_to_str(num_b, len(a))
    print(b)
