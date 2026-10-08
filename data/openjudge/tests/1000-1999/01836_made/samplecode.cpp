// External reference: http://cs101.openjudge.cn/practice/01836/statistics/
// Accepted submission: 52502642
// Source: http://cs101.openjudge.cn/practice/solution/52502642/
// License: not declared on the submission page; no license is inferred.

#include <algorithm>
#include <bitset>
#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <functional>
#include <numeric>
#include <queue>
#include <set>
#include <array>
#include <bit>
#include <map>
#include <cmath>
#include <iomanip>
#include <cstring>

using namespace std;
typedef long long ll;
typedef unsigned long long ull;

int n;
double a[1001];
// 修正：原提交用 char 存子序列长度，长度超过 127 时溢出（如 n=1000 严格递增会答错），改为 int。
int maxIncreasing[1001], maxDecreasing[1001];

int main()
{
	cin >> n;
	for (int i = 0; i < n; i++)cin >> a[i];
	for (int i = 0; i < 1001; i++) maxIncreasing[i] = maxDecreasing[i] = 1;
	for (int i = 0; i < n; i++)
		for (int j = 0; j < i; j++)if (a[j] < a[i])
			maxIncreasing[i] = max(maxIncreasing[i], (int)(maxIncreasing[j] + 1));
	for (int i = n - 1; i >= 0; i--)
		for (int j = n - 1; j > i; j--)if (a[j] < a[i])
			maxDecreasing[i] = max(maxDecreasing[i], (int)(maxDecreasing[j] + 1));
	int ans = 0;
	for (int i = 0; i < n; i++)
		for (int j = i; j < n; j++)
			ans = max(ans, maxIncreasing[i] + maxDecreasing[j] + (j == i ? -1 : 0));
	cout << n - ans << endl;
	return 0;
}
