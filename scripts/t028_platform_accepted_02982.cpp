// External reference: http://cs101.openjudge.cn/practice/02982/statistics/
// Accepted submission: 50273762
// Source: http://cs101.openjudge.cn/practice/solution/50273762/
// License: not declared on the submission page; no license is inferred.

#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
#include <cstring>
#include <queue>
#include <stack>
#include <string>
#include <iomanip>
#include <unordered_set>
#include <unordered_map>
#include <cmath>
#include <cstdio>
#include <set>
#include <string>
#include <sstream>
#include <numeric>
#include <map>
using namespace std;

bool check(vector<vector<char>>& mat, int x, int y, char num) {
    if (mat[x][y] != '0') return false;
    for (int i = 0;i < 9;i++) {
        if (mat[i][y] == num) return false;
    }
    for (int j = 0;j < 9;j++) {
        if (mat[x][j] == num) return false;
    }
    int x_begin = (x / 3) * 3, y_begin = (y / 3) * 3;
    for (int k = 0;k < 3;k++) {
        for (int t = 0;t < 3;t++) {
            int nx = x_begin + k, ny = y_begin + t;
            if (mat[nx][ny] == num) return false;
        }
    }
    return true;
}

bool DFS(vector<vector<char>>& mat) {
    for (int i = 0;i < 9;i++) {
        for (int j = 0;j < 9;j++) {
            if (mat[i][j] != '0') continue;
            for (char c = '1';c <= '9';c++) {
                if (check(mat, i, j, c)) {
                    mat[i][j] = c;
                    if (DFS(mat)) return true;
                    mat[i][j] = '0';
                }
            }
            return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        vector<vector<char>> mat(9, vector<char>(9));
        for (int i = 0;i < 9;i++) {
            for (int j = 0;j < 9;j++) {
                cin >> mat[i][j];
            }
        }
        DFS(mat);
        for (int i = 0;i < 9;i++) {
            for (int j = 0;j < 9;j++) {
                cout << mat[i][j];
            }
            cout << endl;
        }
    }




    return 0;
}
