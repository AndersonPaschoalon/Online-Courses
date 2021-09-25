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

#include <future>

void run_03_33();
void s03_33_printing();
int s03_33_addition(int x, int y);
int s03_33_substract(int x, int y);

void run_03_33()
{
	std::cout << "main thread id -" << std::this_thread::get_id() << std::endl;
	int x = 100;
	int y = 50;
	// will run on a different thread
	std::future<void> f1 = std::async(std::launch::async, s03_33_printing);
	// will run when .get() is called
	std::future<int> f2 = std::async(std::launch::deferred, s03_33_addition, x, y);
	// the compiler will decide
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
#include <numeric>

int s3_34_MIN_ELEMENT_COUNT = 1000;

void run_03_34();
template<typename iterator>
int s3_34_parallel_accumulate(iterator begin, iterator end);

void run_03_34()
{
	std::cout << " -- run_03_34 \n";
	std::vector<int> v(10000, 1);
	std::cout << std::this_thread::get_id() << std::endl;
	int summval = s3_34_parallel_accumulate(v.begin(), v.end());
	printf("The sum is %d", summval);
}

template<typename iterator>
int s3_34_parallel_accumulate(iterator begin, iterator end)
{
	//
	// base case(stop case): len is smaller than s3_34_MIN_ELEMENT_COUNT, so acumullate all
	//

	long length = std::distance(begin, end);
	printf("length:%d\n", length);
	if (length <= s3_34_MIN_ELEMENT_COUNT)
	{
		std::cout << std::this_thread::get_id() << std::endl;
		// returns the summ for the base case
		return std::accumulate(begin, end, 0);
	}

	//
	// recursive case: split the vector in half, than call
	//
 
	// parallel accumulate for both
	iterator mid = begin; 
	std::advance(mid, (length + 1) / 2); // find the iterator for the middle of the vector
	//recursive all to parallel_accumulate
	// call s3_34_parallel_accumulate from the second half in another thread  (or in the same, the 
	// compiler will decide, based on CPU resources)
	std::future<int> f1 = std::async(std::launch::deferred | std::launch::async,
		s3_34_parallel_accumulate<iterator>, mid, end);
	// call s3_34_parallel_accumulate for the first half in the current thread
	auto sum = s3_34_parallel_accumulate(begin, mid);
	// returns the summ for the recursive case
	return sum + f1.get();
}

//
// ----------------------------------------------------
//

#include <iostream>
#include <future>
#include <numeric>
#include <thread>
#include <functional>

void run_03_35();
int s3_35_add(int x, int y);
void s3_35_task_thread();
void s3_35_task_normal();

void run_03_35()
{
	std::cout << "main thread id : " << std::this_thread::get_id() << std::endl;
	s3_35_task_thread();
	s3_35_task_normal();
}

int s3_35_add(int x, int y)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(500));
	std::cout << "add function runs in : " << std::this_thread::get_id() << std::endl;
	return x + y;
}

void s3_35_task_thread()
{
	std::packaged_task<int(int, int)> task_1(s3_35_add);
	std::future<int> future_1 = task_1.get_future();

	std::thread thread_1(std::move(task_1), 5, 6);
	thread_1.detach();

	std::cout << "task thread - " << future_1.get() << "\n";
}

void s3_35_task_normal()
{
	std::packaged_task<int(int, int)> task_1(s3_35_add);
	
	std::future<int> future_1 = task_1.get_future();
	// task_1 must be called explicitly, otherwise get will not work
	task_1(7, 8);
	std::cout << "task normal - " << future_1.get() << "\n";
}


//
// ----------------------------------------------------
//
#include <functional>
#include <future>
#include <thread>
#include <stdexcept>

// promises
void run_03_36();
void s3_36_print_int(std::future<int>& fut);

void run_03_36()
{
	std::cout << "main thread id : " << std::this_thread::get_id() << std::endl;
	std::promise<int> prom;
	std::future<int> fut = prom.get_future();

	std::thread print_thread(s3_36_print_int, std::ref(fut));

	std::this_thread::sleep_for(std::chrono::milliseconds(5000));
	std::cout << "setting the value in main thread \n";
	prom.set_value(10);

	print_thread.join();
}

void s3_36_print_int(std::future<int>& fut)
{
	std::cout << "thread id : " << std::this_thread::get_id() << std::endl;
	std::cout << "waiting for the value from print thread \n";
	// get() blocks and waits for the value to be set on the other thread.
	// when it is ready, this thread unblocks.
	std::cout << "value: " << fut.get() << "\n";
}


//
// ----------------------------------------------------
//


void run_03_37();
void s3_37_throw_exception();
void s3_37_calculate_square_root(std::promise<int>& prom);
void s3_37_print_result(std::future<int>& fut);

void run_03_37()
{
	// here a promise is created, and a future is instantiated, so the 
	// thread may have access of values set in the future
	std::promise<int> prom;
	std::future<int> fut = prom.get_future();

	// hre a thread responsible for the display is instantiated, and a reference to the 
	// future value is passed to it
	std::thread printing_thread(s3_37_print_result, std::ref(fut));

	// here the function responsible for calculating the future value is instantiated
	// it takes the promisse object, so it can set the future value
	std::thread calculation_thread(s3_37_calculate_square_root, std::ref(prom));

	printing_thread.join();
	calculation_thread.join();
}

void s3_37_throw_exception()
{
	throw std::invalid_argument("input cannot be negative");
}

void s3_37_calculate_square_root(std::promise<int>& prom)
{
	// this thread waits for the user input. When it is received,
	// it sets the value in the promise class.
	int x = 1;
	std::cout << "Please, enter an integer value:";
	try
	{
		std::cin >> x;
		if (x < 0)
		{
			s3_37_throw_exception();
		}
		prom.set_value(std::sqrt(x));
	}
	catch (std::exception& e)
	{
		prom.set_exception(std::current_exception());
	}
}

void s3_37_print_result(std::future<int>& fut)
{
	try
	{
		// it try to get the future value. if it is not set, it blocks, until 
		// the value is set by another thread.
		int x = fut.get();
		std::cout << "value: " << x << "\n";
	}
	catch (std::exception& e)
	{
		std::cout << "[exception caught: " << e.what() << "]\n";
	}
}

//
// ----------------------------------------------------
//

void run_03_38();
void s3_38_print_result(std::shared_future<int>& fut);

void s3_38_print_result(std::shared_future<int>& fut)
{
	printf("%d - valid future\n", fut.get());
}

void run_03_38()
{
	std::promise<int> prom;
	std::shared_future<int> fut(prom.get_future());

	std::thread th1(s3_38_print_result, std::ref(fut));
	std::thread th2(s3_38_print_result, std::ref(fut));

	prom.set_value(5);

	th1.join();
	th2.join();
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

void Section3::s03_33_async_task_details_discussion()
{
	run_03_33();
}

void Section3::s3_34_parallel_accumulate_algorithm()
{
	run_03_34();
}

void Section3::s3_35_introduction_to_package_tasks()
{
	run_03_35();
}

void Section3::s3_36_communication_between_threads_using_promisses()
{
	run_03_36();
}

void Section3::s3_37_retrieving_exception_using_futures()
{
	run_03_37();
}
void Section3::s3_38_shared_futures()
{
	run_03_38();
}





