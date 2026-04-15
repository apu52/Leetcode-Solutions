class Solution:
    def closestTarget(self, words: list[str], target: str, startIndex: int) -> int:
        n = len(words)

        for i in range(n):
            if words[(startIndex + i) % n] == target:
                return i
            if words[(startIndex - i + n) % n] == target:
                return i

        return -1
