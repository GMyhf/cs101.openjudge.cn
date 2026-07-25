# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def main():
    # 读取所有输入
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    # 第一行为提交记录数 M
    m = int(input_data[0].strip())
    
    teams = {}
    
    for i in range(1, m + 1):
        if i >= len(input_data):
            break
        line = input_data[i].strip()
        if not line:
            continue
        
        # 解析每行提交数据，去除两端空格
        parts = line.split(',')
        if len(parts) < 3:
            continue
        team_name = parts[0].strip()
        problem = parts[1].strip()
        result = parts[2].strip()
        
        # 初始化队伍数据
        if team_name not in teams:
            teams[team_name] = {
                'solved': set(),
                'subs': 0
            }
        
        # 记录提交次数
        teams[team_name]['subs'] += 1
        
        # 如果通过，则加入已解决题目集合
        if result == 'yes':
            teams[team_name]['solved'].add(problem)
            
    # 排序规则：
    # 1. 做对题目数降序：-len(x[1]['solved'])
    # 2. 总提交次数升序：x[1]['subs']
    # 3. 队伍名称字典序升序：x[0]
    sorted_teams = sorted(
        teams.items(),
        key=lambda x: (-len(x[1]['solved']), x[1]['subs'], x[0])
    )
    
    # 输出前 12 名（若不足 12 名，则输出全部）
    limit = min(12, len(sorted_teams))
    for rank in range(1, limit + 1):
        team_name, data = sorted_teams[rank - 1]
        solved_count = len(data['solved'])
        subs_count = data['subs']
        print(f"{rank} {team_name} {solved_count} {subs_count}")

if __name__ == '__main__':
    main()
