# External reference: statistics page /practice/20163/
# Accepted submission: 32204981
# Source: http://cs101.openjudge.cn/practice/solution/32204981/
# License: not declared on the submission page; no license is inferred.

n = int(input())
s = []
for i in range(n):
    s += input().split()
output = []
for j in range(len(s)):
    if s[j][0].isupper():
        # check if it is the start of a sentence
        if j == 0 or s[j-1] == ".":
            word = s[j]
            continue
        else:
            if word:
                word += " " + s[j]
            else:
                word = s[j]

    else:
        if word and (j != 0 and s[j-2] != ".") and word not in output:
            output.append(word)
        word = ""
if output:
    print("\n".join(output))
else:
    print("Khong!")
