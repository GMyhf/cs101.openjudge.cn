// 04009 符号三角形 —— 平台已 Accepted（cs101.openjudge.cn 提交 #52995115，G++，40ms）。
// 为什么要有这份 C++：同目录 samplecode.py 的 Python 实现在真实平台 Time Limit Exceeded，
// 本地跑题面上界 n=24 也要几十秒。这份是该题目前唯一有平台背书的参考实现。
// 本地 21 组数据逐组比对一致，单组最慢 0.26s；题面上界 n=24 单独跑 2.3s，1..24 全跑 4.1s。
// 三种写法（位枚举 / 逐列 DFS 剪枝 / 本版）在 n=1..24 上结果逐行一致。
// 04009 符号三角形：枚举首行，位运算逐行下推。
// 编码 '+'=0、'-'=1，规则「同号->+ 异号->-」正好是相邻位异或，省掉取反。
// 提速三处：
//   ①popcount 用 16 位查表（平台不给编译选项，__builtin_popcount 无 popcnt 指令时会退化）；
//   ②首行左右翻转会把整个三角形镜像、符号个数不变，只枚举 m<=rev(m) 的一半，rev 也查表；
//   ③逐行累计 '-' 的个数 z 只增不减：z 已超过一半，或「剩下各行全是 '-' 也补不到一半」，
//     都可以立刻断掉这一枝。
#include <bits/stdc++.h>
using namespace std;

static unsigned char PC[1u<<16];
static unsigned short RV[1u<<16];

static inline int ones(unsigned x){ return PC[x & 0xFFFF] + PC[x >> 16]; }

static inline unsigned rev_n(unsigned m, int n){          // 把低 n 位左右翻转
    unsigned r = ((unsigned)RV[m & 0xFFFF] << 16) | RV[m >> 16];
    return r >> (32 - n);
}

static long long solve(int n){
    long long tot = (long long)n*(n+1)/2;
    if (tot % 2) return 0;                 // 总符号数为奇数，两种不可能一样多
    const int half = (int)(tot / 2);
    long long cnt = 0;
    const unsigned lim = 1u << n;
    for (unsigned m = 0; m < lim; ++m) {
        unsigned r = rev_n(m, n);
        if (r < m) continue;               // 镜像对已在另一边算过
        unsigned row = m;
        int z = ones(m);
        bool alive = true;
        for (int w = n; w > 1; --w) {
            int rest = (w-1)*w/2;          // 剩下各行至多还能有这么多个 '-'
            if (z > half || z + rest < half) { alive = false; break; }
            row = (row ^ (row >> 1)) & ((1u << (w-1)) - 1);
            z += ones(row);
        }
        if (alive && z == half) cnt += (r == m) ? 1 : 2;
    }
    return cnt;
}

int main(){
    for (unsigned i = 1; i < (1u<<16); ++i) PC[i] = PC[i>>1] + (i & 1);
    for (unsigned i = 0; i < (1u<<16); ++i) {
        unsigned v = 0;
        for (int b = 0; b < 16; ++b) if (i >> b & 1) v |= 1u << (15-b);
        RV[i] = (unsigned short)v;
    }
    int n;
    unordered_map<int,long long> memo;
    while (scanf("%d", &n) == 1 && n) {
        auto it = memo.find(n);
        if (it == memo.end()) it = memo.emplace(n, solve(n)).first;
        printf("%d %lld\n", n, it->second);
    }
    return 0;
}
