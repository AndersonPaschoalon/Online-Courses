#include "Section04.h"
#include "Matrix.h"
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
void print_results(const char* msg, std::chrono::steady_clock::time_point start_time, std::chrono::steady_clock::time_point end_time);

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
	print_results("STL                   ", startTime, endTime);

	startTime = high_resolution_clock::now();
	for_each(std::execution::seq, ints.cbegin(), ints.cend(), long_function);
	endTime = high_resolution_clock::now();
	print_results("STL-seq               ", startTime, endTime);

	startTime = high_resolution_clock::now();
	for_each(std::execution::par, ints.cbegin(), ints.cend(), long_function);
	endTime = high_resolution_clock::now();
	print_results("STL-par               ", startTime, endTime);

	startTime = high_resolution_clock::now();
	parallel_for_each_pt(ints.cbegin(), ints.cend(), long_function);
	endTime = high_resolution_clock::now();
	print_results("Parallel-package task ", startTime, endTime);

	startTime = high_resolution_clock::now();
	parallel_for_each_async(ints.cbegin(), ints.cend(), long_function);
	endTime = high_resolution_clock::now();
	print_results("Parallel-async        ", startTime, endTime);
}

template<typename Iterator, typename Func>
void parallel_for_each_pt(Iterator first, Iterator last, Func f)
{
	unsigned long const length = std::distance(first, last);

	if (!length)
	{
		return;
	}

	// Calculate the optimized number of threads to run the algorithm
	unsigned long const min_per_thread = 25;
	unsigned long const max_threads = (length + min_per_thread - 1) / (min_per_thread);
	unsigned long const hardware_threads = std::thread::hardware_concurrency();
	unsigned long const num_threads = std::min(hardware_threads != 0 ? hardware_threads : 2, max_threads);
	unsigned long const block_size = length / num_threads;

	// declare the needed data structures
	std::vector<std::future<void>> futures(num_threads - 1);
	std::vector<std::thread> threads(num_threads - 1);
	join_threads joiner(threads);

	// divide the workload between threads
	Iterator block_start = first;
	for (unsigned long i = 0; i <= (num_threads - 2); i++)
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
	    threads[i] = std::thread(std::move(task));

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
void parallel_for_each_async(Iterator first, Iterator last, Func f)
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
		parallel_for_each_async(mid_point, last, f);
		first_half.get();
	}

}

void print_results(const char* msg, std::chrono::steady_clock::time_point start_time, std::chrono::steady_clock::time_point end_time)
{
	std::cout << msg << ":" << std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count() << " microseconds." << std::endl;
}

//
// Section 04.45: prallel find algorithm implementation with package task
//

void run_04_45();

template<typename Iterator, typename MatchType>
Iterator parallel_find_pt(Iterator first, Iterator last, MatchType match);

void run_04_45()
{
	printf("Implementation using promisses at parallel_find_pt()\n");
}

template<typename Iterator, typename MatchType>
Iterator parallel_find_pt(Iterator first, Iterator last, MatchType match)
{
	struct find_element
	{
		void operator()(Iterator begin, Iterator end,
			MatchType match,
			std::promise<Iterator>* result,
			std::atomic<bool>* done_flag)
		{
			try
			{
				for (; (begin != end) && !std::atomic_load(done_flag); ++begin)
				{
					if (*begin == match)
					{
						result->set_value(begin);
						//done_flag.store(true);
						std::atomic_store(done_flag, true);
						return;
					}
				}
			}
			catch (...)
			{
				result->set_exception(std::current_exception());
				done_flag->store(true);
			}
		}
	};

	unsigned long const length = std::distance(first, last);

	if (!length)
		return last;

	//	Calculate the optimized number of threads to run the algorithm

	unsigned long const min_per_thread = 25;
	unsigned long const max_threads = (length + min_per_thread - 1) / min_per_thread;

	unsigned long const hardware_threads = std::thread::hardware_concurrency();
	unsigned long const num_threads = std::min(hardware_threads != 0 ? hardware_threads : 2, max_threads);
	unsigned long const block_size = length / num_threads;

	//	Declare the needed data structure
	std::promise<Iterator> result;
	// it is a normal boolean value, the only difference is that only one thread will be able to update it.
	std::atomic<bool> done_flag(false);

	std::vector<std::thread> threads(num_threads - 1);

	{
		join_threads joiner(threads);

		// task dividing loop
		Iterator block_start = first;
		for (unsigned long i = 0; i < (num_threads - 1); i++)
		{
			Iterator block_end = block_start;
			std::advance(block_end, block_size);

			// need to lauch threads with tasks
			threads[i] = std::thread(find_element(), block_start, block_end, match, &result, &done_flag);

			block_start = block_end;
		}

		// perform the find operation for final block in this thread.
		find_element()(block_start, last, match, &result, &done_flag);
	}

	if (!done_flag.load())
	{
		return last;
	}

	return result.get_future().get();
}

//
// Section 04.46: Parallel find algorithm implementation with async 
//

void run_04_46();

