// practice/31454 is the public version of private/1000002.
// firstSquare follows the method supplied by the problem author.
#include <iostream>
#include <string>
using namespace std;

int firstSquare(const string& s) {
    int n = s.size(), best = -1;
    for (int L = 1; 2 * L <= n; ++L) {
        int run = 0;
        for (int j = 0; j + L < n; ++j) {
            run = (s[j] == s[j + L]) ? run + 1 : 0;
            if (run >= L) {
                int start = j - L + 1;
                if (best < 0 || start < best) best = start;
                break;
            }
        }
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        string s;
        cin >> s;
        cout << firstSquare(s) << '\n';
    }
}
