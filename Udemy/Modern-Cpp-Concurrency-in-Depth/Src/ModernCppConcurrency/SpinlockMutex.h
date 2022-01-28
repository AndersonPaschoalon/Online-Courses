#pragma once

#include <thread>
#include <mutex>

class SpinlockMutex
{
	std::atomic_flag flag = ATOMIC_FLAG_INIT;

public:
	SpinlockMutex()
	{
	}

	void lock()
	{
		while (this->flag.test_and_set(std::memory_order_acquire));
	}

	void unlock()
	{
		this->flag.clear(std::memory_order_release);
	}
};



