from collections import deque
M, N = map(int, input().split())
words = [int(x) for x in input().split()]
q = deque()
length = 0
dict = [False]*(max(words)+1)
res = 0
for word in words:
    if dict[word]:
        continue
    if length == M:
        x = q.popleft()
        dict[x] = False
    else:
        length += 1
    res += 1
    dict[word] = True
    q.append(word)
print(res)