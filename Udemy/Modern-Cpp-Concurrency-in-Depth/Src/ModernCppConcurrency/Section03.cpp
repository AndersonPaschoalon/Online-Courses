#include "Section03.h"
#include "ThreadSafeStack.h"
#include "ThreadSafeStack2.h"
#include "ThreadSafeQueue.h"

///////////////////////////////////////////////////////////////////////////////
// SECTION 03 - EXERCISES
///////////////////////////////////////////////////////////////////////////////

//
// Section 03.28: Introduction to condition variables
//
bool s2_28_have_i_arrived = false;
int s3_28_distance_my_destination = 10;
int s3_28_distance_covered = 0;

void run_03_28();
bool s3_28_keep_driving();
void s3_28_keep_awake_all_night();
void s3_28_set_the_alarm_and_take_a_nap();


void run_03_28()
{
	std::thread driver_thread(s3_28_keep_driving);
	std::thread keep_awake_all_night_thread(s3_28_keep_awake_all_night);
	std::thread set_the_alarm_and_take_a_nap_trhead(s3_28_set_the_alarm_and_take_a_nap);
	driver_thread.join();
	keep_awake_all_night_thread.join();
	set_the_alarm_and_take_a_nap_trhead.join();
}

bool s3_28_keep_driving()
{
	while (true)
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));
		s3_28_distance_covered++;
	}
	return false;

}

void s3_28_keep_awake_all_night()
{
	while (s3_28_distance_covered < s3_28_distance_my_destination)
	{
		std::cout << "keep check, whether I am there\n";
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));
	}
	std::cout << "finally I'm thre, discance_covered = " << s3_28_distance_covered << std::endl;
}

void s3_28_set_the_alarm_and_take_a_nap()
{
	if (s3_28_distance_covered < s3_28_distance_my_destination)
	{
		std::cout << "let me take a nap \n";
		std::this_thread::sleep_for(std::chrono::milliseconds(10000));
	}
	std::cout << "Finally I'm there, distance covered = " << s3_28_distance_covered << std::endl;
}

//
// Section 03.29: Details about condition variables
//

#include <condition_variable>

bool s3_29_have_i_arrived = false;
int s3_29_total_distance = 10;
int s3_29_distance_coverd = 0;
std::condition_variable cv;
std::mutex s3_29_m;

void run_03_29();
void s3_29_keep_moving();
void s3_29_ask_driver_to_wake_you_up_at_right_time();


void run_03_29()
{
	std::thread driver_thread(s3_29_keep_moving);
	std::thread passener_thread(s3_29_ask_driver_to_wake_you_up_at_right_time);
	driver_thread.join();
	passener_thread.join();
}

void s3_29_keep_moving()
{
	while (true)
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(10000));
		s3_29_distance_coverd++;

		/// notify the waiting threads if the event occurss
		if (s3_29_distance_coverd == s3_29_total_distance)
		{
			cv.notify_one();
		}
	}
}

void s3_29_ask_driver_to_wake_you_up_at_right_time()
{
	std::unique_lock<std::mutex> ul(s3_29_m);
	cv.wait(ul, [] {return s3_29_distance_coverd == s3_29_total_distance;});
	std::cout << "finally I'm there, distance_coverd = " << s3_29_distance_coverd << std::endl;
}

//
// Section 03.31: Threadsafe queue implementation: implementation
//
ThreadSafeQueue<int> s3_31_queue;

void run_03_31();
void s3_31_func_1();
void s3_31_func_2();


void run_03_31()
{
	std::thread thread_1(s3_31_func_1);
	std::thread thread_2(s3_31_func_2);

	thread_1.join();
	thread_2.join();
}

void s3_31_func_1()
{
	int value;
	s3_31_queue.wait_pop(value);
	std::cout << value << std::endl;
}

void s3_31_func_2()
{
	int x = 10;
	std::this_thread::sleep_for(std::chrono::milliseconds(2000));
	s3_31_queue.push(x);
}

//
// Section 03.32 Introduction to futures and async tasks 
// 
#include <future>

void run_03_32();
int s3_32_find_answer_how_old_universe_is();
void s3_32_do_other_calculations();

void run_03_32()
{
	std::future<int> the_answer_future = std::async(s3_32_find_answer_how_old_universe_is);
	s3_32_do_other_calculations();
	std::cout << "The answer is " << the_answer_future.get() << std::endl;
}

int s3_32_find_answer_how_old_universe_is()
{
	return 13000000000;
}

void s3_32_do_other_calculations()
{
	std::cout << "Doing other stuff " << std::endl;
}

//
// ----------------------------------------------------
//
#include <numeric>

int s3_temp01_MIN_ELEMENT_COUNT = 1000;

