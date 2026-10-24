"""仓库自产参考：枚举区间并按十进制各位立方和判断；非外部提交。"""
def solve(text):
    a,b=map(int,text.split())
    values=[str(n) for n in range(a,b+1) if sum(int(c)**3 for c in str(n))==n]
    return ' '.join(values) if values else 'NO'

if __name__=='__main__':
    import sys
    print(solve(sys.stdin.read()))
