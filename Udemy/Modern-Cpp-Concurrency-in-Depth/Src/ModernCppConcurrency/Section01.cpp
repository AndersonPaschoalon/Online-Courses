#include <thread>
#include <iostream>
#include <chrono>
#include <string>
#include <numeric>
#include <string>
#include <functional>
#include<algorithm>
#include <atomic>

#include "common_objs.h"
#include "Section01.h"
#include "Utils.h"



///////////////////////////////////////////////////////////////////////////////
// SECTION 01 - EXERCISES
///////////////////////////////////////////////////////////////////////////////

//
// Section 01.04
//

void foo();
void run_01_04();
class callable_class;

void foo()
{
	printf("[%d] Hello from foo trhread\n", std::this_thread::get_id());
}

class callable_class
{
public:

	void operator()()
	{
		printf("[%d] Hello callable_class from operator()\n", std::this_thread::get_id());
	}
private:
};

void run_01_04()
{
	printf("[%d] Hello from main\n", std::this_thread::get_id());

	// function
	std::thread thread1(foo);
	// objects
	callable_class obj;
	std::thread thread2(obj);
	// lambda functions
	std::thread thread3([]
	{
		printf("[%d] Hellow form lambda\n", std::this_thread::get_id());
	});

	thread1.join();
	thread2.join();
	thread3.join();

	printf("[%d] Back from main\n", std::this_thread::get_id());
}

//
// Section 01.05
//

void test_01_05();
void functionA();
void functionB();

void test_01_05()
{
	printf("[%d] Hello from test_01_05()\n", std::this_thread::get_id());
}

void functionA()
{
	printf("[%d] Hello from functionA()\n", std::this_thread::get_id());
	std::thread threadC(test_01_05);
	threadC.join();
}

void functionB()
{
	printf("[%d] hello from functionB()\n", std::this_thread::get_id());
}

//
// Section 01.06 Joinability of threads
//

void test_01_06();
void run_01_06();

void test_01_06()
{
	printf("Actual thread: Hello from test01_06\n");
}

void run_01_06()
{
	std::thread thread01(test_01_06);

	if (thread01.joinable())
	{
		printf("Thread01 is joinable before join\n");
	}
	else
	{
		printf("Thread01 is not joinable before join\n");
	}

	thread01.join();

	if (thread01.joinable())
	{
		printf("Thread01 is joinable after join\n");
	}
	else
	{
		printf("Thread01 is not joinable after join\n");
	}

}

//
// Section 01.07
//

void run_01_07();
void foo_01_07();
void bar_01_07();


void run_01_07()
{
	std::thread foo_thread(foo_01_07);
	std::thread bar_thread(bar_01_07);

	bar_thread.detach();
	printf("This is after bar_01_07 thread detach\n");

	foo_thread.join();
	printf("This is after foo_01_07 thread join\n");
}

void foo_01_07()
{
	printf("Hello from foo_01_07 enter\n");
	std::this_thread::sleep_for(std::chrono::milliseconds(5000));
	printf("Hello from foo_01_07 exit\n");
}

void bar_01_07()
{
	printf("Hello from bar_01_07 enter\n");
	std::this_thread::sleep_for(std::chrono::milliseconds(5000));
	printf("Hello from bar_01_07 exit\n");
}

//
// Section 01.08 How to handle join, in exceptions scenarios
//

void run_01_08();
void foo_01_08();
void other_operations_01_08();

void run_01_08()
{
	std::thread foo_thread(foo_01_08);
	thread_guard tg(foo_thread);
	try
	{
		other_operations_01_08();

	}
	catch (...)
	{
	}


}

void foo_01_08()
{

}

void other_operations_01_08()
{
	std::cout << "This is other oprations" << std::endl;
	throw std::runtime_error("this is a runtime error");
}


//
// Section 01.10 how to pass parameters to a thread
//

void run_01_10();
void func1_01_10(int x, int y);
void func2_value_01_10(int x);
void func2_ref_01_10(int& x);


