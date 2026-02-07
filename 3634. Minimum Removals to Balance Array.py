from typing import List
from bisect import bisect_right


class Solution:
    def minRemoval(self, nums: List[int], k: int) -> int:
        # Sort the array to enable binary search
        nums.sort()
      
        # Track the maximum number of elements that can be kept
        max_elements_to_keep = 0
      
        # For each element as the minimum value in a valid subarray
        for i, min_value in enumerate(nums):
            # Find the rightmost position where nums[j] <= k * min_value
            # This gives us the range [i, j) where all elements satisfy
            # min_value <= nums[x] <= k * min_value
            right_bound = bisect_right(nums, k * min_value)
          
            # Update the maximum number of elements we can keep
            # right_bound - i gives the count of valid elements starting from index i
            max_elements_to_keep = max(max_elements_to_keep, right_bound - i)
      
        # Return minimum removals = total elements - maximum elements we can keep
        return len(nums) - max_elements_to_keep
