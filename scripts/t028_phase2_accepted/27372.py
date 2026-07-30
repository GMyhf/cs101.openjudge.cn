# External reference: http://cs101.openjudge.cn/practice/27372/statistics/
# Accepted submission: 52443119
# Source: http://cs101.openjudge.cn/practice/solution/52443119/
# License: not declared on the submission page; no license is inferred.

n=int(input())
query=[]
for i in range(n):
    query.append(input())
query.sort(key=lambda x:len(x))

def has_relation(x,y):
    return x.startswith(y) or y.startswith(x)

class Node:
    def __init__(self,name):
        self.name=name
        self.son=[]
    def append(self,node):
        for i in self.son:
            if has_relation(i.name,node.name):
                i.append(node)
                break
        else:
            self.son.append(node)
    def calculate(self):
        if not self.son:
            return 2
        result=1
        for i in self.son:
            result*=i.calculate()
        return result+1

class Tree:
    def __init__(self):
        self.root=Node("")
    def append(self,node):
        self.root.append(node)
    def calc(self):
        return self.root.calculate()

tree=Tree()
for i in query:
    tree.append(Node(i))
print(tree.calc()-1)
