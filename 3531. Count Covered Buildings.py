from collections import defaultdict
from typing import List

class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        # Group buildings by their x-coordinate (vertical lines)
        buildings_by_x = defaultdict(list)
        # Group buildings by their y-coordinate (horizontal lines)
        buildings_by_y = defaultdict(list)
      
        # Populate the groupings
        for x_coord, y_coord in buildings:
            buildings_by_x[x_coord].append(y_coord)
            buildings_by_y[y_coord].append(x_coord)
      
        # Sort y-coordinates for each x group (for finding min/max efficiently)
        for x_coord in buildings_by_x:
            buildings_by_x[x_coord].sort()
      
        # Sort x-coordinates for each y group (for finding min/max efficiently)
        for y_coord in buildings_by_y:
            buildings_by_y[y_coord].sort()
      
        covered_count = 0
      
        # Check each building to see if it's covered
        for x_coord, y_coord in buildings:
            # Get all y-coordinates for buildings with same x
            y_coords_at_x = buildings_by_x[x_coord]
            # Get all x-coordinates for buildings with same y
            x_coords_at_y = buildings_by_y[y_coord]
          
            # A building is covered if:
            # 1. There are buildings with same y-coordinate both to its left and right
            # 2. There are buildings with same x-coordinate both above and below it
            if (x_coords_at_y[0] < x_coord < x_coords_at_y[-1] and 
                y_coords_at_x[0] < y_coord < y_coords_at_x[-1]):
                covered_count += 1
      
        return covered_count
