# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
# 23n2300011072(蒋子轩)
def add(n, left, right, string):
    # 终止条件：如果已经放置了所有的括号
    if left == n and right == n:
        print(string)
        return

    # 如果我们仍然可以放置左括号，则添加左括号
    if left < n:
        add(n, left+1, right, string+'(')

    # 如果右括号数量小于左括号数量，则添加右括号
    if right < left:
        add(n, left, right+1, string+')')

n = int(input())
add(n, 0, 0, '')
