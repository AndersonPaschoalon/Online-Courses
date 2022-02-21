#include "Section08.h"
#include "Utils.h"

void run_08_82();
void run_08_83();
void run_08_84();
void run_08_85();
void run_08_86();


//
// ----------------------------------------------------
//

std::atomic<int> counterOperations;

void run_08_82()
{
	thread_pool pool;
	std::cout << "Testing thread pool" << std::endl;

	counterOperations.store(0);
	for (int i = 0; i < 100; i++)
	{
		try
		{
			pool.submit(
				[=] 
				{
					counterOperations++;
					printf(" %d printed by thread - %d \n", i, std::this_thread::get_id());
				});
		}
		catch (...)
		{
			printf("Exception at %d\n", i);
		}
	}
	system("pause");
	printf("Executions %d\n", counterOperations.load());
}

//
// ----------------------------------------------------
//


void run_08_83()
{
	/*
	std::cout << "Simple thread pool with waiting \n";
	const int size = 1000;
	int* my_array = new int[size];

	srand(0);

	for (size_t i = 0; i < size; i++)
	{
		//my_array[i] = rand() % 10;
		my_array[i] = 1;
	}

	long result = parallel_accumulate<int*, int>(my_array, my_array + size, 0);
	std::cout << "final sum is  - " << result << std::endl;
	return;
	*/
}

//
// ----------------------------------------------------
//


void run_08_84()
{
	/*
	std::cout << "Simple thread pool with waiting for other tasks \n";
	const int size = 800;
	std::list<int> my_array;

	srand(0);

	for (size_t i = 0; i < size; i++)
	{
		my_array.push_back(rand());
	}

	my_array = parallel_quick_sort(my_array);

	for (size_t i = 0; i < size; i++)
	{
		std::cout << my_array.front() << std::endl;
		my_array.pop_front();
	}
	*/
}

//
// ----------------------------------------------------
//


void run_08_85()
{
	/*
	std::cout << "Simple thread pool with local work queue \n";
	const int size = 800;
	std::list<int> my_array;

	srand(0);

	for (size_t i = 0; i < size; i++)
	{
		my_array.push_back(rand());
	}

	my_array = parallel_quick_sort(my_array);

	for (size_t i = 0; i < size; i++)
	{
		std::cout << my_array.front() << std::endl;
		my_array.pop_front();
	}
	*/
}

//
// ----------------------------------------------------
//


void run_08_86()
{
	/*
#include <iostream>
#include <future>
#include <numeric>

#include "simple_threadpool_with_work_stealing.h"

int main()
{
	const int size = 800;
	std::list<int> my_array;

	srand(0);

	for (size_t i = 0; i < size; i++)
	{
		my_array.push_back(rand());
	}

	my_array = parallel_quick_sort(my_array);

	for (size_t i = 0; i < size; i++)
	{
		std::cout << my_array.front() << std::endl;
		my_array.pop_front();
	}
}
	*/
}


//
// ----------------------------------------------------
//


void Section08::s8_82_Simple_thread_pool()
{
	Utils::printHeader("// Section 08.82 - Simple thread pool");
	run_08_82();
}

void Section08::s8_83_Thread_pool_which_allowed_to_wait_on_submitted_tasks()
{
	Utils::printHeader("// Section 08.83 - Thread pool which allowed to wait on submitted tasks");
	run_08_83();
}

void Section08::s8_84_Thread_pool_with_waiting_tasks()
{
	Utils::printHeader("// Section 08.84 - Thread pool with waiting tasks");
	run_08_84();
}

void Section08::s8_85_Minimizing_contention_on_work_queue()
{
	Utils::printHeader("// Section 08.85 - Minimizing contention on work queue");
	run_08_85();
}

void Section08::s8_86_Thread_pool_with_work_stealing()
{
	Utils::printHeader("// Section 08.86 - Thread pool with work stealing");
	run_08_86();
}


