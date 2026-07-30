# External reference: http://cs101.openjudge.cn/practice/30912/statistics/
# Accepted submission: 52724535
# Source: http://cs101.openjudge.cn/practice/solution/52724535/
# License: not declared on the submission page; no license is inferred.

# 1147
import sys
data = sys.stdin.read().splitlines()
n = int(data[0])
li = list(map(int, data[1].split()))
a = 0

class Tree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def make(l):
    if not l:
        return None
    root_val = l[0]
    t = len(l)
    for i in range(1, len(l)):
        if l[i] > root_val:
            t = i
            break
    r = Tree(root_val)
    r.left = make(l[1:t])
    r.right = make(l[t:])
    return r

def lwjx(r):
    global a
    if not r:
        return
    lwjx(r.right)
    a += r.val
    r.val = a
    lwjx(r.left)

r = make(li)
lwjx(r)
que = [[r]]
ans = []
k = 0
while que[k]:
    que.append([])
    for root in que[k]:
        ans.append(str(root.val))
        if root.left:
            que[-1].append(root.left)
        if root.right:
            que[-1].append(root.right)
    k += 1

print(*(ans), sep=' ')
