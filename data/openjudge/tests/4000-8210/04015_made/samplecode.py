# External reference: http://cs101.openjudge.cn/practice/04015/statistics/
# Accepted submission: 52594412
# Source: http://cs101.openjudge.cn/practice/solution/52594412/
# License: not declared on the submission page; no license is inferred.

import sys

if __name__=="__main__":
    for line in sys.stdin:
        line=line.strip()
        if not line:
            continue
        ok=0
        if (geshu:=line.count("@"))==1:
            if line[0] not in ("." , "@") and line[-1] not in ("." , "@"):
                weizhi=line.find("@")
                if "." in line[weizhi+2:] and "." not in (line[weizhi+1],line[weizhi-1]):
                    ok=1
                    print("YES")
        if ok==0:
            print("NO")
