class Solution:
    def makeFancyString(self, s: str) -> str:
        # Initialize an empty list to store the modified characters of the string
        result = []
      
        # Iterate over each character in the input string
        for char in s:
            # Check if the last two characters in 'result' are the same as the current character
            if len(result) > 1 and result[-1] == result[-2] == char:
                # If true, skip adding the current character to avoid three consecutive identical characters
                continue
            # Otherwise, append the current character to the result list
            result.append(char)
      
        # Join all characters in the result list to form the modified string
        return ''.join(result)
