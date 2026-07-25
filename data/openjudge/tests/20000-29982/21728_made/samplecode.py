# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def main():
    n = int(input())
    # Read experiment durations. There are n numbers.
    durations = list(map(int, input().split()))
    # Read the order of students. There are n numbers.
    order = list(map(int, input().split()))

    total_waiting_time = 0
    current_time = 0
    # Process students in the given order.
    for student in order:
        total_waiting_time += current_time
        # Convert student id (1-indexed) to index (0-indexed)
        current_time += durations[student - 1]

    average_waiting_time = total_waiting_time / n
    # Output the average waiting time rounded to two decimals.
    print(f"{average_waiting_time:.2f}")


if __name__ == "__main__":
    main()
