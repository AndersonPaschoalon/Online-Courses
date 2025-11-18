/*
436. Find Right Interval
Solved
Medium
Topics
premium lock iconCompanies

You are given an array of intervals, where intervals[i] = [starti, endi] and each starti is unique.

The right interval for an interval i is an interval j such that startj >= endi and startj is minimized. Note that i may equal j.

Return an array of right interval indices for each interval i. If no right interval exists for interval i, then put -1 at index i.

 

Example 1:

Input: intervals = [[1,2]]
Output: [-1]
Explanation: There is only one interval in the collection, so it outputs -1.

Example 2:

Input: intervals = [[3,4],[2,3],[1,2]]
Output: [-1,0,1]
Explanation: There is no right interval for [3,4].
The right interval for [2,3] is [3,4] since start0 = 3 is the smallest start that is >= end1 = 3.
The right interval for [1,2] is [2,3] since start1 = 2 is the smallest start that is >= end2 = 2.

Example 3:

Input: intervals = [[1,4],[2,3],[3,4]]
Output: [-1,2,-1]
Explanation: There is no right interval for [1,4] and [3,4].
The right interval for [2,3] is [3,4] since start2 = 3 is the smallest start that is >= end1 = 3.

 

Constraints:

    1 <= intervals.length <= 2 * 104
    intervals[i].length == 2
    -106 <= starti <= endi <= 106
    The start point of each interval is unique.


*/


#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdio.h>


void printIntervals(int** intervals, int intervalsSize, int* intervalsColSize);
int compare(const void *a, const void *b);
int lower_bound(int arr[], int n, int target);

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* findRightInterval(int** intervals, int intervalsSize, int* intervalsColSize, int* returnSize) {
    //printIntervals(intervals, intervalsSize, intervalsColSize);
    int* indexes = (int*)malloc(sizeof(int)*intervalsSize);
    *returnSize = intervalsSize;

    // prepare startj_array
    int i = 0;
    int p1 = 0;
    int p2 = 0;
    int lastPos = 0;
    int* startj_array = (int*)malloc(sizeof(int)*2*intervalsSize); // startj_array[i] = [index, val]
    for (i = 0; i < intervalsSize; i++){
        p1 = i*2;
        p2 = p1 + 1;
        lastPos = intervalsColSize[i] -1;
        startj_array[p1] = i;
        startj_array[p2] = intervals[i][0];
    }
    int startj_array_nelements = intervalsSize;
    qsort (startj_array, startj_array_nelements, sizeof(int)*2, compare);

    int len = 0;
    int endi = 0;
    int pos = 0;
    for(i = 0; i < intervalsSize; i++){
        len = intervalsColSize[i] - 1;
        endi = intervals[i][len];
        pos = lower_bound(startj_array, startj_array_nelements, endi) ;
        if (pos < 0){
            indexes[i] = -1;
        } 
        else{
            indexes[i] = startj_array[pos*2];
        }
    }
    return indexes;
}

int compare(const void *a, const void *b) {
  int* key_val_a = a;
  int* key_val_b = b;
  return key_val_a[1] - key_val_b[1];
}

void printIntervals(int** intervals, int intervalsSize, int* intervalsColSize){
    int i = 0;
    int j = 0;
    for(i = 0; i < intervalsSize; i++){
        printf("Interval[%d]: [", i);
        for(j = 0; j < intervalsColSize[i]; j++){
            printf("%d ", intervals[i][j]);
        }
        printf("]\n");
    }
}

int lower_bound(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    int result = n;  // caso todos sejam menores que target
    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid * 2 + 1] >= target) {
            result = mid;
            right = mid - 1;  // ainda pode haver algo menor à esquerda
        } else {
            left = mid + 1;
        }
    }
    return (result < n) ? result : -1;  // -1 indica "não encontrado"
}


