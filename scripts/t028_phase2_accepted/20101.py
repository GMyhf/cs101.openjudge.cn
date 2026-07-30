# External reference: http://cs101.openjudge.cn/practice/20101/statistics/
# Accepted submission: 51358790
# Source: http://cs101.openjudge.cn/practice/solution/51358790/
# License: not declared on the submission page; no license is inferred.

n=int(input())
s=input()
lx=[]
lnum=[]
l=[]
i=0
ab=""
while i<len(s):
    if s[i] in ("+","-"):
        if ab:
            l.append(ab)
        ab=s[i]
        i+=1
    else:
        ab+=s[i]
        i+=1
l.append(ab)
def xnum(x):
    x=x.replace("^","")
    if "x" not in x:
        lnum.append(int(x))
        lx.append(0)
    else:
        a,b=x.split("x")
        if a in ("+",""):
            lnum.append(1)
        elif a=="-":
            lnum.append(-1)
        else:
            lnum.append(int(a))
        if b=="":
            lx.append(1)
        else:
            lx.append(int(b))
for i in l:
    xnum(i)
k=lx[0]
m=len(lx)
sans=""
for i in range(k+1):
    ans=0
    for j in range(m):
        if lx[j]>=0:
            ans+=lnum[j]*(n**lx[j])
            lnum[j]*=lx[j]
            lx[j]-=1
    for j in range(1,i+1):
        ans//=j
    if ans==0:
        continue
    elif ans>0:
        if sans and ans!=1:
            sans+="+"+str(ans)
        elif sans and ans==1:
            sans+="+"
        elif ans==1 and i!=0:
            sans+=""
        else:
            sans+=str(ans)
    else:
        if i==0 or ans!=-1:
            sans+=str(ans)
        else:
            sans+="-"
    if i==0:
        continue
    elif i==1:
        sans+="(x-"+str(n)+")"
    else:
        sans+="(x-"+str(n)+")"+"^"+str(i)
sans=sans.replace("--","+")
print(sans)
