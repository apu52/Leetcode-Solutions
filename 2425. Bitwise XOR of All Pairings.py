class Solution:
  def xorAllNums(self, nums1: list[int], nums2: list[int]) -> int:
    xors1 = functools.reduce(operator.xor, nums1)
    xors2 = functools.reduce(operator.xor, nums2)
    
    
    return (len(nums1) % 2 * xors2) ^ (len(nums2) % 2 * xors1)
        
