#if 0
import os
def main():
    stdin = open(os.dup(0), "r")
    os.dup2(os.open(os.devnull, os.O_RDONLY), 0)
    stdout = open(os.dup(1), "w")
    os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
    while True:
        length, target = map(int, stdin.readline().split())
        if length == target == 0:
            break
        nums = list(map(int, stdin.readline().split()))
        ans = two_sum(nums, target)
        stdout.write(f'{min(ans)} {max(ans)}\n')
if __name__ == "__main__":
    main()
""" "
#endif
int main() {
    // 提高 I/O 效率
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int length, target;
    while (cin >> length >> target) {
        if (length == 0 && target == 0) {
            break;
        }
        vector<int> nums(length);
        for (int i = 0; i < length; ++i) {
            cin >> nums[i];
        }
        pair<int, int> ans = twoSum(nums, target);
        // 输出排序后的下标
        int first = min(ans.first, ans.second);
        int second = max(ans.first, ans.second);
        cout << first << " " << second << "\n";
    }
    return 0;
}
#if 0
" """
#endif
