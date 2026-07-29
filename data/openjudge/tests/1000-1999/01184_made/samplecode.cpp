// External reference: http://cs101.openjudge.cn/practice/01184/statistics/
// Accepted submission: 52500637
// Source: http://cs101.openjudge.cn/practice/solution/52500637/
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

bitset<6000000> vis;
int main()
{
	int pow[7] = { 1,10,100,1000,10000,100000,1000000 };
	int s, t; cin >> s >> t;
	s += pow[6] * 5;
	vis[s] = 1;
	queue<int> q;
	q.push(s);
	int dist = 0;
	while (!q.empty())
	{
		int size = q.size();
		for (int i = 0; i < size; i++)
		{
			int x = q.front();
			q.pop();
			if (x % pow[6] == t)
			{
				cout << dist << endl;
				return 0;
			}
			int cursor = x / pow[6];
			int digit = (x / pow[cursor]) % 10;
			// swap 0
			if (cursor != 0)
			{
				int x2 = x;
				int digit0 = x2 % 10;
				x2 -= digit0;
				x2 -= digit * pow[cursor];
				x2 += digit0 * pow[cursor];
				x2 += digit;
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
			// swap 1
			if (cursor != 5)
			{
				int x2 = x;
				int digit5 = (x2 / pow[5]) % 10;
				x2 -= digit5 * pow[5];
				x2 -= digit * pow[cursor];
				x2 += digit5 * pow[cursor];
				x2 += digit * pow[5];
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
			// up
			if (digit < 9)
			{
				int x2 = x + pow[cursor];
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
			// down
			if (digit > 0)
			{
				int x2 = x - pow[cursor];
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
			// left
			if (cursor != 0)
			{
				int x2 = x - pow[6];
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
			// right
			if (cursor != 5)
			{
				int x2 = x + pow[6];
				if (!vis[x2])
				{
					vis[x2] = true;
					q.push(x2);
				}
			}
		}
		dist++;
	}
	return 0;
}
