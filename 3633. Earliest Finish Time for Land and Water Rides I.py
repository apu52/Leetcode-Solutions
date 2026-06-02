class Solution:
    def earliestFinishTime(
        self,
        landStartTime: List[int],
        landDuration: List[int],
        waterStartTime: List[int],
        waterDuration: List[int],
    ) -> int:
        def calculate_finish_time(
            first_stage_start: List[int],
            first_stage_duration: List[int],
            second_stage_start: List[int],
            second_stage_duration: List[int]
        ) -> int:
            """
            Calculate the minimum finish time when completing first stage then second stage.

            Args:
                first_stage_start: Start times for first stage activities
                first_stage_duration: Durations for first stage activities
                second_stage_start: Start times for second stage activities
                second_stage_duration: Durations for second stage activities

            Returns:
                Minimum finish time for completing both stages
            """
            # Find the earliest possible completion time of the first stage
            # by choosing the activity with minimum (start_time + duration)
            min_first_stage_end = min(
                start + duration
                for start, duration in zip(first_stage_start, first_stage_duration)
            )

            # For the second stage, we can start each activity at the maximum of:
            # - its own start time
            # - the completion time of the first stage
            # Then find the minimum total completion time
            min_total_time = min(
                max(start, min_first_stage_end) + duration
                for start, duration in zip(second_stage_start, second_stage_duration)
            )

            return min_total_time

        # Try both orderings: land first then water, or water first then land
        land_then_water = calculate_finish_time(
            landStartTime, landDuration,
            waterStartTime, waterDuration
        )
        water_then_land = calculate_finish_time(
            waterStartTime, waterDuration,
            landStartTime, landDuration
        )

        # Return the minimum of both orderings
        return min(land_then_water, water_then_land)
