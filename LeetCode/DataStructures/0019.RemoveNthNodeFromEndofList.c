/** 
19. Remove Nth Node From End of List
Solved
Medium
Topics
premium lock iconCompanies
Hint

Given the head of a linked list, remove the nth node from the end of the list and return its head.

 

Example 1:

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]

Example 2:

Input: head = [1], n = 1
Output: []

Example 3:

Input: head = [1,2], n = 1
Output: [1]

 

Constraints:

    The number of nodes in the list is sz.
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz

 

Follow up: Could you do this in one pass?

*/

struct ListNode {
    int val;
    struct ListNode *next;
};

int tellNodeIndex(struct ListNode* head){
    if (head == 0){
        return 0;
    }
    int c = 1 + tellNodeIndex(head->next);
    return c;        
}

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    struct ListNode* c = head;
    struct ListNode* p = NULL;
    int count = 0;
    while(c != NULL){
        count++;
        int i = tellNodeIndex(c);
        printf("count:%d, i:%d\n", count, i);
        if (i == n){
            if(p != NULL){
                p->next = c->next;
            } 
            else{
                head = c->next;
            }
            //free(c);    
        }
        p = c;
        c = p->next;
    }
    return head;
}








