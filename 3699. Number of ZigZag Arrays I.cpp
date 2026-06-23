class Solution {
public:
    const int MOD = 1e9 + 7;

    int zigZagArrays(int n, int l, int r) {
        int m = r - l + 1;  // range size
        // dp arrays: up[i][val], down[i][val]
        vector<vector<int>> up(n + 1, vector<int>(m, 0));
        vector<vector<int>> down(n + 1, vector<int>(m, 0));

        // Base case: arrays of length 2
        for (int x = 0; x < m; x++) {
            for (int y = 0; y < m; y++) {
                if (x == y) continue;
                if (x < y) up[2][y] = (up[2][y] + 1) % MOD;
                else down[2][y] = (down[2][y] + 1) % MOD;
            }
        }

        // Build DP for lengths 3..n
        for (int i = 3; i <= n; i++) {
            // prefix sums for fast range queries
            vector<int> prefUp(m + 1, 0), prefDown(m + 1, 0);

            for (int v = 0; v < m; v++) {
                prefUp[v + 1] = (prefUp[v] + up[i - 1][v]) % MOD;
                prefDown[v + 1] = (prefDown[v] + down[i - 1][v]) % MOD;
            }

            for (int y = 0; y < m; y++) {
                // up[i][y] = sum of down[i-1][x] for x < y
                up[i][y] = prefDown[y];

                // down[i][y] = sum of up[i-1][x] for x > y
                down[i][y] = ((prefUp[m] - prefUp[y + 1]) % MOD + MOD) % MOD;
            }
        }

        long long ans = 0;
        if (n == 1) {
            // Single element arrays are always valid
            ans = m;
        } else {
            for (int y = 0; y < m; y++) {
                ans = (ans + up[n][y] + down[n][y]) % MOD;
            }
        }

        return ans;
    }
};