void run_01_10()
{
	printf("-- test01\n");
	int p = 9;
	int q = 8;
	std::thread thread_01(func1_01_10, p, q);
	thread_01.join();

	printf("-- test02 value\n");

	int x = 9;
	printf("(main thread) x:%d\n", x);
	std::thread thread_02(func2_value_01_10, x);
	std::this_thread::sleep_for(std::chrono::seconds(5));
	x = 15;
	printf("(main thread) x:%d\n", x);
	//if(thread_02.joinable()) 
		thread_02.join();

	printf("-- test02 ref\n");
	x = 9;
	printf("(main thread) x:%d\n", x);
	std::thread thread_03(func2_ref_01_10, std::ref(x));
	std::this_thread::sleep_for(std::chrono::seconds(5));
	x = 15;
	printf("(main thread) x:%d\n", x);
	if (thread_03.joinable())  
		thread_03.join();


}

void func1_01_10(int x, int y)
{
	printf("x + y = %d \n", x+y);
}

void func2_value_01_10(int x)
{
	int i = 0;
	while (true)
	{
		printf("Thread func2_value_01_10 x:%d\n", x);
		std::this_thread::sleep_for(std::chrono::seconds(1));
		//std::this_thread::sleep_for(std::chrono::microseconds(1000));
		i++;
		if (i == 15)
		{
			break;
		}
	}
}

void func2_ref_01_10(int& x)
{
	int i = 0;
	while (true)
	{
		printf("Thread func2_ref_01_10 x:%d\n", x);
		std::this_thread::sleep_for(std::chrono::seconds(1));
		i++;
		if (i == 15)
		{
			break;
		}
	}
}

//
// Section 01.12 Transfering ownership of a thread
//

void run_01_12();
void foo_01_12();
void bar_01_12();

void run_01_12()
{
	std::thread thread_1(foo_01_12);
	std::thread thread_2 = std::move(thread_1);
	printf("Now, the object thread_1  foo_01_12 thread");

	// implicit std::move happens here. it is equivalent to:
	// thread_1 = std::move(std::thread(bar_01_12));
	thread_1 = std::thread(bar_01_12);
	printf("Now, the object thread_1 is managing bar_01_12 thread, and thread_1 is managing foo_01_12 thread");

	thread_1.join();
	thread_2.join();
}

void foo_01_12()
{
	int i = 0;
	while (true)
	{
		printf("Thread foo_01_12() i:%d\n", i);
		std::this_thread::sleep_for(std::chrono::seconds(1));
		i++;
		if (i == 15)
		{
			break;
		}
	}
}

void bar_01_12()
{
	int i = 0;
	while (true)
	{
		printf("Thread bar_01_12() i:%d\n", i);
		std::this_thread::sleep_for(std::chrono::seconds(1));
		i++;
		if (i == 15)
		{
			break;
		}
	}
}

//
// 01.13 Some useful operations on thread
//

void run_01_13();
void foo_01_13();
void get_id_test_01_13();
void hardware_concurrency_01_13();

void run_01_13()
{
	printf("-- get id test\n");
	get_id_test_01_13();

	printf("\n-- hardware_concurrency test\n");
	hardware_concurrency_01_13();
}

void foo_01_13()
{
	printf("This thread id:{%d}\n", std::this_thread::get_id());
}

void get_id_test_01_13()
{
	std::thread thread_1(foo_01_13);
	std::thread thread_2(foo_01_13);
	std::thread thread_3(foo_01_13);
	std::thread thread_4;

	printf("Thread 01 id:{%d}  \n", thread_1.get_id());
	printf("Thread 02 id:{%d}  \n", thread_2.get_id());
	printf("Thread 03 id:{%d}  \n", thread_3.get_id());
	printf("Thread 04 id:{%d}  \n", thread_4.get_id());

	thread_1.join();
	thread_2.join();
	thread_3.join();
	printf("Thread 03 id:{%d}  \n", thread_3.get_id());
}

