/*
35. Search Insert Position
Solved
Easy
Topics
premium lock iconCompanies

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

 

Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2

Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1

Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4

*/

int searchInsert(int* nums, int numsSize, int target) {
    int left = 0;
    int right = numsSize - 1;
    int med = (left + right)/2;
    while(true){

        if(nums[med] == target)
            return med;
        
        if (nums[med] < target)
            left = med + 1;
        else // nums[med] > target
            right = med - 1;
        
        med = (left + right)/2;

        if (left > right){
            // return med + 1;
            return left;
        }
    }
}


int main()
{
    int nums1[4] = {1,3,5,6};
    int nums2[4] = {1,3,5,6};
    int nums3[4] = {1,3,5,6};
    int target1 = 5;
    int target2 = 2;
    int target3 = 7;
    int exp1 = 2;
    int exp2 = 1;
    int exp3 = 4;
    printf("resp: %d, exp:\n", searchInsert(nums1, sizeof(nums)/sizeof(int), target1), exp1);
    printf("resp: %d, exp:\n", searchInsert(nums2, sizeof(nums)/sizeof(int), target2), exp2);
    printf("resp: %d, exp:\n", searchInsert(nums3, sizeof(nums)/sizeof(int), target3), exp3);

    return 0;
}












