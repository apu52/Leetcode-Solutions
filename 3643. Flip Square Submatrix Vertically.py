class Solution:
    def reverseSubmatrix(
        self, grid: List[List[int]], x: int, y: int, k: int
    ) -> List[List[int]]:

        # Iterate through the first half of the submatrix rows
        for row_idx in range(x, x + k // 2):
            # Calculate the corresponding row index from the bottom
            # that should be swapped with the current row
            mirror_row_idx = x + k - 1 - (row_idx - x)
          
            # Swap all elements in the current row with the mirror row
            # within the column range [y, y + k)
            for col_idx in range(y, y + k):
                grid[row_idx][col_idx], grid[mirror_row_idx][col_idx] = (
                    grid[mirror_row_idx][col_idx], 
                    grid[row_idx][col_idx]
                )
      
        return grid
