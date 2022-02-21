#pragma once

#include <atomic>
#include <thread>
#include <iostream>


template<typename T>
class lock_free_stack
{
private: 

	struct node
	{
		std::shared_ptr<T>  data;
		node* next;

		node(T const& _data) :data(std::make_shared<T>(_data))
		{
		}
	};

	std::atomic<node*> head;
	// just log msg in the code execution
	std::atomic<int> conflicts;
	std::atomic<int> thread_in_pop;
	std::atomic<node*> to_be_deleted;

	void delete_nodes(node* nodes)
	{
		while (nodes)
		{
			node* next = nodes->next;
			delete nodes;
			nodes = next;
		}
	}

	void try_reclaim(node* old_head)
	{
		if (this->thread_in_pop == 1)
		{
			// delete node pointed by old_head
			delete old_head;

			node* claimed_list = to_be_deleted.exchange(nullptr);
			if (!--thread_in_pop)
			{
				this->delete_nodes(claimed_list);
			}
			else if(claimed_list)
			{
				node* last = claimed_list;
				while (node* const next = last->next)
				{
					last = next;
				}
				last->next = to_be_deleted;
				while (!to_be_deleted.compare_exchange_weak(last->next, claimed_list));
			}
		}
		else
		{
			// add node pointed by old_head to the to_be_deleted list
			old_head->next = to_be_deleted;
			while (!to_be_deleted.compare_exchange_weak(old_head->next, old_head));
			--thread_in_pop;
		}

	}

public:

	lock_free_stack(T typeVal)
	{
		conflicts.store(0);
	}

	void showInfo()
	{
		printf("%d conflicts detected!\n", conflicts.load());
	}

	void push(T const& _data)
	{
		node* const new_node = new node(_data);
		new_node->next = this->head.load();
		// // race condition!
		// head = new_node;
		// no log implementation
		//while (this->head.compare_exchange_weak(new_node->next, new_node));
		int i = 0;
		while (this->head.compare_exchange_weak(new_node->next, new_node))
		{
			i++;
			printf("[%d]compare_exchange_weak failed, another thread was pushing to the stack!\n", i);
			int nConflicts = conflicts.load();
			nConflicts++;
			conflicts.store(nConflicts);
		}
	}

	std::shared_ptr<T> pop()
	{
		// not safe implementation
		// node* old_head = head;
		// head = old_head->next;
		// result = old_head->data;
		// delete old_head;

		++this->thread_in_pop;


		node* old_head = head.load();
		while (old_head && !head.compare_exchange_weak(old_head, old_head->next));

		std::shared_ptr<T> res;
		if (old_head)
		{
			res.swap(old_head->data);
		}

		this->try_reclaim(old_head);

		return res;
	}

};






