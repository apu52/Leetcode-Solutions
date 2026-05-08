
class Solution:
    def minJumps(self, nums):
        n = len(nums)

        MAXV = max(nums) + 1
        spf = list(range(MAXV))

        for i in range(2, isqrt(MAXV) + 1):
            if spf[i] == i:
                for j in range(i * i, MAXV, i):
                    if spf[j] == j:
                        spf[j] = i

        def is_prime(x):
            return x > 1 and spf[x] == x

        divisible = defaultdict(list)

        for i, val in enumerate(nums):
            x = val
            factors = set()

            while x > 1:
                p = spf[x]
                factors.add(p)

                while x % p == 0:
                    x //= p

            for p in factors:
                divisible[p].append(i)

        q = deque([0])
        dist = [-1] * n
        dist[0] = 0

        used_prime = set()

        while q:
            i = q.popleft()

            if i == n - 1:
                return dist[i]

            for ni in (i - 1, i + 1):
                if 0 <= ni < n and dist[ni] == -1:
                    dist[ni] = dist[i] + 1
                    q.append(ni)

            val = nums[i]

            if is_prime(val) and val not in used_prime:
                for ni in divisible[val]:
                    if dist[ni] == -1:
                        dist[ni] = dist[i] + 1
                        q.append(ni)

                used_prime.add(val)

        return -1
