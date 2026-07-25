# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import math
s = input()

slen = len(s)
maxp = int(math.log2(slen))

extracted = ""
for i in range(maxp+1):
    extracted += s[2**i - 1]

left, right = 0, len(extracted)-1
ns = ""
while left < right:
    ns = ns + extracted[left] + extracted[right]
    left += 1
    right -= 1

if len(extracted) % 2 != 0:
    ns += extracted[right]
print(ns)
