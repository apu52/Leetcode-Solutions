class Solution:
  def canSortArray(self, nums: list[int]) -> int:

    prevSetBits = 0
    prevMax = -math.inf  
    currMax = -math.inf  
    currMin = math.inf   

    for num in nums:
      setBits = num.bit_count()
      if setBits != prevSetBits:  
        if prevMax > currMin:
          return False
        prevSetBits = setBits
        prevMax = currMax
        currMax = num
        currMin = num
      else:  
        currMax = max(currMax, num)
        currMin = min(currMin, num)

    return prevMax <= currMin
