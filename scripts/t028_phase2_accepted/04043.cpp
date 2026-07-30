// External reference: http://cs101.openjudge.cn/practice/04043/statistics/
// Accepted submission: 51701672
// Source: http://cs101.openjudge.cn/practice/solution/51701672/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    vector<string> course(n);
    for (int i = 0; i < n; i++) cin >> course[i];

    vector<vector<int>> g(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> g[i][j];

    for (int i = 0; i < n; i++) {
        vector<int> students;
        for (int s = 0; s < m; s++) {
            if (g[s][i] > 0) students.push_back(s);
        }

        long long di = 0;

        if (!students.empty()) {
            long long sumCourse = 0;
            for (int s : students) sumCourse += g[s][i];
            long long avgCourse = sumCourse / (long long)students.size(); // 截断

            long long total = 0, cnt = 0;
            for (int s : students) {
                for (int j = 0; j < n; j++) {
                    if (g[s][j] > 0) {
                        total += g[s][j];
                        cnt++;
                    }
                }
            }
            long long avgAll = (cnt == 0 ? 0 : total / cnt); // 理论上 cnt>0
            di = avgAll - avgCourse;
        } else {
            // 没人选这门课：题意下均值无定义，通常测试不会出现；这里输出 0 兜底
            di = 0;
        }

        cout << course[i] << ' ' << di << "\n";
    }

    return 0;
}
