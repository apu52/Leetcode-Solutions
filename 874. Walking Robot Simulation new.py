class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        # Directions represent the movement of the robot: North, East, South, West
        directions = (0, 1, 0, -1, 0)
        # Set of obstacle positions for quick look-up
        obstacle_set = {(x, y) for x, y in obstacles}
        # Initialize the maximum distance squared, direction index, and starting position
        max_distance_squared = direction_index = 0
        position_x = position_y = 0

        # Loop through each command and execute
        for command in commands:
            if command == -2:  # Turn left
                direction_index = (direction_index + 3) % 4
            elif command == -1: # Turn right
                direction_index = (direction_index + 1) % 4
            else:
                # Move the robot forward for the number of steps specified in the command
                for _ in range(command):
                    next_x, next_y = position_x + directions[direction_index], position_y + directions[direction_index + 1]
                    # Check if the new position is an obstacle
                    if (next_x, next_y) in obstacle_set:
                        break  # Stop if there's an obstacle ahead
                    # Update the robot's position
                    position_x, position_y = next_x, next_y
                    # Update the maximum Euclidean distance squared from the origin
                    max_distance_squared = max(max_distance_squared, position_x * position_x + position_y * position_y)
      
        # Return the maximum Euclidean distance squared the robot has been from the origin
        return max_distance_squared
