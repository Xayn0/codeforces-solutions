#include <bits\stdc++.h>
#define ll long long
using namespace std;
ll a[100005];
int main()
{
    ll t,n, ans = -1;
    cin >> t;
    while (t--)
    {
        bool o = false;
        cin >> n;
        for (ll i = 0; i < n ; i++)
            cin >> a[i];
        for (ll  i = 2; i < i+1; i++)
        {
            if(o == true)
                break;
            for (ll j = 0; j < n ; j++)
            {
                if(__gcd(a[j],i ) == 1)
                {
                    ans = i;
                    o = true;
                    break;
                }

            }
        }
        cout << ans << "\n";

    }



    return 0;
}
