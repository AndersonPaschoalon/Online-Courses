/**
14. Longest Common Prefix
Solved
Easy
Topics
premium lock iconCompanies

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

 

Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"

Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.

 

Constraints:

    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] consists of only lowercase English letters if it is non-empty.


 */

 
void match_str_fun(char* str1, char* str2, char* match_str, int match_str_len){
    int str1_len = strlen(str1);
    int str2_len = strlen(str2);
    int min_str = (str1_len > str2_len )? str2_len : str1_len;
    // memset(match_str, '\0', match_str_len);
    //match_str[0] = '\0';
    int i = 0;
    for(i = 0; i < min_str; i++){
        if(str1[i] == str2[i]){
            match_str[i] = str1[i];
        }
        else{
            break;
        }
    }
    match_str[i] = '\0';
}

char* longestCommonPrefix(char** strs, int strsSize) {
    char match_str[201];
    memset(match_str, '\0', sizeof(match_str));
    //printf("%d\n", strsSize);
    if(strsSize == 1){
        int len = strlen(strs[0]) + 1;
        memcpy(match_str, strs[0],  len*sizeof(char));
    }
    else{
        for(int i = 1; i < strsSize; i++){
            if(i == 1){
                match_str_fun(strs[0], strs[1], match_str, 201);
            }
            else {
                match_str_fun(match_str, strs[i], match_str, 201);
            }
            //printf("%s\n", match_str);
        }   
    }

    char* out = (char*) malloc(sizeof(char)*201);
    memcpy(out, match_str, 201);
    //printf("match_str:%s\n", match_str);
    //printf("out:%s\n", out);
    return out;
}

