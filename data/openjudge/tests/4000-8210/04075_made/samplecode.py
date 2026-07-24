# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def rotate_matrix_90(matrix):
    n = len(matrix)
    return [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def main():
    M = int(input())
    results = []
    for _ in range(M):
        n = int(input())
        matrix = [list(map(int, input().split())) for _ in range(n)]
        rotated = rotate_matrix_90(matrix)
        results.append(rotated)
    
    for result in results:
        print_matrix(result)

if __name__ == "__main__":
    main()

