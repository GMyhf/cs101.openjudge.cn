// External reference: http://cs101.openjudge.cn/practice/03186/statistics/
// Accepted submission: 51696137
// Source: http://cs101.openjudge.cn/practice/solution/51696137/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    int M = N * N;

    vector<int> a(M * M);
    for (int i = 0; i < M * M; ++i) {
        cin >> a[i];
        if (a[i] < 0 || a[i] > M) { // 非法数字
            cout << "INCORRECT\n";
            return 0;
        }
    }

    bitset<101> seen; // M<=100

    // Check rows
    for (int r = 0; r < M; ++r) {
        seen.reset();
        int base = r * M;
        for (int c = 0; c < M; ++c) {
            int v = a[base + c];
            if (v == 0) continue;
            if (seen.test(v)) {
                cout << "INCORRECT\n";
                return 0;
            }
            seen.set(v);
        }
    }

    // Check columns
    for (int c = 0; c < M; ++c) {
        seen.reset();
        for (int r = 0; r < M; ++r) {
            int v = a[r * M + c];
            if (v == 0) continue;
            if (seen.test(v)) {
                cout << "INCORRECT\n";
                return 0;
            }
            seen.set(v);
        }
    }

    // Check sub-squares (N x N blocks, each of size N x N)
    for (int br = 0; br < N; ++br) {
        for (int bc = 0; bc < N; ++bc) {
            seen.reset();
            int r0 = br * N, c0 = bc * N;
            for (int dr = 0; dr < N; ++dr) {
                int rowBase = (r0 + dr) * M;
                for (int dc = 0; dc < N; ++dc) {
                    int v = a[rowBase + (c0 + dc)];
                    if (v == 0) continue;
                    if (seen.test(v)) {
                        cout << "INCORRECT\n";
                        return 0;
                    }
                    seen.set(v);
                }
            }
        }
    }

    cout << "CORRECT\n";
    return 0;
}
