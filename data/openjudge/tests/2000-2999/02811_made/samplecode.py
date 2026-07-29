# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2811: 熄灯问题
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02811/
# License: not declared in source collection; no license is inferred.
import sys
x=[list(map(int,input().split())) for _ in range(5)]
for mask in range(64):
 p=[[0]*6 for _ in range(5)];p[0]=[(mask>>j)&1 for j in range(6)]
 for i in range(1,5):
  for j in range(6):p[i][j]=x[i-1][j]^p[i-1][j]^(p[i-2][j] if i>1 else 0)^(p[i-1][j-1] if j else 0)^(p[i-1][j+1] if j<5 else 0)
 if all((x[4][j]^p[4][j]^p[3][j]^(p[4][j-1] if j else 0)^(p[4][j+1] if j<5 else 0))==0 for j in range(6)):
  print('\n'.join(' '.join(map(str,row)) for row in p));break
