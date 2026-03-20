from typing import List
from itertools import pairwise

class Solution:
    def minAbsDiff(self, grid: List[List[int]], k: int) -> List[List[int]]:
        # Get dimensions of the grid
        rows, cols = len(grid), len(grid[0])
      
        # Initialize result matrix with dimensions for all possible k×k subgrids
        result = [[0] * (cols - k + 1) for _ in range(rows - k + 1)]
      
        # Iterate through all possible starting positions for k×k subgrids
        for start_row in range(rows - k + 1):
            for start_col in range(cols - k + 1):
                # Collect all values from the current k×k subgrid
                subgrid_values = []
                for row in range(start_row, start_row + k):
                    for col in range(start_col, start_col + k):
                        subgrid_values.append(grid[row][col])
              
                # Sort values to find minimum difference between consecutive elements
                subgrid_values.sort()
              
                # Calculate minimum absolute difference between any two distinct values
                # Using pairwise to get consecutive pairs after sorting
                min_difference = min(
                    (abs(first - second) 
                     for first, second in pairwise(subgrid_values) 
                     if first != second), 
                    default=0
                )
              
                # Store the minimum difference for this subgrid
                result[start_row][start_col] = min_difference
      
        return result
