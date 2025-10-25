/*
Given a m x n matrix grid which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in grid.

 

Example 1:

Input: grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]
Output: 8
Explanation: There are 8 negatives number in the matrix.

Example 2:

Input: grid = [[3,2],[1,0]]
Output: 0

 

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 100
    -100 <= grid[i][j] <= 100


*/

int countNegatives(int** grid, int gridSize, int* gridColSize);
int countNegativeRowOn(int* ptr, int gridColSize, int nNeg);
void printMatrix(int** grid, int gridSize, int* gridColSize);

int countNegatives(int** grid, int gridSize, int* gridColSize) {
    int nNeg = gridColSize[gridSize - 1];
    int acc = 0;
    for(int i = gridSize -1; i >= 0; i--){
        nNeg = countNegativeRowOn(grid[i], gridColSize[i], nNeg);
        acc += nNeg;
    }
    return acc;
}

// Recebe ponteiro para o primeiro element
// nNeg - numero de negativos na ultima iteração, ou seja se count > nNeg, pode parar
int countNegativeRowOn(int* ptr, int gridColSize, int nNeg)
{
    int* currPtr = &ptr[gridColSize - 1] ;
    int count = 0;
    //printf("Começando por %d\n", *currPtr);
    while(true){
        if(*currPtr < 0){

            count++;
        }
        else 
            break;
        currPtr--;
        if(count >= nNeg || count > gridColSize -1){
            break;
        }
    }
    printf("\n");
    return count;
}
void printMatrix(int** grid, int gridSize, int* gridColSize){
    for (int i = 0; i < gridSize; i++){
        for (int j = 0; j < gridColSize[i]; j++){
            printf("%d\t", grid[i][j]);
        }
        printf("\n");
    }
}


