/** 
206. Reverse Linked List
Solved
Easy
Topics
premium lock iconCompanies

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:

Input: head = [1,2]
Output: [2,1]

Example 3:

Input: head = []
Output: []

Constraints:

    The number of nodes in the list is the range [0, 5000].
    -5000 <= Node.val <= 5000

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
struct ListNode* reverseList(struct ListNode* head) {
    // case base 1: lista vazia
    if(head == NULL){
        return NULL;
    }
    // caso base 2: next é nulo, logo o reversed é ele proprio
    else if(head->next == NULL){
        return head;
    }
    else{
        // Aqui eu assumo que a função reverseList vai ordenar corretamente a lista, e portanto vai retornar
        // o ponteiro head->next, com os demais elementos já ordenados
        struct ListNode* reversed = reverseList(head->next);
        // Agora preciso atualizar o ponteise reversed.
        // Ele deverá apontar para o head
        head->next->next = head;
        // o ponteiro head deverá apontar para null agora
        head->next = NULL;
        return reversed;
    }
    
}