from typing import List
from collections import Counter

class Solution:
    def specialTriplets(self, nums: List[int]) -> int:
        # Initialize counters for elements to the left and right of current position
        left_counter = Counter()  # Tracks frequency of elements seen so far (left side)
        right_counter = Counter(nums)  # Initially contains all elements (right side)
      
        # Initialize result and modulo constant
        result = 0
        MOD = 10**9 + 7
      
        # Iterate through each element as the middle element of a potential triplet
        for current_num in nums:
            # Remove current element from right counter (moving it from right to current position)
            right_counter[current_num] -= 1
          
            # Count triplets where current_num is the middle element
            # Looking for pattern: left_element * 2 = current_num and current_num * 2 = right_element
            # This means: left_element = current_num * 2 and right_element = current_num * 2
            # So we're counting triplets of form (x*2, x, x*2)
            double_value = current_num * 2
            triplet_count = (left_counter[double_value] * right_counter[double_value]) % MOD
            result = (result + triplet_count) % MOD
          
            # Add current element to left counter (moving it from current position to left side)
            left_counter[current_num] += 1
      
        return result
