# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def collatz_sequence(n):
    if n == 1:
        print("End")
        return

    while n != 1:
        if n % 2 == 1:
            next_n = 3 * n + 1
            print(f"{n}*3+1={next_n}")
        else:
            next_n = n // 2
            print(f"{n}/2={next_n}")
        n = next_n

    print("End")

# Sample input
n = int(input())

# Calculate and print the result
collatz_sequence(n)
