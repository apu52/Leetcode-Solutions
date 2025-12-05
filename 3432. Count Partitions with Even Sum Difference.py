class Solution:
    def countPartitions(self, nums: List[int]) -> int:
        # Initialize left and right partition sums
        # Left starts empty (sum = 0), right contains all elements
        left_sum = 0
        right_sum = sum(nums)
      
        # Counter for valid partitions
        partition_count = 0
      
        # Iterate through all possible partition points (except the last element)
        # We need at least one element in the right partition
        for num in nums[:-1]:
            # Move current element from right partition to left partition
            left_sum += num
            right_sum -= num
          
            # Check if the difference between partitions is even
            # If (left_sum - right_sum) is even, increment counter
            partition_count += (left_sum - right_sum) % 2 == 0
      
        return partition_count
