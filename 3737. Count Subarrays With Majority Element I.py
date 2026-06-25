from typing import List

class Solution:
    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)

        pref = [0]
        for x in nums:
            pref.append(pref[-1] + (1 if x == target else -1))

        ans = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if pref[j] > pref[i]:
                    ans += 1

        return ans
