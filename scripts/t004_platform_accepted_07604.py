n = int(input())
string = input()
dict_ = {} # 注意用dict()或者{}都可以但是不能用dict
for i in range(len(string) - n + 1): # 注意要- n + 1
    if string[i: i + n] in dict_:
        dict_[string[i: i + n]] += 1
    else:
        dict_[string[i: i + n]] = 1
maxim_count = max(dict_.values()) # 注意value写法
if maxim_count <= 1: # 注意是小于等于不是小于
    print("NO")
else:
    print(maxim_count)
    for gram in dict_:
        if dict_[gram] == maxim_count:
            print(gram)