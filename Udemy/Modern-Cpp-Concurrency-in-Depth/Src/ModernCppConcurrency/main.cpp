// ModernCppConcurrency.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include "Section01.h"


int main()
{
	bool test01 = false;
	bool test02 = false;
	bool test03 = false;
	bool test04 = false;
	bool test05 = false;
	bool test06 = true;
	bool test07 = false;
	bool test08 = false;
	bool test09 = false;
	bool test10 = false;
	bool test11 = false;
	bool test12 = false;
	bool test13 = false;

	if (test01) Section01::s1_04_launch_a_thread();
	if (test02) Section01::s1_05_programming_exercise01();
	if (test03) Section01::s1_06_joinable_threads();
	if (test04) Section01::s1_07_join_and_detach_functions();
	if (test05) Section01::s1_08_handle_join_in_exceptions();
	if (test06) Section01::s1_10_how_to_pass_parameters_to_a_thread();


}
