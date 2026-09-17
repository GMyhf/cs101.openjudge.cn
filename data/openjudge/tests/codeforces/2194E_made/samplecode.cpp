// Codeforces 2194E The Turtle Strikes Back -- reference solution.
// Written for this repository as a hand-off artifact for building judge data; no external license.
//
// f = best prefix path sum ending at a cell, g = best suffix path sum starting at it.
// Through(i,j) = f+g-a.  Negating (i,j): a path through it becomes Through-2a; a path avoiding it
// crosses the anti-diagonal i+j at another cell, so best avoiding = max Through over the other
// cells of that diagonal (top-2 per diagonal; -inf if the diagonal has one cell).
// Answer = min over cells of max(Through-2a, avoid).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
static char buf[1 << 25];
int bl, bp;
inline int gc() {
    if (bp == bl) { bl = fread(buf, 1, sizeof(buf), stdin); bp = 0; if (bl <= 0) return -1; }
    return buf[bp++];
}
inline ll rd() {
    int c = gc(); while (c != '-' && (c < '0' || c > '9')) c = gc();
    bool neg = false; if (c == '-') { neg = true; c = gc(); }
    ll x = 0; while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return neg ? -x : x;
}
int main() {
    const ll NEG = LLONG_MIN / 4;
    int t = rd();
    string out;
    while (t--) {
        int n = rd(), m = rd();
        vector<ll> a((size_t)n * m), f(a.size()), g(a.size());
        for (auto &x : a) x = rd();
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            ll best = NEG;
            if (i) best = max(best, f[(i - 1) * (size_t)m + j]);
            if (j) best = max(best, f[i * (size_t)m + j - 1]);
            if (!i && !j) best = 0;
            f[i * (size_t)m + j] = best + a[i * (size_t)m + j];
        }
        for (int i = n - 1; i >= 0; i--) for (int j = m - 1; j >= 0; j--) {
            ll best = NEG;
            if (i + 1 < n) best = max(best, g[(i + 1) * (size_t)m + j]);
            if (j + 1 < m) best = max(best, g[i * (size_t)m + j + 1]);
            if (i == n - 1 && j == m - 1) best = 0;
            g[i * (size_t)m + j] = best + a[i * (size_t)m + j];
        }
        int D = n + m - 1;
        vector<ll> t1(D, NEG), t2(D, NEG);
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            size_t k = i * (size_t)m + j; ll th = f[k] + g[k] - a[k]; int d = i + j;
            if (th > t1[d]) { t2[d] = t1[d]; t1[d] = th; }
            else if (th > t2[d]) t2[d] = th;
        }
        ll ans = LLONG_MAX;
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            size_t k = i * (size_t)m + j; ll th = f[k] + g[k] - a[k]; int d = i + j;
            ll avoid = (th == t1[d]) ? t2[d] : t1[d];
            ans = min(ans, max(th - 2 * a[k], avoid));
        }
        out += to_string(ans); out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
}
