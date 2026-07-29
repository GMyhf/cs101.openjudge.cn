# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2039: 反反复复
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02039/
# License: not declared in source collection; no license is inferred.
import sys
a=sys.stdin.read().split();cols=int(a[0]);s=a[1];g=[s[i:i+cols] for i in range(0,len(s),cols)]
for i in range(1,len(g),2):g[i]=g[i][::-1]
print(''.join(g[i][j] for j in range(cols) for i in range(len(g))))
