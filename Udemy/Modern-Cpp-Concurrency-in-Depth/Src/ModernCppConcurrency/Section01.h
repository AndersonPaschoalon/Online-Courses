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

	//
	static void s1_06_joinable_threads();

	// 
	static void s1_07_join_and_detach_functions();

	// 
	static void s1_08_handle_join_in_exceptions();

	// 
	static void s1_10_how_to_pass_parameters_to_a_thread();

	//
	static void s1_15_accumulate_explanation();

	// 
	static void s1_16_accumulate_implementation();

	//
	static void s1_17_local_storage();


private:

	static void printHeader(const char* title);
};

