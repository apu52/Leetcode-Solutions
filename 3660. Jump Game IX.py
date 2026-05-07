class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
      
        # Initialize result array with zeros
        ans = [0] * n
      
        # Build prefix maximum array
        # pre_max[i] stores the maximum value from index 0 to i
        pre_max = [nums[0]] * n
        for i in range(1, n):
            pre_max[i] = max(pre_max[i - 1], nums[i])
      
        # Initialize suffix minimum to infinity
        suf_min = float('inf')
      
        # Traverse from right to left to build answer array
        for i in range(n - 1, -1, -1):
           
            if i + 1 < n:
                ans[i] = ans[i + 1] if pre_max[i] > suf_min else pre_max[i]
            else:
                # For the last element, use prefix max if condition fails
                ans[i] = pre_max[i] if pre_max[i] <= suf_min else 0
          
            # Update suffix minimum including current element
            suf_min = min(suf_min, nums[i])
      
        return ans
