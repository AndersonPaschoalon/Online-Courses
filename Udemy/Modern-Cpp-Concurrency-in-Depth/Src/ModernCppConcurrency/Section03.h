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

	//
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

	// async will run the functin in another thread in parallel, while defered will 
	// be called when the function get() is called.
	static void s03_33_async_task_details_discussion();

	// a recursive implementation of the parallel algorithm
	static void s3_34_parallel_accumulate_algorithm();

	// * Package task can be considered as much insider layer, than the async.
	//	* Theoretically speaking, you can even implement async using pakaged_task
	static void s3_35_introduction_to_package_tasks();

	//  * Each std::promise object is paired with a std::future object
	//	* A thread with access to the std::future object can wait for the 
	//    result to be set, while another thread that has access to the 
	//    corresponding std::primisse object can call set_value() to 
	//    store the value and make the future ready.
	//    When you calll get(), the thread who is using the future will
	//    block until you use set_value() in another thread. Once you have 
	//    done that, the function will unblock, and it will continue to 
	//    run normally
	static void s3_36_communication_between_threads_using_promisses();

	// The idea is that an exception on a thread can be propagated to another,
	// if it is waiting the first one to response. 
	static void s3_37_retrieving_exception_using_futures();


	// You have to take care of using promisses and futures, because futures are 
	// single use objects. Once you have called future.get(), the object will be unusable, 
	// since the resource has been consumed. If you try to read the same future from a different
	// thrad, it will thrown an exception. If you must use the same future object among many
	// threads, you have to use shared_futures instead.
	static void s3_38_shared_futures();

private:

};

