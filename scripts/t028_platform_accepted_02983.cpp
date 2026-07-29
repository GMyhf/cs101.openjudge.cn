// External reference: http://cs101.openjudge.cn/practice/02983/statistics/
// Accepted submission: 51696117
// Source: http://cs101.openjudge.cn/practice/solution/51696117/
// License: not declared on the submission page; no license is inferred.

#include <iostream>
#include <string>
#include <cstring>

using namespace std;

static const int N = 16;
static const int COLS = 1024;                 // 4 * 256
static const int MAXR = 4096;                 // 16*16*16 (worst: all empty)
static const int MAXNODE = COLS + MAXR * 4 + 10;

struct DLX {
    int L[MAXNODE], R[MAXNODE], U[MAXNODE], D[MAXNODE];
    int C[MAXNODE];          // column node index (1..COLS)
    int S[COLS + 1];         // column sizes
    int rowId[MAXNODE];      // which exact-cover row this node belongs to
    int sz;                  // next free node
    int ans[256];            // selected row ids (solution)

    // mapping row id -> (r,c,v)
    int rr[MAXR], cc[MAXR], vv[MAXR];

    void init() {
        // header = 0, columns = 1..COLS
        for (int i = 0; i <= COLS; i++) {
            L[i] = i - 1;
            R[i] = i + 1;
            U[i] = D[i] = i;
            S[i] = 0;
        }
        L[0] = COLS;
        R[COLS] = 0;
        sz = COLS + 1;
    }

    inline void addRow(int rid, const int cols[4], int r, int c, int v) {
        rr[rid] = r; cc[rid] = c; vv[rid] = v;

        int first = -1;
        for (int k = 0; k < 4; k++) {
            int colNode = cols[k] + 1;       // convert 0..1023 -> 1..1024
            int p = sz++;

            C[p] = colNode;
            rowId[p] = rid;

            // link vertically into column
            U[p] = U[colNode];
            D[p] = colNode;
            D[U[colNode]] = p;
            U[colNode] = p;
            S[colNode]++;

            // link horizontally within row (circular)
            if (first == -1) {
                first = p;
                L[p] = R[p] = p;
            } else {
                L[p] = L[first];
                R[p] = first;
                R[L[first]] = p;
                L[first] = p;
            }
        }
    }

    inline void cover(int c) {
        L[R[c]] = L[c];
        R[L[c]] = R[c];
        for (int i = D[c]; i != c; i = D[i]) {
            for (int j = R[i]; j != i; j = R[j]) {
                U[D[j]] = U[j];
                D[U[j]] = D[j];
                S[C[j]]--;
            }
        }
    }

    inline void uncover(int c) {
        for (int i = U[c]; i != c; i = U[i]) {
            for (int j = L[i]; j != i; j = L[j]) {
                S[C[j]]++;
                U[D[j]] = j;
                D[U[j]] = j;
            }
        }
        L[R[c]] = c;
        R[L[c]] = c;
    }

    bool dfs(int k) {
        if (R[0] == 0) return true; // all columns covered => solved

        // choose column with minimal size (heuristic)
        int c = R[0];
        int best = S[c];
        for (int j = R[0]; j != 0; j = R[j]) {
            if (S[j] < best) {
                best = S[j];
                c = j;
                if (best <= 1) break;
            }
        }
        if (best == 0) return false;

        cover(c);
        for (int r = D[c]; r != c; r = D[r]) {
            ans[k] = rowId[r];
            for (int j = R[r]; j != r; j = R[j]) cover(C[j]);
            if (dfs(k + 1)) return true;
            for (int j = L[r]; j != r; j = L[j]) uncover(C[j]);
        }
        uncover(c);
        return false;
    }
};

static inline int boxId(int r, int c) {
    return (r / 4) * 4 + (c / 4);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    bool firstOut = true;

    while (true) {
        string gridStr[16];
        int got = 0;

        // read 16 non-empty lines; datasets separated by empty lines
        while (got < 16 && std::getline(cin, line)) {
            if (line.empty()) continue;
            if ((int)line.size() < 16) continue; // defensive
            gridStr[got++] = line.substr(0, 16);
        }
        if (got < 16) break; // EOF

        DLX dlx;
        dlx.init();

        int rid = 0;
        for (int r = 0; r < 16; r++) {
            for (int c = 0; c < 16; c++) {
                char ch = gridStr[r][c];
                int cellCol = r * 16 + c;

                if (ch != '-') {
                    int v = ch - 'A'; // 0..15
                    int rowCol = 256 + r * 16 + v;
                    int colCol = 512 + c * 16 + v;
                    int boxCol = 768 + boxId(r, c) * 16 + v;

                    int cols[4] = { cellCol, rowCol, colCol, boxCol };
                    dlx.addRow(rid++, cols, r, c, v);
                } else {
                    for (int v = 0; v < 16; v++) {
                        int rowCol = 256 + r * 16 + v;
                        int colCol = 512 + c * 16 + v;
                        int boxCol = 768 + boxId(r, c) * 16 + v;

                        int cols[4] = { cellCol, rowCol, colCol, boxCol };
                        dlx.addRow(rid++, cols, r, c, v);
                    }
                }
            }
        }

        dlx.dfs(0);

        int out[16][16];
        for (int r = 0; r < 16; r++)
            for (int c = 0; c < 16; c++)
                out[r][c] = -1;

        // DLX solution has exactly 256 chosen rows (one per cell)
        for (int i = 0; i < 256; i++) {
            int id = dlx.ans[i];
            int r = dlx.rr[id], c = dlx.cc[id], v = dlx.vv[id];
            out[r][c] = v;
        }

        if (!firstOut) cout << "\n";
        firstOut = false;

        for (int r = 0; r < 16; r++) {
            for (int c = 0; c < 16; c++) {
                cout << char('A' + out[r][c]);
            }
            cout << "\n";
        }
    }
    return 0;
}
