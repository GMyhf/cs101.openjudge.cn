#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>
#include<vector>
#include<map>
#include<set>
#include<queue>
#include<stack>
#include<algorithm>
using namespace std;
#define INF 0x3f3f3f3f
#define N 16

int main() {
    int n, flag, i;
    unsigned short int a, b, a1, a2;
    scanf("%d", &n);
    while (n--) {
        scanf("%hd%hd", &a, &b);
        flag = 0;
        if (a == b) flag = 1;
        else for (i = 1; i < N; i++) {
            a1 = a << i;
            a2 = a >> (N - i);
            if ((a1 | a2) == b) {
                flag = 1;
                break;
            }
        }
        printf("%s\n", flag == 1 ? "YES" : "NO");
    }
    return 0;
}
