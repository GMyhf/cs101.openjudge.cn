# Project-authored reference for CS101 local test construction.
# Replaces submission 51275218, which raises NameError when the h-index is zero.
# Platform verification: http://cs101.openjudge.cn/practice/solution/53015094/ (Accepted).
# License: project-authored for this repository.

li = [int(x) for x in input().split()]
li.sort(reverse=True)
h = 0
for i in range(len(li)):
    if li[i] >= i + 1:
        h = i + 1
    else:
        break
print(h)
