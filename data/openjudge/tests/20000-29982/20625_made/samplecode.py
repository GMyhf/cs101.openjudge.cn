# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def count_balanced_substrings(s):
    # 初始化当前字符和前一个字符的计数器
    curr_count = 1
    prev_count = 0
    result = 0

    # 遍历字符串的每个字符
    for i in range(1, len(s)):
        # 如果当前字符和前一个字符相同，增加当前计数器
        if s[i] == s[i - 1]:
            curr_count += 1
        else:
            # 如果当前字符和前一个字符不同，那么我们可以创建
            # min(curr_count, prev_count) 个子串
            result += min(curr_count, prev_count)
            # 将当前计数器值赋给前一个计数器，并重置当前计数器为1
            prev_count = curr_count
            curr_count = 1

    # 出循环后，处理最后一组字符
    result += min(curr_count, prev_count)

    return result

# 测试样例输入
#print(count_balanced_substrings("10101"))  # 输出应该是4
#print(count_balanced_substrings("00110011"))  # 输出应该是6
print(count_balanced_substrings(input()))
