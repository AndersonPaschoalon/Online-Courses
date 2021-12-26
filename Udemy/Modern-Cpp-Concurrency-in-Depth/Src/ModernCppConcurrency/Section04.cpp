#include "Section04.h"
#include "Utils.h"
#include "s4_thread_safe_queue.h"
#include "s4_thread_safe_queue2.h"
#include "common_objs.h"

#include <list>
#include <future>
#include <mutex>
#include <chrono>
#include <execution>

using std::chrono::duration;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;
using std::milli;


///////////////////////////////////////////////////////////////////////////////
// SECTION 04 - EXERCISES
///////////////////////////////////////////////////////////////////////////////


//
// Section 04.39: Introduction to lock based thread safe data structores and algorithms
//

void run_04_39();

void run_04_39()
{
	printf("Runs the implementation s4_thread_safe_queue tSafeQueue\n");
	s4_thread_safe_queue<int>* tSafeQueue = new s4_thread_safe_queue<int>();
	int val = 1;
	tSafeQueue->push(val);
	printf("Empty?<%d>\n", tSafeQueue->empty());
	tSafeQueue->wait_pop();
	printf("Empty?<%d>\n", tSafeQueue->empty());
}

//
// Section 04.41: Thread safe queue implementation
//

void run_04_41();

void run_04_41()
{
	s4_thread_safe_queue2<int>* tsq = new  s4_thread_safe_queue2<int>();
	int val1 = 1;
	tsq->push(val1);
}


//
// Section 04.42: Parallel STL introduction
//

void run_04_42();

void run_04_42()
{
}


//
// Section 04.43: Parallel Quick sort algorithm implementation
//

void run_04_43();
template<typename T>
std::list<T> sequential_quick_sort(std::list<T> input);
template<typename T>
std::list<T> parallel_quick_sort(std::list<T> input);

void run_04_43()
{
	printf("Serial implementation of quicksort\n");

	std::list<int> list1 = std::list<int>({ 6, 3, 5, 8 });
	std::list<int> list2 = std::list<int>({ 6, 3, 5, 8 });
	sequential_quick_sort(list1);
	parallel_quick_sort(list2);
}

template<typename T>
std::list<T> sequential_quick_sort(std::list<T> input)
{
	// recursive return condition
	if (input.size() < 2)
	{
		return input;
	}

	// select the pivot value
	std::list<T> result;
	result.splice(result.begin(), input, input.begin());
	T pivot = *result.begin();

	// arrange the input array
	auto divide_point = std::partition(input.begin(), input.end(), [&](T const& t)
		{
			return t < pivot;
		});

	// call the sequential_quick_sort recursively
	std::list<T> lower_list;
	lower_list.splice(lower_list.end(), input, input.begin(), divide_point);

	auto new_lower(sequential_quick_sort(std::move(lower_list)));
	auto new_upper(sequential_quick_sort(std::move(input)));

	// arranging the result list
	result.splice(result.begin(), new_lower);
	result.splice(result.end(), new_upper);

	return result;
}

template<typename T>
std::list<T> parallel_quick_sort(std::list<T> input)
{
	// recursive return condition
	if (input.size() < 2)
	{
		return input;
	}

	// select the pivot value
	std::list<T> result;
	result.splice(result.begin(), input, input.begin());
	T pivot = *result.begin();

	// arrange the input array
	auto divide_point = std::partition(input.begin(), input.end(), [&](T const& t)
		{
			return t < pivot;
		});

	// call the sequential_quick_sort recursively
	std::list<T> lower_list;
	lower_list.splice(lower_list.end(), input, input.begin(), divide_point);

	auto new_lower(sequential_quick_sort(std::move(lower_list)));
	//auto new_upper(sequential_quick_sort(std::move(input)));
	std::future<std::list<T>> new_upper_future(std::async(&parallel_quick_sort<T>, std::move(input)));


	// arranging the result list
	result.splice(result.begin(), new_lower);
	result.splice(result.end(), new_upper_future.get());

	return result;
}


//
// Section 04.44: Parallel for each implementation
//

void run_04_44();

template<typename Iterator, typename Func>
void parallel_for_each_pt(Iterator first, Iterator, Func f);
template<typename Iterator, typename Func>
void parallel_for_each_async(Iterator first, Iterator, Func f);


void run_04_44()
{
	const size_t TestSize = 1000;
	std::vector<int> ints(TestSize);
	for (auto& i : ints)
	{
		i = 1;
	}

	auto long_function = [](const int& m)
	{
		int sum = 0;
		for (auto i = 0; i < 100000; i++)
		{
			sum += 1 * (i - 499);
		}
	};

	auto startTime = high_resolution_clock::now();
	std::for_each(ints.cbegin(), ints.cend(), long_function);
	auto endTime = high_resolution_clock::now();
	



}

