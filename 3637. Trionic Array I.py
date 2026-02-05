class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        """
        Check if the array follows a trionic pattern:
        1. First phase: strictly increasing
        2. Second phase: strictly decreasing  
        3. Third phase: strictly increasing
        Each phase must contain at least one transition.
        """
        n = len(nums)
      
        # Phase 1: Find the end of the first increasing sequence
        first_peak_index = 0
        while first_peak_index < n - 2 and nums[first_peak_index] < nums[first_peak_index + 1]:
            first_peak_index += 1
      
        # If no increasing phase found at the start, pattern is invalid
        if first_peak_index == 0:
            return False
      
        # Phase 2: Find the end of the decreasing sequence (valley point)
        valley_index = first_peak_index
        while valley_index < n - 1 and nums[valley_index] > nums[valley_index + 1]:
            valley_index += 1
      
        # Check if decreasing phase exists and doesn't reach the end
        # valley_index == first_peak_index means no decreasing phase
        # valley_index == n - 1 means no room for final increasing phase
        if valley_index == first_peak_index or valley_index == n - 1:
            return False
      
        # Phase 3: Find the end of the final increasing sequence
        final_index = valley_index
        while final_index < n - 1 and nums[final_index] < nums[final_index + 1]:
            final_index += 1
      
        # Valid trionic pattern if the final increasing phase reaches the end
        return final_index == n - 1
