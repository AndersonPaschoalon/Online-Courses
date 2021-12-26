# Section 04: Lock based thread safe data structures and algorithm

## Section 04.39. Introduction to lock based thread safe data structures and algorithms

Introduction to lock based thread safe data structures and algorithms

(1) Invariants were uphelds at all times
(2) Avoiding race conditions inherit from the interface
(3) Handling exception scenarios
(4) Avoid deadlocks at all cost

In the thread safe queue implementation:

(1) To update the queue, any thread using the queue object must use the same mutext object.

(2) To avoid the race condition inherit form the interface, the pop function was changed, wo it must return the popped value as well.



39. Introduction to lock based thread safe data structures and algorithms

(1) Invariants were uphelds at all times
(2) Avoiding race conditions inherit from the interface
(3) Handling exception scenarios
(4) Avoid deadlocks at all cost

In the thread safe queue implementation:

(1) To update the queue, any thread using the queue object must use the same mutext object.

(2) To avoid the race condition inherit form the interface, the pop function was changed, wo it must return the popped value as well.


40. queue data structure implementation using linked list data structure

#include <memory>
#include <condition_variable>
#include <thread>

template<typename T>

class sequential_queue2
{

private:

	struct node 
	{
		T data;
		std::unique_ptr<node> next;

		node(T _data):data(std::move(_data))
		{
		}
	};

	std::unique_ptr<node> head;
	node* tail;

public:

	void push(T value)
	{
		std::unique_ptr<node> new_node(new node(std::move(value)));
		node *const new_tail = new_node.get();

		if(tail)
		{
			tail->next = std::move(new_node);
		}
		else
		{
			head = std::move(new_node);
		}
		tail = new_tail;

	}

	std::shared_ptr<T> pop()
	{
	}

};

41. What is parallel STL?

- With C++ 17 we can specify algorithms about user preferred way of execution, parallel or sequential

TODO: 
- estudar std::splice();
- estudar std::partition();






