template<typename Iterator, typename MatchType>
Iterator parallel_find_async(Iterator first, Iterator last, MatchType match, std::atomic<bool>* done_flag);

void run_04_46()
{
	printf("Implementation using async tasks on the method parallel_find_async.\n");
}

template<typename Iterator, typename MatchType>
Iterator parallel_find_async(Iterator first, Iterator last, MatchType match, std::atomic<bool>* done_flag)
{
	// propagate exceptions to the calling thread, in case exceptions happen
	try
	{
		// we need now the lengh of the datachunk to be processed. Therefore, call std::distance
		unsigned long const length = std::distance(first, last);
		// minnimum size of the datachunck to be processed by a single thread.
		unsigned long const min_per_thread = 25;

		// ** BASE CASE**
		// the datachunk cannot be divided anymore. Therefore we must do the search in this datablock.
		if (length < 2 * min_per_thread)
		{
			// if the current element is not the last and done_flag is not set yet...
			for (; (first != last) && done_flag; ++first)
			{
				if (*first == match)
				{
					*done_flag = true;
					return first;
				}
			}
			return last;
		}
		// ** RECUSIVE CALL** 
		// the datablock is big enough, so it must be divided! Divide and call recursivelly!
		else
		{
			Iterator const mid_point = first + (length / 2);

			// call the method recursively for the SECOND half block!
			std::future<Iterator> async_result = std::async(
				&parallel_find_async<Iterator, MatchType>,
				mid_point,
				last,
				match,
				std::ref(done_flag)
			);
			// ... and for the FIRST half
			std::future<Iterator> direct_result = parallel_find_async(
				first,
				mid_point,
				match,
				done_flag
			);
			// once they are completed, the searching process is DONE!
			return (direct_result == mid_point) ? async_result.get() : direct_result;
		}
	}
	catch (const std::exception& ex)
	{
		*done_flag = true;
		throw ex;
	}
}

//
// Section 04.47: Partial sum algorithm introduction
//

// What is prefix sum?
//   Given a sequence of numbers, x0, ..., xn prefix sum calculate output sequence 
// y0, ..., yn where yi = y(i-1) + xi.
//   For example:
//   y0 = x0
//   y1 = y0 + x1 = x0 + x1
//   y2 = y1 + x2 = (y0 + x1) + x2 = ((x0) + x1) + x2 = x0 + x1 + x2
void run_04_47();

void test_sequential_sum(size_t vecSize);

template<typename Iterator, typename OutIterator>
void sequential_partial_sum(Iterator first, Iterator last, OutIterator y);


void run_04_47()
{
	// 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
	std::vector<int> ints(10);
	std::vector<int> outs(10);
	const char msg_seq_scan[]    = "* sequential scan: ";
	const char msg_stdpar_scan[] = "* parallel scan  : ";
	for (size_t i = 0; i < ints.size(); i++)
	{
		ints[i] = i;
	}

	// sequential implementation
	auto startTime = high_resolution_clock::now();
	sequential_partial_sum(ints.begin(), ints.end(), outs.begin());
	auto endtime = high_resolution_clock::now();
	//print the results...
	for (size_t i = 0; i < outs.size(); i++)
	{
		std::cout << outs[i] << ", ";
	}
	printf("\n");
	print_results(msg_seq_scan, startTime, endtime);

	// std parallel implementation
	startTime = high_resolution_clock::now();
	std::inclusive_scan(std::execution::par, ints.begin(), ints.end(), outs.begin());
	endtime = high_resolution_clock::now();
	print_results(msg_stdpar_scan, startTime, endtime);

	// expected result for the first test
	// 0, 1, 3, 6, 10, 15, 21, 28, 36, 45,
	// * sequential scan: :71 microseconds.
	// * parallel scan  : :327 microseconds.

	test_sequential_sum(10);
	test_sequential_sum(1000);
	test_sequential_sum(100000);
	test_sequential_sum(10000000);

}

void test_sequential_sum(size_t vecSize)
{
	const char msg_seq_scan[] = "* sequential scan: ";
	const char msg_stdpar_scan[] = "* parallel scan  : ";
	const size_t TestSize = vecSize;
	std::vector<int> ints2(TestSize);
	std::vector<int> outs2(TestSize);
	for (size_t i = 0; i < ints2.size(); i++)
	{
		ints2[i] = i;
	}
	printf("\n");
	std::cout << "Test Vector Size: " << vecSize << std::endl;

	// sequential implementation
	auto startTime = high_resolution_clock::now();
	sequential_partial_sum(ints2.begin(), ints2.end(), outs2.begin());
	auto endtime = high_resolution_clock::now();
	//print the results...
	print_results(msg_seq_scan, startTime, endtime);

	// std parallel implementation
	startTime = high_resolution_clock::now();
	std::inclusive_scan(std::execution::par, ints2.begin(), ints2.end(), outs2.begin());
	endtime = high_resolution_clock::now();
	print_results(msg_stdpar_scan, startTime, endtime);
	printf("\n");
}

