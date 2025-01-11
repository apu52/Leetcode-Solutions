class Solution:
  def canConstruct(self, s: str, k: int) -> bool:

    return sum(freq & 1
               for freq in collections.Counter(s).values()) <= k <= len(s)
