# External reference: http://cs101.openjudge.cn/practice/28674/statistics/
# Accepted submission: 52354504
# Source: http://cs101.openjudge.cn/practice/solution/52354504/
# License: not declared on the submission page; no license is inferred.

k=int(input())
s=input()
def decrypt(char,k):
    o=ord(char)
    if o<=ord("Z"):
        c=o-ord("A")
        kr=k%26
        ans=c-kr if c>=kr else 26+c-kr
        return chr(ans+ord("A"))
    else:
        c=o-ord("a")
        kr=k%26
        ans=c-kr if c>=kr else 26+c-kr
        return chr(ans+ord("a"))
answer=""
for i in s:
    answer+=decrypt(i,k)
print(answer)
