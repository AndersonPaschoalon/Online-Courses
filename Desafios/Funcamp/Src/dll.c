#include <stdio.h>
#include <stdlib.h>


typedef struct _node {
	int data;
	struct _node* next;
	struct _node* prev;
} node;


typedef struct _header {
	node* head;
	node* tail;
} header;


/***************************************************************************
 * Utils
 **************************************************************************/
 void swap(node* a, node* b);
 node* create_new_node(int val);
 header* create_empty_doubly_linked_list();


void swap(node* a, node* b) {
	if(a == NULL || b == NULL){
		return;
	}

	node* aprev = a->prev;
	node* anext = a->next;
	node* bprev = b->prev;
	node* bnext = b->next;

	// update a
	if(aprev != NULL) aprev->next = b;
	a->prev = bprev;
	a->next = bnext;
	if(anext != NULL) anext->prev = b;
	// update b
	if(bprev != NULL) bprev->next = a;
	if(bnext != NULL) bnext->prev = a;
	b->next = anext;
	b->prev = aprev;
}


node* create_new_node(int val){
	node* n = (node*)malloc(sizeof(node));
	n->prev = NULL;
	n->next = NULL;
	n->data = val;
	return n;
}


header* create_empty_doubly_linked_list(){
	header* h = (header*) malloc(sizeof(header));
	h->head = NULL;
	h->tail = NULL;
	return h;
}


/***************************************************************************
 * Basic Algorithms
 **************************************************************************/
void add_node_head(int val, header* h);
void add_node_tail(int val, header* h);
void add_node_sorted(int val, header* h);
void print_list_forward(header* h);
void print_list_backward(header* h);
node* search_node_forward(int val, header* h, int* position);
node* search_node_backward(int val, header* h, int* position);
int list_len(header* h);
int delete_from_list_backward(int val, header* h);
int delete_from_list_forward(int val, header* h);
void purge_list(header** h);

void add_node_head(int val, header* h){
	if(h == NULL) return;
	node* n = create_new_node(val);
	node* c = h->head;

	if(c == NULL){ // add first node
		h->tail = n;
	} else { // already has nodes
		n->next = c;
		c->prev = n;
	}
	h->head = n;
}


void add_node_tail(int val, header* h){
	if(h == NULL) return;
	node* c = h->tail;
	node* n = create_new_node(val);
	
	if(c == NULL){ // list is empty!
		h->head = n;
	} else { // there is more elements
		n->prev = c;
		c->next = n;
	}
	h->tail = n;
}


void add_node_sorted(int val, header* h){
	
	// list not created
	if(h == NULL) return;

	// search node position
	node* c = h->head;
	// printf(".\n");
	while(c != NULL){
		if(c->data > val){
			break;
		}
		c = c->next;
	}
	//printf("....\n");
	//printf("add val %d\n", val);
	if(c == NULL){
		// (1) c is NULL, we reached the last position and did not find the position
		//     insert in the tail
		add_node_tail(val, h);
	} else if(c->prev == NULL){
		// (2) c-Prev is NULL, so c is the head => Must be inserted as the new head
		add_node_head(val, h);
	} else {
		// (3) c->data is larger than val, we must inset the new node just before c!
		node* n = create_new_node(val);
		node* p = c->prev;
		
		// update new node
		n->next = c;
		n->prev = p;

		// update current c and prev p
		p->next = n;
		c->prev = n;
	}
}


// Forward transversal
void print_list_forward(header* h){
	node* c = h->head;
	while(c != NULL){
		printf("%d ", c->data);
		c = c->next;
	}
	printf("\n");
}


// backward transversal
void print_list_backward(header* h){
	node* c = h->tail;
	while(c != NULL){
		printf("%d ", c->data);
		c = c->prev;
	}
	printf("\n");
}


node* search_node_forward(int val, header* h, int* position){
	*position = 0;
	node* c = h->head;
	while(c != NULL){
		if(c->data == val){
			break;
		}
		(*position)++;
		c = c->next;
	}
	return c;
}


