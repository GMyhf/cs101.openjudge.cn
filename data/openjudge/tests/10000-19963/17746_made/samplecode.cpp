// External reference: statistics page /practice/17746/
// Accepted submission: 52515040
// Source: http://cs101.openjudge.cn/practice/solution/52515040/
// License: not declared on the submission page; no license is inferred.

// External reference: cs101.openjudge.cn practice/17746 statistics, Accepted solution 52515040.
// Source: http://cs101.openjudge.cn/practice/solution/52515040/
// Statistics: http://cs101.openjudge.cn/practice/17746/statistics/
// License: not declared on submission page; no license inferred
#include<iostream>
#include<cstdio>
#include<string>
#include<cstring>
#include<vector>
#include<queue>
#include<stack>
#include<unordered_map>
#include<unordered_set>
#include<algorithm>
#include<climits>
#include<sstream>
#include<set>
#include<map>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, c;
    cin >> n >> m >> c;
    vector<int> v(n + 1);
    for (int i = 1;i <= n;++i)cin >> v[i];
    deque<int> max_st, min_st;
    bool flag = false;
    for (int i = 1;i <= n;++i) {
        while (!max_st.empty() && v[i] > max_st.back()) {
            max_st.pop_back();
        }
        max_st.push_back(v[i]);
        if (i > m) {
            if (v[i - m] == max_st.front()) {
                max_st.pop_front();
            }
        }
        while (!min_st.empty() && v[i] < min_st.back()) {
            min_st.pop_back();
        }
        min_st.push_back(v[i]);
        if (i > m) {
            if (v[i - m] == min_st.front()) {
                min_st.pop_front();
            }
        }
        if (i >= m) {
            if (max_st.front() - min_st.front() <= c) {
                cout << i-m+1 << '\n';
                flag = true;
            }
        }
    }
    if (!flag)cout << "NONE";
    return 0;
}
