// External reference: http://cs101.openjudge.cn/practice/01816/statistics/
// Accepted submission: 52502472
// Source: http://cs101.openjudge.cn/practice/solution/52502472/
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

struct Node
{
	vector<int> idx;
	Node* next[28]{ nullptr };// ?=26,*=27
};

void insert(string& s, int idx, Node* root)
{
	Node* cur = root;
	for (char c : s)
	{
		int x = c == '?' ? 26 : c == '*' ? 27 : c - 'a';
		if (cur->next[x] == nullptr)
			cur->next[x] = new Node();
		cur = cur->next[x];
	}
	(cur->idx).push_back(idx);
}

vector<int> res;
void compute(string& s, Node* cur, int l)
{
	if (l == s.size())
	{
		for (int i : cur->idx)res.push_back(i);
		// tailing *
		cur = cur->next[27];
		while (cur != nullptr)
		{
			for (int i : cur->idx)res.push_back(i);
			cur = cur->next[27];
		}
		return;
	}
	if (cur->next[s[l] - 'a'] != nullptr)compute(s, cur->next[s[l] - 'a'], l + 1);
	if (cur->next[26] != nullptr)compute(s, cur->next[26], l + 1);
	if (cur->next[27] != nullptr)
	{
		for (; l <= s.size(); l++)compute(s, cur->next[27], l);
	}
}

int main()
{
	int n, m; cin >> n >> m;
	Node* root = new Node();
	string p;
	for (int i = 0; i < n; i++)
	{
		cin >> p;
		insert(p, i, root);
	}
	for (int i = 0; i < m; i++)
	{
		cin >> p;
		res.clear();
		compute(p, root, 0);
		sort(res.begin(), res.end());
		res.erase(unique(res.begin(), res.end()), res.end());
		if (res.empty())
			cout << "Not match";
		else
			for (int i : res)
				cout << i << " ";
		cout << endl;
	}
	return 0;
}
