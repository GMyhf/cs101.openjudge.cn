# External reference: http://cs101.openjudge.cn/practice/20052/statistics/
# Accepted submission: 48701463
# Source: http://cs101.openjudge.cn/practice/solution/48701463/
# License: not declared on the submission page; no license is inferred.

# pylint:skip-file
def up(list1):
	temp=[[0 for i in range(n)] for j in range(m)]
	for i in range(n):
		line=list(list1[x][i] for x in range(m))
		index=0
		for j in range(m-1):
			if line[j]!=0:
				flag=True
				for k in range(j+1,m):
					if line[k]!=0 and line[k]!=line[j]:
						break
					if line[k]==line[j]:
						temp[index][i]=2*line[j]
						line[k]=0
						index+=1
						flag=False
						break
				if flag:
					temp[index][i]=line[j]
					index+=1
		if line[-1]!=0:
			temp[index][i]=line[-1]
	return temp

def down(list1):
	temp=[[0 for i in range(n)] for j in range(m)]
	for i in range(n):
		line=list(list1[x][i] for x in range(m))
		index=-1
		for j in range(m-1,0,-1):
			if line[j]!=0:
				flag=True
				for k in range(j-1,-1,-1):
					if line[k]!=0 and line[k]!=line[j]:
						break
					if line[k]==line[j]:
						temp[index][i]=2*line[j]
						line[k]=0
						index-=1
						flag=False
						break
				if flag:
					temp[index][i]=line[j]
					index-=1
		if line[0]!=0:
			temp[index][i]=line[0]
	return temp

def right(list1):
	temp=[[0 for i in range(n)] for j in range(m)]
	for i in range(m):
		line=list(list1[i][x] for x in range(n))
		index=-1
		for j in range(n-1,0,-1):
			if line[j]!=0:
				flag=True
				for k in range(j-1,-1,-1):
					if line[k]!=0 and line[k]!=line[j]:
						break
					if line[k]==line[j]:
						temp[i][index]=2*line[j]
						line[k]=0
						index-=1
						flag=False
						break
				if flag:
					temp[i][index]=line[j]
					index-=1
		if line[0]!=0:
			temp[i][index]=line[0]
	return temp

def left(list1):
	temp=[[0 for i in range(n)] for j in range(m)]
	for i in range(m):
		line=list(list1[i][x] for x in range(n))
		index=0
		for j in range(n-1):
			if line[j]!=0:
				flag=True
				for k in range(j+1,n):
					if line[k]!=0 and line[k]!=line[j]:
						break
					if line[k]==line[j]:
						temp[i][index]=2*line[j]
						line[k]=0
						index+=1
						flag=False
						break
				if flag:
					temp[i][index]=line[j]
					index+=1
		if line[-1]!=0:
			temp[i][index]=line[-1]
	return temp


def dfs(cnt,tri):
	global output
	if cnt==p:
		for i in range(m):
			now=max(x for x in tri[i])
			output=max(output,now)
		return
	dfs(cnt+1,up(tri))
	dfs(cnt+1,down(tri))
	dfs(cnt+1,right(tri))
	dfs(cnt+1,left(tri))

m,n,p=map(int,input().split())
Matrix=[list(map(int,input().split())) for i in range(m)]
output=0
dfs(0,Matrix)
print(output)
