// External reference: cs101.openjudge.cn practice/04120 statistics, Accepted solution 52493018.
// Source: http://cs101.openjudge.cn/practice/solution/52493018/
// License: no explicit license stated on the submission page; retained as an external platform reference.

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

using namespace std;

int main() {
    int n, x;
    cin >> n >> x;

    vector<int> v(n);
    for (int i = 0; i < n; ++i) cin >> v[i];

    vector<int> o;

    for (int out = 0; out < n; ++out) {
        vector<char> have(x + 1, false);
        have[0] = true;

        for (int i = 0; i < n; ++i) {
            if (i == out) continue;
            if (v[i] > x) continue;

            for (int j = x; j >= v[i]; --j) {
                if (have[j - v[i]]) {
                    have[j] = true;
                }
            }

            if (have[x]) break;
        }

        if (!have[x]) {
            o.push_back(v[out]);
        }
    }

    cout << o.size() << endl;
    for (auto num : o) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
