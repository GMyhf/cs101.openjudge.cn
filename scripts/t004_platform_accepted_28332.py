# External reference: statistics page /practice/28332/
# Accepted submission: 52377415
# Source: http://cs101.openjudge.cn/practice/solution/52377415/
# License: not declared on the submission page; no license is inferred.

try:
    while True:
        query=input()
        l=[0]*26
        result=[]
        for i in query:
            if i!=" ":
                l[ord(i)-ord("a")]+=1
                if l[ord(i)-ord("a")]==26-(ord(i)-ord("a")):
                    result.append(chr(ord(i)+ord("A")-ord("a")))
        print(len(result),"".join(result))
except EOFError:
    pass