void hardware_concurrency_01_13()
{
	int allowedThreads = std::thread::hardware_concurrency();
	printf("Allowed threa count in my device: {%d}", allowedThreads);
}

// Section 01.15 Parallel Accumulate - algorithm explanation
//

void run_01_15();

void run_01_15()
{
	std::vector<int> v = { 1, 2, 3, 4, 5 };
	// lambda expression
	auto comma_fold = [](std::string a, int b)
	{
		return (std::move(a) + "," + std::to_string(b));
	};

	int sum = std::accumulate(v.begin(), v.end(), 0);
	int prod = std::accumulate(v.begin(), v.end(), 1, std::multiplies<int>());
    std::string csv = std::accumulate(std::next(v.begin()), v.end(), std::to_string(v[0]), comma_fold);

	std::cout << "sum  : " << sum << std::endl;
	std::cout << "prod : " << prod << std::endl;
	std::cout << "csv  : " << csv << std::endl;


}


//
// 01.16. Parallel Accumulate algorithm implementation 
// 
void run_01_16();

template<typename iterator, typename T>
void accumulateStdWrapper(iterator start, iterator end, T& ref);

template<typename iterator, typename T>
void parallel_accumulate(iterator start, iterator end, T& ref);

template<typename iterator, typename T>
void accumulateStdWrapper(iterator first, iterator last, T& val)
{
	val = std::accumulate(first, last, val);
}

template<typename iterator, typename T>
void parallel_accumulate(iterator start, iterator end, T& ref)
{
	unsigned MIN_BLOCK_SIZE = 1000;
	unsigned inputSize = (int)std::distance(start, end);
	unsigned allowedThreadByElements = (int)(inputSize) / MIN_BLOCK_SIZE;
	unsigned allowerdThreadByHardware = (int)std::thread::hardware_concurrency();

	if (allowerdThreadByHardware < 1)
		allowerdThreadByHardware = 2;
	unsigned numThread = (int)std::min(allowedThreadByElements, allowerdThreadByHardware);

	unsigned blockSize = (inputSize + 1) / numThread;
	std::vector<int> results((int)numThread);
	std::vector<std::thread> threads(numThread - 1);

	//iterate and craeting new threads to calculate sum for each blocks
	iterator last;
	for (unsigned i = 0; i < numThread - 1; i++)
	{
		last = start;
		std::advance(last, blockSize);
		std::thread threadIter(accumulateStdWrapper<iterator, T>, start, last, std::ref(results[i]));
		threads[i] = std::move(threadIter);
		start = last;
	}

	//final block will be calculated from this thread
	results[numThread - 1] =
		std::accumulate(start, end, results[numThread - 1]);

	for_each(threads.begin(), threads.end(), std::mem_fn(&std::thread::join));
	//std::for_each(threads.begin(), threads.end(), std::mem_fn(&std::thread::join));
	ref = std::accumulate(results.begin(), results.end(), ref);
}

void run_01_16()
{
	const int size = 8000;
	int ref = 0;
	std::vector<int> myArray(10000);
	// for random values
	srand(0);
	for (int i = 0; i < size; i++)
	{
		myArray[i] = 1;
		// for random values on the vector
		// 	myArray[i] = rand() % 10;

	}
	//parallel_accumulate<int*, int>(myArray, myArray + size, ref);
	parallel_accumulate(myArray.begin(), myArray.end(), ref);

	printf("Accumulated values: %d \n", ref);
}


//
// 17. Thread Local Storage
//

// #include <atomic>

std::atomic<int> iglobal_s1_17 = 0;
thread_local std::atomic<int> ilocal_s1_17 = 0;

void run_01_17();
void foo_s1_17();
void bar_s1_17();

void foo_s1_17()
{
	iglobal_s1_17++;
	std::cout << iglobal_s1_17;
}

void bar_s1_17()
{
	ilocal_s1_17++;
	std::cout << ilocal_s1_17;
}

