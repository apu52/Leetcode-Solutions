class Solution {
    public int[] sortByBits(int[] arr) {
        Integer[] wrappedArr = Arrays.stream(arr).boxed().toArray(Integer[]::new);
        Arrays.sort(wrappedArr, (a, b) -> Integer.bitCount(a) == Integer.bitCount(b) ? a - b : Integer.bitCount(a) - Integer.bitCount(b));
        return Arrays.stream(wrappedArr).mapToInt(Integer::intValue).toArray();
    }
}
