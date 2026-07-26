#include <bits/stdc++.h>
using namespace std;

struct Node {
    long long val, mn;
    long long addTag;
    bool revTag;
    int pr, sz;
    Node *l, *r;
    Node(long long v, int p): val(v), mn(v), addTag(0), revTag(false), pr(p), sz(1), l(nullptr), r(nullptr) {}
};

static std::mt19937 rng((uint32_t)chrono::steady_clock::now().time_since_epoch().count());

int getSize(Node* t){ return t ? t->sz : 0; }
long long getMin(Node* t){ return t ? t->mn : (long long)4e18; }

void applyAdd(Node* t, long long d){
    if(!t) return;
    t->val += d;
    t->mn += d;
    t->addTag += d;
}

void applyRev(Node* t){
    if(!t) return;
    t->revTag ^= 1;
    swap(t->l, t->r);
}

void push(Node* t){
    if(!t) return;
    if(t->addTag != 0){
        applyAdd(t->l, t->addTag);
        applyAdd(t->r, t->addTag);
        t->addTag = 0;
    }
    if(t->revTag){
        applyRev(t->l);
        applyRev(t->r);
        t->revTag = false;
    }
}

void pull(Node* t){
    if(!t) return;
    t->sz = 1 + getSize(t->l) + getSize(t->r);
    t->mn = min(t->val, min(getMin(t->l), getMin(t->r)));
}

// split by first k elements: returns (a,b)
pair<Node*, Node*> split(Node* t, int k){
    if(!t) return {nullptr, nullptr};
    push(t);
    if(getSize(t->l) >= k){
        auto [a, b] = split(t->l, k);
        t->l = b;
        pull(t);
        return {a, t};
    }else{
        auto [a, b] = split(t->r, k - getSize(t->l) - 1);
        t->r = a;
        pull(t);
        return {t, b};
    }
}

Node* merge(Node* a, Node* b){
    if(!a) return b;
    if(!b) return a;
    if(a->pr < b->pr){
        push(a);
        a->r = merge(a->r, b);
        pull(a);
        return a;
    }else{
        push(b);
        b->l = merge(a, b->l);
        pull(b);
        return b;
    }
}

Node* newNode(long long v){
    return new Node(v, (int)rng());
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    Node* root = nullptr;
    for(int i=0;i<n;i++){
        long long x; cin >> x;
        root = merge(root, newNode(x));
    }

    int M;
    cin >> M;
    string op;
    while(M--){
        cin >> op;
        if(op == "ADD"){
            int x,y; long long d;
            cin >> x >> y >> d;
            auto [A, BC] = split(root, x-1);
            auto [B, C] = split(BC, y-x+1);
            applyAdd(B, d);
            root = merge(A, merge(B, C));
        }else if(op == "REVERSE"){
            int x,y; cin >> x >> y;
            auto [A, BC] = split(root, x-1);
            auto [B, C] = split(BC, y-x+1);
            applyRev(B);
            root = merge(A, merge(B, C));
        }else if(op == "REVOLVE"){
            int x,y; long long T;
            cin >> x >> y >> T;
            int len = y - x + 1;
            long long k = T % len;
            auto [A, BC] = split(root, x-1);
            auto [B, C] = split(BC, len);
            if(k != 0){
                auto [B1, B2] = split(B, len - (int)k);
                B = merge(B2, B1);
            }
            root = merge(A, merge(B, C));
        }else if(op == "INSERT"){
            int x; long long p;
            cin >> x >> p;
            auto [A, B] = split(root, x);
            Node* N = newNode(p);
            root = merge(A, merge(N, B));
        }else if(op == "DELETE"){
            int x; cin >> x;
            auto [A, BC] = split(root, x-1);
            auto [B, C] = split(BC, 1);
            // delete B;  // 可选：不手动释放也能过（OJ一般不查内存泄漏）
            root = merge(A, C);
        }else if(op == "MIN"){
            int x,y; cin >> x >> y;
            auto [A, BC] = split(root, x-1);
            auto [B, C] = split(BC, y-x+1);
            cout << getMin(B) << "\n";
            root = merge(A, merge(B, C));
        }
    }
    return 0;
}
