// Codeforces 2201G "Codeforces Heuristic Contest 1001" -- reference solution.
// Written for this repository as a hand-off artifact; no external license.
//
// Only n = 5 and n = 1001 are legal inputs.  n = 5 prints a fixed 16-cycle.
// For n = 1001 (the constants below were found offline with a SAT solver and
// are specific to n mod 54 == 29, i.e. to n = 1001):
//   1. Interior pattern: row%3==0 -> col%3 in {0,1}; otherwise col%3==2.  Every
//      chosen cell has exactly two chosen (2,3)-neighbours (density 4/9); it is a
//      weave of vertical and horizontal zig-zag strands.
//   2. Border strips of width 8 (periods 18/18/9/27) turn the strands around, so
//      the grid splits into 53 "vertical" cycles, 35 "horizontal" cycles and a
//      few tiny or broken pieces next to the empty 8x8 corners.
//   3. TOPLINK every 18 columns along the top edge re-pairs two strand ends and
//      fuses consecutive vertical cycles (a 2-opt move on two distinct cycles
//      always yields one cycle).  LEFTLINK every 27 rows does the same for the
//      horizontal cycles (two interleaved chains).  One 24x24 CROSS patch at
//      (99,99) then fuses the three remaining big cycles.
//   4. Everything outside the largest cycle is deleted (a whole component can be
//      removed without changing any other chosen cell's degree).
// The result is one induced cycle of 420144 cells >= floor(1001^2/e) = 368615.
#include <bits/stdc++.h>
using namespace std;

static const char *TOP[8] = {
    "000000000000011001",
    "000100100000000000",
    "001001000010000011",
    "010100100000101000",
    "001101001010100000",
    "000000001000001000",
    "110110110110110110",
    "000000000001000000",
};
static const char *BOTTOM[8] = {
    "001000001000001000",
    "000001001001000001",
    "010001000001000101",
    "000000000000000000",
    "110110110110110110",
    "000000000000000000",
    "001001001001001001",
    "110110110110110110",
};
static const char *LEFT[8] = {
    "000000000",
    "000000000",
    "000000100",
    "000010001",
    "000000000",
    "011011011",
    "000000000",
    "100100100",
};
static const char *RIGHT[8] = {
    "001010000000001011010000001",
    "100000100100100000000000100",
    "010101000001010010111101000",
    "100101110100100100000100100",
    "000000000000000000000000000",
    "011011011011011011011011011",
    "000000000000000000000000000",
    "100100100100100100100100100",
};
static const char *TOPLINK[12] = {
    "000001001000",
    "000000000000",
    "001001000010",
    "010100100000",
    "001100000010",
    "000000001000",
    "110110110110",
    "000000000001",
    "001001001001",
    "110110110110",
    "001001001001",
    "001001001001",
};
static const char *LEFTLINK[14] = {
    "00010001011011011011",
    "00010100100100100100",
    "10010100100100100100",
    "01000001011011011011",
    "00100100100100100100",
    "00100100100100100100",
    "00010001011011011011",
    "10000100100100100100",
    "00100100100100100100",
    "01010001011011011011",
    "10000100100100100100",
    "10010100100100100100",
    "00010001011011011011",
    "00100100100100100100",
};
static const char *CROSS[24] = {
    "110110110110110110110110",
    "001001001001001001001001",
    "001000000001001001001001",
    "110110110110110110110110",
    "001001001001001001001001",
    "001001100000001001001001",
    "100110100110110110110110",
    "001011011011011001001001",
    "001000100100001001001001",
    "100100100000110110110110",
    "001001010010011011001001",
    "001001100100101001001001",
    "110100100000000010010110",
    "001001001010010011001001",
    "001001101100100101001001",
    "110110110110000010010010",
    "001001001000010010001001",
    "001001001101101101101001",
    "110110110110110010110010",
    "001001001000000011001001",
    "001001001001001001001001",
    "110110110110110110110110",
    "001001001001000000001001",
    "001001001001001001001001",
};

static const int DR[8] = {2, 3, -2, -3, 2, 3, -2, -3};
static const int DC[8] = {3, 2, 3, 2, -3, -2, -3, -2};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    if (n != 1001) {
        puts("01110\n11011\n10001\n11011\n01110");
        return 0;
    }
    const int W = 8;
    vector<char> g((size_t)n * n, 0);
    auto at = [&](int r, int c) -> char & { return g[(size_t)r * n + c]; };
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            bool t = r < W, b = r >= n - W, l = c < W, rt = c >= n - W;
            if (t + b + l + rt >= 2) continue;              // corners stay empty
            char x;
            if (t) x = TOP[r][c % 18];
            else if (b) x = BOTTOM[n - 1 - r][c % 18];
            else if (l) x = LEFT[c][r % 9];
            else if (rt) x = RIGHT[n - 1 - c][r % 27];
            else x = (r % 3 == 0) ? (c % 3 < 2 ? '1' : '0') : (c % 3 == 2 ? '1' : '0');
            at(r, c) = x == '1';
        }
    auto patch = [&](const char *const *tile, int h, int w, int r0, int c0) {
        for (int a = 0; a < h; a++)
            for (int b = 0; b < w; b++) at(r0 + a, c0 + b) = tile[a][b] == '1';
    };
    for (int c0 = 36; c0 <= 954; c0 += 18) patch(TOPLINK, 12, 12, 0, c0);
    for (int r0 = 69; r0 <= 933; r0 += 27) patch(LEFTLINK, 14, 20, r0, 0);
    patch(CROSS, 24, 24, 99, 99);

    // label components, remember which are simple cycles
    vector<int> lab((size_t)n * n, -1), stack;
    int best = -1; long long bestSize = 0;
    int id = 0;
    for (int s = 0; s < n * n; s++) {
        if (!g[s] || lab[s] >= 0) continue;
        long long size = 0; bool cycle = true;
        stack.assign(1, s); lab[s] = id;
        while (!stack.empty()) {
            int x = stack.back(); stack.pop_back(); size++;
            int r = x / n, c = x % n, deg = 0;
            for (int k = 0; k < 8; k++) {
                int rr = r + DR[k], cc = c + DC[k];
                if (rr < 0 || rr >= n || cc < 0 || cc >= n) continue;
                int y = rr * n + cc;
                if (!g[y]) continue;
                deg++;
                if (lab[y] < 0) { lab[y] = id; stack.push_back(y); }
            }
            if (deg != 2) cycle = false;
        }
        if (cycle && size > bestSize) { bestSize = size; best = id; }
        id++;
    }
    string out;
    out.reserve((size_t)n * (n + 1));
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) out += (g[r * n + c] && lab[r * n + c] == best) ? '1' : '0';
        out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
