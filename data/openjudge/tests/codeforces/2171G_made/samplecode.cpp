// Codeforces 2171G Sakura Adachi and Optimal Sequences -- reference solution.
// Written for this repository as a hand-off artifact for building judge data; no external license.
//
// Fix the number k of doublings (a_i * 2^k <= b_i for all i).  With d_i = b_i - a_i*2^k, index i
// needs c_{i,0} increments before the first doubling and c_{i,j} after the j-th, with
// sum_j c_{i,j} 2^{k-j} = d_i; the minimum is unique: c_{i,0} = d_i >> k, c_{i,j} = bit (k-j).
// x = min_k (k + sum_i cost_i(k)); sequences for a given k = product over stages of the
// multinomial (C_j; c_{1,j},...,c_{n,j}), counted mod p via Lucas; sum over all optimal k.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll P = 1000003;
ll fact[P], inv[P];
ll pw(ll b, ll e) { ll r = 1; b %= P; while (e) { if (e & 1) r = r * b % P; b = b * b % P; e >>= 1; } return r; }
// C(N, m) mod P with m < P, N arbitrary (Lucas: only the lowest digit of m is non-zero).
ll binom(ll N, ll m) {
    ll n0 = N % P;
    if (m > n0) return 0;
    return fact[n0] * inv[m] % P * inv[n0 - m] % P;
}
int main() {
    fact[0] = 1; for (ll i = 1; i < P; i++) fact[i] = fact[i - 1] * i % P;
    inv[P - 1] = pw(fact[P - 1], P - 2); for (ll i = P - 1; i > 0; i--) inv[i - 1] = inv[i] * i % P;
    int t; if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        int n; scanf("%d", &n);
        vector<ll> a(n), b(n);
        for (auto &x : a) scanf("%lld", &x);
        for (auto &x : b) scanf("%lld", &x);
        int K = 60;
        for (int i = 0; i < n; i++) { int k = 0; while ((a[i] << (k + 1)) <= b[i]) k++; K = min(K, k); }
        vector<ll> cost(K + 1);
        for (int k = 0; k <= K; k++) {
            ll c = k;
            for (int i = 0; i < n; i++) { ll d = b[i] - (a[i] << k); c += (d >> k) + __builtin_popcountll(d & ((1LL << k) - 1)); }
            cost[k] = c;
        }
        ll x = *min_element(cost.begin(), cost.end());
        ll total = 0;
        for (int k = 0; k <= K; k++) {
            if (cost[k] != x) continue;
            ll ways = 1, pref = 0;
            for (int i = 0; i < n; i++) { ll c0 = (b[i] - (a[i] << k)) >> k; pref += c0; ways = ways * binom(pref, c0) % P; }
            for (int j = 1; j <= k; j++) {
                ll cnt = 0;
                for (int i = 0; i < n; i++) cnt += ((b[i] - (a[i] << k)) >> (k - j)) & 1;
                ways = ways * fact[cnt] % P;
            }
            total = (total + ways) % P;
        }
        printf("%lld %lld\n", x, total);
    }
}
