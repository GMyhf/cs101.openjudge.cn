# External reference: http://cs101.openjudge.cn/practice/30894/statistics/
# Accepted submission: 52713911
# Source: http://cs101.openjudge.cn/practice/solution/52713911/
# License: not declared on the submission page; no license is inferred.

import heapq
class huffmannode:
    def __init__(self,char,weight):
        self.left = None
        self.right = None
        self.char = char
        self.weight = weight
    def __lt__(self, other):
        if self.weight == other.weight:
            return self.char < other.char
        return self.weight<other.weight

def main():
    n = int(input())
    heap = []
    for _ in range(n):
        char,weight = input().split()
        weight = int(weight)
        heap.append(huffmannode(char,weight))
    heapq.heapify(heap)
    while len(heap)>1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merge = huffmannode(min(left.char,right.char),left.weight+right.weight)
        merge.left = left
        merge.right = right
        heapq.heappush(heap,merge)
    root = heap[0]
    codes = {}
    def encode(root,code):
        if not root:
            return
        if not root.left and not root.right:
            codes[root.char] = code
            return
        encode(root.left,code+'0')
        encode(root.right,code+'1')
    encode(root,'')

    def huffencode(s):
        code = ''
        for ch in s:
            code += codes[ch]
        return code
    def decode(s):
        nonlocal root
        ans = ''
        node = root
        for ch in s:
            if ch == '0':
                node = node.left
            else:
                node = node.right
            if not node.left and not node.right:
                ans += node.char
                node = root
        return ans
    res = []
    while True:
        try:
            line = input()
            if line.isdigit():
                res.append(decode(line))
            else:
                res.append(huffencode(line))
        except EOFError:
            break
    for tt in res:
        print(tt)
if __name__=='__main__':
    main()
