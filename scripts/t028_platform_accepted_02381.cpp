// External reference: http://cs101.openjudge.cn/practice/02381/statistics/
// Accepted submission: 52506143
// Source: http://cs101.openjudge.cn/practice/solution/52506143/
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

bitset<16000001> bs;

int main()
{
	int a, c, m, r;
	cin >> a >> c >> m >> r;
	bs[r] = true;
	r = (a * r + c) % m;
	while (!bs[r])
	{
		bs[r] = true;
		r = (a * r + c) % m;
	}
	int last = -1;
	int ans = 0;
	for (int i = 0; i <= m; i++)
	{
		if (!bs[i])continue;
		if (last != -1)ans = max(ans, i - last);
		last = i;
	}
    cout << ans << endl;
	return 0;
}
