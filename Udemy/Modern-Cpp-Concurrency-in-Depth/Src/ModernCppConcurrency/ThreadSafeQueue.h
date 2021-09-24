#pragma once

#include <iostream>
#include <mutex>
#include <queue>
#include <memory>
#include <condition_variable>
#include <thread>

template<typename T>
class ThreadSafeQueue
{
public :
	ThreadSafeQueue()
	{
		// nothing to do
	}

	ThreadSafeQueue(ThreadSafeQueue const& obj)
	{
		std::lock_guard<std::mutex> lg(obj.m);
		this->queue = this->obj.queue;
	}


	void push(T value)
	{
		std::lock_guard<std::mutex> lg(this->m);
		// to avoid the exception scenario wich can occur in the 
		// resource constraint environment while we are 
		// returning the value, I have stored the shared pointer
		// instead of raw value in the queue.
		this->queue.push(std::make_shared<T>(value));
		this->cv.notify_one();
	}

	std::shared_ptr<T> wait_pop()
	{
		std::unique_lock<std::mutex> lg(this->m);
		cv.wait(lg, [this] {
			return !this->queue.empty();
			});
		std::shared_ptr<T> ref = this->queue.front();
		this->queue.pop();
		return ref;
	}

	std::shared_ptr<T> pop()
	{
		std::lock_guard<std::mutex> lg(this->m);
		if (this->queue.empty())
		{
			return std::shared_ptr<T>();
		}
		else
		{
			// create pointer for a copy of the first element
			std::shared_ptr<T> ref(this->queue.front());
			// remove the element from the queue
			this->queue.pop();
			// return the pointer of the copy
			return ref;
		}
	}

	bool wait_pop(T& ref)
	{
		std::unique_lock<std::mutex> lg(this->m);
		cv.wait(lg, [this] {
			return !this->queue.empty();
			});
		ref = *(this->queue.front().get());
		this->queue.pop();
		return true;
	}

	bool pop(T& ref)
	{
		std::lock_guard<std::mutex> lg(this->m);
		if (this->queue.empty())
		{
			return false;
		}
		else
		{
			ref = this->queue.front();
			this->queue.pop();
			return true;
		}
	}

	bool empty()
	{
		std::lock_guard<std::mutex> lg(this->m);
		return this->queue.empty();
	}


	size_t size()
	{
		std::unique_lock<std::mutex> lg(this->m);
		return this->queue.size();
	}

private:

	std::mutex m;
	std::condition_variable cv;
	std::queue<std::shared_ptr<T>> queue;
};
