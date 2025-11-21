/**
21. Merge Two Sorted Lists
Solved
Easy
Topics
premium lock iconCompanies

You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:

Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:

Input: list1 = [], list2 = []
Output: []

Example 3:

Input: list1 = [], list2 = [0]
Output: [0]

Constraints:

    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.
*/


struct ListNode {
    int val;
    struct ListNode *next;
};
 
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode* mergeTwoLists(struct ListNode* list1, struct ListNode* list2) {
    if(list1 == NULL){
        return list2;
    }
    else if (list2 == NULL){
        return list1;
    }
    struct ListNode*  p = list1;
    struct ListNode*  q = list2;
    struct ListNode* p_p = NULL;
    struct ListNode* temp = NULL;
    while(1){
        if(p->val < q->val){
            //printf("p:%d\n", p->val);
            p_p = p;
            p = p->next;
        }
        else{
            //printf("q:%d", q->val);
            if(p_p != NULL){
                //printf("[p_p:%d, q:%d]", p_p->val, q->val);
                p_p->next = q;
                temp = q->next;
                q->next = p;
                p_p = q;
                q = temp;
                //printf("[p_p:%d, q:%d]", p_p->val, q->val);
            }
            else{
                //printf(" [1o elemento da lista add]\n");
                list1 = q;
                temp = q->next;
                p_p = q;
                q->next = p;
                q = temp;                
            }

        }
        
        if(p == NULL){
            //printf("p NULL");
            p_p->next = q;
            break;
        }
        else if (q == NULL){
            //printf("1 NULL");
            break;
        }
    }
    return list1;
}