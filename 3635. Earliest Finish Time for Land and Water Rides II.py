from typing import List

class Solution:
    def earliestFinishTime(
        self,
        landStartTime: List[int],
        landDuration: List[int],
        waterStartTime: List[int],
        waterDuration: List[int],
    ) -> int:
        def calculate_finish_time(
            first_start_times: List[int],
            first_durations: List[int],
            second_start_times: List[int],
            second_durations: List[int]
        ) -> int:
            """
            Calculate the minimum finish time when completing first task then second task.

            Args:
                first_start_times: Start times for first set of tasks
                first_durations: Durations for first set of tasks
                second_start_times: Start times for second set of tasks
                second_durations: Durations for second set of tasks

            Returns:
                Minimum possible finish time
            """
            # Find the earliest possible completion time among all first tasks
            min_first_task_end = min(
                start + duration
                for start, duration in zip(first_start_times, first_durations)
            )

            # For each second task, calculate finish time considering:
            # - Must start after first task completes (min_first_task_end)
            # - Must respect the second task's own start time constraint
            # Then find the minimum among all possible second tasks
            return min(
                max(start, min_first_task_end) + duration
                for start, duration in zip(second_start_times, second_durations)
            )

        # Try both orderings: land first then water, or water first then land
        land_then_water = calculate_finish_time(
            landStartTime, landDuration, waterStartTime, waterDuration
        )
        water_then_land = calculate_finish_time(
            waterStartTime, waterDuration, landStartTime, landDuration
        )

        # Return the minimum finish time between both orderings
        return min(land_then_water, water_then_land)
