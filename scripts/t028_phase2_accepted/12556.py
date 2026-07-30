# External reference: http://cs101.openjudge.cn/practice/12556/statistics/
# Accepted submission: 51375933
# Source: http://cs101.openjudge.cn/practice/solution/51375933/
# License: not declared on the submission page; no license is inferred.

string=input().lower()
if len(string)==1:
    print(f"({string},1)")
    exit()
ans=[]
cou=1
for i in range(1,len(string)):
    if string[i]!=string[i-1]:
        ans.append((string[i-1],cou))
        cou=1
    else:
        cou+=1
    if i==len(string)-1:
        ans.append((string[i],cou))
r=' '
for w,c in ans:
    r+=f"({w},{c})"
print(r[1:])
