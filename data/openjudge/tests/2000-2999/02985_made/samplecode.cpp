// External reference: http://cs101.openjudge.cn/practice/02985/statistics/
// Accepted submission: 51696130
// Source: http://cs101.openjudge.cn/practice/solution/51696130/
// License: not declared on the submission page; no license is inferred.

#include <bits/stdc++.h>
using namespace std;

static const int FULL = (1<<9)-1;

struct SudokuSolver {
    int g[9][9]{};
    int rowUsed[9]{}, colUsed[9]{}, boxUsed[9]{};

    static inline int boxId(int r,int c){ return (r/3)*3 + (c/3); }

    bool init(const vector<string>& lines){
        memset(rowUsed,0,sizeof(rowUsed));
        memset(colUsed,0,sizeof(colUsed));
        memset(boxUsed,0,sizeof(boxUsed));
        for(int r=0;r<9;r++){
            for(int c=0;c<9;c++){
                int v = lines[r][c]-'0';
                g[r][c]=v;
                if(v==0) continue;
                int bit = 1<<(v-1);
                int b = boxId(r,c);
                if(rowUsed[r]&bit) return false;
                if(colUsed[c]&bit) return false;
                if(boxUsed[b]&bit) return false;
                rowUsed[r]|=bit; colUsed[c]|=bit; boxUsed[b]|=bit;
            }
        }
        return true;
    }

    bool dfs(){
        int bestR=-1,bestC=-1,bestMask=0, bestCnt=10;
        for(int r=0;r<9;r++){
            for(int c=0;c<9;c++){
                if(g[r][c]!=0) continue;
                int b=boxId(r,c);
                int mask = FULL & ~(rowUsed[r] | colUsed[c] | boxUsed[b]);
                int cnt = __builtin_popcount((unsigned)mask);
                if(cnt==0) return false;
                if(cnt < bestCnt){
                    bestCnt=cnt; bestMask=mask; bestR=r; bestC=c;
                    if(cnt==1) goto CHOSEN;
                }
            }
        }
        CHOSEN:
        if(bestR==-1) return true; // solved

        int r=bestR,c=bestC,b=boxId(r,c);
        int mask=bestMask;
        while(mask){
            int bit = mask & -mask;
            mask -= bit;
            int v = __builtin_ctz((unsigned)bit) + 1;
            g[r][c]=v;
            rowUsed[r]|=bit; colUsed[c]|=bit; boxUsed[b]|=bit;
            if(dfs()) return true;
            rowUsed[r]^=bit; colUsed[c]^=bit; boxUsed[b]^=bit;
            g[r][c]=0;
        }
        return false;
    }
};

static array<array<int,9>,9> rotateGrid(const array<array<int,9>,9>& A, int rot){
    array<array<int,9>,9> B{};
    if(rot==0){
        B=A;
    }else if(rot==1){ // 90° clockwise
        for(int i=0;i<9;i++) for(int j=0;j<9;j++) B[i][j]=A[8-j][i];
    }else if(rot==2){ // 180°
        for(int i=0;i<9;i++) for(int j=0;j<9;j++) B[i][j]=A[8-i][8-j];
    }else{ // rot==3, 270° clockwise
        for(int i=0;i<9;i++) for(int j=0;j<9;j++) B[i][j]=A[j][8-i];
    }
    return B;
}

static vector<array<int,9>> buildRowPerms(){
    vector<array<int,9>> perms;
    array<int,3> base{0,1,2};
    vector<array<int,3>> p3;
    sort(base.begin(), base.end());
    do{ p3.push_back(base); }while(next_permutation(base.begin(), base.end()));

    // rowSrc[i] = source row index in [0..8]
    for(auto bandPerm: p3){
        for(auto p0: p3) for(auto p1: p3) for(auto p2: p3){
            array<array<int,3>,3> inBand{p0,p1,p2};
            array<int,9> rowSrc{};
            for(int i=0;i<9;i++){
                int band=i/3, pos=i%3;
                int srcBand = bandPerm[band];
                int srcRowInBand = inBand[band][pos];
                rowSrc[i] = srcBand*3 + srcRowInBand;
            }
            perms.push_back(rowSrc);
        }
    }
    return perms; // 1296
}

