/* 
You are given an m x n integer matrix matrix with the following two properties:

    Each row is sorted in non-decreasing order.
    The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

 

Example 1:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Example 2:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false

 

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 100
    -104 <= matrix[i][j], target <= 104


*/

int* col_to_array(int** matrix, int nl, int c);
void print_array(int* array, int len);
void free_array(int* array);
int floor_value(int* arr, int n, int x);
int bin_search(int* arr, int n, int x);

// para saber se o elemento estará presente na matriz:
// 1. Selectionar linha candidata, sendo a linha cujo primeiro elemento é menor ou igual ao target
//    * se for igual a resposta  é true
//    * se for diferente procurar nessa linha
//  2. Se o elemento existir na linha é true, se não é falso.
bool searchMatrix(int** matrix, int matrixSize, int* matrixColSize, int target) {
    int nl = matrixSize;
    int* a = col_to_array(matrix, nl, 0);
    //print_array(a, nl);
    int p = floor_value(a, nl, target);
    if (p < 0)
        return false;
    //printf("p:%d\n", p);
    if(matrix[p][0] == target){
        free_array(a);
        return true;
    }
    else {
        // busca binaria
        int q = bin_search(matrix[p], matrixColSize[p], target);
        //printf("q:%d\n", p);
        if (q < 0){
            return false;
        }
    }
    return true;
}

int* col_to_array(int** matrix, int nl, int c){
    int* array = (int*) malloc(nl*sizeof(int));
    for (int i = 0; i < nl; i++){
        array[i] = matrix[i][c];
    }
    return array;
}

void free_array(int* array){
    free(array);
}

void print_array(int* array, int len){
    printf("[");
    for(int i = 0; i < len; i++){
        printf("%d ", array[i]);
    }
    printf("]\n");
}

// floor: Buscar o maior valor menor ou igual a x
// Intuição: todo valor arr[m] <= x é um candidato. Mas é necessário continuar
// procurando a direita para encontrar um valor maior 
int floor_value(int* arr, int n, int x){
    int l = 0;
    int r = n -1;
    int ans = -1;
    while(l <= r){
        int m = l + (r - l)/2;
        if(arr[m] <= x){
            ans = m;
            l = m + 1;
        }
        else { // arr[m] > x
            r = m -1;
        }
    }
    return ans;
}

int bin_search(int* arr, int n, int x){
    int l = 0;
    int r = n -1;
    while(l <= r){
        int m = l + (r - l)/2;
        if(arr[m] == x){
            return m;
        }
        else if (arr[m] < x){
            // procurar a direita
            l = m + 1;
        }
        else {// arr[m] > x
            // procurar a esquerda
            r = m -1;
        }
    }
    return -1;
}

