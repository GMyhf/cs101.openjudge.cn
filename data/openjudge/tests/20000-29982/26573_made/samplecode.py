# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def print_cantor_set(n):
    def cantor(start, end, level):
        if level == 0:
            for i in range(start, end):
                cantor_set[i] = '*'  # Mark the segment as occupied
        else:
            segment_length = (end - start) // 3
            # Recursively mark the first third and the last third
            cantor(start, start + segment_length, level - 1)
            cantor(end - segment_length, end, level - 1)

    # Initialize the list with dashes, representing an empty line
    cantor_set = ['-' for _ in range(3 ** n)]
    cantor(0, 3 ** n, n)
    return ''.join(cantor_set)

# Read the input
n = int(input())

# Generate and print the Cantor set
print(print_cantor_set(n))
