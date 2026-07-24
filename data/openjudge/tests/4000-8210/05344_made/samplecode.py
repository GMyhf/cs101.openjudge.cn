# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class Node:
    def __init__(self, number):
        self.number = number
        self.next = None

def josephus_circle(n, k):
    # 创建循环链表
    head = Node(1)
    current = head
    for i in range(2, n + 1):
        new_node = Node(i)
        current.next = new_node
        current = new_node
    current.next = head  # 形成环

    result = []
    current = head
    prev = None

    while current.next != current:
        # 找到第k个节点
        for _ in range(k - 1):
            prev = current
            current = current.next
        # 杀掉第k个节点
        result.append(str(current.number))
        prev.next = current.next
        current = prev.next

    # 最后剩下的一个人
    #result.append(str(current.number))
    #return ' '.join(result[:-1])  # 根据题意，只输出被杀掉的编号
    return ' '.join(result)

# 读取输入
n, k = map(int, input().split())

# 计算并输出结果
print(josephus_circle(n, k))