template<typename Iterator, typename OutIterator>
void sequential_partial_sum(Iterator first, Iterator last, OutIterator y)
{
	unsigned long const length = std::distance(first, last);
	y[0] = first[0];

	for (size_t i = 1; i < length; i++)
	{
		y[i] = first[i] + y[i - 1];
	}
}

//
// Section 04.48: Partial sum algorithm parallel implementation
//

void run_04_48();

template<typename Iterator>
void parallel_partial_sum(Iterator first, Iterator last);


void run_04_48()
{
}


template<typename Iterator>
void parallel_partial_sum(Iterator first, Iterator last)
{
	typedef typename Iterator::value_type value_type;

	struct process_chunk
	{
		void operator()(Iterator begin, Iterator last,
			std::future<value_type>* previous_end_value,
			std::promise<value_type>* end_value)
		{
			try
			{
				Iterator end = last;
				++end;
				std::partial_sum(begin, end, begin);
				if (previous_end_value)
				{
					//this is not the first thread
					auto addend = previous_end_value->get();
					*last += addend;
					if (end_value)
					{
						//not the last block
						end_value->set_value(*last);
					}
					std::for_each(begin, last, [addend](value_type& item)
						{
							item += addend;
						});
				}
				else if (end_value)
				{
					//this is the first thread
					end_value->set_value(*last);
				}
			}
			catch (...)
			{
				if (end_value)
				{
					end_value->set_exception(std::current_exception());
				}
				else
				{
					//final block - main therad is the one process the final block
					throw;
				}
			}
		}
	};

	unsigned long const length = std::distance(first, last);
	if (!length)
	{
		return;
	}
	unsigned long const min_per_thread = 25;
	unsigned long const max_threads = (length + min_per_thread - 1) / min_per_thread;
	unsigned long const hardware_threads  =  std::thread::hardware_concurrency();
	unsigned long const num_threads = std::min(hardware_threads != 0 ? hardware_threads : 2, max_threads);
	unsigned long const block_size = length / num_threads;

	std::vector<std::thread> threads(num_threads - 1);
	std::vector<std::promise<value_type> > end_values(num_threads - 1);
	std::vector<std::future<value_type> > previous_end_values;
	previous_end_values.reserve(num_threads - 1);

	join_threads joiner(threads);
	Iterator block_start = first;

	for (unsigned long i = 0; i < (num_threads - 1); ++i)
	{
		Iterator block_last = block_start;
		std::advance(block_last, block_size - 1);
		threads[i] = std::thread(process_chunk(), 
			block_start,
			block_last,
			(i != 0) ? &previous_end_values[i - 1] : 0, 
			&end_values[i]
		);

		block_start = block_last;
		++block_start;
		previous_end_values.push_back(end_values[i].get_future());
	}

	Iterator final_element = block_start;
	std::advance(final_element, std::distance(block_start, last) - 1);
	process_chunk()(block_start, final_element, (num_threads > 1) ? &previous_end_values.back() : 0, 0);

}




//
// Section 04.49: Intorduction to Matrix
//

void run_04_49();

void run_04_49()
{
	Matrix A(10, 10);
	Matrix B(10, 10);
	Matrix results(10, 10);
	A.set_all(1);
	B.set_all(1);
	Matrix::multiply(&A, &B, &results);
	results.print();

}


//
// Section 04.50: Parallel Matrix multiplication
//

void run_04_50();

void run_04_50()
{
	const char msg_par[] = "Parallel Matrix Multiplication Time  ";
	const char msg_seq[] = "Sequential Matrix Multiplication Time";

	const int matrix_size = 200;

	Matrix A(matrix_size, matrix_size);
	Matrix B(matrix_size, matrix_size);
	Matrix C(matrix_size, matrix_size);
	Matrix D(matrix_size, matrix_size);

	A.set_all(1);
	B.set_all(1);
	
	auto startTime = high_resolution_clock::now();
	Matrix::multiply(&A, &B, &C);
	auto endTime = high_resolution_clock::now();
	print_results(msg_seq, startTime, endTime);

	startTime = high_resolution_clock::now();
	Matrix::parallel_multiply(&A, &B, &C);
	endTime = high_resolution_clock::now();
	print_results(msg_par, startTime, endTime);

}


//
// Section 04.51: Parallel Matrix transpose
//

void run_04_51();

void run_04_51()
{
	const char msg_par[] = "Parallel Matrix Transpose Time  ";
	const char msg_seq[] = "Sequential Matrix Transpose Time";

	const int matrix_size = 10000;

	Matrix A(matrix_size, matrix_size);
	Matrix B(matrix_size, matrix_size);


	A.set_all(1);


	auto startTime = high_resolution_clock::now();
	Matrix::transpose(&A, &B);
	auto endTime = high_resolution_clock::now();
	print_results(msg_seq, startTime, endTime);

	startTime = high_resolution_clock::now();
	Matrix::parallel_transpose(&A, &B);
	endTime = high_resolution_clock::now();
	print_results(msg_par, startTime, endTime);
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

void Section04::s46_parallel_find_algorithm_implementation_with_package_task()
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


