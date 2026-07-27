# External reference: statistics page /practice/28404/
# Accepted submission: 52363840
# Source: http://cs101.openjudge.cn/practice/solution/52363840/
# License: not declared on the submission page; no license is inferred.

n=int(input())

tables={}
foodset=set()
for _ in range(n):
    query=input().split(",")
    table=int(query[1])
    menu=query[2]
    foodset.add(menu)
    if table in tables:
        tables[table].append(menu)
    else:
        tables[table]=[menu]

food=list(foodset)
food.sort()
output="Table\t"+"\t".join(food)
print(output)
table=list(tables.keys())
table.sort()

for i in table:
    print()
    output=str(i)
    tmp=[0]*len(food)
    for j in tables[i]:
        ind=food.index(j)
        tmp[ind]+=1
    output+="\t"+"\t".join([str(i) for i in tmp])
    print(output)
    
