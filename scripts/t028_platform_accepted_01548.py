# External reference: http://cs101.openjudge.cn/practice/01548/statistics/
# Accepted submission: 41540671
# Source: http://cs101.openjudge.cn/practice/solution/41540671/
# License: not declared on the submission page; no license is inferred.

while True:
	gar, ret = [], 0
	while True:
		ix, iy = map(int, input().split())
		if ix < 0:
			exit(0)
		if not ix:
			break
		gar.append((ix, iy))
	while gar:
		ret += 1
		cy = 1
		for i in range(len(gar)):
			x,y = gar[i]
			if y >= cy:
				cy = y
				gar[i] = None
		gar = list(filter(lambda x : x,gar))
	print(ret)
