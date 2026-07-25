# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()

    num1 = int(data[0][:2])
    num2 = int(data[1][:2])

    result = num1 + num2
    print(result)

if __name__ == "__main__":
    main()
