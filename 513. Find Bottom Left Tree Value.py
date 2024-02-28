from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def findBottomLeftValue(self, root: TreeNode) -> int:
        # Initialize a queue with the root node.
        node_queue = deque([root])
      
        # This will hold the leftmost value as the tree is traversed level by level.
        bottom_left_value = 0
      
        # Perform a level order traversal on the tree.
        while node_queue:
            # At new level's beginning, the first node is the leftmost node.
            bottom_left_value = node_queue[0].val
          
            # Iterate through nodes at the current level.
            for _ in range(len(node_queue)):
                # Pop the node from the front of the queue.
                node = node_queue.popleft()
              
                # If the left child exists, add it to the queue.
                if node.left:
                    node_queue.append(node.left)
                # If the right child exists, add it to the queue.
                if node.right:
                    node_queue.append(node.right)
      
        # Return the bottom left value found during traversal.
        return bottom_left_value
