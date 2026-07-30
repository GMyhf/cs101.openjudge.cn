# External reference: http://cs101.openjudge.cn/practice/27653/statistics/
# Accepted submission: 51920502
# Source: http://cs101.openjudge.cn/practice/solution/51920502/
# License: not declared on the submission page; no license is inferred.

class Fraction:
    def __init__(self, numerator, denominator):
        m,n=numerator,denominator
        while m%n!=0:
            m,n=n,m%n
        self.numerator,self.denominator=numerator//n,denominator//n
    def __str__(self):
        if self.denominator==0:
            return '0'
        if self.denominator==1:
            return f'{self.numerator}'
        if self.denominator*self.numerator<0:
            return f'-{abs(self.numerator)}/{abs(self.denominator)}'
        return f'{self.numerator}/{self.denominator}'
    def __add__(self,other):
        return Fraction(self.numerator*other.denominator+other.numerator*self.denominator,self.denominator*other.denominator)
a,b,c,d=map(int,input().split())
print(Fraction(a,b)+Fraction(c,d))
