// ModernCppConcurrency.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include "Section01.h"
#include "Section02.h"
#include "Section03.h"


int main()
{
	bool test01 = false;
	bool test02 = false;
	bool test03 = false;
	bool test04 = false;
	bool test05 = false;
	bool test06 = false;
	bool test07 = false;
	bool test08 = false;
	bool test09 = false;
	bool test10 = false;
	bool test11 = false;
	bool test12 = false;
	bool test13 = false;
	bool test14 = false;
	bool test15 = false;
	bool test16 = false;
	bool test17 = false;
	bool test18 = false;
	bool test19 = false;
	bool test20 = false;
	bool test21 = false;
	bool test22 = false;
	bool test23 = true;
	bool test24 = true;
	bool test25 = true;
	bool test26 = true;
	bool test27 = true;
	bool test28 = true;
	bool test29 = true;
	bool test30 = true;
	bool test31 = true;
	bool test32 = true;
	bool test33 = true;
	bool test34 = true;
	bool test35 = true;
	bool test36 = true;
	bool test37 = true;
	bool test38 = true;

	//
	// Section 01
	//

	if (test01) Section01::s1_04_launch_a_thread();
	if (test02) Section01::s1_05_programming_exercise01();
	if (test03) Section01::s1_06_joinable_threads();
	if (test04) Section01::s1_07_join_and_detach_functions();
	if (test05) Section01::s1_08_handle_join_in_exceptions();
	if (test06) Section01::s1_10_how_to_pass_parameters_to_a_thread();
	if (test07) Section01::s1_12_transfering_ownership_of_a_thread();
	if (test08) Section01::s1_13_usefull_functions();
	if (test09) Section01::s1_15_accumulate_explanation();
	if (test10) Section01::s1_16_accumulate_implementation();
	if (test11) Section01::s1_17_local_storage();
	if (test12) Section01::s1_18_debuging_an_application_in_visual_studio();

	//
	// Section 02
	//

	if (test13) Section02::s2_21_mutexes();

	//
	// Section 03
	//

	if (test14) Section3::s3_28_introduction_to_condition_variables();
	if (test15) Section3::s3_29_details_about_condition_variables();
	if (test16) Section3::s3_31_thread_safe_queue_implementation();
	if (test17) Section3::s3_32_introduction_to_futures_and_async_tasks();
	if (test18) Section3::s03_33_async_task_details_discussion();
	if (test19) Section3::s3_34_parallel_accumulate_algorithm();
	if (test20) Section3::s3_35_introduction_to_package_tasks();
	if (test21) Section3::s3_36_communication_between_threads_using_promisses();
	if (test22) Section3::s3_37_retrieving_exception_using_futures();
	if (test23) Section3::s3_38_shared_futures();


	return 0;
}
