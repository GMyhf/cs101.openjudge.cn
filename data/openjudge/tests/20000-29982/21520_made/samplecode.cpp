// User-supplied verified reference; platform Accepted submission #53000347
// Source: http://cs101.openjudge.cn/practice/solution/53000347/
// License: not declared; no license is inferred.

# include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 INF = (1LL << 62);
struct Edge { int to; int next; int cost; };
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N, M; cin >> N >> M;
    vector<vector<char>> village(N, vector<char>(M));
    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) { int x; cin >> x; village[r][c] = x; }
    vector<vector<int>> vertical(N, vector<int>(M + 1));
    vector<vector<int>> horizontal(N + 1, vector<int>(M));
    for (int r = 0; r < N; ++r) for (int c = 0; c <= M; ++c) cin >> vertical[r][c];
    for (int r = 0; r <= N; ++r) for (int c = 0; c < M; ++c) cin >> horizontal[r][c];
    const int columns = M + 1; const int pointCount = (N + 1) * (M + 1);
    auto pointId = [&](int r, int c) { return r * columns + c; };
    vector<int64> dist(pointCount, INF); vector<int> parent(pointCount, -1);
    vector<char> visited(pointCount, false);
    using State = pair<int64, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    dist[pointId(0, 0)] = 0; heap.push({0, pointId(0, 0)});
    auto relax = [&](int u, int v, int cost) {
        if (dist[v] > dist[u] + cost) { dist[v] = dist[u] + cost; parent[v] = u; heap.push({dist[v], v}); } };
    while (!heap.empty()) {
        auto [currentDistance, u] = heap.top(); heap.pop();
        if (visited[u]) continue; visited[u] = true;
        int r = u / columns; int c = u % columns;
        if (r > 0) relax(u, pointId(r - 1, c), vertical[r - 1][c]);
        if (r < N) relax(u, pointId(r + 1, c), vertical[r][c]);
        if (c > 0) relax(u, pointId(r, c - 1), horizontal[r][c - 1]);
        if (c < M) relax(u, pointId(r, c + 1), horizontal[r][c]);
    }
    vector<vector<char>> blockedVertical(N, vector<char>(M + 1, false));
    vector<vector<char>> blockedHorizontal(N + 1, vector<char>(M, false));
    auto markEdge = [&](int u, int v) -> bool {
        int ur = u / columns, uc = u % columns, vr = v / columns, vc = v % columns;
        if (ur == vr) { int c = min(uc, vc); bool old = blockedHorizontal[ur][c]; blockedHorizontal[ur][c] = true; return old; }
        else { int r = min(ur, vr); bool old = blockedVertical[r][uc]; blockedVertical[r][uc] = true; return old; } };
    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
        if (!village[r][c]) continue;
        int u = pointId(r, c);
        while (u != pointId(0, 0)) { int p = parent[u]; if (markEdge(u, p)) break; u = p; } }
    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
        if (!village[r][c]) continue;
        blockedHorizontal[r][c] = true; blockedHorizontal[r + 1][c] = true;
        blockedVertical[r][c] = true; blockedVertical[r][c + 1] = true; }
    const int expandedPointCount = 4 * pointCount;
    auto stateId = [&](int r, int c, int quadrant) { return 4 * pointId(r, c) + quadrant; };
    vector<int> head(expandedPointCount, -1); vector<Edge> edges;
    edges.reserve(20LL * pointCount);
    auto addDirectedEdge = [&](int u, int v, int cost) { edges.push_back({v, head[u], cost}); head[u] = (int)edges.size() - 1; };
    auto addUndirectedEdge = [&](int u, int v, int cost) { addDirectedEdge(u, v, cost); addDirectedEdge(v, u, cost); };
    for (int r = 0; r <= N; ++r) for (int c = 0; c <= M; ++c) {
        bool isRoot = (r == 0 && c == 0);
        if (!isRoot && (r == 0 || !blockedVertical[r - 1][c])) addUndirectedEdge(stateId(r,c,0), stateId(r,c,1), 0);
        if (r == N || !blockedVertical[r][c]) addUndirectedEdge(stateId(r,c,2), stateId(r,c,3), 0);
        if (!isRoot && (c == 0 || !blockedHorizontal[r][c - 1])) addUndirectedEdge(stateId(r,c,0), stateId(r,c,3), 0);
        if (c == M || !blockedHorizontal[r][c]) addUndirectedEdge(stateId(r,c,1), stateId(r,c,2), 0); }
    for (int r = 0; r < N; ++r) for (int c = 0; c < M; ++c) {
        if (village[r][c]) continue;
        addUndirectedEdge(stateId(r,c,2), stateId(r,c+1,3), horizontal[r][c]);
        addUndirectedEdge(stateId(r,c+1,3), stateId(r+1,c+1,0), vertical[r][c+1]);
        addUndirectedEdge(stateId(r+1,c+1,0), stateId(r+1,c,1), horizontal[r+1][c]);
        addUndirectedEdge(stateId(r,c,2), stateId(r+1,c,1), vertical[r][c]); }
    for (int r = 0; r < N; ++r) {
        addUndirectedEdge(stateId(r,0,3), stateId(r+1,0,0), vertical[r][0]);
        addUndirectedEdge(stateId(r,M,2), stateId(r+1,M,1), vertical[r][M]); }
    for (int c = 0; c < M; ++c) {
        addUndirectedEdge(stateId(0,c,1), stateId(0,c+1,0), horizontal[0][c]);
        addUndirectedEdge(stateId(N,c,2), stateId(N,c+1,3), horizontal[N][c]); }
    const int source = stateId(0,0,1); const int target = stateId(0,0,3);
    vector<int64> answerDistance(expandedPointCount, INF); vector<char> finalized(expandedPointCount, false);
    while (!heap.empty()) heap.pop();
    answerDistance[source] = 0; heap.push({0, source});
    while (!heap.empty()) {
        auto [currentDistance, u] = heap.top(); heap.pop();
        if (finalized[u]) continue; finalized[u] = true;
        if (u == target) break;
        for (int ei = head[u]; ei != -1; ei = edges[ei].next) {
            const Edge &e = edges[ei]; int v = e.to;
            int64 nd = currentDistance + (int64)e.cost;
            if (nd < answerDistance[v]) { answerDistance[v] = nd; heap.push({nd, v}); } } }
    cout << answerDistance[target] << '\n';
    return 0;
}