template<typename Iterator, typename Func>
void parallel_for_each_pt(Iterator first, Iterator, Func f)
{
	unsigned long const length = std::distance(first, last);

	if (!length)
	{
		return;
	}

	// Calculate the optimized number of threads to run the algorithm
	unsined long const min_per_thread = 25;
	unsigned long const max_threads = (lenght + min + per_thread - 1) / min_per_thread;
	unsigned long const hartware_threads = std::thread::hardware_concurrency();
	unsigned long const num_threads = std::min(hastware_threads != 0 ? hardware_threads : 2, max_threads);
	unsigned lng const block_size = length / num_threads;

	// declare the needed data structures
	std::vector<std::future<void>> futures(num_threads - 1);
	std::vector<std::thread> threads(num_threads - 1);
	join_threads joiner(threads);

	// divide the workload between threads
	Iterator block_start = first;
	for (unsigned long i = 0; i <= (num_threads - 1); i++)
	{
		Iterator block_end = block_start;
		std::advance(block_end, block_size);

		std::packaged_task<void(void)> task(
			[=]() 
			{
				std::for_each(block_start, block_end, f);
			}
		);

		futures[i] = task.get_future();
		threads[i] std::thread(std::move(task));

		block_start = block_end;
	}

	// call the function for last block from this thread
	std::for_each(block_start, last, f);

	// wait until futures are ready
	for (unsigned long i = 0; i < (num_threads - 1); ++i)
	{
		futures[i].get();
	}

}


template<typename Iterator, typename Func>
void parallel_for_each_async(Iterator first, Iterator, Func f)
{
	unsigned long const lenght = std::distance(first, last);

	if (!lenght)
	{
		return;
	}

	unsigned long const min_per_thread = 25;

	if (lenght < 2 * min_per_thread)
	{
		std::for_each(first, last, f);
	}
	else
	{
		Iterator const mid_point = first + lenght / 2;
		std::future<void> first_half = std::async(&parallel_for_each_async<Iterator, Func>, first, mid_point, f);

		parallel_for_each_async(&parallel_for_each_async<Iterator, Func>, first, mid_point, f);

		parallel_for_each_async(mid_point, last, f);
		first_half.get();
	}

}


//
// Section 04.45: àrallel find algorithm implementation with package task
//

void run_04_45();

void run_04_45()
{
}


//
// Section 04.46: Parallel find algorithm implementation with async 
//

void run_04_46();

void run_04_46()
{
}

//
// Section 04.47: Partial sum algorithm introduction
//

void run_04_47();

void run_04_47()
{
}


//
// Section 04.48: Partial sum algorithm parallel implementation
//

void run_04_48();

void run_04_48()
{
}


//
// Section 04.49: Intorduction to Matrix
//

void run_04_49();

void run_04_49()
{
}


//
// Section 04.50: Parallel Matrix multiplication
//

void run_04_50();

void run_04_50()
{
}


//
// Section 04.51: Parallel Matrix transpose
//

void run_04_51();

void run_04_51()
{
}


//
// Section 04.52: Factors affectiong the performance of current code
//

void run_04_52();

void run_04_52()
{
}


///////////////////////////////////////////////////////////////////////////////
// SECTION 04 - MAIN CLASS
///////////////////////////////////////////////////////////////////////////////

void Section04::s39_introduction_to_lock_based_thread_safe_data_structures_and_algotithms()
{
	Utils::printHeader("// Section 04.39: Introduction to lock based thread safe data structores and algorithms");
	run_04_39();
}

void Section04::s41_thread_sage_queue_implementation()
{
	Utils::printHeader("// Section 04.41: Thread safe queue implementation");
	run_04_41();
}

void Section04::s42_parallel_ste_intruduction()
{
	Utils::printHeader("// Section 04.42: Parallel STL introduction");
	run_04_42();
}

void Section04::s43_parallel_quick_sort_algorithm_implementation()
{
	Utils::printHeader("// Section 04.43: Parallel Quick sort algorithm implementation");
	run_04_43();
}

void Section04::s44_parallel_for_each_implementation()
{
	Utils::printHeader("// Section 04.44: Parallel for each implementation");
	run_04_44();
}

void Section04::s45_parallel_for_each_implementation()
{
	Utils::printHeader("// Section 04.45: Prallel find algorithm implementation with package task");
	run_04_45();
}

void Section04::s46_parallel_fund_algorithm_implementation_with_package_task()
{
	Utils::printHeader("// Section 04.46: Parallel find algorithm implementation with async ");
	run_04_46();
}

void Section04::s47_partial_sum_algorithm_introduction()
{
	Utils::printHeader("// Section 04.47: Partial sum algorithm introduction");
	run_04_47();
}

void Section04::s48_partial_sum_algorithm_implementation()
{
	Utils::printHeader("// Section 04.48: Partial sum algorithm parallel implementation");
	run_04_48();
}

void Section04::s49_introduction_to_matrix()
{
	Utils::printHeader("// Section 04.49: Intorduction to Matrix");
	run_04_49();
}

void Section04::s50_parallel_matrix_multiplication()
{
	Utils::printHeader("// Section 04.50: Parallel Matrix multiplication");
	run_04_50();
}

void Section04::s51_paralle_matrix_transpose()
{
	Utils::printHeader("// Section 04.51: Parallel Matrix transpose");
	run_04_51();
}

void Section04::s52_factors_affection_the_performance_of_current_code()
{
	Utils::printHeader("// Section 04.52: Factors affectiong the performance of current code");
	run_04_52();
}


