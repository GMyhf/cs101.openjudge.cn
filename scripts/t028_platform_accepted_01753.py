# External reference: statistics page /practice/01753/
# Accepted submission: 50209622
# Source: http://cs101.openjudge.cn/practice/solution/50209622/
# License: not declared on the submission page; no license is inferred.

from collections import deque
matrix = []
limit = 2**16
for i in range(4):
    matrix.append(input())
temp = ''
for i in range(4):
    for j in range(4):
        if matrix[i][j] == 'b':
            temp += '1'
        else:
            temp += '0'
target = int(temp,2)
target_ = target ^ limit-1
dict_ = dict()
my_deque = deque()
my_deque.append((0,0))

def flip(number,place):
    x = place % 4
    y = place // 4
    number ^= (1 << (y*4+x))
    for a,b in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if 0 <= a < 4 and 0 <= b < 4:
            number ^= (1 << (b*4+a))
    return number


def bfs():
    while True:
        if my_deque:
            a, count = my_deque.popleft()
            for i in range(16):
                _ = flip(a,i)
                if not dict_.get(_,False):
                    dict_[_] = count + 1
                    my_deque.append((_,count+1))
        else:
            return
bfs()
if target == 0 or target == limit-1:
    print(0)
elif dict_.get(target,False) or dict_.get(target_,False):
    print(min(dict_.get(target,float('inf')), dict_.get(target_,float('inf'))))
else:
    print('Impossible')
