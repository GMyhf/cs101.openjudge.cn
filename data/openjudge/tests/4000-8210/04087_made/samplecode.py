// External reference: cs101.openjudge.cn practice/04087 statistics, Accepted solution 52367412.
// Source: http://cs101.openjudge.cn/practice/solution/52367412/
// License: no explicit license stated on the submission page; retained as an external platform reference.

#include<iostream>
#include<queue>
#include<vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, k;
    cin >> n >> k;
    
    // 使用最大堆来维护当前看到的k个最小数
    priority_queue<int> maxHeap;
    
    for (int i = 0; i < n; ++i) {
        int num;
        cin >> num;
        
        if (maxHeap.size() < k) {
            // 堆还没满，直接加入
            maxHeap.push(num);
        } else if (num < maxHeap.top()) {
            // 新数比当前第k小的小，替换堆顶
            maxHeap.pop();
            maxHeap.push(num);
        }
    }
    
    // 堆顶就是第k小的数
    cout << maxHeap.top();
    
    return 0;
}
