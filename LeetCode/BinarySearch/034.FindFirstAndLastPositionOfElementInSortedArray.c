/*

Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

 

Example 1:

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:

Input: nums = [], target = 0
Output: [-1,-1]

 

Constraints:

    0 <= nums.length <= 105
    -109 <= nums[i] <= 109
    nums is a non-decreasing array.
    -109 <= target <= 109



*/

int searchFirstOrLast(int* nums, int numsSize, int target, char searchType);

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* searchRange(int* nums, int numsSize, int target, int* returnSize) {
    int* vetResult = (int*) malloc(sizeof(int)*2);
    *returnSize = 2;
    vetResult[0] = searchFirstOrLast(nums, numsSize, target, 'f');
    if (vetResult[0] == -1){
        vetResult[1] = -1;
    }
    else {
        vetResult[1] = searchFirstOrLast(nums, numsSize, target, 'l');
    }

    return vetResult;
}

// searchType f - first, l - last
int searchFirstOrLast(int* nums, int numsSize, int target, char searchType){
    int left = 0;
    int right = numsSize -1;
    int result = -1;
    int med = 0;
    while(left <= right){
        med = (left + right)/2;
        if (nums[med] == target){
            result = med;
            // continua busca pela pelo lado especificado
            if (searchType == 'f'){
                right = med - 1;
            }
            else {
                left = med + 1;
            }
        }
        else if (nums[med] < target){
            left = med + 1;
        }
        else { // nums[med] > target
            right = med -1;
        }
    }
    return result;
}

