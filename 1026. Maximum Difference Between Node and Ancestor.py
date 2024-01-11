class Solution:
    def maxAncestorDiff(self, root: TreeNode) -> int:

        self.res = 0
        self.helper(root, root.val, root.val)
        return self.res

    def helper(self, root, Min, Max):

        if not root:
            return

        Max = max(Max, root.val)
        Min = min(Min, root.val)

        self.res = max(self.res, Max - Min)

        self.helper(root.left, Min, Max)
        self.helper(root.right, Min, Max)
