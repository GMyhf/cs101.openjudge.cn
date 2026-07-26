// 04011 Chase —— 人提供的平台 Accepted 实现（2026-07-26 立为参考实现）。
// 原自写 Python 参考在平台 Python3/PyPy3 两档都 TLE，无法取得平台背书；
// 本实现与原 Python 在全部 21 组数据上输出一致，因此数据内容不变、只是换了产出方。
// 原 Python 实现（穷举分配 vs 本实现的按子树背包合并）保留为独立 oracle 的候选。
#include <bits/stdc++.h>
using namespace std;

static const double NEG = -1e100;
static const long long INFLL = (1LL<<60);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    while ( (cin >> N >> M) ) {
        if (N == 0 && M == 0) break;

        vector<vector<pair<int,int>>> g(N);
        for (int i = 0; i < M; i++) {
            int a,b,c;
            cin >> a >> b >> c;
            g[a].push_back({b,c});
            g[b].push_back({a,c});
        }

        int P;
        cin >> P;

        vector<vector<double>> PT(N, vector<double>(P+1, 0.0));
        for (int i = 0; i < N; i++) {
            for (int j = 1; j <= P; j++) {
                cin >> PT[i][j];
            }
            // 前缀最大化：确保“多派人不更差”
            for (int j = 1; j <= P; j++) {
                PT[i][j] = max(PT[i][j], PT[i][j-1]);
            }
        }

        // Dijkstra from 0
        vector<long long> dist(N, INFLL);
        vector<int> parent(N, -1);
        dist[0] = 0;
        using T = pair<long long,int>;
        priority_queue<T, vector<T>, greater<T>> pq;
        pq.push({0,0});
        while (!pq.empty()) {
            auto [d,u] = pq.top(); pq.pop();
            if (d != dist[u]) continue;
            for (auto [v,w] : g[u]) {
                long long nd = d + w;
                if (nd < dist[v]) {
                    dist[v] = nd;
                    parent[v] = u;
                    pq.push({nd, v});
                }
                // nd == dist[v] 理论上不会发生（唯一最短路），忽略即可
            }
        }

        // Build shortest path tree (only reachable nodes)
        vector<vector<int>> children(N);
        vector<int> reachable;
        reachable.reserve(N);
        for (int i = 0; i < N; i++) {
            if (dist[i] < INFLL) reachable.push_back(i);
        }
        for (int v = 1; v < N; v++) {
            if (parent[v] != -1) {
                children[parent[v]].push_back(v);
            }
        }

        // Order nodes by dist descending for bottom-up DP
        sort(reachable.begin(), reachable.end(),
             [&](int a, int b){ return dist[a] > dist[b]; });

        vector<vector<double>> f(N, vector<double>(P+1, 0.0));

        for (int u : reachable) {
            int deg = (int)children[u].size();
            if (deg == 0) {
                for (int p = 0; p <= P; p++) {
                    double best = 0.0;
                    for (int k = 0; k <= p; k++) best = max(best, PT[u][k]);
                    f[u][p] = best;
                }
                continue;
            }

            // knapsack merge for children: gsum[q] = max sum of f[child][alloc] with total alloc=q
            vector<double> gsum(P+1, NEG);
            gsum[0] = 0.0;
            for (int v : children[u]) {
                vector<double> ng(P+1, NEG);
                for (int used = 0; used <= P; used++) {
                    if (gsum[used] <= NEG/2) continue;
                    for (int add = 0; used + add <= P; add++) {
                        ng[used + add] = max(ng[used + add], gsum[used] + f[v][add]);
                    }
                }
                gsum.swap(ng);
            }

            for (int p = 0; p <= P; p++) {
                double best = 0.0;
                for (int k = 0; k <= p; k++) {
                    double A = PT[u][k];
                    double childAvg = gsum[p - k] / (double)deg;
                    double val = A + (1.0 - A) * childAvg;
                    if (val > best) best = val;
                }
                f[u][p] = best;
            }
        }

        double ans = f[0][P] * 100.0;
        cout.setf(std::ios::fixed);
        cout << setprecision(2) << ans + 1e-12 << "\n";
    }
    return 0;
}
