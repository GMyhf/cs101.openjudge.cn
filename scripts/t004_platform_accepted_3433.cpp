#include <iostream>
#include <cstdio>
#include <algorithm>
#include <stdlib.h>
#include <string>
#include <memory>
#include <iomanip>
#include <math.h>
#include <cmath>
using namespace std;

int iflag=0;
int citystr[30] = { 0 };
int RED = 0, BLUE = 0;
int M, N, R, K, T;
int r_n, b_n, r_w = 1, b_w = 1;
int d_str, n_str, i_str, l_str, w_str;
int d_for, n_for, i_for, l_for, w_for;
int strmin;
int hour, minute, _hour, _minute;
int flag_redcreate, flag_bluecreate, flag_redtaken, flag_bluetaken;

class weapon {
public:
    int num=0;
    int wornarrow;
    string name;
};

class base
{
public:
    string type;
    int warriors;
    int locat;
    int d_n, n_n, i_n, l_n, w_n;
    int source;
    void getelements(int&);
};

class warrior {
public:
    int str;
    int id;
    int forcew[3] = { 0 };
    string type;
    weapon weapons[3];
    int force;
    int posi;
    base*mast;
    int state;
    int loyalty;
    double morale;
    int flag = 0;

    void mainset(base*a) {
        mast = a;
        id = (*a).warriors;
        posi = (*a).locat;
        state = 1;
        loyalty = 0;
        morale = 0;
        for (int i = 0; i <= 3; i++)
        {
            weapons[i].num = 0;
        }
    }
    void subset2() {
        for (int i = 0; i < 3; i++)
            switch (i) {
            case 0: {weapons[i].name = "sword"; forcew[i] = force * 2 / 10; break; }
            case 1: {weapons[i].name = "bomb"; break; }
            case 2: {weapons[i].name = "arrow";  weapons[i].wornarrow = 3; forcew[i] = R;  break; }
            }
    }

    virtual void rob(warrior*sb) {}
    virtual void subset() = 0;
    virtual void yell() {};
    virtual void attackback(warrior*sb)
    {
        sb->str -= weapons[0].num*forcew[0] + force / 2;
        forcew[0] *= 0.8;
        if (forcew[0] <1)
        {
            weapons[0].num = 0;
        }
    }
    virtual void attack(warrior*sb)
    {
        sb->str -= weapons[0].num*forcew[0] + force;
        forcew[0] = (int)forcew[0] * 8 / 10;
        int t = 0;
        if (forcew[0] <1)
        {
            weapons[0].num = 0;
        }
    }
    virtual void toescape() {}

    void march();
    void die();
    void getweapon(warrior*sb)
    {
        for (int i = 0; i <= 2; i++)
        {
            if (weapons[i].num == 0)
            {
                if (sb->weapons[i].num != 0)
                {
                    weapons[i] = sb->weapons[i];
                    forcew[i] = sb->forcew[i];
                }
            }
        }
    }
};

class city {
public:
    int soldier_n;
    warrior* red;
    warrior* blue;
    int redwin = 0;
    int bluewin = 0;
    bool redflag = false;
    bool blueflag = false;
    bool redarrowmatk = false;
    bool bluearrowmark = false;
    bool redif = false;
    bool blueif = false;
}allcity[30];
city redbase[5];
city bluebase[5];

void warrior::march() {
    if (type == "iceman")
    {
        flag++;
        if (flag % 2 == 0)
        {
            flag = 0;
            if (str > 9)
            {
                str -= 9;
                force += 20;
            }
            else
            {
                str = 1;
                force += 20;
            }
        }
    }
    if ((*mast).type == "red"&&state)
        posi++;
    else if ((*mast).type == "blue"&&state)
        posi--;
}
void warrior::die() {
    allcity[posi].soldier_n--;
    if ((*mast).type == "red")
        allcity[posi].red = NULL;
    if ((*mast).type == "blue")
        allcity[posi].blue = NULL;
    posi = -1;
    state = 0;
}

class dragon :public warrior {
public:
    void subset() {
        str = d_str;
        type = "dragon";
        force = d_for;
        weapons[id % 3].num++;
        morale = (double)(*mast).source / d_str;
    }
    void attackback() {

    }
    void yell() {
        printf("%03d:%02d %s dragon %d yelled in city %d\n", hour, minute, (*mast).type.c_str(), id, posi);
    }
};

class ninja :public warrior {
public:
    void subset() {
        str = n_str;
        type = "ninja";
        force = n_for;

        weapons[id % 3].num++;


        weapons[(id+1) % 3].num++;


    }
    void attackback(warrior*sb) {};
    void attack(warrior*sb, int weaponid) {
        weapons[weaponid].num--;
        switch (weaponid) {
        case 0: {sb->str -= force * 2 / 10; weapons[weaponid].num++;   break; }
        case 1: {sb->str -= force * 4 / 10;  break; }
        case 2: {sb->str -= force * 3 / 10; weapons[3].num++; break; }
        case 3: {sb->str -= force * 3 / 10;  break; }
        }
    }
};

class iceman :public warrior {
public:
    void subset() {
        str = i_str;
        type = "iceman";
        force = i_for;

        weapons[id % 3].num++;


    }
    void yell() {}
};

class wolf :public warrior {
public:
    void subset() {
        str = w_str;
        type = "wolf";
        force = w_for;
    }
    void rob(warrior*sb)
    {

    }
    void yell() {}
};

class lion :public warrior
{
public:
    void subset() {
        str = l_str;
        type = "lion";
        force = l_for;
        loyalty = (*mast).source;
    }

