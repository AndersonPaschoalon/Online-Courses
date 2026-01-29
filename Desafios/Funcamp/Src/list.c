#include <stdio.h>
#include <stdlib.h>

typedef struct _node {
    int data;
    struct _node* next;
} node;


/***************************************************************************
 * Utils
 **************************************************************************/
 
void swap(node* a, node* b, node* a_prev) {
    if(a == NULL || b == NULL){
        return;
    }
    node* temp = b->next;
    b->next = a;
    a->next = temp;
    if(a_prev != NULL){
        a_prev->next = b;
    }

    return;
}


// Function to insert a node at the beginning of a linked list
void insertAtTheBegin(node** start_ref, int data)
{
    node* ptr1
        = (node*)malloc(sizeof(node));

    ptr1->data = data;
    ptr1->next = *start_ref;
    *start_ref = ptr1;
}


/***************************************************************************
 * Basic Algorithms
 **************************************************************************/

// Function to print the list
void print_list(node* n)
{
    while (n != NULL) {
        printf("%d -> ", n->data);
        n = n->next;
    }
    printf("\n");
}


void print_list_rec(node* head){
	if(head == NULL){
		printf("\n");
		return;
	}
	printf("%d ", head->data);
	print_list_rec(head->next);
}


node* insert_on_list(int val, node* head){
	node* c = head;
	node* p = NULL;
	node* new_node = (node*) malloc(sizeof(node));
	new_node->data = val;
	while(c != NULL && c->data < val){
		p = c;
		c = c->next;
	}
	
	new_node->next = c;
	if(p == NULL){
		return new_node;
	} else {
		p->next = new_node;
		return head;
	}
}


node* insert_on_list_rec(int val, node* head){
	// Base case: head is null or head is largen than val
	if(head == NULL || head->data > val){
		node* new_node = (node*)malloc(sizeof(node));
		new_node->data = val;
		new_node->next = head;
		return new_node;
	}
	// Default case: it is not the correct node, call on the next
	head->next = insert_on_list_rec(val, head->next);
	return head;
}


node* delete_from_list(node* head, int val){
	node* p = NULL;
	node* c = head;
	while(c!= NULL && c->data != val){
		p = c;
		c = c->next;
	}
	
	if(c == NULL)
        return head;
    if(c == head){
        head = c->next;
        free(c);
    } else {
        p->next = c->next;
        free(c);
    }

    return head;
}


node* delete_from_list_rec(node* head, int val){
	// Base case 1 head is null => return null
    if(head == NULL){
        return NULL;
    }
    // Base case 2: value matches head, delete head
    if(head->data == val){
        node* t = head->next;
        free(head);
        return t;
    }
    // Default case: call recursivally, update head next and return
    // unchanged head
    head->next = delete_from_list_rec(head->next, val);
    return head;
}


node* search(node* head, int val){
    node* c = head;
    while(c != NULL && c->data != val){
        c = c->next;
    }
    return c;
}


node* search_rec(node* head, int val){
    if(head == NULL || head->data == val){
        return head;
    }
    return search_rec(head->next, val);
}

int list_len(node* head){
    int len = 0;
    node* c = head;
    while(c != NULL){
        len++;
        c = c->next;
    }
    return len;
}


int list_len_rec(node* head){
    if(head == NULL){
        return 0;
    }
    return list_len_rec(head->next) + 1;
}


node* invert(node* head){
    if(head == NULL)
        return NULL;
    node* c = head;
    node* n = head->next;
    head->next = NULL;
    while(n != NULL){
        node* nn = n->next; 
        n->next = c;
        c = n;
        n = nn;
    }
    return c;
}


node* invert_rec(node* head){
    // Base case: last node or no node, already inverted!
    if(head == NULL || head->next == NULL){
        return head;
    }

    // Default case: capture the last value from recursive call, this will 
    // be the new head. Current next node must point to current, and current
    // must point to null. In the next call current will be the next, so it
    // will be updated unless it is the last one, wich must point to null.
    node* last = invert_rec(head->next);
    node* n = head->next;
    n->next = head;
    head->next = NULL;
    return last;
}


void purge_rec(node** head){
    if(*head == NULL){
        return;
    }
    if ((*head)->next == NULL){
        free(*head);
        return;
    }
    purge_rec(&(*head)->next);
    free(*head);
    *head = NULL;
}



