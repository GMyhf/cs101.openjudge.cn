// External reference: http://cs101.openjudge.cn/practice/27072/statistics/
// Accepted submission: 52514407
// Source: http://cs101.openjudge.cn/practice/solution/52514407/
// License: not declared on the submission page; no license is inferred.

#pragma GCC optimize("Ofast,inline,unroll-loops")
#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <cmath>

using namespace std;
typedef long long ll;
typedef unsigned long long ull;

const int pow10[7] = { 1, 10, 100, 1000, 10000, 100000, 1000000 };

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);

	int n; cin >> n;

	long long ans = 0;

	unordered_map<ull, int> cnt;

	vector<int> w; w.reserve(10);
	for (int k = 1; k <= 6; ++k) {
		cnt.clear();

		long long M = 1;
		for (int i = 0; i < k; ++i) M *= 10;
		M += 1; // M = 10^k + 1

		for (int x = 1; x <= n; ++x) {
			int len = log10(x) + 1;
			w.clear();
			for (int i = 0; i <= len - k; ++i)
				w.push_back(x % pow10[i + k] / pow10[i]);

			// 排序去重，得到独一无二的长度 k 的子串
			sort(w.begin(), w.end());
			int m = unique(w.begin(), w.end()) - w.begin();

			int num_subsets = 1 << m;
			for (int mask = 1; mask < num_subsets; ++mask) {
				ull val = 0;
				ull p = 1;
				int size = 0;
				for (int bit = 0; bit < m; ++bit) {
					if ((mask >> bit) & 1) {
						val += (ull)(w[bit] + 1) * p;
						p *= M;
						size++;
					}
				}
				cnt[val | ((ull)(size % 2) << 62)]++;
			}
		}
		for (auto [val,freq]: cnt)
			ans += freq * freq * (((val >> 62) & 1)?1:-1);
	}

	cout << ans << "\n";

	return 0;
}
