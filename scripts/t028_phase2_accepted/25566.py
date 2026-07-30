# External reference: http://cs101.openjudge.cn/practice/25566/statistics/
# Accepted submission: 52533878
# Source: http://cs101.openjudge.cn/practice/solution/52533878/
# License: not declared on the submission page; no license is inferred.

n=int(input())
process=[]
for _ in range(n):
    compute,write=[int(i) for i in input().split()]
    process.append((compute,write))
process.sort(key=lambda x:-x[1])
compute_border=0
write_border=0
for compute,write in process:
    compute_border+=compute
    write_border=max(write_border,compute_border+write)
print(write_border)