/***************************************************************************
 * Sorting Algorithms
 **************************************************************************/
 
void bubbleSort(node** head) {
    int swapped = 1;
    node* p1 = NULL;
    node* p2 = NULL;
    node* p1_prev = NULL;
    node* last = NULL;
    
    if(*head == NULL || (*head)->next == NULL){
        return;
    }
    
    while(swapped == 1){
        p1 = *head;
        p2 = (*head)->next;
        p1_prev = NULL;
        swapped = 0;
        while(1){
            if(p1->data > p2->data){
                swap(p1, p2, p1_prev);
                if(p1_prev == NULL){
                    *head = p2;
                }
                swapped = 1;
            }
            p1_prev = p1;
            p1 = p2;
            p2 = p2->next;
            if(p2 == last){
                last = p1;
                break;
            }
        }
    }
}


/***************************************************************************
 * Test
 **************************************************************************/

void test_sorting_helper(int* arr, int arraySize, void (*sortingFunc)(node** head), const char* funcName){
	node* start = NULL;
	int list_size = arraySize / sizeof(arr[0]);
	
    for (int i = list_size - 1; i >= 0; i--){
        insertAtTheBegin(&start, arr[i]);
	}

    printf("== %s\n", funcName);
    printf("Linked list before sorting\n");
    print_list(start);
    sortingFunc(&start);
    printf("Linked list after sorting\n");
    print_list(start);
}


void test_list_basic_operations(){
	int arr1[] = { 78, 20, 10, 32, 1, 5, 78, 45, 12, 5, 
		56, 32, 89, 45, 78, 20, 12, 67, 5, 89 };
	int arr2[] = { 78, 20, 10, 32, 2, 5, 78, 45, 12, 5, 
		56, 32, 89, 45, 78, 20, 12, 67, 5, 89 };
	node* head1 = NULL;
	node* head2 = NULL;
	int size1 = sizeof(arr1)/sizeof(int);
	int size2 = sizeof(arr1)/sizeof(int);

    // list 1
	printf("[1] insert_on_list %d elements\n", size1);
	for (int i = size1 - 1; i >= 0; i--){
		head1 = insert_on_list(arr1[i], head1);
	}
	printf("[1] print_list_rec 1\n");
	print_list_rec(head1);
	printf("[1] list_len:%d\n", list_len(head1));
	
	node* n1 = search(head1, 32);
    printf("[1] search node 32: n1->data:%d\n", n1->data);
    
    printf("[1] invert list 1\n");
    head1 = invert(head1);
    
    printf("[1] print list 1\n");
    print_list_rec(head1);
    
    printf("[1] delete_from_list 78\n");
    head1 = delete_from_list(head1, 78);
    printf("[1] print list 1\n");
    print_list_rec(head1);    
    
    printf("[1] purge_rec\n");
    purge_rec(&head1);
    
    printf("\n");
    
	// list 2
	
	printf("[2] insert_on_list_rec %d elements\n", size2);
	for (int i = size2 - 1; i >= 0; i--){
		head2 = insert_on_list_rec(arr2[i], head2);
	}
	printf("[2] print_list_rec 2\n");
	print_list_rec(head2);
	printf("[2] list_len_rec:%d\n", list_len_rec(head2));

    node* n2 = search_rec(head2, 67);
    printf("[2] search node rec 67: n2->data:%d\n", n2->data);
    
    printf("[2] invert_rec list 2\n");
    head2 = invert_rec(head2);
    printf("[2] print list 2\n");
    print_list_rec(head2);

    printf("[2] delete_from_list_rec 32\n");
    head2 = delete_from_list_rec(head2, 32);
    printf("[2] print list 2\n");
    print_list_rec(head2);

    printf("[2] purge_rec\n");
    purge_rec(&head2);
    
    printf("\n");
}


void test_all_list_sorting(){
	
    int arr[] = { 78, 20, 10, 32, 1, 5, 78, 45, 12, 5, 
                  56, 32, 89, 45, 78, 20, 12, 67, 5, 89 };
				  
	test_sorting_helper(arr, sizeof(arr), bubbleSort, "bubbleSort");
}


int main(){

	test_list_basic_operations();
	test_all_list_sorting();

    return 0;
}






