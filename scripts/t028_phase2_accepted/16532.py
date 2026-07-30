# External reference: http://cs101.openjudge.cn/practice/16532/statistics/
# Accepted submission: 52155643
# Source: http://cs101.openjudge.cn/practice/solution/52155643/
# License: not declared on the submission page; no license is inferred.

def move(x,y,kind,energy,dx,dy,tarx,tary):
    if (x==0 or x==8 or x==16) and (y==0 or y==5):
        print(kind)
        return
    if energy==0:
        print(0)
        return
    if 0<x<16 and 0<y<5:
        x+=dx
        y+=dy
        if x==tarx and y==tary:
            move(x,y,-kind,energy-1,dx,dy,x,y)
        else:
            move(x,y,kind,energy-1,dx,dy,tarx,tary)
    elif x==0 or x==16:
        move(x-dx,y+dy,kind,energy-1,-dx,dy,tarx,tary)
    elif y==0 or y==5:
        move(x+dx,y-dy,kind,energy-1,dx,-dy,tarx,tary)

x1,y1=map(int,input().split())
x2,y2=map(int,input().split())
di1,di2=map(int,input().split())
ener=int(input())
move(x1,y1,-1,ener,di1,di2,x2,y2)
