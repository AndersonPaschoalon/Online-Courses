#include "ThreadSafeStack.h"

template<typename T>
ThreadSafeStack<T>::ThreadSafeStack()
{
}

template<typename T>
void ThreadSafeStack<T>::push(T element)
{
	std::lock_guard<std::mutex> lg(this->m);
	this->stk.push(element);
}

template<typename T>
void ThreadSafeStack<T>::pop(T element)
{
	std::lock_guard<std::mutex> lg(this->m);
	this->stk.pop(element);
}

template<typename T>
T& ThreadSafeStack<T>::top()
{
	std::lock_guard<std::mutex> lg(this->m);
	return this->stk.top();
}

template<typename T>
bool ThreadSafeStack<T>::empty()
{
	std::lock_guard<std::mutex> lg(this->m);
	return this->stk.empty();
}

template<typename T>
size_t ThreadSafeStack<T>::size()
{
	std::lock_guard<std::mutex> lg(this->m);
	return this->stk.size();
}

