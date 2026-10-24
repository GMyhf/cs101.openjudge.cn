"""修正可证明的题面约束及缺失样例参数；不改变算法规则。"""

def recovered_samples(number, fields):
    if number in (28277,28680):
        import re
        result=[]
        for i,key in ((1,'sampleInput'),(2,'sampleOutput')):
            match=re.search(rf'sample{i} input:\s*(.*?)\s*sample{i} output:',fields[key],re.S)
            assert match is not None
            result.append(match[1].strip())
        return result
    if number == 25685:
        v=list(map(int,fields['sampleInput'].split()))
        m,a=v[0],v[1:]
        assert m>=0 and len(a)>=2 and len(set(a))==len(a)
        shift=max(0,m-min(a))
        return [str(m)+'\n'+' '.join(str(x+shift) for x in a)]
    if number == 31303:
        rows=fields['sampleInput'].strip().splitlines()
        assert len(rows)==1
        a=list(map(int,rows[0].split()));out=list(map(int,fields['sampleOutput'].split()))
        k=len(a)-len(out)+1
        assert 1<=k<=len(a) and [max(a[i:i+k]) for i in range(len(a)-k+1)]==out
        return [rows[0]+'\n'+str(k)]
    return [fields['sampleInput'].strip()]

def changed_form(number,fields,answers):
    result=dict(fields)
    if number==28277:
        assert result['description'].count('(m,n)')==1
        result['description']=result['description'].replace('(m,n)','(m-1,n-1)')
    elif number==28680:
        assert result['output'].count('数字 2')==1
        result['output']=result['output'].replace('数字 2','数字 a')
    elif number==25685:
        assert answers==['2']
        result['sampleInput']=recovered_samples(number,fields)[0]
        result['sampleOutput']='2\n解释：[3,5,9]收发款变成[3+3,5+3,9-3]即[6,8,6]时，有最小贫富差距8-6=2。'
    elif number==29329:
        old='1 <= N <= K <= 10^6'
        assert result['input'].count(old)==1
        result['input']=result['input'].replace(old,'1 <= K <= N <= 10^6')
    elif number==30125:
        old='每行包含三个值：玩家名字、意图（需求Need, 贪婪Greed, 或放弃Pass）和掷骰点数（1 到 100 间的整数）。'
        new='每行先给出玩家名字和意图（需求Need, 贪婪Greed, 或放弃Pass）。Need和Greed还须给出掷骰点数（1到100间的整数）；Pass可省略掷骰点数，若提供则不参与分配。'
        assert result['input'].count(old)==1
        result['input']=result['input'].replace(old,new)
    elif number==31303:
        result['sampleInput']=recovered_samples(number,fields)[0]
    else:raise ValueError(number)
    return result
