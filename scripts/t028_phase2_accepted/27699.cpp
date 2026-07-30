// External reference: http://cs101.openjudge.cn/practice/27699/statistics/
// Accepted submission: 44028522
// Source: http://cs101.openjudge.cn/practice/solution/44028522/
// License: not declared on the submission page; no license is inferred.

#include <cstdio>
#include <algorithm>
#include <queue>

const int Inf = 0x3f3f3f3f;
const int MN = 500005, MS = 1 << 20 | 7;

int N, K, P[MN], Ans[MN];

#define li (i << 1)
#define ri (li | 1)
#define mid ((l + r) >> 1)
#define ls li, l, mid
#define rs ri, mid + 1, r
int mxp[MS];
void Build(int i, int l, int r) {
	if (l == r) return mxp[i] = l, void();
	Build(ls), Build(rs);
	mxp[i] = P[mxp[li]] > P[mxp[ri]] ? mxp[li] : mxp[ri];
}
void Del(int i, int l, int r, int p) {
	if (l == r) return mxp[i] = 0, void();
	p <= mid ? Del(ls, p) : Del(rs, p);
	mxp[i] = P[mxp[li]] > P[mxp[ri]] ? mxp[li] : mxp[ri];
}
int Qur(int i, int l, int r, int a, int b) {
	if (r < a || b < l) return 0;
	if (a <= l && r <= b) return mxp[i];
	int v1 = Qur(ls, a, b), v2 = Qur(rs, a, b);
	return P[v1] > P[v2] ? v1 : v2;
}

int inq[MN];
std::priority_queue<int> pq;
inline void check(int id) {
	if (inq[id]) return ;
	if (Qur(1, 1, N, id - K + 1, id + K - 1) == id)
		pq.push(id), inq[id] = 1;
}

int main() {
	scanf("%d%d", &N, &K);
	for (int i = 1; i <= N; ++i) scanf("%d", &P[i]);
	P[0] = -Inf;
	Build(1, 1, N);
	for (int i = 1; i <= N; ++i) check(i);
	for (int i = N; i >= 1; --i) {
		int u = pq.top(); pq.pop();
		Ans[u] = i;
		Del(1, 1, N, u);
		int pos;
		if ((pos = Qur(1, 1, N, u - K + 1, u - 1))) check(pos);
		if ((pos = Qur(1, 1, N, u + 1, u + K - 1))) check(pos);
	}
	for (int i = 1; i <= N; ++i) printf("%d\n", Ans[i]);
	return 0;
}
