// External reference: http://cs101.openjudge.cn/practice/02984/statistics/
// Accepted submission: 51696118
// Source: http://cs101.openjudge.cn/practice/solution/51696118/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

static int rowOf[81], colOf[81], boxOf[81];

struct Solver {
    int grid[81];              // 0 表示空，否则 1..9
    int rowMask[9], colMask[9], boxMask[9]; // 已使用数字的bit集合
    vector<int> empties;       // 空格位置

    bool dfs(int idx) {
        const int E = (int)empties.size();
        if (idx == E) return true;

        // MRV：从 idx..E-1 选候选数最少的格子
        int best = -1;
        int bestMask = 0;
        int bestCnt = 10;

        for (int i = idx; i < E; i++) {
            int pos = empties[i];
            int r = rowOf[pos], c = colOf[pos], b = boxOf[pos];
            int cand = ~(rowMask[r] | colMask[c] | boxMask[b]) & 0x1FF; // 9 bits
            int cnt = __builtin_popcount((unsigned)cand);
            if (cnt < bestCnt) {
                bestCnt = cnt;
                bestMask = cand;
                best = i;
                if (cnt == 1) break; // 已经最优
            }
        }
        if (bestCnt == 0) return false;

        // 把 best 位置的空格换到当前 idx 位置
        swap(empties[idx], empties[best]);
        int pos = empties[idx];
        int r = rowOf[pos], c = colOf[pos], b = boxOf[pos];

        int cand = bestMask;
        while (cand) {
            int bit = cand & -cand;
            cand -= bit;

            int d = __builtin_ctz((unsigned)bit); // 0..8
            grid[pos] = d + 1;

            rowMask[r] |= bit;
            colMask[c] |= bit;
            boxMask[b] |= bit;

            if (dfs(idx + 1)) return true;

            rowMask[r] ^= bit;
            colMask[c] ^= bit;
            boxMask[b] ^= bit;
            grid[pos] = 0;
        }

        // 恢复 empties 顺序
        swap(empties[idx], empties[best]);
        return false;
    }

    string solve(const string& s) {
        empties.clear();
        memset(grid, 0, sizeof(grid));
        memset(rowMask, 0, sizeof(rowMask));
        memset(colMask, 0, sizeof(colMask));
        memset(boxMask, 0, sizeof(boxMask));

        for (int i = 0; i < 81; i++) {
            char ch = s[i];
            if (ch == '.') {
                empties.push_back(i);
            } else {
                int v = ch - '1';      // 0..8
                int bit = 1 << v;
                int r = rowOf[i], c = colOf[i], b = boxOf[i];
                grid[i] = v + 1;
                rowMask[r] |= bit;
                colMask[c] |= bit;
                boxMask[b] |= bit;
            }
        }

        dfs(0);

        string out;
        out.reserve(81);
        for (int i = 0; i < 81; i++) out.push_back(char('0' + grid[i]));
        return out;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 预计算每个格子的行/列/宫编号
    for (int i = 0; i < 81; i++) {
        int r = i / 9, c = i % 9;
        rowOf[i] = r;
        colOf[i] = c;
        boxOf[i] = (r / 3) * 3 + (c / 3);
    }

    Solver solver;
    string s;
    while (cin >> s) {
        if (s == "end") break;
        cout << solver.solve(s) << "\n";
    }
    return 0;
}
