# External reference: /practice/29778/statistics/
# Accepted submission: 52682233
# Source: http://cs101.openjudge.cn/practice/solution/52682233/
# License: not declared on the submission page; no license is inferred.

c = 0

def sorting(l):
    if len(l) == 1:
        return l
    global c
    l1, l2 = sorting(l[:len(l)//2]), sorting(l[len(l)//2:])
    n = []
    while l1 or l2:
        if l1 and l2:
            if l1[-1] >= l2[-1]:
                n.append(l1.pop())
            else:
                if not 2*l1[0] >= l2[-1]:
                    l, r = 0, len(l1)
                    while l < r:
                        mid = (l + r)//2
                        if 2*l1[mid] < l2[-1]:
                            l = mid + 1
                        else:
                            r = mid
                    c += l
                n.append(l2.pop())
        elif l1:
            n.extend(l1[::-1])
            l1.clear()
        else:
            n.extend(l2[::-1])
            l2.clear()
    return n[::-1]

sorting([int(input()) for i in range(int(input()))])
print(c)