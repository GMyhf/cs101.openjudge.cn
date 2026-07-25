# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
'''
greedy，从后往前遍历，看当前这个和他的前面那个，如果这两个相同，并且都需要变化，那就使用一次魔法2，
用magic来记录当前这个位置使用过的魔法2，方便后续判断；
如果这两个不同，也就是当前这个需要被改变，而前面那个不需要，那么就是用魔法1，改变当前这一个
'''

def judge(c,m):
    if c=="B":
        return m==1
    if c=="R":
        return m==0

s=input()
L=len(s)
cnt=0
magic=0

for i in range(L-1,-1,-1):
    if judge(s[i],magic)==True:
        continue
    if i>0 and s[i]==s[i-1]:
        magic = 1 - magic
    cnt += 1
print(cnt)
