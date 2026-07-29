// External reference: http://cs101.openjudge.cn/practice/01581/statistics/
// Accepted submission: 51691711
// Source: http://cs101.openjudge.cn/practice/solution/51691711/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int nTeams;
    if (!(cin >> nTeams)) return 0;

    string bestName;
    int bestSolved = -1;
    long long bestPenalty = (1LL<<60);

    for (int t = 0; t < nTeams; ++t) {
        string name;
        cin >> name;

        int solved = 0;
        long long penalty = 0;

        for (int i = 0; i < 4; ++i) {
            long long sub, tim;
            cin >> sub >> tim;
            if (tim > 0) {
                ++solved;
                penalty += tim + 20LL * (sub - 1);
            }
        }

        if (solved > bestSolved || (solved == bestSolved && penalty < bestPenalty)) {
            bestSolved = solved;
            bestPenalty = penalty;
            bestName = name;
        }
    }

    cout << bestName << ' ' << bestSolved << ' ' << bestPenalty << "\n";
    return 0;
}
