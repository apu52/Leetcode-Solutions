class Solution {
    public String mapWordWeights(String[] words, int[] weights) {

        HashMap<Character,Integer> weightMap = new HashMap<>();
        HashMap<Integer,Character> reverseMap = new HashMap<>();

        for(int i = 0; i < 26; i++) {

            char letter = (char)('a' + i);
            char reverseLetter = (char)('z' - i);

            weightMap.put(letter, weights[i]);
            reverseMap.put(i, reverseLetter);
        }

        StringBuilder answer = new StringBuilder();

        for(String word : words) {

            int sum = 0;

            for(char ch : word.toCharArray()) {
                sum += weightMap.get(ch);
            }

            answer.append(reverseMap.get(sum % 26));
        }

        return answer.toString();
    }
}
