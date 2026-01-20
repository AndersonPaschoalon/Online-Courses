/**
169. Majority Element
Solved
Easy
Topics
premium lock iconCompanies

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

 

Example 1:

Input: nums = [3,2,3]
Output: 3

Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2

 

Constraints:

    n == nums.length
    1 <= n <= 5 * 104
    -109 <= nums[i] <= 109
    The input is generated such that a majority element will exist in the array.

 
Follow-up: Could you solve the problem in linear time and in O(1) space?
 */
int alreadyTested(int* nums, int numsSize, int currentPos){
    // Testa de o candidato na posicao atual do array currentPos
    // já foi testado como candidado anteriormente verificando se ele 
    // existia nos elements com indice <= currentPost
    if (currentPos >= numsSize){
        return 0;
    }
    for(int i = 0; i < currentPos; i++){
        if (nums[i] == nums[currentPos])
            return 1;
    }
    return 0;
}

int majorityElement(int* nums, int numsSize) {
    // Intuição: como o majorityElement sempre existe, isso significa que a soma da contagem deste elemento
    // com a dos itens que não são esse elemento sempre será maior ou igual a zero. 
    int candCount = 0;
    int cand = 0;
    for(int i = 0; i < numsSize; i++){
        cand = nums[i];
        if (alreadyTested(nums, numsSize, i) == 1){
            continue;
        }
        for(int j = 0; j < numsSize; j++){
            if(cand == nums[j]){
                candCount++;
            }
            else{
                candCount--;
            }
        }
        if(candCount >= 0){
            return cand;
        }
        candCount = 0;
    }
    return 0;
}

