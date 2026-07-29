// External reference: http://cs101.openjudge.cn/practice/01459/statistics/
// Accepted submission: 51691692
// Source: http://cs101.openjudge.cn/practice/solution/51691692/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

struct FastScanner {
    // 读取下一个非负整数；到 EOF 返回 false
    bool readInt(int &x) {
        x = 0;
        int c = getchar();
        if (c == EOF) return false;
        while (c != EOF && (c < '0' || c > '9')) c = getchar();
        if (c == EOF) return false;
        while (c != EOF && (c >= '0' && c <= '9')) {
            x = x * 10 + (c - '0');
            c = getchar();
        }
        return true;
    }
};

struct Dinic {
    struct Edge {
        int to, rev;
        long long cap;
    };
    int N;
    vector<vector<Edge>> G;
    vector<int> level, it;

    Dinic(int n=0) { init(n); }
    void init(int n) {
        N = n;
        G.assign(N, {});
        level.assign(N, 0);
        it.assign(N, 0);
    }

    void addEdge(int fr, int to, long long cap) {
        Edge a{to, (int)G[to].size(), cap};
        Edge b{fr, (int)G[fr].size(), 0};
        G[fr].push_back(a);
        G[to].push_back(b);
    }

    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (auto &e : G[v]) {
                if (e.cap > 0 && level[e.to] < 0) {
                    level[e.to] = level[v] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[t] >= 0;
    }

    long long dfs(int v, int t, long long f) {
        if (v == t) return f;
        for (int &i = it[v]; i < (int)G[v].size(); i++) {
            Edge &e = G[v][i];
            if (e.cap <= 0) continue;
            if (level[e.to] != level[v] + 1) continue;
            long long ret = dfs(e.to, t, min(f, e.cap));
            if (ret > 0) {
                e.cap -= ret;
                G[e.to][e.rev].cap += ret;
                return ret;
            }
        }
        return 0;
    }

    long long maxflow(int s, int t) {
        long long flow = 0;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while (true) {
                long long pushed = dfs(s, t, (long long)4e18);
                if (!pushed) break;
                flow += pushed;
            }
        }
        return flow;
    }
};

int main() {
    FastScanner fs;
    int n, np, nc, m;

    while (true) {
        if (!fs.readInt(n)) break;
        fs.readInt(np); fs.readInt(nc); fs.readInt(m);

        int S = n, T = n + 1;
        Dinic dinic(n + 2);

        for (int i = 0; i < m; i++) {
            int u, v, z;
            fs.readInt(u); fs.readInt(v); fs.readInt(z);
            dinic.addEdge(u, v, z);
        }

        for (int i = 0; i < np; i++) {
            int u, z;
            fs.readInt(u); fs.readInt(z);
            dinic.addEdge(S, u, z);
        }

        for (int i = 0; i < nc; i++) {
            int u, z;
            fs.readInt(u); fs.readInt(z);
            dinic.addEdge(u, T, z);
        }

        cout << dinic.maxflow(S, T) << "\n";
    }
    return 0;
}
