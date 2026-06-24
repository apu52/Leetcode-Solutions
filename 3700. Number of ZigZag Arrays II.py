class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 10**9 + 7
        m = r - l + 1

        size = 2 * m

        # State:
        # 0..m-1     => U[v] (last move was up, ending at value v)
        # m..2m-1    => D[v] (last move was down, ending at value v)

        T = [[0] * size for _ in range(size)]

        # U'[v] = sum(D[u]) for u < v
        for v in range(m):
            row = v
            for u in range(v):
                T[row][m + u] = 1

        # D'[v] = sum(U[u]) for u > v
        for v in range(m):
            row = m + v
            for u in range(v + 1, m):
                T[row][u] = 1

        def mat_mul(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]

            for i in range(n):
                Ai = A[i]
                Ci = C[i]

                for k in range(n):
                    if Ai[k] == 0:
                        continue

                    aik = Ai[k]
                    Bk = B[k]

                    for j in range(n):
                        if Bk[j]:
                            Ci[j] = (Ci[j] + aik * Bk[j]) % MOD

            return C

        def mat_pow(M, p):
            n = len(M)

            R = [[0] * n for _ in range(n)]
            for i in range(n):
                R[i][i] = 1

            while p:
                if p & 1:
                    R = mat_mul(R, M)

                M = mat_mul(M, M)
                p >>= 1

            return R

        def mat_vec_mul(M, vec):
            n = len(M)
            res = [0] * n

            for i in range(n):
                s = 0
                row = M[i]

                for j in range(n):
                    if row[j]:
                        s += row[j] * vec[j]

                res[i] = s % MOD

            return res

        # Base state for length = 2
        base = [0] * size

        for a in range(m):
            for b in range(m):
                if a == b:
                    continue

                if a < b:
                    base[b] += 1          # U[b]
                else:
                    base[m + b] += 1      # D[b]

        if n == 2:
            return sum(base) % MOD

        P = mat_pow(T, n - 2)
        state = mat_vec_mul(P, base)

        return sum(state) % MOD
