class Solution:
    def countPermutations(self, complexity: List[int]) -> int:
        # Define modulo for large number handling
        MOD = 10**9 + 7
      
        # Check if all elements after the first are strictly greater than the first element
        # This ensures the first element is the minimum in the array
        for i in range(1, len(complexity)):
            if complexity[i] <= complexity[0]:
                # If any element is not greater than the first, no valid permutations exist
                return 0
      
        # Calculate (n-1)! modulo MOD
        # This represents the number of ways to arrange the remaining n-1 elements
        result = 1
        for i in range(1, len(complexity)):
            result = (result * i) % MOD
      
        return result