// colInv: sourceCol -> finalCol
static bool isAllowedColInv(const int colInv[9]){
    bool usedCol[9]={0};
    for(int c=0;c<9;c++){
        int x=colInv[c];
        if(x<0 || x>=9) return false;
        if(usedCol[x]) return false;
        usedCol[x]=true;
    }
    bool usedStack[3]={0};
    for(int s=0;s<3;s++){
        int t = colInv[3*s]/3;
        if(colInv[3*s+1]/3 != t) return false;
        if(colInv[3*s+2]/3 != t) return false;
        if(usedStack[t]) return false;
        usedStack[t]=true;
    }
    return true;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if(!(cin>>T)) return 0;

    auto rowPerms = buildRowPerms();

    for(int tc=0; tc<T; tc++){
        array<array<int,9>,9> A{};
        vector<string> aLines(9), bLines(9);
        for(int i=0;i<9;i++){
            cin >> aLines[i];
            for(int j=0;j<9;j++) A[i][j]=aLines[i][j]-'0';
        }
        for(int i=0;i<9;i++) cin >> bLines[i];

        // solve this week's puzzle
        SudokuSolver solver;
        solver.init(bLines);
        solver.dfs();
        array<array<int,9>,9> S{};
        for(int i=0;i<9;i++) for(int j=0;j<9;j++) S[i][j]=solver.g[i][j];

        // precompute posRowS[d][r] = col index of digit d in row r
        int posRowS[10][9];
        for(int d=1; d<=9; d++){
            for(int r=0;r<9;r++){
                int cFound=-1;
                for(int c=0;c<9;c++) if(S[r][c]==d){ cFound=c; break; }
                posRowS[d][r]=cFound;
            }
        }
        int d0 = S[0][0];

        bool ok=false;

        for(int rot=0; rot<4 && !ok; rot++){
            auto G = rotateGrid(A, rot);

            int posRowG[10][9];
            for(int v=1; v<=9; v++){
                for(int r=0;r<9;r++){
                    int cFound=-1;
                    for(int c=0;c<9;c++) if(G[r][c]==v){ cFound=c; break; }
                    posRowG[v][r]=cFound;
                }
            }

            // guess which digit v in G maps to digit d0 in S
            for(int v=1; v<=9 && !ok; v++){
                for(const auto& rowSrc : rowPerms){
                    int colInv[9];
                    for(int k=0;k<9;k++) colInv[k]=-1;

                    // derive colInv uniquely from occurrences of digit v
                    for(int i=0;i<9;i++){
                        int sr = rowSrc[i];
                        int sc = posRowG[v][sr];
                        int fc = posRowS[d0][i];
                        colInv[sc]=fc;
                    }

                    if(!isAllowedColInv(colInv)) continue;

                    // inverse: finalCol -> sourceCol
                    int colSrc[9];
                    for(int sc=0; sc<9; sc++){
                        int fc = colInv[sc];
                        colSrc[fc]=sc;
                    }

                    int fwd[10], rev[10];
                    for(int i=0;i<=9;i++) fwd[i]=rev[i]=-1;

                    bool good=true;
                    for(int i=0;i<9 && good;i++){
                        int sr=rowSrc[i];
                        for(int j=0;j<9;j++){
                            int sc=colSrc[j];
                            int x=G[sr][sc];
                            int y=S[i][j];
                            if(fwd[x]==-1 && rev[y]==-1){
                                fwd[x]=y; rev[y]=x;
                            }else if(fwd[x]!=y || rev[y]!=x){
                                good=false; break;
                            }
                        }
                    }
                    if(good){ ok=true; break; }
                }
            }
        }

        cout << (ok ? "Yes" : "No") << "\n";
    }
    return 0;
}