    void toescape() {
        state = 0;
        if (posi <= N && posi >= 1)
        {
            if ((*mast).type == "red")
                allcity[posi].red = NULL;
            else if ((*mast).type == "blue")
                allcity[posi].blue = NULL;
            allcity[posi].soldier_n--;
        }
        posi = -1;
        printf("%03d:%02d ", hour, minute);
        cout << (*mast).type;
        printf(" lion %d ran away\n", id);
    }
    void yell() {}
};

struct node {
    char type;
    node*next;
};

warrior*redwaror[1000];
warrior*bluewaror[1000];
dragon d_r[100], d_b[100];
ninja n_r[100], n_b[100];
iceman i_r[100], i_b[100];
lion l_r[100], l_b[100];
wolf w_r[100], w_b[100];
base r;
base b;
node*red, *blue;
node redline, redline1, redline2, redline3, redline4, blueline, blueline1, blueline2, blueline3, blueline4;
void lineset() {
    redline.type = 'i';
    redline1.type = 'l';
    redline2.type = 'w';
    redline3.type = 'n';
    redline4.type = 'd';
    redline.next = &redline1;
    redline1.next = &redline2;
    redline2.next = &redline3;
    redline3.next = &redline4;
    redline4.next = &redline;
    blueline.type = 'l';
    blueline1.type = 'd';
    blueline2.type = 'n';
    blueline3.type = 'i';
    blueline4.type = 'w';
    blueline.next = &blueline1;
    blueline1.next = &blueline2;
    blueline2.next = &blueline3;
    blueline3.next = &blueline4;
    blueline4.next = &blueline;
    red = &redline;
    blue = &blueline;
}

void mem() {

    red = &redline;
    blue = &blueline;
    flag_bluecreate = 1, flag_redcreate = 1;
    r.type = "red", b.type = "blue";
    r.warriors = 0, b.warriors = 0;
    r.locat = 0, b.locat = N + 1;
    r.d_n = 0, r.i_n = 0, r.l_n = 0, r.n_n = 0, r.w_n = 0;
    b.d_n = 0, b.i_n = 0, b.l_n = 0, b.n_n = 0, b.w_n = 0;
    r.source = M, b.source = M;
    flag_bluetaken = 0, flag_redtaken = 0;

    strmin = min(d_str, i_str);
    strmin = min(strmin, n_str);
    strmin = min(strmin, l_str);
    strmin = min(strmin, w_str);

    for (int i = 0; i <= N + 1; i++)
    {
        allcity[i].soldier_n = 0;
        allcity[i].red = NULL;
        allcity[i].blue = NULL;
    }
    for (int i = 0; i < 5; i++)
    {
        redbase[i].soldier_n = 0;
        bluebase[i].soldier_n = 0;
        redbase[i].blue = NULL;
        bluebase[i].red = NULL;
    }
    for (int i = 0; i < 100; i++)
    {
        i_r[i].flag = 0;
        i_b[i].flag = 0;
    }

    hour = 0, minute = 0;
    _hour = T / 60, _minute = T % 60;
}
void base::getelements(int&i)
{
    source += i;
    i = 0;
}

void init() {
    cin >> M >> N >> R >> K >> T;
    cin >> d_str >> n_str >> i_str >> l_str >> w_str;
    cin >> d_for >> n_for >> i_for >> l_for >> w_for;
}

