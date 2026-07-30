# External reference: http://cs101.openjudge.cn/practice/28700/statistics/
# Accepted submission: 52352789
# Source: http://cs101.openjudge.cn/practice/solution/52352789/
# License: not declared on the submission page; no license is inferred.

query=input()
if query[0] in "IVXLCDM":
    d={"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    value=[d[i] for i in query]
    stack=[]
    for i in value:
        if not stack:
            stack.append(i)
        else:
            if i/stack[-1]>=5:
                x=stack.pop()
                stack.append(i-x)
            else:
                stack.append(i)
    print(sum(stack))
else:
    num=int(query)
    answer=""
    if num>=1000:
        answer+="M"*(num//1000)
        num%=1000
    if num>=900:
        answer+="CM"
        num-=900
    if num>=500:
        answer+="D"
        num-=500
    if num>=400:
        answer+="CD"
        num-=400
    if num>=100:
        answer+="C"*(num//100)
        num%=100
    if num>=90:
        answer+="XC"
        num-=90
    if num>=50:
        answer+="L"
        num-=50
    if num>=40:
        answer+="XL"
        num-=40
    if num>=10:
        answer+="X"*(num//10)
        num%=10
    if num==9:
        answer+="IX"
        num-=9
    if num>=5:
        answer+="V"
        num-=5
    if num==4:
        answer+="IV"
        num=0
    if num>=1:
        answer+="I"*num
    print(answer)
