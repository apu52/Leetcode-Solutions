class Solution:
    def countOdds(self, low: int, high: int) -> int:
        """
        Count the number of odd integers in the inclusive range [low, high].
      
        The algorithm works by calculating how many odd numbers exist from 0 up to each bound.
        - For any integer n, there are (n+1)//2 odd numbers in range [1, n]
        - Right shift by 1 (>> 1) is equivalent to integer division by 2
        - (high + 1) >> 1 gives count of odds from 1 to high
        - low >> 1 gives count of odds from 1 to low-1
        - The difference gives odds in range [low, high]
      
        Args:
            low: The lower bound of the range (inclusive)
            high: The upper bound of the range (inclusive)
          
        Returns:
            The count of odd integers in the range [low, high]
        """
        # Calculate number of odd integers from 1 to high
        odds_up_to_high = (high + 1) >> 1
      
        # Calculate number of odd integers from 1 to low-1
        odds_before_low = low >> 1
      
        # Return the difference to get odds in [low, high]
        return odds_up_to_high - odds_before_low
