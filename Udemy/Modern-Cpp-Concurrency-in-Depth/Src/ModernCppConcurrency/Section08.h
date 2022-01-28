#pragma once
#include <iostream>
#include <mutex>
#include <thread>
#include <string>
#include <chrono>

class Section08
{
public:

	// 
	static void s8_82_Simple_thread_pool();

	// 
	static void s8_83_Thread_pool_which_allowed_to_wait_on_submitted_tasks();

	// 
	static void s8_84_Thread_pool_with_waiting_tasks();

	// 
	static void s8_85_Minimizing_contention_on_work_queue();

	// 
	static void s8_86_Thread_pool_with_work_stealing();

private:
};

