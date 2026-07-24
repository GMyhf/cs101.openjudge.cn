# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_number = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, number):
        node = self.root
        for digit in number:
            if digit not in node.children:
                node.children[digit] = TrieNode()
            node = node.children[digit]
            # 如果当前节点已经是某个电话号码的结尾，则说明存在前缀冲突
            if node.is_end_of_number:
                return False
        # 插入完成后，标记为完整电话号码
        node.is_end_of_number = True
        # 如果当前节点还有子节点，说明有其他号码以它为前缀
        return len(node.children) == 0
    
    def is_consistent(self, numbers):
        # 按长度从短到长排序，确保短号码先被检查
        numbers.sort(key=len)
        for number in numbers:
            if not self.insert(number):
                return False
        return True

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    t = int(data[0])  # 测试样例数量
    index = 1
    results = []
    
    for _ in range(t):
        n = int(data[index])  # 当前测试样例的电话号码数量
        index += 1
        numbers = data[index:index + n]
        index += n
        
        trie = Trie()
        if trie.is_consistent(numbers):
            results.append("YES")
        else:
            results.append("NO")
    
    print("\n".join(results))

# 调用主函数
if __name__ == "__main__":
    main()
