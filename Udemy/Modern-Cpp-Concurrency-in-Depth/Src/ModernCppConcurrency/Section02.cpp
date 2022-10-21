#include "Section02.h"
#include <iostream>
#include <mutex>
#include <list>
#include <thread>
#include "ThreadSafeStack2.h"
#include "ThreadSafeStack.h"

///////////////////////////////////////////////////////////////////////////////
// SECTION 02 - EXERCISES
///////////////////////////////////////////////////////////////////////////////

//
// Section 02.21
// 
void run_02_21();
#define LOCK_MANUAL 1
#define LOCK_LOCKGUARD 1

std::list<int> s02_21_myList;
std::mutex s02_21_m;
void s02_21_add_to_list(int const& x);
int s02_21_size();

void run_02_21()
{
	s02_21_size();
	std::thread thread_1(s02_21_add_to_list, 4);
	std::thread thread_2(s02_21_add_to_list, 11);
	thread_1.join();
	thread_2.join();
	s02_21_size();
}
void s02_21_add_to_list(int const& x)
{
#ifdef LOCK_LOCKGUARD
	std::lock_guard<std::mutex> lg(s02_21_m);
	s02_21_myList.push_front(x);
#else // LOCK_MANUAL
	s02_21_m.lock();
	s02_21_myList.push_front(x);
	s02_21_m.unlock();
#endif

}
int s02_21_size()
{
#ifdef LOCK_LOCKGUARD
	std::lock_guard<std::mutex> lg(s02_21_m);
	int size = s02_21_myList.size();
#else // LOCK_MANUAL
	s02_21_m.lock();
	int size = s02_21_myList.size();
	s02_21_m.unlock();
#endif
	std::cout << "size of the list s02_21_myList is:{" << size << "}" << std::endl;
	return size;
}

//
// Section 02.24-25
// 

void run_02_24();
void run_02_25();

void run_02_24()
{
	//	ThreadSafeStack s = ThreadSafeStack();
}

void run_02_25()
{
	//	ThreadSafeStack2 s = ThreadSafeStack2();
}

//
// Section 02.26
// 

///////////////////////////////////////////////////////////////////////////////
// SECTION 02 - MAIN CLASS
///////////////////////////////////////////////////////////////////////////////

void Section02::s2_21_mutexes()
{
	run_02_21();
}

void Section02::s2_24_thrad_safe_implementation()
{
	run_02_24();
}

void Section02::s2_25_thrad_safe_implementation_race_condition_inherit_from_the_interface()
{
	run_02_25();
}
