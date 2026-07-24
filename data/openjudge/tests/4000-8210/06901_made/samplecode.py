# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def find_topic_center_and_mentioners():
    n = int(input())
    mention_count = {}  # 记录每个人被提及的次数
    mention_relations = {}  # 记录提及关系，key为提及的人，value为提及的人的集合
    
    for _ in range(n):
        tweet = input().split()
        sender, k = int(tweet[0]), int(tweet[1])
        if k > 0:
            mentioned = list(map(int, tweet[2:]))
            for person in mentioned:
                if person not in mention_count:
                    mention_count[person] = 1
                    mention_relations[person] = set([sender])
                else:
                    mention_count[person] += 1
                    mention_relations[person].add(sender)
    
    # 找到被提及最多的人
    topic_center = max(mention_count, key=mention_count.get)
    
    # 输出结果
    print(topic_center)
    print(' '.join(map(str, sorted(mention_relations[topic_center]))))

# 调用函数处理输入数据
find_topic_center_and_mentioners()
