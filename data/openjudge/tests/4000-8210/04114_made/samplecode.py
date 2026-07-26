#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

const double EPS = 1e-10;

struct Point {
    double x, y;
};

struct Segment {
    Point a, b;
};

// 计算叉积 (p2-p1) x (p3-p1)
double cross_product(Point p1, Point p2, Point p3) {
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x);
}

// 检查经过 l1, l2 的直线是否与线段 seg 相交
bool check_intersect(Point l1, Point l2, Segment seg) {
    // 如果直线上的两点重合，无法构成直线
    if (abs(l1.x - l2.x) < EPS && abs(l1.y - l2.y) < EPS) return false;
    
    // 如果线段两端点在直线两侧，叉积乘积应 <= 0
    return cross_product(l1, l2, seg.a) * cross_product(l1, l2, seg.b) < EPS;
}

void solve() {
    int n;
    cin >> n;
    vector<Segment> segs(n);
    vector<Point> pts;
    for (int i = 0; i < n; ++i) {
        cin >> segs[i].a.x >> segs[i].a.y >> segs[i].b.x >> segs[i].b.y;
        pts.push_back(segs[i].a);
        pts.push_back(segs[i].b);
    }

    if (n <= 2) {
        cout << "Yes!" << endl;
        return;
    }

    bool found = false;
    int m = pts.size();
    for (int i = 0; i < m && !found; ++i) {
        for (int j = i + 1; j < m && !found; ++j) {
            // 距离太近的点不能构成直线
            if (abs(pts[i].x - pts[j].x) < EPS && abs(pts[i].y - pts[j].y) < EPS) continue;

            bool ok = true;
            for (int k = 0; k < n; ++k) {
                if (!check_intersect(pts[i], pts[j], segs[k])) {
                    ok = false;
                    break;
                }
            }
            if (ok) found = true;
        }
    }

    if (found) cout << "Yes!" << endl;
    else cout << "No!" << endl;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}