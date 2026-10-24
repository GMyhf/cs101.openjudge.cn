"""仓库自产参考：转为子集和计数，保留零元素的不同符号选择；非外部提交。"""
def solve(text):
    lines=text.splitlines(); nums=list(map(int,lines[0].split())); target=int(lines[1]); total=sum(nums)
    if abs(target)>total or (total+target)%2: return '0'
    goal=(total+target)//2; counts=[0]*(goal+1); counts[0]=1
    for value in nums:
        for amount in range(goal,value-1,-1): counts[amount]+=counts[amount-value]
    return str(counts[goal])

if __name__=='__main__':
    import sys
    print(solve(sys.stdin.read()))