void run_01_17()
{

	std::thread t1(foo_s1_17);
	std::thread t2(foo_s1_17);
	std::thread t3(foo_s1_17);

	t1.join();
	t2.join();
	t3.join();

	std::cout << std::endl;

	std::thread tl1(bar_s1_17);
	std::thread tl2(bar_s1_17);
	std::thread tl3(bar_s1_17);

	tl1.join();
	tl2.join();
	tl3.join();

}
 

//
// 18. Debugging an applicaion in Visual Studion _s1_18
//

// #include <iostream>
// #include <thread>
// #include <future>
// #include <chrono>
// #include <execution>
// #include <string>

const size_t testSize_s1_18 = 1000;

using std::chrono::duration;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;
using std::milli;

void run_01_18();

void function3_s1_18();

std::string function1_s1_18(int i);

double function2_s1_18(int i);

int init_number_s1_18(int i);

void run_01_18()
{
	std::vector<int> ints(testSize_s1_18);
	for (size_t i = 0; i < testSize_s1_18; i++)
	{
		ints[i] = init_number_s1_18(i);
		std::cout << init_number_s1_18(i) << " " << function1_s1_18(i) << " " << function2_s1_18(i);
	}
}

void function3_s1_18()
{
	throw;
}

std::string function1_s1_18(int i)
{
	//function3_s1_18();

	if (i < 100)
	{
		return std::string("Hello");
	}

	return std::string("Hi");
}

double function2_s1_18(int i)
{
	std::string str = function1_s1_18(i);

	if (i < 200)
	{
		return 3.98;
	}

	return 9.45;
}

int init_number_s1_18(int i)
{
	//function2_s1_18(i);

	if (i < 1000)
	{
		i = i;
	}
	else
	{
		i = i * 2;
	}

	return i;
}


///////////////////////////////////////////////////////////////////////////////
// SECTION 01 - MAIN CLASS
///////////////////////////////////////////////////////////////////////////////

//void Section01::printHeader(const char* title)
//{
//	printf("###################################################################\n");
//	printf("# %s\n", title);
//	printf("###################################################################\n");
//	printf("\n");
//}

void Section01::s1_04_launch_a_thread()
{
	Utils::printHeader("s1_04_launch_a_thread()");
	run_01_04();
}

// - I want you to launch 2 threads fom the main chread call threadA and threadB
// - Thread A Should execute a function called functionA and the ThreadB should 
//   execute a function called FunctionB
// - From function A you have to launch another thread call threadC which will tun 
//   the function call test. This test function should printout hello from test
// - Then I want you to order the thread in the order htey are going to finish execution. 
//   First thread in the order should be the first one to finish, Last thread in the 
//   order should be the last one to finish. Consider the main thread as well
void Section01::s1_05_programming_exercise01()
{
	Utils::printHeader("s1_05_programming_exercise()");
	printf("[%d] s1_05_programming_exercise\n", std::this_thread::get_id());
	std::thread threadA(functionA);
	std::thread threadB(functionB);
	threadA.join();
	threadB.join();
}

void Section01::s1_06_joinable_threads()
{
	run_01_06();
}

void Section01::s1_07_join_and_detach_functions()
{
	run_01_07();
}

void Section01::s1_08_handle_join_in_exceptions()
{
	run_01_08();
}

void Section01::s1_10_how_to_pass_parameters_to_a_thread()
{
	run_01_10();
}

void Section01::s1_12_transfering_ownership_of_a_thread()
{
	run_01_12();
}

void Section01::s1_13_usefull_functions()
{
	run_01_13();
}

void Section01::s1_15_accumulate_explanation()
{
	run_01_15();
}

void Section01::s1_16_accumulate_implementation()
{
	run_01_16();
}

void Section01::s1_17_local_storage()
{
	run_01_17();
}

void Section01::s1_18_debuging_an_application_in_visual_studio()
{
	run_01_18();
}
