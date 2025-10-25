/*
744. Find Smallest Letter Greater Than Target
Solved
Easy
Topics
premium lock iconCompanies
Hint

You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters.

Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist, return the first character in letters.

 

Example 1:

Input: letters = ["c","f","j"], target = "a"
Output: "c"
Explanation: The smallest character that is lexicographically greater than 'a' in letters is 'c'.

Example 2:

Input: letters = ["c","f","j"], target = "c"
Output: "f"
Explanation: The smallest character that is lexicographically greater than 'c' in letters is 'f'.

Example 3:

Input: letters = ["x","x","y","y"], target = "z"
Output: "x"
Explanation: There are no characters in letters that is lexicographically greater than 'z' so we return letters[0].

 

Constraints:

    2 <= letters.length <= 104
    letters[i] is a lowercase English letter.
    letters is sorted in non-decreasing order.
    letters contains at least two different characters.
    target is a lowercase English letter.
*/


char nextGreatestLetter(char* letters, int lettersSize, char target);
char getNextValOrFirst(char* letters, int lettersSize, int pos);

char nextGreatestLetter(char* letters, int lettersSize, char target) {
    printf("lettersSize:%d\n", lettersSize);
    int right = lettersSize - 1;
    int left = 0;
    int med = (right + left)/2;
    while(true){
        // 1. value was found
        if (letters[med] == target){
            return getNextValOrFirst(letters, lettersSize, med);
        }
        if (letters[med] < target)
            left = med + 1;
        else // letters[med] > target
            right = med - 1;
        printf("med:%d\n", med);
        // value was not found: chose nums[left]
        if (left > right){
            printf("left:%d\n", left);
            if (left >= lettersSize){
                return letters[0];
            }
            if (letters[left] < target)
                return getNextValOrFirst(letters, lettersSize, left);
            else
                return letters[left];

        }
        med = (left + right)/2;
    }
}

char getNextValOrFirst(char* letters, int lettersSize, int pos){
    int curr = pos;
    printf("Elemento atual letters[curr]:%c, pos atual:%d \n", letters[curr], curr);
    while(curr < lettersSize - 1){
        curr++;
        if (letters[curr] != letters[pos])
            return letters[curr];
    }
    return letters[0];
}



int main() {
    // Caso 1: básico
    char letters1[] = {'c', 'f', 'j'};
    printf("Caso 1: %c\n", nextGreatestLetter(letters1, 3, 'a'));  // esperado: 'c'

    // Caso 2: valor igual existente
    printf("Caso 2: %c\n", nextGreatestLetter(letters1, 3, 'c'));  // esperado: 'f'

    // Caso 3: valor maior que todos (wrap-around)
    printf("Caso 3: %c\n", nextGreatestLetter(letters1, 3, 'z'));  // esperado: 'c'

    // Caso 4: duplicatas
    char letters2[] = {'x', 'x', 'y', 'y'};
    printf("Caso 4: %c\n", nextGreatestLetter(letters2, 4, 'z'));  // esperado: 'x'

    // Caso 5: repetição no início
    printf("Caso 5: %c\n", nextGreatestLetter(letters2, 4, 'x'));  // esperado: 'y'

    // Caso 6: target entre dois elementos
    char letters3[] = {'a', 'd', 'h', 'k'};
    printf("Caso 6: %c\n", nextGreatestLetter(letters3, 4, 'f'));  // esperado: 'h'

    // Caso 7: target antes do primeiro elemento
    printf("Caso 7: %c\n", nextGreatestLetter(letters3, 4, 'a' - 1));  // esperado: 'a'

    // Caso 8: target exatamente igual ao último
    printf("Caso 8: %c\n", nextGreatestLetter(letters3, 4, 'k'));  // esperado: 'a'

    // Caso 9: todas as letras iguais (embora o enunciado diga que não ocorre, só para testar)
    char letters4[] = {'m', 'm', 'm'};
    printf("Caso 9: %c\n", nextGreatestLetter(letters4, 3, 'm'));  // esperado: 'm' (comportamento consistente)

    return 0;
}


