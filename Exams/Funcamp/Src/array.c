#include <stdio.h>
#include <string.h>
#include <stdlib.h>


// Utils

void swap(int* a, int* b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

void print_array(int* array, int arraySize){
    for(int i = 0; i < arraySize; i++){
        printf("%d ", array[i]);
    }
    printf("\n");
}


// Algorithms

void bubleSort(int* array, int arraySize){
    int p1 = 0;
    int p2 = 1;
    int swapped = 1;
    
    while(swapped == 1){
        swapped = 0;
        int p1 = 0;
        int p2 = 1;
        for(int i = 1; i < arraySize; i++){
            if(array[p1] > array[p2]){
                swap(&array[p1], &array[p2]);
                swapped = 1;
            }
            p1 = p2;
            p2++;
        }
        arraySize--;
    }   
}

void bubleSort2(int* array, int arraySize){
	int swapped = 1;
	do{
		swapped = 0;
		for(int i = 1; i < arraySize; i++){
			if(array[i] < array[i - 1]){
				swap(&array[i], &array[i - 1]);
				swapped = 1;
			}
		}
		arraySize--;
	}while(swapped == 1);
}



void insertionSort(int* arr, int size){
	for(int i = 1; i < size; i++){
		for(int j = i; j > 0; j--){
			if(arr[j] < arr[j - 1]){
				swap(&arr[j], &arr[j - 1]);
			}
		}
	}
}

void insertionSort2(int* arr, int size){
	for(int i = 1; i < size; i++){
		int j = i;
		while(j > 0 && arr[j -1] > arr[j]){
			swap(&arr[j], &arr[j - 1]);
			j--;
		}
	}
}

void selectionSort(int* arr, int size){
    for(int j = 0; j < size; j++){
        int minPos = j;
        for(int i = j + 1; i < size; i++){
            if(arr[i] < arr[minPos]){
                minPos = i;
            }
        }
        if(minPos != j){
            swap(&arr[j], &arr[minPos]);
        }
    }
}

// Testers

void run_array_sorting_alg(int* array, int arraySize, void (*sortingFunc)(int* array, int arraySize), const char* algName){
	int* tempArray = (int*)malloc(arraySize*sizeof(int));
	for(int i = 0; i < arraySize; i++)
	    tempArray[i] = array[i];
	
    printf("\n== %s\n", algName);
    printf("Before sorting:\n");
    print_array(tempArray, arraySize);
    sortingFunc(tempArray, arraySize);
    printf("After sorting:\n");
    print_array(tempArray, arraySize);
	
	free(tempArray);
	tempArray = NULL;
}

void run_sorting_tests(){
    int arr1[] = {9, 3, 4, 7, 2, 1, 7, 4, 0, 8, 2};
    int arr2[] = {};
    int arr3[] = {3};
    int arr4[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int arr5[] = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};

    run_array_sorting_alg(arr1, sizeof(arr1)/sizeof(int), bubleSort, "bubleSort");
    run_array_sorting_alg(arr2, sizeof(arr2)/sizeof(int), bubleSort, "bubleSort");
    run_array_sorting_alg(arr3, sizeof(arr3)/sizeof(int), bubleSort, "bubleSort");
    run_array_sorting_alg(arr4, sizeof(arr4)/sizeof(int), bubleSort, "bubleSort");
    run_array_sorting_alg(arr5, sizeof(arr5)/sizeof(int), bubleSort, "bubleSort");

    run_array_sorting_alg(arr1, sizeof(arr1)/sizeof(int), insertionSort, "insertionSort");
    run_array_sorting_alg(arr2, sizeof(arr2)/sizeof(int), insertionSort, "insertionSort");
    run_array_sorting_alg(arr3, sizeof(arr3)/sizeof(int), insertionSort, "insertionSort");
    run_array_sorting_alg(arr4, sizeof(arr4)/sizeof(int), insertionSort, "insertionSort");
    run_array_sorting_alg(arr5, sizeof(arr5)/sizeof(int), insertionSort, "insertionSort");

    run_array_sorting_alg(arr1, sizeof(arr1)/sizeof(int), insertionSort2, "insertionSort2");
    run_array_sorting_alg(arr2, sizeof(arr2)/sizeof(int), insertionSort2, "insertionSort2");
    run_array_sorting_alg(arr3, sizeof(arr3)/sizeof(int), insertionSort2, "insertionSort2");
    run_array_sorting_alg(arr4, sizeof(arr4)/sizeof(int), insertionSort2, "insertionSort2");
    run_array_sorting_alg(arr5, sizeof(arr5)/sizeof(int), insertionSort2, "insertionSort2");

    run_array_sorting_alg(arr1, sizeof(arr1)/sizeof(int), bubleSort2, "bubleSort2");
    run_array_sorting_alg(arr2, sizeof(arr2)/sizeof(int), bubleSort2, "bubleSort2");
    run_array_sorting_alg(arr3, sizeof(arr3)/sizeof(int), bubleSort2, "bubleSort2");
    run_array_sorting_alg(arr4, sizeof(arr4)/sizeof(int), bubleSort2, "bubleSort2");
    run_array_sorting_alg(arr5, sizeof(arr5)/sizeof(int), bubleSort2, "bubleSort2");


    run_array_sorting_alg(arr1, sizeof(arr1)/sizeof(int), selectionSort, "selectionSort");
    run_array_sorting_alg(arr2, sizeof(arr2)/sizeof(int), selectionSort, "selectionSort");
    run_array_sorting_alg(arr3, sizeof(arr3)/sizeof(int), selectionSort, "selectionSort");
    run_array_sorting_alg(arr4, sizeof(arr4)/sizeof(int), selectionSort, "selectionSort");
    run_array_sorting_alg(arr5, sizeof(arr5)/sizeof(int), selectionSort, "selectionSort");



}

void test_swap(){
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    swap(&arr[2], &arr[3]);
    print_array(arr, sizeof(arr)/sizeof(int));
}

int main(){
    // test_swap();
    run_sorting_tests();
}
