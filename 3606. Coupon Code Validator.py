class Solution:
    def validateCoupons(
        self, code: List[str], businessLine: List[str], isActive: List[bool]
    ) -> List[str]:
        """
        Validates and returns sorted coupon codes based on specific criteria.
      
        Args:
            code: List of coupon codes to validate
            businessLine: List of business lines corresponding to each coupon
            isActive: List of boolean flags indicating if each coupon is active
          
        Returns:
            List of valid coupon codes sorted by business line and then by code
        """
      
        def is_valid_code(coupon_code: str) -> bool:
            """
            Checks if a coupon code contains only alphanumeric characters and underscores.
          
            Args:
                coupon_code: The coupon code string to validate
              
            Returns:
                True if the code is valid, False otherwise
            """
            # Empty strings are invalid
            if not coupon_code:
                return False
          
            # Check each character is alphanumeric or underscore
            for char in coupon_code:
                if not (char.isalpha() or char.isdigit() or char == "_"):
                    return False
          
            return True
      
        # Define valid business lines
        valid_business_lines = {"electronics", "grocery", "pharmacy", "restaurant"}
      
        # Collect indices of valid coupons
        valid_indices = []
      
        # Iterate through all coupons with their index
        for index, (coupon_code, business, is_active_flag) in enumerate(
            zip(code, businessLine, isActive)
        ):
            # Check all validation criteria:
            # 1. Coupon must be active
            # 2. Business line must be in the valid set
            # 3. Coupon code must pass character validation
            if (is_active_flag and 
                business in valid_business_lines and 
                is_valid_code(coupon_code)):
                valid_indices.append(index)
      
        # Sort indices by business line first, then by coupon code
        valid_indices.sort(key=lambda i: (businessLine[i], code[i]))
      
        # Return the sorted list of valid coupon codes
        return [code[i] for i in valid_indices]
