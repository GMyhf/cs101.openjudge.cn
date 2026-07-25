# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def subarray_sum(nums, k):
    count = 0
    sums = 0
    d = dict()
    d[0] = 1

    for i in range(len(nums)):
        sums += nums[i]
        count += d.get(sums - k, 0)
        d[sums] = d.get(sums, 0) + 1

    return count

nums = list(map(int, input().split()))
k = int(input().strip())
print(subarray_sum(nums, k))