void createwarriors() {
    if (flag_redcreate) {
        int flag = 0;
        switch ((*red).type) {
        case 'i':
            if (r.source >= i_str) {
                flag = 1;
                r.source -= i_str;
                r.i_n++;
                r.warriors++;
                i_r[r.i_n].mainset(&r);
                i_r[r.i_n].subset(); i_r[r.i_n].subset2();
                if (i_r[r.i_n].weapons[0].num != 0 && i_r[r.i_n].forcew[0] < 1)
                {
                    i_r[r.i_n].weapons[0].num--;
                }
                redwaror[r.warriors] = &i_r[r.i_n];
                printf("%03d:%02d red iceman %d born\n", hour, minute, r.warriors);
                allcity[0].soldier_n = 1;
                allcity[0].red = &i_r[r.i_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'l':
            if (r.source >= l_str) {
                flag = 1;
                r.source -= l_str;
                r.l_n++;
                r.warriors++;
                l_r[r.l_n].mainset(&r);
                l_r[r.l_n].subset(); l_r[r.l_n].subset2();
                redwaror[r.warriors] = &l_r[r.l_n];
                printf("%03d:%02d red lion %d born\n", hour, minute, r.warriors);
                printf("Its loyalty is %d\n", l_r[r.l_n].loyalty);
                allcity[0].soldier_n = 1;
                allcity[0].red = &l_r[r.l_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'w':
            if (r.source >= w_str) {
                flag = 1;
                r.source -= w_str;
                r.w_n++;
                r.warriors++;
                w_r[r.w_n].mainset(&r);
                w_r[r.w_n].subset(); w_r[r.w_n].subset2();
                redwaror[r.warriors] = &w_r[r.w_n];
                printf("%03d:%02d red wolf %d born\n", hour, minute, r.warriors);
                allcity[0].soldier_n = 1;
                allcity[0].red = &w_r[r.w_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'n':
            if (r.source >= n_str) {
                flag = 1;
                r.source -= n_str;
                r.n_n++;
                r.warriors++;
                n_r[r.n_n].mainset(&r);
                n_r[r.n_n].subset(); n_r[r.n_n].subset2();
                if (n_r[r.n_n].weapons[0].num != 0 && n_r[r.n_n].forcew[0] < 1)
                {
                    n_r[r.n_n].weapons[0].num--;
                }
                redwaror[r.warriors] = &n_r[r.n_n];
                printf("%03d:%02d red ninja %d born\n", hour, minute, r.warriors);
                allcity[0].soldier_n = 1;
                allcity[0].red = &n_r[r.n_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'd':
            if (r.source >= d_str) {
                flag = 1;
                r.source -= d_str;
                r.d_n++;
                r.warriors++;
                d_r[r.d_n].mainset(&r);
                d_r[r.d_n].subset(); d_r[r.d_n].subset2();
                if (d_r[r.d_n].weapons[0].num != 0 && d_r[r.d_n].forcew[0] < 1)
                {
                    d_r[r.d_n].weapons[0].num--;
                }
                redwaror[r.warriors] = &d_r[r.d_n];
                allcity[0].soldier_n = 1;
                allcity[0].red = &d_r[r.d_n];
                printf("%03d:%02d red dragon %d born\n", hour, minute, r.warriors);
                cout << "Its morale is " << setiosflags(ios::fixed) << setprecision(2) << d_r[r.d_n].morale << endl;
                break;
            }
            else {
                flag = 0;
                break;
            }
        }
        if (flag == 1)
        {
            red = red->next;
            flag = 0;
        }
    }
    if (flag_bluecreate) {
        int flag = 0;
        switch ((*blue).type) {
        case 'i':
            if (b.source >= i_str) {
                flag = 1;
                b.source -= i_str;
                b.i_n++;
                b.warriors++;
                i_b[b.i_n].mainset(&b);
                i_b[b.i_n].subset(); i_b[b.i_n].subset2();
                if (i_b[b.i_n].weapons[0].num != 0 && i_b[b.i_n].forcew[0] < 1)
                {
                    i_b[b.i_n].weapons[0].num--;
                }
                bluewaror[b.warriors] = &i_b[b.i_n];
                printf("%03d:%02d blue iceman %d born\n", hour, minute, b.warriors);
                allcity[N + 1].soldier_n = 1;
                allcity[N + 1].blue = &i_b[b.i_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'l':
            if (b.source >= l_str) {
                flag = 1;
                b.source -= l_str;
                b.l_n++;
                b.warriors++;
                l_b[b.l_n].mainset(&b);
                l_b[b.l_n].subset(); l_b[b.l_n].subset2();
                bluewaror[b.warriors] = &l_b[b.l_n];
                printf("%03d:%02d blue lion %d born\n", hour, minute, b.warriors);
                printf("Its loyalty is %d\n", l_b[b.l_n].loyalty);
                allcity[N + 1].soldier_n = 1;
                allcity[N + 1].blue = &l_b[b.l_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'w':
            if (b.source >= w_str) {
                flag = 1;
                b.source -= w_str;
                b.w_n++;
                b.warriors++;
                w_b[b.w_n].mainset(&b);
                w_b[b.w_n].subset(); w_b[b.w_n].subset2();
                bluewaror[b.warriors] = &w_b[b.w_n];
                printf("%03d:%02d blue wolf %d born\n", hour, minute, b.warriors);
                allcity[N + 1].soldier_n = 1;
                allcity[N + 1].blue = &w_b[b.w_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'n':
            if (b.source >= n_str) {
                flag = 1;
                b.source -= n_str;
                b.n_n++;
                b.warriors++;
                n_b[b.n_n].mainset(&b);
                n_b[b.n_n].subset(); n_b[b.n_n].subset2();
                if (n_b[b.n_n].weapons[0].num != 0 && n_b[b.n_n].forcew[0] < 1)
                {
                    n_b[b.n_n].weapons[0].num--;
                }
                bluewaror[b.warriors] = &n_b[b.n_n];
                printf("%03d:%02d blue ninja %d born\n", hour, minute, b.warriors);
                allcity[N + 1].soldier_n = 1;
                allcity[N + 1].blue = &n_b[b.n_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        case 'd':
            if (b.source >= d_str) {
                flag = 1;
                b.source -= d_str;
                b.d_n++;
                b.warriors++;
                d_b[b.d_n].mainset(&b);
                d_b[b.d_n].subset(); d_b[b.d_n].subset2();
                if (d_b[b.d_n].weapons[0].num != 0 && d_b[b.d_n].forcew[0] < 1)
                {
                    d_b[b.d_n].weapons[0].num--;
                }
                bluewaror[b.warriors] = &d_b[b.d_n];
                printf("%03d:%02d blue dragon %d born\n", hour, minute, b.warriors);
                cout << "Its morale is " << setiosflags(ios::fixed) << setprecision(2) << d_b[b.d_n].morale << endl;
                allcity[N + 1].soldier_n = 1;
                allcity[N + 1].blue = &d_b[b.d_n];
                break;
            }
            else {
                flag = 0;
                break;
            }
        }
        if (flag == 1)
        {
            blue = blue->next;
            flag = 0;
        }
    }
}

void lionsescape() {
    for (int i = 0; i <= N + 1; i++) {
        if (allcity[i].red != NULL)
        {
            if ((*allcity[i].red).type == "lion" && (*allcity[i].red).loyalty <= 0)
                (*allcity[i].red).toescape();
        }
        if (allcity[i].blue != NULL)
        {
            if ((*allcity[i].blue).type == "lion" && (*allcity[i].blue).loyalty <= 0)
                (*allcity[i].blue).toescape();
        }
    }
}

void marching() {
    for (int i = 0; i <= N + 1; i++) {
        if (allcity[i].red)
            allcity[i].red->march();
        if (allcity[i].blue)
            allcity[i].blue->march();
    }

    for (int i = 0; i <= N + 1; i++)
        allcity[i].soldier_n = 0, allcity[i].blue = NULL, allcity[i].red = NULL, allcity[i].redarrowmatk = false, allcity[i].bluearrowmark = false;
    for (int i = 1; i <= r.warriors; i++)
    {
        allcity[redwaror[i]->posi].soldier_n++;
        allcity[redwaror[i]->posi].red = redwaror[i];
    }
    for (int i = 1; i <= b.warriors; i++)
    {
        allcity[bluewaror[i]->posi].soldier_n++;
        allcity[bluewaror[i]->posi].blue = bluewaror[i];
    }
    for (int i = 0; i <= N + 1; i++) {
        if (i == 0 && allcity[i].soldier_n) {
            BLUE++;
            printf("%03d:%02d blue %s %d reached red headquarter with %d elements and force %d\n", hour, minute, allcity[i].blue->type.c_str(), allcity[i].blue->id, allcity[i].blue->str, allcity[i].blue->force);
            redbase[BLUE] = allcity[i];

            if (BLUE == 2)
            {
                printf("%03d:%02d red headquarter was taken\n", hour, minute);
            }
        }
        else if (i == N + 1 && allcity[i].soldier_n) {
            RED++;
            printf("%03d:%02d red %s %d reached blue headquarter with %d elements and force %d\n", hour, minute, allcity[i].red->type.c_str(), allcity[i].red->id, allcity[i].red->str, allcity[i].red->force);
            bluebase[RED] = allcity[i];

            if (RED == 2)
            {
                printf("%03d:%02d blue headquarter was taken\n", hour, minute);
            }
        }
        else {
            if (allcity[i].red)
                printf("%03d:%02d red %s %d marched to city %d with %d elements and force %d\n", hour, minute, allcity[i].red->type.c_str(), allcity[i].red->id, i, allcity[i].red->str, allcity[i].red->force);
            if (allcity[i].blue)
                printf("%03d:%02d blue %s %d marched to city %d with %d elements and force %d\n", hour, minute, allcity[i].blue->type.c_str(), allcity[i].blue->id, i, allcity[i].blue->str, allcity[i].blue->force);
        }
    }
}

void productstr()
{
    for (int i = 1; i <= N; i++)
    {
        citystr[i] += 10;
    }
}

void aloneget()
{
    for (int i = 1; i <= N; i++)
    {
        if (allcity[i].soldier_n == 1)
        {
            if (allcity[i].red)
            {
                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                r.getelements(citystr[i]);
            }
            else
            {
                if (allcity[i].blue)
                {
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                    b.getelements(citystr[i]);
                }
            }
        }
    }
}

void shoot() {
    if (allcity[1].red)
    {
        if (allcity[1+ 1].blue)
        {
            if (allcity[1].red->weapons[2].num != 0)
            {
                allcity[1 + 1].blue->str -= R;
                if (allcity[1 + 1].blue->str <= 0)
                {
                    allcity[1 + 1].soldier_n--;
                    allcity[1 + 1].redarrowmatk = true;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[1].red->type << " " << allcity[1].red->id << " shot and killed blue " << allcity[1 + 1].blue->type << " " << allcity[1 + 1].blue->id << endl;
                }
                else
                {
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[1].red->type << " " << allcity[1].red->id << " shot" << endl;
                }
                allcity[1].red->weapons[2].wornarrow--;
                if (allcity[1].red->weapons[2].wornarrow <= 0)
                {
                    allcity[1].red->weapons[2].num = 0;
                }
            }
        }
    }
    for (int i = 2; i < N; i++)
    {
        if (allcity[i].red)
        {
            if (allcity[i + 1].blue)
            {
                if (allcity[i].red->weapons[2].num != 0)
                {
                    allcity[i + 1].blue->str -= R;
                    if (allcity[i + 1].blue->str <= 0)
                    {
                        allcity[i + 1].soldier_n--;
                        allcity[i + 1].redarrowmatk = true;
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " shot and killed blue " << allcity[i + 1].blue->type << " " << allcity[i + 1].blue->id << endl;
                    }
                    else
                    {
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " shot" << endl;
                    }
                    allcity[i].red->weapons[2].wornarrow--;
                    if (allcity[i].red->weapons[2].wornarrow <= 0)
                    {
                        allcity[i].red->weapons[2].num = 0;
                    }
                }
            }
        }
        if (allcity[i].blue)
        {
            if (allcity[i - 1].red) {
                if (allcity[i].blue->weapons[2].num != 0)
                {
                    allcity[i - 1].red->str -= R;
                    if (allcity[i - 1].red->str <= 0)
                    {
                        allcity[i - 1].soldier_n--;
                        allcity[i - 1].bluearrowmark = true;
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " shot and killed red " << allcity[i - 1].red->type << " " << allcity[i - 1].red->id << endl;
                    }
                    else
                    {
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " shot" << endl;
                    }
                    allcity[i].blue->weapons[2].wornarrow--;
                    if (allcity[i].blue->weapons[2].wornarrow <= 0)
                    {
                        allcity[i].blue->weapons[2].num = 0;
                    }
                }
            }
        }
    }
    if (allcity[N].blue)
    {
        int i = N;
        if (allcity[i - 1].red) {
            if (allcity[i].blue->weapons[2].num != 0)
            {
                allcity[i - 1].red->str -= R;
                if (allcity[i - 1].red->str <= 0)
                {
                    allcity[i - 1].soldier_n--;
                    allcity[i - 1].bluearrowmark = true;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " shot and killed red " << allcity[i - 1].red->type << " " << allcity[i - 1].red->id << endl;
                }
                else
                {
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " shot" << endl;
                }
                allcity[i].blue->weapons[2].wornarrow--;
                if (allcity[i].blue->weapons[2].wornarrow <= 0)
                {
                    allcity[i].blue->weapons[2].num = 0;
                }
            }
        }
    }
}

void explode() {
    for (int i = 1; i <= N; i++)
    {
        int flag = 0;
        if (allcity[i].soldier_n == 2)
        {
            if (allcity[i].red->weapons[1].num != 0)
            {
                if (allcity[i].redflag || (i % 2 != 0 && allcity[i].redflag == false && allcity[i].blueflag == false))
                {
                    if (allcity[i].blue->str > (allcity[i].red->force + allcity[i].red->forcew[0] * allcity[i].red->weapons[0].num))
                    {
                        if (allcity[i].blue->type != "ninja")
                        {
                            if (allcity[i].red->str <= ( allcity[i].blue->force*1/2 + allcity[i].blue->weapons[0].num*allcity[i].blue->forcew[0]))
                            {
                                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " used a bomb and killed blue " << allcity[i].blue->type << " " << allcity[i].blue->id << endl;
                                flag = 1;
                                allcity[i].red->die();
                                allcity[i].blue->die();
                            }
                        }
                    }
                }
                else
                {
                    if (allcity[i].blueflag || (i % 2 == 0 && allcity[i].redflag == false && allcity[i].blueflag == false))
                    {
                        if (allcity[i].red->str <= (allcity[i].blue->force + allcity[i].blue->weapons[0].num*allcity[i].blue->forcew[0]))
                        {
                            cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " used a bomb and killed blue " << allcity[i].blue->type << " " << allcity[i].blue->id << endl;
                            flag = 1;
                            allcity[i].red->die();
                            allcity[i].blue->die();
                        }
                    }
                }
            }
            if (flag == 0)
            {
                if (allcity[i].blue->weapons[1].num != 0)
                {
                    if (allcity[i].blueflag || (i % 2 == 0 && allcity[i].redflag == false && allcity[i].blueflag == false))
                    {
                        if (allcity[i].red->str > (allcity[i].blue->force + allcity[i].blue->forcew[0] * allcity[i].blue->weapons[0].num))
                        {
                            if (allcity[i].red->type != "ninja")
                            {
                                if (allcity[i].blue->str <= ( allcity[i].red->force*1/2 + allcity[i].red->weapons[0].num*allcity[i].red->forcew[0]))
                                {
                                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " used a bomb and killed red " << allcity[i].red->type << " " << allcity[i].red->id << endl;
                                    flag = 1;
                                    allcity[i].red->die();
                                    allcity[i].blue->die();
                                }
                            }
                        }
                    }
                    else
                    {
                        if (allcity[i].redflag || (i % 2 != 0 && allcity[i].redflag == false && allcity[i].blueflag == false))
                        {
                            if (allcity[i].blue->str <= (allcity[i].red->force + allcity[i].red->weapons[0].num*allcity[i].red->forcew[0]))
                            {
                                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " used a bomb and killed red " << allcity[i].red->type << " " << allcity[i].red->id << endl;
                                flag = 1;
                                allcity[i].red->die();
                                allcity[i].blue->die();
                            }
                        }
                    }
                }
            }
        }
    }
}

void activeattack()
{
    for (int i = 1; i <= N; i++)
    {
        if (allcity[i].soldier_n == 2)
        {
            if ((allcity[i].blueflag == false && allcity[i].redflag == false && i % 2 != 0) || (allcity[i].redflag == true))
            {
                int bb = allcity[i].blue->str;
                allcity[i].red->attack(allcity[i].blue);
                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " attacked blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " in city " << i << " with " << allcity[i].red->str << " elements and force " << allcity[i].red->force << endl;
                if (allcity[i].blue->str <= 0)
                {
                    if (allcity[i].red->type == "wolf")
                    {
                        allcity[i].red->getweapon(allcity[i].blue);
                    }
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " was killed in city " << i << endl;
                    if (allcity[i].blue->type == "lion")
                    {
                        allcity[i].red->str += bb;
                    }
                    if (allcity[i].red->type == "dragon")
                    {
                        allcity[i].red->morale += 0.2;
                        if (allcity[i].red->morale > 0.8)
                        {
                            allcity[i].red->yell();
                        }
                    }

                    allcity[i].redif = true;
                    allcity[i].blueif = false;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                    allcity[i].redwin++;
                    allcity[i].bluewin = 0;
                    if (allcity[i].redflag == false)
                    {
                        if (allcity[i].redwin >= 2)
                        {
                            allcity[i].redflag = true;
                            allcity[i].blueflag = false;
                            cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red flag raised in city " << i << endl;
                        }
                    }
                    allcity[i].blue->die();
                }
                else
                {

                    int rr = allcity[i].red->str;
                    if (allcity[i].blue->type != "ninja")
                    {
                        allcity[i].blue->attackback(allcity[i].red);
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " fought back against red " << allcity[i].red->type << " " << allcity[i].red->id << " in city " << i << endl;
                    }
                    if (allcity[i].red->str <= 0)
                    {
                        if (allcity[i].blue->type == "wolf")
                        {
                            allcity[i].blue->getweapon(allcity[i].red);
                        }
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " was killed in city " << i << endl;
                        if (allcity[i].red->type == "lion")
                        {
                            allcity[i].blue->str += rr;
                        }
                        if (allcity[i].blue->type == "dragon")
                        {
                            allcity[i].blue->morale += 0.2;
                        }

                        allcity[i].blueif = true;
                        allcity[i].redif = false;
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                        allcity[i].bluewin++;
                        allcity[i].redwin = 0;
                        if (allcity[i].blueflag == false)
                        {
                            if (allcity[i].bluewin >= 2)
                            {
                                allcity[i].blueflag = true;
                                allcity[i].redflag = false;
                                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue flag raised in city " << i << endl;
                            }
                        }
                        allcity[i].red->die();
                    }
                    else
                    {
                        if (allcity[i].red->type == "dragon")
                        {
                            allcity[i].red->morale -= 0.2;
                            if (allcity[i].red->morale > 0.8)
                            {
                                allcity[i].red->yell();
                            }
                        }
                        if (allcity[i].blue->type == "dragon")
                        {
                            allcity[i].blue->morale -= 0.2;
                        }
                        if (allcity[i].red->type == "lion")
                        {
                            allcity[i].red->loyalty -= K;
                        }
                        if (allcity[i].blue->type == "lion")
                        {
                            allcity[i].blue->loyalty -= K;
                        }
                        allcity[i].blueif = false;
                        allcity[i].redif = false;
                        if (allcity[i].redflag)
                        {
                            allcity[i].bluewin = 0;
                        }
                        else
                        {
                            allcity[i].redwin = 0;
                            allcity[i].bluewin = 0;
                        }
                    }
                }
            }
            else
            {
                int bb = allcity[i].red->str;
                allcity[i].blue->attack(allcity[i].red);
                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " attacked red " << allcity[i].red->type << " " << allcity[i].red->id << " in city " << i << " with " << allcity[i].blue->str << " elements and force " << allcity[i].blue->force << endl;
                if (allcity[i].red->str <= 0)
                {
                    if (allcity[i].blue->type == "wolf")
                    {
                        allcity[i].blue->getweapon(allcity[i].red);
                    }
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " was killed in city " << i << endl;
                    if (allcity[i].red->type == "lion")
                    {
                        allcity[i].blue->str += bb;
                    }
                    if (allcity[i].blue->type == "dragon")
                    {
                        allcity[i].blue->morale += 0.2;
                        if (allcity[i].blue->morale > 0.8)
                        {
                            allcity[i].blue->yell();
                        }
                    }

                    allcity[i].blueif = true;
                    allcity[i].redif = false;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                    allcity[i].bluewin++;
                    allcity[i].redwin = 0;
                    if (allcity[i].blueflag == false)
                    {
                        if (allcity[i].bluewin >= 2)
                        {
                            allcity[i].blueflag = true;
                            allcity[i].redflag = false;
                            cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue flag raised in city " << i << endl;
                        }
                    }
                    allcity[i].red->die();
                }
                else
                {
                    int rr = allcity[i].blue->str;
                    if (allcity[i].red->type != "ninja")
                    {
                        allcity[i].red->attackback(allcity[i].blue);
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " fought back against blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " in city " << i << endl;
                    }
                    if (allcity[i].blue->str <= 0)
                    {
                        if (allcity[i].red->type == "wolf")
                        {
                            allcity[i].red->getweapon(allcity[i].blue);
                        }
                        if (allcity[i].red->type == "dragon")
                        {
                            allcity[i].red->morale += 0.2;
                        }
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " was killed in city " << i << endl;
                        if (allcity[i].blue->type == "lion")
                        {
                            allcity[i].red->str += rr;
                        }

                        allcity[i].blueif = false;
                        allcity[i].redif = true;
                        cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                        allcity[i].redwin++;
                        allcity[i].bluewin = 0;
                        if (allcity[i].redflag == false)
                        {
                            if (allcity[i].redwin >= 2)
                            {
                                allcity[i].redflag = true;
                                allcity[i].blueflag = false;
                                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red flag raised in city " << i << endl;
                            }
                        }
                        allcity[i].blue->die();
                    }
                    else
                    {
                        if (allcity[i].red->type == "dragon")
                        {
                            allcity[i].red->morale -= 0.2;
                        }
                        if (allcity[i].blue->type == "dragon")
                        {
                            allcity[i].blue->morale -= 0.2;
                            if (allcity[i].blue->morale > 0.8)
                            {
                                allcity[i].blue->yell();
                            }
                        }
                        if (allcity[i].red->type == "lion")
                        {
                            allcity[i].red->loyalty -= K;
                        }
                        if (allcity[i].blue->type == "lion")
                        {
                            allcity[i].blue->loyalty -= K;
                        }
                        allcity[i].blueif = false;
                        allcity[i].redif = false;
                        if (allcity[i].blueflag)
                        {
                            allcity[i].redwin = 0;
                        }
                        else
                        {
                            allcity[i].redwin = 0;
                            allcity[i].bluewin = 0;
                        }
                    }
                }
            }
        }
        else
        {
            if (allcity[i].red&&allcity[i].soldier_n == 1)
            {
                if (allcity[i].redarrowmatk)
                {
                    allcity[i].redwin++;
                    allcity[i].bluewin = 0;
                    if (allcity[i].red->type == "dragon")
                    {
                        allcity[i].red->morale += 0.2;
                        if ((allcity[i].blueflag == false && allcity[i].redflag == false && i % 2 != 0) || (allcity[i].redflag == true))
                        {
                            if (allcity[i].red->morale > 0.8)
                            {
                                allcity[i].red->yell();
                            }
                        }
                    }
                    if (allcity[i].red->type == "wolf")
                    {
                        allcity[i].red->getweapon(allcity[i].blue);
                    }

                    allcity[i].blueif = false;
                    allcity[i].redif = true;
                    allcity[i].blue->die();
                    allcity[i].soldier_n++;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                    if ((allcity[i].redflag == false && allcity[i].blueflag == false) || allcity[i].blueflag == true)
                    {
                        if (allcity[i].redwin >= 2)
                        {
                            allcity[i].redflag = true;
                            allcity[i].blueflag = false;
                            cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red flag raised in city " << i << endl;
                        }
                    }
                }
            }
            if (allcity[i].blue&&allcity[i].soldier_n == 1)
            {
                if (allcity[i].bluearrowmark)
                {
                    if (allcity[i].blue->type == "dragon")
                    {
                        allcity[i].blue->morale += 0.2;
                        if ((allcity[i].blueflag == false && allcity[i].redflag == false && i % 2 == 0) || (allcity[i].blueflag == true))
                        {
                            if (allcity[i].blue->morale > 0.8)
                            {
                                allcity[i].blue->yell();
                            }
                        }
                    }
                    if (allcity[i].blue->type == "wolf")
                    {
                        allcity[i].blue->getweapon(allcity[i].red);
                    }
                    allcity[i].bluewin++;
                    allcity[i].redwin = 0;

                    allcity[i].blueif = true;
                    allcity[i].redif = false;
                    allcity[i].red->die();
                    allcity[i].soldier_n++;
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " earned " << citystr[i] << " elements for his headquarter" << endl;
                    if ((allcity[i].redflag == false && allcity[i].blueflag == false) || allcity[i].redflag == true)
                    {
                        if (allcity[i].bluewin >= 2)
                        {
                            allcity[i].blueflag = true;
                            allcity[i].redflag = false;
                            cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue flag raised in city " << i << endl;
                        }
                    }
                }
            }
            if (allcity[i].soldier_n == 0)
            {
                if (allcity[i].redarrowmatk&&allcity[i].bluearrowmark==false)
                {
                    allcity[i].soldier_n++;
                    allcity[i].blue->die();
                }
                if (allcity[i].bluearrowmark&&allcity[i].redarrowmatk==false)
                {
                    allcity[i].soldier_n++;
                    allcity[i].red->die();
                }
            }
            if (allcity[i].soldier_n == 0 && allcity[i].redarrowmatk==true&&allcity[i].bluearrowmark==true)
            {
                allcity[i].redif = false;
                allcity[i].blueif = false;
                allcity[i].red->die();
                allcity[i].soldier_n++;
                allcity[i].blue->die();
                allcity[i].soldier_n++;
            }
        }
    }
}

void award()
{
    for (int i = 1; i <= N; i++)
    {
        if (r.source >= 8 && allcity[i].redif == true)
        {
            r.source -= 8;
            allcity[i].red->str += 8;
        }
        if (r.source < 8)
        {
            break;
        }
    }
    for (int i = N; i >= 1; i--)
    {
        if (b.source >= 8 && allcity[i].blueif == true)
        {
            b.source -= 8;
            allcity[i].blue->str += 8;
        }
        if (b.source < 8)
        {
            break;
        }
    }
}

void geteletments()
{
    for (int i = 1; i <= N; i++)
    {
        if (allcity[i].redif == true)
        {
            r.getelements(citystr[i]);
        }
        if (allcity[i].blueif == true)
        {
            b.getelements(citystr[i]);
        }
    }
}

void reportsource() {
    printf("%03d:%02d %d elements in red headquarter\n", hour, minute, r.source);
    printf("%03d:%02d %d elements in blue headquarter\n", hour, minute, b.source);
}

void reportwaror() {
    for (int i = 1; i <= N + 1; i++)
    {
        if (i >= 1 && i <= N)
        {
            int flag = 0;
            if (allcity[i].red)
            {
                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << allcity[i].red->type << " " << allcity[i].red->id << " has ";
                flag = 0;
                for (int j = 2; j >= 0; j--)
                {
                    if (allcity[i].red->weapons[j].num != 0)
                    {
                        flag = 1;

                        if (j == 0)
                        {
                            if (allcity[i].red->forcew[j] >= 1)
                            {
                                cout << allcity[i].red->weapons[j].name;
                                cout << "(" << allcity[i].red->forcew[j] << ")";
                            }
                        }
                        if (j == 1)
                        {
                            cout << allcity[i].red->weapons[j].name;
                            if (allcity[i].red->weapons[j - 1].num != 0)
                            {
                                cout << ",";
                            }
                        }
                        if (j == 2)
                        {
                            cout << allcity[i].red->weapons[j].name;
                            cout << "(" << allcity[i].red->weapons[j].wornarrow << ")";
                            if (allcity[i].red->weapons[j - 1].num != 0 || allcity[i].red->weapons[j - 2].num != 0)
                            {
                                cout << ",";
                            }
                        }
                    }
                }
                if (flag == 0)
                {
                    cout << "no weapon" << endl;
                }
                else
                {
                    cout << endl;
                }
            }
        }
        else
        {
            for (int i = 1; i <= 2; i++)
            {
                int flag = 0;
                if (bluebase[i].red)
                {
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " red " << bluebase[i].red->type << " " << bluebase[i].red->id << " has ";
                    flag = 0;
                    for (int j = 2; j >= 0; j--)
                    {
                        if (bluebase[i].red->weapons[j].num != 0)
                        {
                            flag = 1;

                            if (j == 0)
                            {
                                if (allcity[i].blue->forcew[j] >= 1)
                                {
                                    cout << bluebase[i].red->weapons[j].name;
                                    cout << "(" << bluebase[i].red->forcew[j] << ")";
                                }
                            }

                            if (j == 1)
                            {
                                cout << bluebase[i].red->weapons[j].name;
                                if (bluebase[i].red->weapons[j - 1].num != 0)
                                {
                                    cout << ",";
                                }
                            }
                            if (j == 2)
                            {
                                cout << bluebase[i].red->weapons[j].name;
                                cout << "(" << bluebase[i].red->weapons[j].wornarrow << ")";
                                if (bluebase[i].red->weapons[j - 1].num != 0 || bluebase[i].red->weapons[j - 2].num != 0)
                                {
                                    cout << ",";
                                }
                            }
                        }
                    }
                    if (flag == 0)
                    {
                        cout << "no weapon" << endl;
                    }
                    else
                    {
                        cout << endl;
                    }
                }
            }
        }
    }
    for (int i = 0; i <= N; i++)
    {
        if (i >= 1 && i <= N)
        {
            int flag = 0;
            if (allcity[i].blue)
            {
                cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << allcity[i].blue->type << " " << allcity[i].blue->id << " has ";
                flag = 0;
                for (int j = 2; j >= 0; j--)
                {
                    if (allcity[i].blue->weapons[j].num != 0)
                    {
                        flag = 1;
                        cout << allcity[i].blue->weapons[j].name;
                        if (j == 0)
                        {
                            cout << "(" << allcity[i].blue->forcew[j] << ")";

                        }
                        if (j == 1)
                        {
                            if (allcity[i].blue->weapons[j - 1].num != 0)
                            {
                                cout << ",";
                            }
                        }
                        if (j == 2)
                        {
                            cout << "(" << allcity[i].blue->weapons[j].wornarrow << ")";
                            if (allcity[i].blue->weapons[j - 1].num != 0 || allcity[i].blue->weapons[j - 2].num != 0)
                            {
                                cout << ",";
                            }
                        }
                    }
                }
                if (flag == 0)
                {
                    cout << "no weapon" << endl;
                }
                else
                {
                    cout << endl;
                }
            }
        }
        else
        {
            for (int i = 1; i <= 2; i++)
            {
                int flag = 0;
                if (redbase[i].blue)
                {
                    cout << setfill('0') << setw(3) << hour << ":" << setfill('0') << setw(2) << minute << " blue " << redbase[i].blue->type << " " << redbase[i].blue->id << " has ";
                    flag = 0;
                    for (int j = 2; j >= 0; j--)
                    {
                        if (redbase[i].blue->weapons[j].num != 0)
                        {
                            flag = 1;
                            cout << redbase[i].blue->weapons[j].name;
                            if (j == 0)
                            {
                                cout << "(" << redbase[i].blue->forcew[j] << ")";

                            }
                            if (j == 1)
                            {
                                if (redbase[i].blue->weapons[j - 1].num != 0)
                                {
                                    cout << ",";
                                }
                            }
                            if (j == 2)
                            {
                                cout << "(" << redbase[i].blue->weapons[j].wornarrow << ")";
                                if (redbase[i].blue->weapons[j - 1].num != 0 || redbase[i].blue->weapons[j - 2].num != 0)
                                {
                                    cout << ",";
                                }
                            }
                        }
                    }
                    if (flag == 0)
                    {
                        cout << "no weapon" << endl;
                    }
                    else
                    {
                        cout << endl;
                    }
                }
            }
        }
    }
}
int main()
{
    int n;
    cin >> n;
    lineset();
    for (int c = 1; c <= n; c++) {
        for (int i = 1; i <= N; i++)
        {
            citystr[i] = 0;
        }
        BLUE = 0;
        RED = 0;
        int a = 1;
        init();
        mem();
        for (int i = 1; i <= N; i++)
        {
            for (int i = 1; i <= N; i++)
            {
                allcity[i].redwin = 0;
                allcity[i].bluewin = 0;
                allcity[i].redflag = false;
                allcity[i].blueflag = false;
                allcity[i].redarrowmatk = false;
                allcity[i].bluearrowmark = false;
                allcity[i].redif = false;
                allcity[i].blueif = false;
            }
        }
        printf("Case %d:\n", c);
        while (1) {
            for (int i = 1; i <= N; i++)
            {
                allcity[i].bluearrowmark = false;
                allcity[i].redarrowmatk = false;
                allcity[i].redif = false;
                allcity[i].blueif = false;
            }

            minute = 0;
            if (hour == _hour && minute > _minute)
                break;
            createwarriors();

            minute = 5;
            if (hour == _hour && minute > _minute)
                break;
            lionsescape();

            minute = 10;
            if (hour == _hour && minute > _minute)
                break;
            marching();
            if (BLUE == 2 || RED == 2)
                break;

            minute = 20;
            if (hour == _hour && minute > _minute)
                break;
            productstr();

            minute = 30;
            if (hour == _hour && minute > _minute)
                break;
            aloneget();

            minute = 35;
            if (hour == _hour && minute > _minute)
                break;
            shoot();

            minute = 38;
            if (hour == _hour && minute > _minute)
                break;
            explode();

            minute = 40;
            if (hour == _hour && minute > _minute)
                break;
            activeattack();
            award();
            geteletments();

            minute = 50;
            if (hour == _hour && minute > _minute)
                break;
            reportsource();

            minute = 55;
            if (hour == _hour && minute > _minute)
                break;
            reportwaror();
            hour++;
        }
    }

    system("pause");
    return 0;
}