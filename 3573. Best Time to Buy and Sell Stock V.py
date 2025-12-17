class Solution {
public:
    long long maximumProfit(vector<int>& prices, int k) {
        int n = prices.size();
        vector memo(n, vector<array<long long, 3>>(k + 1, {-1, -1, -1}));
        auto dfs = [&](this auto&& dfs, int i, int j, int end_state) -> long long {
            if (j < 0) {
                return LLONG_MIN / 2; 
            }
            if (i < 0) {
                return end_state ? LLONG_MIN / 2 : 0;
            }
            long long& res = memo[i][j][end_state]; 
            if (res != -1) { 
                return res;
            }
            int p = prices[i];
            if (end_state == 0) {
                return res = max({dfs(i - 1, j, 0), dfs(i - 1, j, 1) + p, dfs(i - 1, j, 2) - p});
            }
            if (end_state == 1) {
                return res = max(dfs(i - 1, j, 1), dfs(i - 1, j - 1, 0) - p);
            }
            return res = max(dfs(i - 1, j, 2), dfs(i - 1, j - 1, 0) + p);
        };
        return dfs(n - 1, k, 0);
    }
};
