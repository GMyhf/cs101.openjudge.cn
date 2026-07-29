# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2159: Ancient Cipher
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02159/
# License: not declared; no license is inferred.
def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()

    str1 = data[0]
    str2 = data[1]

    cnt1 = [0] * 26
    cnt2 = [0] * 26

    for char in str1:
        cnt1[ord(char) - ord('A')] += 1

    for char in str2:
        cnt2[ord(char) - ord('A')] += 1

    cnt1.sort()
    cnt2.sort()

    if cnt1 == cnt2:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
