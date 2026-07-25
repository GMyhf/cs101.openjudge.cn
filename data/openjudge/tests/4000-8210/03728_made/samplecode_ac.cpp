// 03728 Blah数集 —— 平台已 Accepted（cs101.openjudge.cn 提交 #52995114，G++，17ms）。
// 为什么要有这份 C++：同目录 samplecode.py 的 Python 实现在真实平台 Time Limit Exceeded
// （题面 n<=1000000），本地小域对拍过不代表能过平台。这份是该题目前唯一有平台背书的参考实现。
// 本地 21 组数据逐组比对一致，单组最慢 0.06s。
// 03728 Blah数集：以 a 为基，闭包于 2x+1 与 3x+1，升序第 n 个。
// 双指针归并生成有序序列，天然去重；按基分组，同一个基只算到该基需要的最大 n。
#include <bits/stdc++.h>
using namespace std;
int main(){
    vector<pair<long long,long long>> qs;      // (a, n)
    long long a, n;
    while (scanf("%lld %lld", &a, &n) == 2) qs.push_back({a, n});
    unordered_map<long long,long long> need;
    for (auto &q : qs) need[q.first] = max(need[q.first], q.second);
    unordered_map<long long, vector<long long>> seq;
    for (auto &kv : need) {
        long long base = kv.first, upto = kv.second;
        vector<long long> v;
        v.reserve(upto);
        v.push_back(base);
        size_t i2 = 0, i3 = 0;
        while ((long long)v.size() < upto) {
            long long x = min(2*v[i2]+1, 3*v[i3]+1);
            v.push_back(x);
            while (2*v[i2]+1 <= x) ++i2;       // 去重：把所有等于 x 的候选一并跳过
            while (3*v[i3]+1 <= x) ++i3;
        }
        seq[base] = move(v);
    }
    for (auto &q : qs) printf("%lld\n", seq[q.first][q.second-1]);
    return 0;
}