void temp01_run();
template<typename iterator>
int s3_temp01_parallel_accumulate(iterator begin, iterator end);

void temp01_run()
{
	std::vector<int> v(10000, 1);
	std::cout << "The sum is " << s3_temp01_parallel_accumulate(v.begin(), v.end()) << '\n';
}

template<typename iterator>
int s3_temp01_parallel_accumulate(iterator begin, iterator end)
{
	long length = std::distance(begin, end);

	//atleast runs 1000 element
	if (length <= s3_temp01_MIN_ELEMENT_COUNT)
	{
		std::cout << std::this_thread::get_id() << std::endl;
		return std::accumulate(begin, end, 0);
	}

	iterator mid = begin;
	std::advance(mid, (length + 1) / 2);

	//recursive all to parallel_accumulate
	std::future<int> f1 = std::async(std::launch::deferred | std::launch::async,
		s3_temp01_parallel_accumulate<iterator>, mid, end);
	auto sum = s3_temp01_parallel_accumulate(begin, mid);
	return sum + f1.get();
}

//
// ----------------------------------------------------
//

void run_03_33();
void s03_33_printing();
int s03_33_addition(int x, int y);
int s03_33_substract(int x, int y);

void run_03_33()
{
	std::cout << "main thread id -" << std::this_thread::get_id() << std::endl;
	int x = 100;
	int y = 50;
	std::future<void> f1 = std::async(std::launch::async, s03_33_printing);
	std::future<int> f2 = std::async(std::launch::deferred, s03_33_addition, x, y);
	std::future<int> f3 = std::async(std::launch::deferred | std::launch::async,
		s03_33_substract, x, y);

	f1.get();
	std::cout << "value recieved using f2 future -" << f2.get() << std::endl;
	std::cout << "value recieved using f2 future -" << f3.get() << std::endl;
}

void s03_33_printing()
{
	std::cout << "printing runs on-" << std::this_thread::get_id() << std::endl;
}

int s03_33_addition(int x, int y)
{
	std::cout << "addition runs on-" << std::this_thread::get_id() << std::endl;
	return x + y;
}

int s03_33_substract(int x, int y)
{
	std::cout << "substract runs on-" << std::this_thread::get_id() << std::endl;
	return x - y;
}


//
// ----------------------------------------------------
//

#include <iostream>
#include <future>
#include <numeric>
#include <thread>
#include <functional>

void temp03_run();
int s3_temp03_add(int x, int y);
void s3_temp03_task_thread();
void s3_temp03_task_normal();

void temp03_run()
{
	s3_temp03_task_thread();
	s3_temp03_task_normal();
	std::cout << "main thread id : " << std::this_thread::get_id() << std::endl;
}

int s3_temp03_add(int x, int y)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(500));
	std::cout << "add function runs in : " << std::this_thread::get_id() << std::endl;
	return x + y;
}

void s3_temp03_task_thread()
{
	std::packaged_task<int(int, int)> task_1(s3_temp03_add);
	std::future<int> future_1 = task_1.get_future();

	std::thread thread_1(std::move(task_1), 5, 6);
	thread_1.detach();

	std::cout << "task thread - " << future_1.get() << "\n";
}

void s3_temp03_task_normal()
{
	std::packaged_task<int(int, int)> task_1(s3_temp03_add);
	std::future<int> future_1 = task_1.get_future();
	task_1(7, 8);
	std::cout << "task normal - " << future_1.get() << "\n";
}


//
// ----------------------------------------------------
//

void temp04_run();


void temp04_run()
{
}

//
// ----------------------------------------------------
//

void temp05_run();


void temp05_run()
{
}

//
// ----------------------------------------------------
//

void temp06_run();


void temp06_run()
{
}


///////////////////////////////////////////////////////////////////////////////
// SECTION 03 - MAIN CLASS
///////////////////////////////////////////////////////////////////////////////

void Section3::s3_28_introduction_to_condition_variables()
{
	run_03_28();
}

void Section3::s3_29_details_about_condition_variables()
{
	run_03_29();
}

void Section3::s3_31_thread_safe_queue_implementation()
{
	run_03_31();
}

void Section3::s3_32_introduction_to_futures_and_async_tasks()
{
	run_03_32();
}

void Section3::s3_00_parallel_accumulate_algorithm()
{
	temp01_run();
}


void Section3::s03_33_async_task_details_discussion()
{
	run_03_33();
}

void Section3::s3_00_introduction_to_package_tasks()
{
	temp03_run();
}

void Section3::s3_00_shared_futures()
{
	temp04_run();
}

void Section3::s3_00_retrieving_exception_using_futures()
{
	temp05_run();
}

void Section3::s3_00_communication_between_threads_using_promisses()
{
	temp06_run();
}


