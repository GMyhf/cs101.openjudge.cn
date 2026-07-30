# External reference: http://cs101.openjudge.cn/practice/27637/statistics/
# Accepted submission: 52708870
# Source: http://cs101.openjudge.cn/practice/solution/52708870/
# License: not declared on the submission page; no license is inferred.

N = int(input())
for _ in range(N):
    s = input()
    preorder = ''
    for c in s:
        if c.isalpha():
            preorder += c
    def get_inorder(st):
        if st == '' or st == '*':
            return ''
        elif st.isalpha():
            return st
        root = st[0]
        p = 0
        index = 0
        for i in range(len(st)):
            if st[i] == '(':
                p += 1
            elif st[i] == ')':
                p -= 1
            elif st[i] == ',' and p == 1:
                index = i
        return get_inorder(st[2:index]) + root + get_inorder(st[index+1:-1])
    print(preorder)
    print(get_inorder(s))
