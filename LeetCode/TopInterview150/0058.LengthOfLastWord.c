/**
58. Length of Last Word
Solved
Easy
Topics
premium lock iconCompanies

Given a string s consisting of words and spaces, return the length of the last word in the string.

A word is a maximal

consisting of non-space characters only.

 

Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.

Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.

Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.

Constraints:

    1 <= s.length <= 104
    s consists of only English letters and spaces ' '.
    There will be at least one word in s.

*/

int lengthOfLastWord(char* s) {
    int len = strlen(s);
    int lastLen = 0;
    int started = false;
    for(int i = len - 1; i >= 0; i--){
        if ((s[i] == ' ') && (started == false)){
            continue;
        }
        
        if (s[i] != ' '){
            started = true;
            lastLen++;
        }
        if (started == true && s[i] == ' '){
            break;
        }
    }
    return lastLen;
}