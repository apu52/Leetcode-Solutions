# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def distributeCoins(self, root: Optional[TreeNode]) -> int:
        # Depth-first search (DFS) function to traverse the tree and redistribute coins
        def dfs(node):
            # If the current node is None, we do not need to redistribute any coins
            if node is None:
                return 0
              
            # Recursively redistribute coins for the left and right subtrees
            left_balance = dfs(node.left)
            right_balance = dfs(node.right)
          
            # Use nonlocal to modify the ans variable declared in the parent function's scope
            nonlocal moves_count
            # Increment the total moves by the absolute amount of coins to move from/left child and right child
            moves_count += abs(left_balance) + abs(right_balance)

            # Return the net balance of coins for the current subtree
            # Net balance is the coins to be redistributed, i.e., current node's coin plus left and right balance,
            # and we subtract 1 because the current node should have 1 coin after redistribution
            return left_balance + right_balance + node.val - 1

        # Initialize the moves counter to 0
        moves_count = 0
        # Start DFS from the root to distribute coins and calculate the moves
        dfs(root)
        # Return the total number of moves required to distribute the coins
        return moves_count
