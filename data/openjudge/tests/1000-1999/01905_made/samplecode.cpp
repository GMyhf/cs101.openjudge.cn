// External reference: http://cs101.openjudge.cn/practice/01905/statistics/
// Accepted submission: 52503961
// Source: http://cs101.openjudge.cn/practice/solution/52503961/
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

int main()
{
	while (true)
	{
		double l, a, b; cin >> l >> a >> b;
		if (l == -1 && a == -1 && b == -1)break;
		double frac = 1. / (1. + a * b);
		double left = 0, right = 3.14;
		for (int i = 0; i < 100; i++)
		{
			double mid = (left + right) / 2;
			if (sin(mid) / mid > frac)left = mid;
            else right = mid;
		}
		double h = l * (1 - cos(right)) / (2 * sin(right));
        cout << fixed << setprecision(3) << h << endl;
	}
	return 0;
}
