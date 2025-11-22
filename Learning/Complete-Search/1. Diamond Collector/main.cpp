
#include <bits/stdc++.h>
#include <fstream>
using namespace std;
#define ll long long
int a[1003];
int main()
{
    ifstream fin("diamond.in");
    ofstream fout ("diamond.out");

    int n, k, sol = 0, ans = 0;
    fin >> n >> k;
    for (int i = 0; i < n; i++)
        fin >> a[i];
    sort(a, a + n);
    for (int i = 0; i < n; i++)
    {
        sol = 0;
        for (int j = i; j < n; j++)
            if (((abs(a[i] - a[j])) <= k))
            {
                sol ++;
                ans = max(ans, sol);
            }
    }

    fout << ans;
}
