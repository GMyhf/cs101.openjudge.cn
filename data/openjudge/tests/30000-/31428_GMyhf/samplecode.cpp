pair<int, int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)nums.size(); ++i) {
        auto found = seen.find(target - nums[i]);
        if (found != seen.end()) return {i, found->second};
        seen.emplace(nums[i], i);
    }
    return {-1, -1};
}
