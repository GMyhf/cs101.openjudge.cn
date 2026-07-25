# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    times = [int(data[2 + i]) for i in range(n)]
    
    # 计算总炸制时间
    total_time = sum(times)
    
    # 对炸制时间进行排序
    times.sort()
    
    # 初始最大持续时间为总炸制时间除以 k
    max_time = total_time / k
    
    # 如果最长的炸制时间大于或等于 max_time，则需要调整 k 的值
    if times[-1] > max_time:
        for i in range(n - 1, -1, -1):
            if times[i] <= max_time:
                break
            total_time -= times[i]
            k -= 1
            max_time = total_time / k
    
    # 输出结果，保留三位小数
    print(f"{max_time:.3f}")

if __name__ == "__main__":
    main()
