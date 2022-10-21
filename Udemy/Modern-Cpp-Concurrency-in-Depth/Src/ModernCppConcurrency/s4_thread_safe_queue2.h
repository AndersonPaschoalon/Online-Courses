#pragma once
#include <iostream>
#include <mutex>
#include <queue>
#include <memory>
#include <condition_variable>
#include <thread>


template<typename T>
class s4_thread_safe_queue2
{
private:

	struct node 
	{
		std::shared_ptr<T> data;
		std::unique_ptr<node> next;

		node()
		{
		}

		node(T _data) : data(std::move(_data))
		{
		}
	};

	std::unique_ptr<node> head;
	node* tail;

	std::mutex head_mutex;
	std::mutex tail_mutex;

	std::condition_variable cv;

	node* get_tail()
	{
		std::lock_guard<std::mutex> lg(this->tail_mutex);
		return this->tail;
	}

	std::unique_ptr<node> wait_pop_head()
	{
		std::unique_lock<std::mutex> lock(head_mutex);
		cv.wait(lock, [&]
			{
				return head.get() != get_tail();
			});
		std::unique_ptr<node> const old_head = std::move(head);
		head = std::move(old_head->next);
		return old_head;
	}


public:


	s4_thread_safe_queue2() : head(new node), tail(this->head.get())
	{
		// creates a dummy node on the head, and points the tail on it
	}

	void push(T value)
	{
		// change current dummy nodes data value
		// - add the data to the (now) dummy node
		std::shared_ptr<T> new_data(std::make_shared<T>(std::move(value)));
		std::unique_ptr<node> p(new node);

		// add new dummy node to tail
		// - creates a new node, and transform it on the new tail, pointing the tail pointer on it
		node* const new_tail = p.get();
		{
			std::lock_guard<std::mutex> lgt(tail_mutex);
			this->tail->data = new_data;
			this->tail->next = std::move(p);
			this->tail = new_tail;
		}
		this->cv.notify_one();
	}

	std::shared_ptr<T> pop()
	{
		std::lock_guard<std::mutex> lg(this->head_mutex);
		if (this->head.get() == this->get_tail())
		{
			return std::shared_ptr<T>();
		}
		std::shared_ptr<T> const res(this->head->data);
		std::unique_ptr<node> const old_head = std::move(this->head);
		this->head = std::move(old_head->next);
		return res;
	}

	std::shared_ptr<T> wait_pop()
	{
		std::unique_lock<node> old_head = wait_pop_head();
		return old_head ? old_head->data : std::shared_ptr<T>();
	}

};

