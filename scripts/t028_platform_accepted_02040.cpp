// External reference: http://cs101.openjudge.cn/practice/02040/statistics/
// Accepted submission: 52503890
// Source: http://cs101.openjudge.cn/practice/solution/52503890/
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
#define contains(x) count(x)

bool adj1[30][30], adj2[30][30];
vector<int> in_degree1, out_degree1, in_degree2, out_degree2;
unordered_map<string, int> indexMap1, indexMap2;
char mapping[30]; // mapping[i] = j 表示语言1的单词i对应语言2的单词j
bool used[30];   // 记录语言2的单词是否已被占用

bool dfs(int u1)
{
	if (u1 == in_degree1.size())return true;
	for (int u2 = 0; u2 < in_degree1.size(); u2++)
	{
		if (used[u2]) continue;
		if (in_degree1[u1] != in_degree2[u2] || out_degree1[u1] != out_degree2[u2]) continue;
		if (adj1[u1][u1] != adj2[u2][u2]) continue;
		bool ok = true;
		for (int prev = 0; prev < u1; ++prev) {
			if (adj1[u1][prev] != adj2[u2][mapping[prev]] ||
				adj1[prev][u1] != adj2[mapping[prev]][u2]) {
				ok = false;
				break;
			}
		}

		if (ok) {
			mapping[u1] = u2;
			used[u2] = true;
			if (dfs(u1 + 1)) return true;
			used[u2] = false;
		}
	}
	return false;
}

void output()
{
	vector<string> word1(indexMap1.size()), word2(indexMap2.size());
	for (auto& [s, i] : indexMap1)
		word1[i] = s;
	for (auto& [s, i] : indexMap2)
		word2[i] = s;
	vector<string> ans(word1.size());
	for (int i = 0; i < word1.size(); i++)
		ans[i] = word1[i] + "/" + word2[mapping[i]];
	sort(ans.begin(), ans.end());
	for (auto& s : ans)
		cout << s << endl;
	cout << endl;
}

int main()
{
	while (true)
	{
		int n;
		cin >> n;
		if (n == 0)
			break;
		memset(adj1, false, sizeof(adj1));
		memset(adj2, false, sizeof(adj2));
		memset(used, false, sizeof(used));
		in_degree1.clear();
		out_degree1.clear();
		indexMap1.clear();
		in_degree2.clear();
		out_degree2.clear();
		indexMap2.clear();
		string l, r; int u, v;
		for (int i = 0; i < n; i++)
		{
			cin >> l >> r;
			if (indexMap1.contains(l))u = indexMap1[l];
			else { u = indexMap1[l] = in_degree1.size(); in_degree1.push_back(0); out_degree1.push_back(0); }
			if (indexMap1.contains(r))v = indexMap1[r];
			else { v = indexMap1[r] = in_degree1.size(); in_degree1.push_back(0); out_degree1.push_back(0); }
			in_degree1[v]++;
			out_degree1[u]++;
			adj1[u][v] = true;
		}
		for (int i = 0; i < n; i++)
		{
			cin >> l >> r;
			if (indexMap2.contains(l))u = indexMap2[l];
			else { u = indexMap2[l] = in_degree2.size(); in_degree2.push_back(0); out_degree2.push_back(0); }
			if (indexMap2.contains(r))v = indexMap2[r];
			else { v = indexMap2[r] = in_degree2.size(); in_degree2.push_back(0); out_degree2.push_back(0); }
			in_degree2[v]++;
			out_degree2[u]++;
			adj2[u][v] = true;
		}
		dfs(0);
		output();
	}
	return 0;
}
