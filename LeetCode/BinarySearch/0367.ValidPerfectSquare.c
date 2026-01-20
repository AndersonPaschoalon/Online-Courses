#include <stdio.h>
#include <stdbool.h>


/*
Given a positive integer num, return true if num is a perfect square or false otherwise.

A perfect square is an integer that is the square of an integer. In other words, it is the product of some integer with itself.

You must not use any built-in library function, such as sqrt.

 

Example 1:

Input: num = 16
Output: true
Explanation: We return true because 4 * 4 = 16 and 4 is an integer.

Example 2:

Input: num = 14
Output: false
Explanation: We return false because 3.742 * 3.742 = 14 and 3.742 is not an integer.

 

Constraints:

    1 <= num <= 231 - 1


*/

bool isPerfectSquare(int num) {

    unsigned long int r = num;
    unsigned long int l = 1;
    unsigned long int m = (l + r)/2;
    unsigned long int s = 0;
    // printf("m:%d, s:%d, l:%d, r:%d\n", m, s, l, r);
    while(l <= r){
        s = m*m;
        // printf("m:%d, s:%d, l:%d, r:%d\n", m, s, l, r);
        if(s == num){
            return true;
        }
        else if (s >  num){
            r = m - 1;
        }
        else { // s <  num
            l = m + 1;
        }
        m = (l + r)/2;
    }
    return false;
}

