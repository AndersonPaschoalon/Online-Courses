/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>


int bin_search(int* array, int len, int target){
    int left = 0;
    int right = len -1;
    int mid = (left + right)/2;
    int result = -1;
    while(left <= right){
        
        if (array[mid] == target){
            result = mid;
            break;
        }
        else if (array[mid] < target){
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
        mid = (left + right)/2;
    }
    return result;
}

int bin_search_lower(int* array, int len, int target){
    int left = 0;
    int right = len -1;
    int mid = (left + right)/2;
    int result = -1;
    while(left <= right){
        
        if (array[mid] == target){
            result = mid;
            right = mid - 1;
            //result = mid;
            //break;
        }
        else if (array[mid] < target){
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
        mid = (left + right)/2;
    }
    return result;
}

int bin_search_upper(int* array, int len, int target){
    int left = 0;
    int right = len -1;
    int mid = (left + right)/2;
    int result = -1;
    while(left <= right){
        
        if (array[mid] == target){
            result = mid;
            left = mid + 1;
        }
        else if (array[mid] < target){
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
        mid = (left + right)/2;
    }
    return result;
}

void print_array(int* array, int len){
    printf("[");
    for(int i = 0; i < len; i++){
        printf("%d ", array[i]);
    }
    printf("]\n");
}




int main()
{
    int array[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 11, 12, 13};
    int array_len = sizeof(array)/sizeof(int);
    int target = 8;
    print_array(array, array_len);
    printf("pos: %d\n", bin_search(array, array_len, target));
    printf("pos_lower: %d\n", bin_search_lower(array, array_len, 10));
    printf("pos_upper: %d\n", bin_search_upper(array, array_len, 10));
    
    return 0;
}





