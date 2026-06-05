class Solution {
public:
    
    struct Node {
        long long waviness;
        long long cnt;
    };

    string s;

    Node dp[17][2][2][11][11];
    bool vis[17][2][2][11][11];
    
    /*
    tight = Are we still equal to N's prefix?
    started = Have we started building a number yet?
    prev2 and prev1 are the last 2 previous digits
    */
    Node dfs(int pos, int tight, int started, int prev2, int prev1) {
        //base case: we have processed all digits
        if (pos == s.size()) {
            return {0, 1};
        }
        //if current state is already solved
        if (vis[pos][tight][started][prev2][prev1]) {
            return dp[pos][tight][started][prev2][prev1];
        }
        // mark this state visited
        vis[pos][tight][started][prev2][prev1] = true;

        long long totalWaviness = 0;
        long long totalCnt = 0;

// if tight =1 then limit will be digit at the pos else limit can be 9
        int limit = tight ? s[pos] - '0' : 9;

        for (int d = 0; d <= limit; d++) {
            //if we were tight and we chose max allowed digit then we ramain tight
            int nextTight = tight && (d == limit);

            if (!started && d == 0) {//skipping leading zeroes
                Node child = dfs(pos + 1,nextTight,0,10,10);

                totalWaviness += child.waviness;
                totalCnt += child.cnt;
            }
            else { //non-leading zero case

                int nPrev2, nPrev1;
                long long add = 0;

                if (!started) {
                    nPrev2 = 10;
                    nPrev1 = d;
                }
                else {

                    if (prev2 != 10) { //checking peak or valley

                        bool peak =(prev1 > prev2 && prev1 > d);
                        bool valley =(prev1 < prev2 && prev1 < d);

                        if (peak || valley) add = 1;
                    }

                    nPrev2 = prev1;
                    nPrev1 = d;
                }

                Node child = dfs(pos + 1,nextTight,1,nPrev2,nPrev1);

                totalWaviness += child.waviness + add * child.cnt;
                totalCnt += child.cnt;
            }
        }

        return dp[pos][tight][started][prev2][prev1] ={totalWaviness, totalCnt};
    }

    long long solve(long long n) {

        if (n <= 0) return 0;

        s = to_string(n);

        memset(vis, 0, sizeof(vis));

        return dfs(0, 1, 0, 10, 10).waviness;
    }

    long long totalWaviness(long long num1, long long num2) {

        return solve(num2) - solve(num1 - 1);
    }
};
