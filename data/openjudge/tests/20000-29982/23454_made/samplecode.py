# External reference: statistics page /practice/23454/
# Accepted submission: 52297305
# Source: http://cs101.openjudge.cn/practice/solution/52297305/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23454/
# Accepted submission: 52297305
# Source: http://cs101.openjudge.cn/practice/solution/52297305/
# License: not declared on the submission page; no license is inferred.

s=input()
ans=''
found=False
for i in range(len(s)):
    if s[i]!=' ':
        ans+=s[i]
        if found==True:
            found=False
    elif found==False:
        ans+=s[i]
        found=True
print(ans)