#pragma once

class Section01
{
public:

	//
	static void s1_04_launch_a_thread();

	// Exercise 01
	//  - I want you to launch 2 threads fom the main chread call threadA and threadB
	//	- Thread A Should execute a function called functionA and the ThreadB should
	//    execute a function called FunctionB
	//	- From function A you have to launch another thread call threadC which will run 
	//    the function call test.This test function should printout hello from test
	//	- Then I want you to order the thread in the order htey are going to finish execution.
	//    First thread in the order should be the first one to finish, Last thread in the order
	//    should be the last one to finish.Consider the main thread as well
	static void s1_05_programming_exercise01();

	// Section 01.06: Joinability of threads
	// Properly constructed theread object represent an active 
	// trhead of execution in hardware level. 
	// Such a thread object is joinable. 
	// For any joinable thread, we must call either join or 
	// detach function.
	// and after we made such  a call that thread object become 
	// non joinable.
	// If you forgot to join or detach on joinable thread, then 
	// at the time of destructor call to that object 
	// std::terminat will be called.
	// If any program have std::terminate call we refer such
	// program as unsefe program.
	static void s1_06_joinable_threads();

	// Section 01.07: Join and detach functions
	// - Join bloqueia a thread até a thread que foi chamado o join retornar. 
	// - Detach permite que as thread executem independentemente.
	static void s1_07_join_and_detach_functions();

	// Section 01.08: How to handle join, in exeption scenarios
	// RAII: Resource acquisition is initialization (Constructor acquire 
	// resources, destructor releases resources)
	static void s1_08_handle_join_in_exceptions();

	// Section 01.10: How to pass parameters to a thread
	// Section 01.11: Problematic situations may arise when passing parameters to a thread 
	static void s1_10_how_to_pass_parameters_to_a_thread();

	// Section 01.12: Transfering ownership of a thread
	static void s1_12_transfering_ownership_of_a_thread();

	// Section 01.13: Some useful operations on thread
	static void s1_13_usefull_functions();

	// Section 01.15: Parallel accumulate - algorithm explanation
	static void s1_15_accumulate_explanation();

	// Section 01.15: Parallel accumulate algorithm implementation
	static void s1_16_accumulate_implementation();

	// Section 1.17: Thread local storage 
	// When you declare a variable thread_local then each thread 
	// is going to have its own, distinct, object
	// The storage duration is the entire execution of the thread in 
	// wich it as creayted, and the value stored in the object is
	// initialized when the thread is started
	// if you declara an global atomic variable, and increment it by
	// diferent threads, the value will be changed. But if you declare
	// it as thread_local, than each thread will have a local intance
	// of this same variable.
	static void s1_17_local_storage();

	static void s1_18_debuging_an_application_in_visual_studio();


private:

	static void printHeader(const char* title);
};

