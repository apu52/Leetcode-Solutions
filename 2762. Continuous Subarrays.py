class Solution:
  def continuousSubarrays(self, nums: list[int]) -> int:
    ans = 1  # [nums[0]]
    left = nums[0] - 2
    right = nums[0] + 2
    l = 0


    for r in range(1, len(nums)):
      if left <= nums[r] <= right:
        left = max(left, nums[r] - 2)
        right = min(right, nums[r] + 2)
      else:
    
        left = nums[r] - 2
        right = nums[r] + 2
        l = r
        
        while nums[r] - 2 <= nums[l] <= nums[r] + 2:
          left = max(left, nums[l] - 2)
          right = min(right, nums[l] + 2)
          l -= 1
        l += 1
      
      ans += r - l + 1

    return ans
        
