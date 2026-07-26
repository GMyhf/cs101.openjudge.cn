// External reference: cs101.openjudge.cn practice/04091 statistics, Accepted solution 51702184.
// Source: http://cs101.openjudge.cn/practice/solution/51702184/
// License: no explicit license stated on the submission page; retained as an external platform reference.

#include <bits/stdc++.h>
using namespace std;

struct Point {
    array<long long, 5> x{};
};

struct Node {
    int idx;     // index of point in pts
    int left;
    int right;
    int dim;     // split dimension
};

static int Kdim;
static vector<Point> pts;
static vector<int> orderIdx;
static vector<Node> nodes;

static inline long long dist2(const Point& p, const array<long long,5>& q) {
    long long s = 0;
    for (int i = 0; i < Kdim; i++) {
        long long d = p.x[i] - q[i];
        s += d * d;
    }
    return s;
}

int buildKD(int l, int r, int depth) {
    if (l >= r) return -1;
    int dim = depth % Kdim;
    int mid = (l + r) / 2;

    nth_element(orderIdx.begin() + l, orderIdx.begin() + mid, orderIdx.begin() + r,
                [&](int a, int b) {
                    return pts[a].x[dim] < pts[b].x[dim];
                });

    int nodeId = (int)nodes.size();
    nodes.push_back(Node{orderIdx[mid], -1, -1, dim});
    nodes[nodeId].left  = buildKD(l, mid, depth + 1);
    nodes[nodeId].right = buildKD(mid + 1, r, depth + 1);
    return nodeId;
}

// max-heap by distance (pair<dist, idx>), top is the worst among current best
void queryKD(int nodeId, const array<long long,5>& q, int M,
             priority_queue<pair<long long,int>>& heap) {
    if (nodeId == -1) return;

    const Node& nd = nodes[nodeId];
    const Point& p = pts[nd.idx];

    long long d = dist2(p, q);
    if ((int)heap.size() < M) {
        heap.push({d, nd.idx});
    } else if (d < heap.top().first) {
        heap.pop();
        heap.push({d, nd.idx});
    }

    int dim = nd.dim;
    long long diff = q[dim] - p.x[dim];

    int nearChild = (diff <= 0) ? nd.left : nd.right;
    int farChild  = (diff <= 0) ? nd.right : nd.left;

    queryKD(nearChild, q, M, heap);

    long long diff2 = diff * diff;
    if ((int)heap.size() < M || diff2 < heap.top().first) {
        queryKD(farChild, q, M, heap);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while ( (cin >> n >> Kdim) ) {
        pts.assign(n, Point{});
        for (int i = 0; i < n; i++) {
            for (int d = 0; d < Kdim; d++) cin >> pts[i].x[d];
        }

        nodes.clear();
        orderIdx.resize(n);
        iota(orderIdx.begin(), orderIdx.end(), 0);
        int root = buildKD(0, n, 0);

        int t;
        cin >> t;
        while (t--) {
            array<long long,5> q{};
            for (int d = 0; d < Kdim; d++) cin >> q[d];
            int M;
            cin >> M;
            if (M > n) M = n;

            priority_queue<pair<long long,int>> heap;
            queryKD(root, q, M, heap);

            vector<pair<long long,int>> best;
            best.reserve(heap.size());
            while (!heap.empty()) {
                best.push_back(heap.top());
                heap.pop();
            }
            sort(best.begin(), best.end(),
                 [](const auto& a, const auto& b){ return a.first < b.first; });

            cout << "the closest " << M << " points are:\n";
            for (auto &it : best) {
                const Point& p = pts[it.second];
                for (int d = 0; d < Kdim; d++) {
                    if (d) cout << ' ';
                    cout << p.x[d];
                }
                cout << "\n";
            }
        }
    }
    return 0;
}
