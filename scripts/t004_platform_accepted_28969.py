# External reference: statistics page /practice/28969/
# Accepted submission: 52842137
# Source: http://cs101.openjudge.cn/practice/solution/52842137/
# License: not declared on the submission page; no license is inferred.


def dec(s):
    n=len(s)
    if n==0:
        return ""
    if n==1:
        return s
    mid=(1+n)//2
    sl=dec(s[1:mid])
    sr=dec(s[mid::])
    return sl+s[0]+sr

def main():
    s=input()
    print(dec(s))

    return 



if __name__=="__main__":
    main()