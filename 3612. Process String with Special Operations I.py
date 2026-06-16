class Solution:
    def processStr(self, s: str) -> str:
        """
        Process a string according to special character rules:
        - Alphabetic characters are added to result
        - '*' removes the last character from result (if exists)
        - '#' duplicates the entire current result
        - '%' reverses the current result
      
        Args:
            s: Input string to process
          
        Returns:
            Processed string after applying all operations
        """
        result = []  # List to store characters for efficient manipulation
      
        for char in s:
            if char.isalpha():
                # Add alphabetic character to result
                result.append(char)
            elif char == "*" and result:
                # Remove last character if result is not empty
                result.pop()
            elif char == "#":
                # Duplicate the entire current result
                result.extend(result[:])  # Use slicing to create a copy
            elif char == "%":
                # Reverse the current result in-place
                result.reverse()
      
        # Convert list back to string and return
        return "".join(result)
