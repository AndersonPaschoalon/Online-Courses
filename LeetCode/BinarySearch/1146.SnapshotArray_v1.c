/*
Implement a SnapshotArray that supports the following interface:

    SnapshotArray(int length) initializes an array-like data structure with the given length. Initially, each element equals 0.
    void set(index, val) sets the element at the given index to be equal to val.
    int snap() takes a snapshot of the array and returns the snap_id: the total number of times we called snap() minus 1.
    int get(index, snap_id) returns the value at the given index, at the time we took the snapshot with the given snap_id

 

Example 1:

Input: ["SnapshotArray","set","snap","set","get"]
[[3],[0,5],[],[0,6],[0,0]]
Output: [null,null,0,null,5]
Explanation: 
SnapshotArray snapshotArr = new SnapshotArray(3); // set the length to be 3
snapshotArr.set(0,5);  // Set array[0] = 5
snapshotArr.snap();  // Take a snapshot, return snap_id = 0
snapshotArr.set(0,6);
snapshotArr.get(0,0);  // Get the value of array[0] with snap_id = 0, return 5

 

Constraints:

    1 <= length <= 5 * 104
    0 <= index < length
    0 <= val <= 109
    0 <= snap_id < (the total number of times we call snap())
    At most 5 * 104 calls will be made to set, snap, and get.


*/


typedef struct node_struct{
    int id;
    int* array;
    struct node_struct* next;
} node;

typedef struct {
    node* history;
    int* array;
    int length;
    int id;
    int val[10000][10000];
} SnapshotArray;;

// List helpers
node* create_node(int arrayLen, node* next_ptr, int* vals, int id);
void append_node(node* head, node* node_ptr);
void free_list(node* head);
void print_snap_array(SnapshotArray* obj);
// API
SnapshotArray* snapshotArrayCreate(int length);
void snapshotArraySet(SnapshotArray* obj, int index, int val);
int snapshotArraySnap(SnapshotArray* obj) ;
int snapshotArrayGet(SnapshotArray* obj, int index, int snap_id) ;
void snapshotArrayFree(SnapshotArray* obj);


node* create_node(int arrayLen, node* next_ptr, int* vals, int id){
    node* head = (node*)malloc(sizeof(node));
    int* array  = NULL;
    if (arrayLen > 0){
        array = (int*) malloc(sizeof(int)*arrayLen);
        // Inicializa com 0 se vals == NULL, copia o conteúdo de vals caso contrario
        if (vals != NULL){
            for(int i = 0; i < arrayLen; i++){
                array[i] = vals[i];
            }
        }
        else {
            for(int i = 0; i < arrayLen; i++){
                array[i] = 0;
            }            
        }
    }
    head->array = array;
    // seta next_ptr em next. Passar nulo caso não deva ser atribuido valor
    head->next = next_ptr;
    head->id = id;
    return head;
}

void append_node(node* head, node* node_ptr){
    if(head == NULL){
        printf("Invalid head\n");
        return;
    }
    node* curr = head;
    while(curr->next != NULL){
        curr = curr->next;
    }
    curr->next = node_ptr;
}

void free_list(node* head){
    node* curr = head;
    while(curr != NULL){
        node* next = curr->next;
        // limpa array
        free(curr->array);
        // limpa node
        free(curr);
        curr = next;
    }
}

// API

SnapshotArray* snapshotArrayCreate(int length) {
    printf("snapshotArrayCreate %d\n", length);
    SnapshotArray* s = (SnapshotArray*) malloc(sizeof(SnapshotArray));
    s->length = length;
    // s->history = create_node(length, NULL, NULL, 0);
    s->history = NULL;
    s->array = (int*) malloc(sizeof(int)*length);
    for(int i = 0; i < length; i++){
        s->array[i] = 0;
    }
    s->id = -1;
    return s;
}

void snapshotArraySet(SnapshotArray* obj, int index, int val) {
    //printf("snapshotArraySet index:%d val:%d\n", index, val);
    if(obj == NULL){
        printf("Obj is NULL");
        return;
    }
    if(index < 0 || index >= obj->length){
        printf("Invalid index %d\n", index);
    }
    obj->array[index] = val;
}

int snapshotArraySnap(SnapshotArray* obj) {
    //printf("snapshotArraySnap\n");
    int next_id = obj->id + 1;
    node* h = create_node(obj->length, NULL, obj->array, next_id);
    // add a new snapshot at the end of history
    if(obj->history == NULL){
        obj->history = h;
    }
    else {
        append_node(obj->history, h);
    }
    
    obj->id = next_id;
    print_snap_array(obj);
    return next_id;
}

int snapshotArrayGet(SnapshotArray* obj, int index, int snap_id) {
    if (snap_id > obj->id){
        printf("Invalid snap_id %d\n",snap_id);
        return 0;
    }
    node* curr = obj->history;
    int i = 0;
    for(int i = 0; i < snap_id; i++){
        if (curr == NULL){
            printf("Erro\n");
        }
        curr = curr->next;
    }
    int val = curr->array[index];
    return val;
}

void snapshotArrayFree(SnapshotArray* obj) {
    node* head = obj->history;
    free_list(head);
    free(obj);
    obj = NULL;
}

void print_snap_array(SnapshotArray* obj){
    node* curr = obj->history;
    //printf("\tsnap_id:%d ----\n", obj->id);
    while(curr != NULL){
        //printf("\t(id:%d)[", curr->id);
        for(int i = 0; i <  obj->length; i++){
            //printf("%d ", curr->array[i]);
        }
        //printf("]\n");
        curr = curr->next;
    }
}


/**
 * Your SnapshotArray struct will be instantiated and called as such:
 * SnapshotArray* obj = snapshotArrayCreate(length);
 * snapshotArraySet(obj, index, val);
 
 * int param_2 = snapshotArraySnap(obj);
 
 * int param_3 = snapshotArrayGet(obj, index, snap_id);
 
 * snapshotArrayFree(obj);
*/


