/**
We are playing the Guess Game. The game is as follows:

I pick a number from 1 to n. You have to guess which number I picked (the number I picked stays the same throughout the game).

Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

You call a pre-defined API int guess(int num), which returns three possible results:

    -1: Your guess is higher than the number I picked (i.e. num > pick).
    1: Your guess is lower than the number I picked (i.e. num < pick).
    0: your guess is equal to the number I picked (i.e. num == pick).

Return the number that I picked.

 

Example 1:

Input: n = 10, pick = 6
Output: 6

Example 2:

Input: n = 1, pick = 1
Output: 1

Example 3:

Input: n = 2, pick = 1
Output: 1

 

Constraints:

    1 <= n <= 231 - 1
    1 <= pick <= n

 
 */

int guess(int num);

/** 
 * Forward declaration of guess API.
 * @param  num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * int guess(int num);
 */

int guessNumber(int n){
    unsigned long int l = 1;
    unsigned long int r = n;
    unsigned long int m = (l + r)/2;
    while(l <= r){
        int g = guess(m);
        if (g == 0){
            break;
        }
        else if (g == -1){
            // m is greater than  the number
            r = m - 1;
        }
        else { // g == 1
            // m is small than  the number
            l = m + 1;
        }
        m = (l + r)/2;
    }
    return m;
}