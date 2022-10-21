#include <iostream>
#include <chrono>
#include <thread>


#include "Section05.h"
#include "Utils.h"
#include "jthread.h"

using namespace std::chrono_literals;

void run_05_53();


void run_05_54();


void run_05_55();


void run_05_56();


void run_05_57();


void run_05_58();


//
// ----------------------------------------------------
//

void do_some_work();
void test_stop_token(std::stop_token token);
void test_stop_token_noninterruptable();

void run_05_53()
{
	// Automatically join the threads if this one go out of scope
	std::jthread thread1(do_some_work);

	// stop thread execution

	std::cout << std::endl;
	std::jthread nonInterruptible(test_stop_token_noninterruptable);
	std::jthread interruptible(test_stop_token);

	std::this_thread::sleep_for(1.0s);
	interruptible.request_stop();
	nonInterruptible.request_stop();
	std::cout << std::endl;

}

void do_some_work()
{
	std::cout << "Do some work\n";
}

void test_stop_token(std::stop_token token)
{
	int counter = 0;
	while (counter < 10)
	{
		if (token.stop_requested())
		{
			std::cout << "* Thread interrupted when counter is " << counter << std::endl;
			return;
		}

		// do some work
		std::this_thread::sleep_for(0.2s);
		std::cout << "* This is the interruptible thread: " << counter << std::endl;
		++counter;
	}
}

void test_stop_token_noninterruptable()
{
	int counter = 0;
	while (counter < 10)
	{
		// do some work
		std::this_thread::sleep_for(0.2s);
		std::cout << "# This is the noninterruptable thread: " << counter << std::endl;
		++counter;
	}
}

//
// ----------------------------------------------------
//

void test_stop_token2();
void test_stop_token_noninterruptable2();

void run_05_54()
{
	// stop thread execution

	std::cout << std::endl;
	jthread_local nonInterruptible(test_stop_token_noninterruptable2);
	jthread_local interruptible(test_stop_token2);

	std::this_thread::sleep_for(1.0s);
	interruptible.interrupt();
	nonInterruptible.interrupt();
	std::cout << std::endl;

}


void test_stop_token2()
{
	int counter = 0;
	while (counter < 10)
	{
		if (interrupt_point())
		{
			std::cout << "* Thread interrupted when counter is " << counter << std::endl;
			return;
		}

		// do some work
		std::this_thread::sleep_for(0.2s);
		std::cout << "* This is the interruptible thread: " << counter << std::endl;
		++counter;
	}
}

void test_stop_token_noninterruptable2()
{
	int counter = 0;
	while (counter < 10)
	{
		// do some work
		std::this_thread::sleep_for(0.2s);
		std::cout << "# This is the noninterruptable thread: " << counter << std::endl;
		++counter;
	}
}


//
// ----------------------------------------------------
//

void run_05_55()
{
}

//
// ----------------------------------------------------
//

void s56_foo();

void run_05_56()
{
	s56_foo();
}

void s56_foo()
{
}


//
// ----------------------------------------------------
//

void run_05_57()
{
}

//
// ----------------------------------------------------
//

void run_05_58()
{
}

void Section05::s5_53_Jthread_Introduction()
{
	Utils::printHeader("// Section 05.53 - Jthread : Introduction");
	run_05_53();
}

void Section05::s5_54_Jthread_Our_own_version_implementation()
{
	Utils::printHeader("// Section 05.54 - Jthread : Our own version implementation");
	run_05_54();
}

void Section05::s5_55_Cpp_coroutines_Introduction()
{
	Utils::printHeader("// Section 05.55 - C++ coroutines : Introduction");
	run_05_55();
}

void Section05::s5_56_Cpp_coroutines_resume_functions()
{
	Utils::printHeader("// Section 05.56 - C++ coroutines : resume functions");
	run_05_56();
}

void Section05::s5_57_Cpp_coroutines_Generators()
{
	Utils::printHeader("// Section 05.57 - C++ coroutines : Generators");
	run_05_57();
}

void Section05::s5_58_Cpp_Barriers()
{
	Utils::printHeader("// Section 05.58 - C++ Barriers");
	run_05_58();
}


