// Reference implementation handed in by the maintainer together with practice/02934.
// Not taken from an OpenJudge submission page; no external license applies.

#include <iostream>
#include <string>
using namespace std;

int main() {
    string str, substr;
    while (cin >> str >> substr) {
        int pos = 0;
        for (int i = 1; i < (int)str.size(); ++i) {
            if (str[i] > str[pos]) pos = i;
        }
        str.insert(pos + 1, substr);
        cout << str << '\n';
    }
    return 0;
}
