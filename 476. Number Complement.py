class Solution:
    def findComplement(self, num: int) -> int:
        # Calculate the length of the binary representation of the number excluding the '0b' prefix.
        binary_length = len(bin(num)) - 2
      
        # Create a mask with all 1's that is the same length as the binary representation of the number.
        mask = (2 ** binary_length) - 1

        # XOR the number with the mask to flip all the bits and obtain its complement.
        return num ^ mask
