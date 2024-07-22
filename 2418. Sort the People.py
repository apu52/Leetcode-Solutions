from typing import List

class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        # This method sorts the people based on descending order of their heights. 
        # It then returns a list of names of the people sorted by their heights.

        # Generate an index list that matches the indexes of the heights list.
        indices = list(range(len(heights)))

        # Sort the indices list based on descending values of heights.
        # The lambda function returns the negated height value for each index, sorting in descending order.
        indices.sort(key=lambda i: -heights[i])

        # Map the sorted indices to their corresponding names.
        # This results in a list of names ordered by descending height.
        sorted_names = [names[i] for i in indices]

        # Return the list of sorted names.
        return sorted_names
