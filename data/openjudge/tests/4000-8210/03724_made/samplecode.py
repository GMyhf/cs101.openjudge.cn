# T-004-r3 reference implementation
import sys
days=[31,28,31,30,31,30,31,31,30,31,30,31]
def leap(y): return y%400==0 or y%4==0 and y%100!=0
for token in sys.stdin.read().split():
    rem=int(token); y=1970
    while rem >= (366 if leap(y) else 365)*86400: rem-=(366 if leap(y) else 365)*86400; y+=1
    month=1
    while True:
        md=days[month-1]+(month==2 and leap(y))
        if rem < md*86400: break
        rem-=md*86400; month+=1
    print(f"{y:04d}-{month:02d}-{rem//86400+1:02d} {(rem%86400)//3600:02d}:{(rem%3600)//60:02d}:{rem%60:02d}")