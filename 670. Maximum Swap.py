class Solution:
    def maximumSwap(self, num: int) -> int:
        # Convert the number to a list of its digits in string form.
        digits = list(str(num))
        # Get the length of the list of digits.
        length = len(digits)
        # Create a list to keep track of the indices of the digits
        # that should be considered for swapping.
        max_digit_indices = list(range(length))
      
        # Populate the max_digit_indices list with the index of the maximum digit
        # from the current position to the end of the list.
        for i in range(length - 2, -1, -1):
            # If the current digit is less than or equal to the maximum digit found
            # to its right, update the max_digit_indices for the current position.
            if digits[i] <= digits[max_digit_indices[i + 1]]:
                max_digit_indices[i] = max_digit_indices[i + 1]
      
        # Loop through each digit to find the first instance where a swap would
        # increase the value of the number. Swap and break the loop.
        for i in range(length):
            max_index = max_digit_indices[i]
            # If the current digit is smaller than the maximum digit to its right,
            # swap the two digits.
            if digits[i] < digits[max_index]:
                # Swap the current digit with the maximum digit found.
                digits[i], digits[max_index] = digits[max_index], digits[i]
                # Only one swap is needed, so break after swapping.
                break
      
        # Convert the list of digits back to a string and then to an integer.
        return int(''.join(digits))
