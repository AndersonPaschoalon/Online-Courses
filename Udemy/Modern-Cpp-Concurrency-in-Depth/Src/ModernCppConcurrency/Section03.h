#pragma once
#include <iostream>
#include <mutex>
#include <thread>
#include <string>
#include <chrono>

#include "ThreadSafeStack2.h"
#include "ThreadSafeStack.h"
#include "ThreadSafeQueue.h"


//extern ThreadSafeQueue<int> s3_31_queue;

class Section3
{
public:

	// Condition variables work as events wich are able to tell your thread 
	// to "wake up" at the right moment.
	static void s3_28_introduction_to_condition_variables();
	static void s3_29_details_about_condition_variables();

	// implementation of a thread safe queue, without 
	// race conditin inherited by the interface.
	static void s3_31_thread_safe_queue_implementation();

	//	Futures and async tasks
	//		- First, creator of the asynchronous task have to obtain the future 
	//		associate with asynchronous task
	//		- When creatio of async task need the result of the async task it 
	//		called get method on future
	//		- Get method may block if the asynchronous operation has not yet 
	//		complete its execution
	//		- When the asynchronous operation is ready to send a result to the 
	//		creator, it can do so by modifying shared state that is linked to 
	//		the creator's std::future.
	static void s3_32_introduction_to_futures_and_async_tasks();

	static void s03_33_async_task_details_discussion();

	//
	static void s3_00_parallel_accumulate_algorithm();


	static void s3_00_introduction_to_package_tasks();

	static void s3_00_shared_futures();
	static void s3_00_retrieving_exception_using_futures();

	static void s3_00_communication_between_threads_using_promisses();





private:

};

