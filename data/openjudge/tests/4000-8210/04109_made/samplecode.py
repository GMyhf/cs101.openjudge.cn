# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def count_common_friends(n, m, k, friend_connections, queries):
    # Create a dictionary to store friend connections
    friends_dict = {}
    for i in range(1, n + 1):
        friends_dict[i] = set()

    # Update the dictionary with friend connections
    for i, j in friend_connections:
        friends_dict[i].add(j)
        friends_dict[j].add(i)

    # Count common friends for each query
    results = []
    for i, j in queries:
        common_friends = len(friends_dict[i].intersection(friends_dict[j]))
        results.append(common_friends)

    return results


def main():
    test_cases = int(input())
    for case in range(1, test_cases + 1):
        n, m, k = map(int, input().split())
        friend_connections = []
        queries = []

        # Read friend connections
        for _ in range(m):
            i, j = map(int, input().split())
            friend_connections.append((i, j))

        # Read queries
        for _ in range(k):
            i, j = map(int, input().split())
            queries.append((i, j))

        # Count common friends and output the results
        print(f"Case {case}:")
        results = count_common_friends(n, m, k, friend_connections, queries)
        for result in results:
            print(result)


if __name__ == "__main__":
    main()
