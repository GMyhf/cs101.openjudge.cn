# External reference: statistics page /practice/19949/
# Accepted submission: 52459098
# Source: http://cs101.openjudge.cn/practice/solution/52459098/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19949 statistics, Accepted solution 52459098.
# Source: http://cs101.openjudge.cn/practice/solution/52459098/
# Statistics: http://cs101.openjudge.cn/practice/19949/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
c=0

def count(query):
    t=query.split()
    cnt=0
    status=False
    for piece in t:
        if "###" in piece:
            if piece.startswith("###") and piece.endswith("###"):
                if not status:
                    cnt+=1
                    status=True
        else:
            status=False
    return cnt

for _ in range(n):
    c+=count(input())

print(c)
