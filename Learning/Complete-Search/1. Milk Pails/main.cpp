#include <bits/stdc++.h>
#include <fstream>
#define ll long long
#define ld long double
#define INF 1e9
using namespace std;

int main()
{
//    ifstream fin ("pails.in");
//    ofstream fout("pails.out");
    ll x , y , M , sol = -1;
    cin >> x >> y >> M;
    ll upperX = M / x + 1 , upperY = M / y + 1;
    for (int i = 0; i < upperX ; i++)
        for (int j = 0 ; j < upperY ; j++)
        if(x*i + y*j <= M)
        sol = max(sol ,x*i + y*j );
   cout << sol;


    return 0;
}
