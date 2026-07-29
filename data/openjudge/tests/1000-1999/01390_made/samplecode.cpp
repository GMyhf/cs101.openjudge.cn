// External reference: http://cs101.openjudge.cn/practice/01390/statistics/
// Accepted submission: 44843318
// Source: http://cs101.openjudge.cn/practice/solution/44843318/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;
const int maxn=205;
int dp[maxn][maxn][maxn],n;
struct node{
    int color,len;
}box[maxn];
int click(int l,int r,int len){
    if(dp[l][r][len])return dp[l][r][len];
    int res=box[r].len+len;
    res*=res;
    if(l==r){
        return dp[l][r][len]=res;
    }
    int tmp;
    res+=click(l,r-1,0);
    for(int i=r-1;i>=l;i--){
        if(box[i].color!=box[r].color)continue;
        tmp=click(l,i,box[r].len+len)+click(i+1,r-1,0);
        if(tmp<=res)continue;
        res=tmp;
        break;
    }
    return dp[l][r][len]=res;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin>>t;
    for(int x=1;x<=t;x++){
        memset(dp,0,sizeof(dp));
        int tag=1;
        cin>>n>>box[tag].color;
        box[tag].len=1;
        for(int i=2;i<=n;i++){
            int tmp;
            cin>>tmp;
            if(tmp==box[tag].color)box[tag].len++;
            else{
                box[++tag].color=tmp;
                box[tag].len=1;
            }
        }
        cout<<"Case "<<x<<": "<<click(1,tag,0)<<"\n";
    }
    return 0;
}