node* search_node_backward(int val, header* h, int* position){
	*position = 0;
	node* c = h->tail;
	while(c != NULL){
		if(c->data == val){
			break;
		}
		(*position)++;
		c = c->prev;
	}
	return c;
}


int list_len(header* h){
	int len = 0;
	node* c = h->head;
	while(c != NULL){
		len++;
		c = c->next;
	}
	return len;
}


int delete_from_list_forward(int val, header* h){
	node* c = h->head;
	while(c != NULL){
		c = c->next;
		if(c->data == val){
			break;
		}
	}

	// no node to remove
	if(c == NULL) return(-1);

	// default
	node* p = c->prev;
	node* n = c->next;

	if(p == NULL && n == NULL){
		// there is only one node, remove it from list header.
		h->head = NULL;
		h->tail = NULL;
	} else if(p == NULL){
		// if p is null, it is head
		h->head = n;
		n->prev = NULL;
	} else if (n == NULL){
		// if n is null, it is tail
		h->tail = p;
		p->next = NULL;
	} else {
		// there are a node p and n
		p->next = n;
		n->prev = p;
	}
	free(c);

	// return list size. if ret value is >= 0, than the node was removed.
	return list_len(h);
}

int delete_from_list_backward(int val, header* h){
	node* c = h->tail;
	while(c != NULL){
		if(c->data == val){
			break;
		}
		c = c->prev;
	}

	// no node to remove
	if(c == NULL) return(-1);

	// default
	node* p = c->prev;
	node* n = c->next;

	if(p == NULL && n == NULL){
		// there is only one node, remove it from list header.
		h->head = NULL;
		h->tail = NULL;
	} else if(p == NULL){
		// if p is null, it is head
		h->head = n;
		n->prev = NULL;
	} else if (n == NULL){
		// if n is null, it is tail
		h->tail = p;
		p->next = NULL;
	} else {
		// there are a node p and n
		p->next = n;
		n->prev = p;
	}
	free(c);

	// return list size. if ret value is >= 0, than the node was removed.
	return list_len(h);
}

void purge_list(header** h){
	node* c = (*h)->head;
	while(c != NULL){
		node* t = c;
		c = c->next;
		free(t);
	}
	(*h)->head = NULL;
	(*h)->tail = NULL;
	free(*h);
	*h = NULL;
}


/***************************************************************************
 * Test
 **************************************************************************/
void test_list_basic_operations();


