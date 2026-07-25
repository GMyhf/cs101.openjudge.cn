# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
"""
the toggle function is used to flip the bit, which simplifies the flip function. 
using a for-loop to iterate over the two cases: pressing the first button or not. 
"""
def toggle(bit):
    return '0' if bit == '1' else '1'

def flip(lock, i):
    if i > 0:
        lock[i-1] = toggle(lock[i-1])
    lock[i] = toggle(lock[i])
    if i + 1 < len(lock):
        lock[i+1] = toggle(lock[i+1])

def main():
    s = input()
    fin = input()
    n = len(s)
    ans = float('inf')

    for press_first in [False, True]:
        tmp = 0
        lock = list(s)
        if press_first:
            flip(lock, 0)
            tmp += 1
        for i in range(1, n):
            if lock[i-1] != fin[i-1]:
                flip(lock, i)
                tmp += 1
        if lock[n-1] == fin[n-1]:
            ans = min(ans, tmp)

    if ans == float('inf'):
        print("impossible")
    else:
        print(ans)

if __name__ == "__main__":
    main()
