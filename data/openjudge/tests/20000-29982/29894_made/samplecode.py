"""仓库自产参考：按上车人数的线性系数反求第二站人数；非外部提交。"""
def coefficients(station):
    if station<=2: return 1,0
    a,b=1,0; previous=(1,0); current=(0,1)
    for _ in range(3,station+1):
        following=(previous[0]+current[0],previous[1]+current[1])
        a+=following[0]-current[0]; b+=following[1]-current[1]
        previous,current=current,following
    return a,b

def solve(text):
    a,n,m,x=map(int,text.split()); ca,cb=coefficients(n-1)
    second=(m-ca*a)//cb if cb else 0
    xa,xb=coefficients(x)
    return str(xa*a+xb*second)

if __name__=='__main__':
    import sys
    print(solve(sys.stdin.read()))
