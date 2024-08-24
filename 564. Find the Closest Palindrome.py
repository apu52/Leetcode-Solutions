class Solution:
    def nearestPalindromic(self, n: str) -> str:
        # Convert the string to an integer for numerical operations
        num = int(n)
        num_length = len(n)

        # Initialize a set with the smallest and largest possible palindromes
        # with different digit lengths compared to the input number
        candidates = {
            10**(num_length - 1) - 1,  # Smallest palindrome with one less digit
            10**num_length + 1          # Smallest palindrome with one more digit
        }

        # Find the higher and lower palindromes around the input number
        # 'prefix' is the first half of the input number
        prefix = int(n[:(num_length + 1) // 2])

        # Generate palindromes by varying the prefix by -1, 0, +1
        for i in range(prefix - 1, prefix + 2):
            # For even lengths, use the entire prefix.
            # For odd lengths, exclude the last digit of the prefix.
            j = i if num_length % 2 == 0 else i // 10

            # Append the reverse of 'j' to 'i' to construct the palindrome
            palindrome = i
            while j > 0:
                palindrome = palindrome * 10 + j % 10
                j //= 10

            # Add the constructed palindrome to the candidate set
            candidates.add(palindrome)

        # Remove the original number itself if it's in the set
        candidates.discard(num)

        # Find the closest palindrome to the original number
        closest_palindrome = -1
        for candidate in candidates:
            # Check for the smallest absolute difference
            # If the absolute difference is the same, choose the smaller number
            if (closest_palindrome == -1 or
                abs(candidate - num) < abs(closest_palindrome - num) or
                (abs(candidate - num) == abs(closest_palindrome - num) and candidate < closest_palindrome)):
                closest_palindrome = candidate

        # Convert the closest palindrome back to a string and return
        return str(closest_palindrome)