void test_list_basic_operations(){
	int arr1[] = { 78, 20, 10, 32, 1, 5, 78, 45, 12, 5, 
		56, 32, 89, 45, 78, 12, 20, 12, 67, 5, 89 };
	int arr2[] = { 78, 20, 10, 32, 2, 5, 78, 45, 12, 5, 
		56, 32, 89, 45, 78, 12, 20, 12, 67, 5, 89 };
	int arr3[] = { 78, 20, 10, 32, 3, 5, 78, 45, 12, 5, 
		56, 32, 89, 45, 78, 12, 20, 12, 67, 6, 89 };
		
	header* head1 = create_empty_doubly_linked_list();
	header* head2 = create_empty_doubly_linked_list();
	header* head3 = create_empty_doubly_linked_list();
	int size1 = sizeof(arr1)/sizeof(int);
	int size2 = sizeof(arr2)/sizeof(int);
	int size3 = sizeof(arr3)/sizeof(int);
	int rm = 12;

	// list 1
	printf("\n\n\n=== list 1");
	
	printf("[1] add_node_head %d elements\n", size1);
	for (int i = 0; i < size1; i++){
		add_node_head(arr1[i], head1);
	}
	
	printf("[1] print_list_forward (the order must be inverted, since we added to head)\n");
	print_list_forward(head1);
	
	printf("[1] print_list_backward\n");
	print_list_backward(head1);
	
	printf("[1] search_node_forward\n");
	int position = 0;
	node* n1 = search_node_forward(rm, head1, &position);
	printf("[1] (%d) n1->data:%d @position:%d\n", rm, n1->data, position);
	
	printf("[1] search_node_backward\n");
	position = 0;
	n1 = search_node_backward(rm, head1, &position);
	printf("[1] (%d) n1->data:%d @position:%d\n", rm, n1->data, position);

	printf("[1] list_len:%d\n", list_len(head1));

	printf("[1] delete_from_list_forward %d\n", rm);
	printf("[1] list before delete_from_list_forward %d\n", rm);
	print_list_forward(head1);
	
	delete_from_list_forward(rm, head1);
	
	printf("[1] list after delete_from_list_forward %d\n", rm);
	print_list_forward(head1);

	printf("[1] delete_from_list_backward %d\n", rm);
	printf("[1] list before delete_from_list_backward %d\n", rm);
	print_list_forward(head1);
	
	delete_from_list_backward(rm, head1);
	
	printf("[1] list after delete_from_list_backward %d\n", rm);
	print_list_forward(head1);

	
	// list 2
	printf("\n\n\n=== list 2");
	
	printf("[2] add_node_head %d elements\n", size2);
	for (int i = 0; i < size2; i++){
		add_node_tail(arr2[i], head2);
	}
	
	printf("[2] print_list_forward\n");
	print_list_forward(head2);
	
	printf("[2] print_list_backward\n");
	print_list_backward(head2);
	
	printf("[2] search_node_forward\n");
	position = 0;
	node* n2 = search_node_forward(rm, head2, &position);
	printf("[2] (%d) n2->data:%d @position:%d\n", rm, n2->data, position);
	
	printf("[2] search_node_backward\n");
	position = 0;
	n2 = search_node_backward(rm, head2, &position);
	printf("[2] (%d) n2->data:%d @position:%d\n", rm, n2->data, position);

	printf("[2] list_len:%d\n", list_len(head2));

	printf("[2] delete_from_list_forward %d\n", rm);
	printf("[2] list before delete_from_list_forward %d\n", rm);
	print_list_forward(head2);
	
	delete_from_list_forward(rm, head2);
	
	printf("[2] list after delete_from_list_forward %d\n", rm);
	print_list_forward(head2);

	printf("[2] delete_from_list_backward %d\n", rm);
	printf("[2] list before delete_from_list_backward %d\n", rm);
	print_list_forward(head2);
	
	delete_from_list_backward(rm, head2);
	
	printf("[2] list after delete_from_list_backward %d\n", rm);
	print_list_forward(head2);


	// list 3
	printf("\n\n\n=== list 3");
	
	printf("[3] add_node_head %d elements\n", size3);
	for (int i = 0; i < size3; i++){
		add_node_sorted(arr3[i], head3);
	}
	
	printf("[3] print_list_forward\n");
	print_list_forward(head3);
	
	printf("[3] print_list_backward\n");
	print_list_backward(head3);
	
	printf("[3] search_node_forward\n");
	position = 0;
	node* n3 = search_node_forward(rm, head3, &position);
	printf("[3] (%d) n3->data:%d @position:%d\n", rm, n3->data, position);
	
	printf("[3] search_node_backward\n");
	position = 0;
	n3 = search_node_backward(rm, head3, &position);
	printf("[3] (%d) n3->data:%d @position:%d\n", rm, n3->data, position);

	printf("[3] list_len:%d\n", list_len(head3));

	printf("[3] delete_from_list_forward %d\n", rm);
	printf("[3] list before delete_from_list_forward %d\n", rm);
	print_list_forward(head3);
	
	delete_from_list_forward(rm, head3);
	
	printf("[3] list after delete_from_list_forward %d\n", rm);
	print_list_forward(head3);

	printf("[3] delete_from_list_backward %d\n", rm);
	printf("[3] list before delete_from_list_backward %d\n", rm);
	print_list_forward(head3);
	
	delete_from_list_backward(rm, head3);
	
	printf("[3] list after delete_from_list_backward %d\n", rm);
	print_list_forward(head3);

	printf("\n");
}


/***************************************************************************
 * Main
 **************************************************************************/
int main(){

	test_list_basic_operations();

	return 0;
}






