// ModernCppConcurrency.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include "Section01.h"
#include "Section02.h"
#include "Section03.h"
#include "Section04.h"
#include "Section05.h"
#include "Section06.h"
#include "Section07.h"
#include "Section08.h"
#include "Section09.h"


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
	bool test23 = false;
	bool test24 = false; // init
	bool test25 = false;
	bool test26 = false;
	bool test27 = false;
	bool test28 = false; // test
	bool test29 = false;
	bool test30 = false;
	bool test31 = false;
	bool test32 = false;
	bool test33 = false;
	bool test34 = false;
	bool test35 = false;
	bool test36 = false;
	bool test37 = false;
	bool test38 = false;
	bool test39 = false;
	bool test40 = false;
	bool test41 = false;
	bool test42 = false;
	bool test43 = false;
	bool test44 = false;
	bool test45 = false;
	bool test46 = false;
	bool test47 = false;
	bool test48 = false;
	bool test49 = false;
	bool test50 = true;
	bool test51 = true;
	bool test52 = true;
	bool test53 = true;
	bool test54 = true;
	bool test55 = true;
	bool test56 = true;
	bool test57 = true;
	bool test58 = true;
	bool test59 = true;
	bool test60 = true;


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

	//
	// Section 04
	//

	if (test24) Section04::s39_introduction_to_lock_based_thread_safe_data_structures_and_algotithms();
	if (test25) Section04::s41_thread_sage_queue_implementation();
	if (test26) Section04::s42_parallel_ste_intruduction();
	if (test27) Section04::s43_parallel_quick_sort_algorithm_implementation();
	if (test28) Section04::s44_parallel_for_each_implementation();
	if (test29) Section04::s45_parallel_for_each_implementation();
	if (test30) Section04::s46_parallel_find_algorithm_implementation_with_package_task();
	if (test31) Section04::s47_partial_sum_algorithm_introduction();
	if (test32) Section04::s48_partial_sum_algorithm_implementation();
	if (test33) Section04::s49_introduction_to_matrix();
	if (test34) Section04::s50_parallel_matrix_multiplication();
	if (test34) Section04::s51_paralle_matrix_transpose();

	//
	// Section 05
	//
	if (test35) Section05::s5_53_Jthread_Introduction();
	if (test36) Section05::s5_54_Jthread_Our_own_version_implementation();
	if (test37) Section05::s5_55_Cpp_coroutines_Introduction();
	if (test38) Section05::s5_56_Cpp_coroutines_resume_functions();
	if (test39) Section05::s5_57_Cpp_coroutines_Generators();
	if (test40) Section05::s5_58_Cpp_Barriers();

	//
	// section 06
	//
	if (test41) Section06::s6_60_Functionality_of_stdatomic_flag();
	if (test42) Section06::s6_61_Functionality_of_stdatomic_bool();
	if (test43) Section06::s6_62_Explanation_of_compare_exchange_functions();
	if (test44) Section06::s6_67_Discussion_on_memory_order_seq_cst();
	if (test45) Section06::s6_69_Discussion_on_memory_order_relaxed();
	if (test46) Section06::s6_75_Implementation_of_spin_lock_mutex();


	//
	// Section 07
	//
	if (test47) Section07::s7_76_Introduction_and_some_terminology();
	if (test48) Section07::s7_77_Stack_recap();

	//
	// Section 08
	// 
	if (test49) Section08::s8_82_Simple_thread_pool();
	if (test50) Section08::s8_83_Thread_pool_which_allowed_to_wait_on_submitted_tasks();

	return 0;
}
