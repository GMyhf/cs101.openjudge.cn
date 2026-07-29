// External reference: http://cs101.openjudge.cn/practice/01073/statistics/
// Accepted submission: 52525370
// Source: http://cs101.openjudge.cn/practice/solution/52525370/
// License: not declared on the submission page; no license is inferred.

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 用于存储横向连接管的结构体
struct Link {
    int u, v, y;
};

void solve() {
    int p;
    if (!(cin >> p)) return;

    vector<int> X(p + 1), Y(p + 1), H(p + 1);
    vector<int> T(p + 1), B(p + 1);
    for (int i = 1; i <= p; ++i) {
        cin >> X[i] >> Y[i] >> H[i];
        T[i] = Y[i];
        B[i] = Y[i] + H[i]; // Bottom 的 Y 坐标是 Top + Height
    }

    int l;
    cin >> l;
    vector<Link> links;
    for (int i = 0; i < l; ++i) {
        int x, y, len;
        cin >> x >> y >> len;
        int u = -1, v = -1;
        for (int j = 1; j <= p; ++j) {
            if (X[j] == x - 1) u = j;        // 右边界连接水管 u
            if (X[j] == x + len) v = j;      // 左边界连接水管 v
        }
        if (u != -1 && v != -1) {
            links.push_back({u, v, y});
        }
    }

    int target_pipe, target_y;
    cin >> target_pipe >> target_y;

    vector<int> L(p + 1);
    // L 数组存储当前各水管内部水面的 Y 坐标位置。起初位于管底
    for (int i = 1; i <= p; ++i) L[i] = B[i];

    int time = 0;
    bool solved = false;

    // 按每 1 cm 高度的空间体积递进模拟
    while (true) {
        // 1. 根据当前各个水管的水位，连通性传播，找出相通的所有水管集合 R
        vector<bool> in_R(p + 1, false);
        in_R[1] = true;
        bool changed = true;
        while (changed) {
            changed = false;
            for (auto& link : links) {
                if (in_R[link.u] && !in_R[link.v] && L[link.u] <= link.y) {
                    in_R[link.v] = true;
                    changed = true;
                }
                if (in_R[link.v] && !in_R[link.u] && L[link.v] <= link.y) {
                    in_R[link.u] = true;
                    changed = true;
                }
            }
        }

        // 2. 找到相通区域里的"最低水面"（Y 坐标数值最大）
        int M = -1;
        for (int i = 1; i <= p; ++i) {
            if (in_R[i]) {
                M = max(M, L[i]);
            }
        }

        // 3. 将达到这一最低深度、需要共同进水填充的管道整理出来
        vector<int> P_max;
        for (int i = 1; i <= p; ++i) {
            if (in_R[i] && L[i] == M) {
                P_max.push_back(i);
            }
        }

        // 4. 判断是否出现水流溢出
        bool overflow = false;
        for (int i : P_max) {
            if (L[i] == T[i]) {
                overflow = true;
                break;
            }
        }
        // 若最底部位已经有水管水满，水将从管口流失，液面无法再上升
        if (overflow) {
            cout << "No Solution\n";
            solved = true;
            break;
        }

        // 5. 命中目标判断。若当前填充目标高度等同于所需，说明下方全部空间恰好已被填满，正要略高于该位置
        bool target_in_Pmax = false;
        for (int i : P_max) {
            if (i == target_pipe) {
                target_in_Pmax = true;
                break;
            }
        }
        if (M == target_y && target_in_Pmax) {
            cout << time << "\n";
            solved = true;
            break;
        }

        // 6. 执行水位推移。当前深度的目标空间全部充公 1cm
        for (int i : P_max) {
            L[i]--;
        }
        time += P_max.size(); // 1cm 管道对应 1s 时间
    }
}

int main() {
    // 提升 IO 流速度
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t;
    if (cin >> t) {
        while (t--) solve();
    }
    return 0;
}
