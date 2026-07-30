# External reference: http://cs101.openjudge.cn/practice/27653/statistics/
# Accepted submission: 51853545
# Source: http://cs101.openjudge.cn/practice/solution/51853545/
# License: not declared on the submission page; no license is inferred.

class Fraction:
    def __init__(self,num=0,den=1):
        self.den=den
        self.num=num
    def reduction(self):
        a, b = int(self.den), int(self.num)
        while b != 0:
            a, b = b, a % b
        check=abs(a)
        if check!=1:
            self.den//=check
            self.num//=check
class FractionAdd:
    def __init__(self,f1,f2):
        self.f1=f1
        self.f2=f2
    def gcd(self,x, y):
        a,b=x,y
        while b != 0:
            a, b = b, a % b
        return abs(a)
    def lcm(self,a, b):
        return a * b // self.gcd(a, b)
    def calculate(self):
        n1, n2, n3, n4 = self.f1.num,self.f1.den,self.f2.num,self.f2.den
        c = self.lcm(n2, n4)
        b1, b2 = c // n2, c // n4
        n = n1 * b1 + n3 * b2
        x3=Fraction(n,c)
        x3.reduction()
        print(f'{x3.num}/{x3.den}')
data=list(map(int,input().split()))
x1=Fraction(data[0],data[1])
x2=Fraction(data[2],data[3])
ad=FractionAdd(x1,x2)
ad.calculate()
