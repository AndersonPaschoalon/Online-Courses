#pragma once
#include <iostream>
#include <mutex>
#include <stack>
#include <thread>

template<typename T>
class ThreadSafeStack
{
public:

	ThreadSafeStack();
	void push(T element);
	void pop(T element);
	T& top();
	bool empty();
	size_t size();


private:

	std::stack<T> stk;
	std::mutex m;
};

