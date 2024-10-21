class Solution {
public:
    int maxUniqueSplit(string s) {
        unordered_set<string> used;
        return backtrack(s, 0, used);
    }
    
    int backtrack(const string& s, int start, unordered_set<string>& used) {
        if (start == s.length()) {
            return 0;
        }
        
        int maxSplit = 0;
        
        string current = "";
        for (int i = start; i < s.length(); ++i) {
            current += s[i];
            if (used.find(current) == used.end()) {
                used.insert(current);
                maxSplit = max(maxSplit, 1 + backtrack(s, i + 1, used));
                used.erase(current);
            }
        }
        
        return maxSplit;
    }
};
