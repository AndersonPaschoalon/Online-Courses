#pragma once
#include <iostream>
#include <mutex>
#include <stack>
#include <thread>

template<typename T>
class ThreadSafeStack2
{
public:

	ThreadSafeStack2()
	{
	}

	void push(T element)
	{
		std::lock_guard<std::mutex> lg(this->m);
		this->stk.push(std::make_shared<T>(element));
	}

	std::shared_ptr<T> pop()
	{
		std::lock_guard<std::mutex> lg(this->m);
		if (this->stk.empty())
		{
			throw std::runtime_error("stack is empty");
		}
		std::shared_ptr<T> res(this->stk.top());
		this->stk.pop();
		return res;
	}

	void pop(T& value)
	{
		std::lock_guard<std::mutex> lg(this->m);
		if (this->stk.empty()) throw std::runtime_error("stack is empty");
		value = *(this->stk.top().get());
		this->stk.pop();
	}

	bool empty()
	{
		std::lock_guard<std::mutex> lg(this->m);
		return this->stk.empty();
	}

	size_t size()
	{
		std::lock_guard<std::mutex> lg(this->m);
		return this->stk.size();
	}


private:

	std::stack<std::shared_ptr<T>> stk;
	std::mutex m;
};
