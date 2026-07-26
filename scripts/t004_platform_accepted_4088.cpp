// External reference: cs101.openjudge.cn practice/04088 statistics, Accepted solution 51702169.
// Source: http://cs101.openjudge.cn/practice/solution/51702169/
// License: no explicit license stated on the submission page; retained as an external platform reference.

#include <bits/stdc++.h>
using namespace std;

// 把非负整数 x 追加到字符串 s（不使用 to_string，减少开销）
static inline void append_uint(string &s, unsigned int x) {
    char buf[16];
    int len = 0;
    if (x == 0) {
        buf[len++] = '0';
    } else {
        char rev[16];
        while (x > 0) {
            rev[len++] = char('0' + (x % 10));
            x /= 10;
        }
        // 反转回正序
        for (int i = len - 1, k = 0; i >= 0; --i, ++k) buf[k] = rev[i];
    }
    s.append(buf, buf + len);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<unsigned int> A;
    A.reserve(n);
    for (int i = 0; i < n; ++i) {
        unsigned int x;
        cin >> x;
        A.push_back(x);
    }

    int m;
    cin >> m;
    vector<unsigned int> B;
    B.reserve(m);
    for (int i = 0; i < m; ++i) {
        unsigned int x;
        cin >> x;
        B.push_back(x);
    }

    size_t i = 0, j = 0;
    string out;
    // 预留一点空间，减少扩容（粗略估计：每个数最多 ~11 位 + 空格）
    out.reserve((size_t)(n + m) * 12);

    bool first = true;
    while (i < A.size() && j < B.size()) {
        if (A[i] == B[j]) {
            ++i; ++j;
        } else if (A[i] < B[j]) {
            if (!first) out.push_back(' ');
            first = false;
            append_uint(out, A[i]);
            ++i;
        } else { // A[i] > B[j]
            if (!first) out.push_back(' ');
            first = false;
            append_uint(out, B[j]);
            ++j;
        }
    }
    while (i < A.size()) {
        if (!first) out.push_back(' ');
        first = false;
        append_uint(out, A[i]);
        ++i;
    }
    while (j < B.size()) {
        if (!first) out.push_back(' ');
        first = false;
        append_uint(out, B[j]);
        ++j;
    }

    cout << out << "\n";
    return 0;
}
