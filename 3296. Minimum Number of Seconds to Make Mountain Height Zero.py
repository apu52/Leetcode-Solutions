from typing import List
from math import sqrt

class Solution:
    def minNumberOfSeconds(self, mountainHeight: int, workerTimes: List[int]) -> int:


        def can_complete_in_time(time_limit: int) -> bool:

            total_height_reduced = 0

            for worker_time in workerTimes:
                # Calculate maximum rounds this worker can complete within time_limit
                # Using the quadratic formula solution for n
                max_rounds = int(sqrt(2 * time_limit / worker_time + 0.25) - 0.5)
                total_height_reduced += max_rounds

            return total_height_reduced >= mountainHeight

        # Binary search using standard template to find minimum valid time
        left, right = 1, 10**16
        first_true_index = -1

        while left <= right:
            mid = (left + right) // 2
            if can_complete_in_time(mid):
                first_true_index = mid
                right = mid - 1  # Found valid time, try smaller
            else:
                left = mid + 1   # Need more time

        return first_true_index
