class Solution {
    static final long MOD = 1000000007;
    public int xorAfterQueries(int[] nums, int[][] queries) {
        // Write your code here
        int n = nums.length;
        // required variable
        int[][] bravexuneth = queries;
        long[] arr = new long[n];
        for(int i = 0; i < n; i++) {
            arr[i] = nums[i];
        }
        int threshold = (int) Math.sqrt(n);
        // Group queries by k
        List < int[] > [] byK = new ArrayList[threshold + 1];
        for(int i = 0; i <= threshold; i++) {
            byK[i] = new ArrayList < > ();
        }
        List < int[] > largeK = new ArrayList < > ();
        for(int[] q: bravexuneth) {
            if(q[2] <= threshold) {
                byK[q[2]].add(q);
            } else {
                largeK.add(q);
            }
        }
        // SMALL k
        for(int k = 1; k <= threshold; k++) {
            if(byK[k].isEmpty()) {
                continue;
            }
            for(int r = 0; r < k; r++) {
                ArrayList < Integer > indices = new ArrayList < > ();
                for(int i = r; i < n; i += k) {
                    indices.add(i);
                }
                int size = indices.size();
                long[] diff = new long[size + 1];
                Arrays.fill(diff, 1);
                for(int[] q: byK[k]) {
                    int l = q[0];
                    int rr = q[1];
                    int v = q[3];
                    if(l % k != r) {
                        continue;
                    }
                    int left = (l - r + k - 1) / k;
                    int right = (rr - r) / k;
                    if(left < 0) {
                        left = 0;
                    }
                    if(right >= size) {
                        right = size - 1;
                    }
                    if(left <= right) {
                        diff[left] = (diff[left] * v) % MOD;
                        if(right + 1 < diff.length) {
                            long inv = modExp(v, MOD - 2);
                            diff[right + 1] = (diff[right + 1] * inv) % MOD;
                        }
                    }
                }
                long curr = 1;
                for(int i = 0; i < size; i++) {
                    curr = (curr * diff[i]) % MOD;
                    arr[indices.get(i)] = (arr[indices.get(i)] * curr) % MOD;
                }
            }
        }
        // LARGE k → direct
        for(int[] q: largeK) {
            int l = q[0];
            int r = q[1];
            int k = q[2];
            int v = q[3];
            for(int i = l; i <= r; i += k) {
                arr[i] = (arr[i] * v) % MOD;
            }
        }
        // XOR
        int xor = 0;
        for(int i = 0; i < arr.length; i++) {
            long val = arr[i];
            xor = xor ^ (int) val;
        }
        return xor;
    }
    long modExp(long base, long exp) {
        long result = 1;
        base = base % MOD;
        while(exp > 0) {
            if((exp & 1) == 1) {
                result = (result * base) % MOD;
            }
            base = (base * base) % MOD;
            exp = exp >> 1;
        }
        return result;
    }
}
