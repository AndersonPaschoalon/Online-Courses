#include "Section07.h"
#include "lock_free_stack.h"
#include "Utils.h"

void run_07_76();
void run_07_77();
void run_07_78();
void run_07_79();
void run_07_80();
void run_07_81();

//
// ----------------------------------------------------
//

void run_07_76()
{

}

//
// ----------------------------------------------------
//

lock_free_stack s_07_77_stk((int)1);


void s_07_77_update_lock_free_stack();

void run_07_77()
{
	std::thread update1(s_07_77_update_lock_free_stack);
	std::thread update2(s_07_77_update_lock_free_stack);
	update1.join();
	update2.join();
	s_07_77_stk.showInfo();
}


void s_07_77_update_lock_free_stack()
{
	for (int i = 0; i < 500; i++)
	{
		s_07_77_stk.push(i);
	}
}


//
// ----------------------------------------------------
//


void run_07_78()
{
}

//
// ----------------------------------------------------
//


void run_07_79()
{
}

//
// ----------------------------------------------------
//


void run_07_80()
{
}

//
// ----------------------------------------------------
//


void run_07_81()
{
}


//
// ----------------------------------------------------
//


void Section07::s7_76_Introduction_and_some_terminology()
{
	Utils::printHeader("// Section 07.76 - Introduction and some terminology");
	run_07_76();
}

void Section07::s7_77_Stack_recap()
{
	Utils::printHeader("// Section 07.77 - Stack recap");
	run_07_77();
}

void Section07::s7_78_Simple_lock_free_thread_safe_stack()
{
	Utils::printHeader("// Section 07.78 - Simple lock free thread safe stack");
	run_07_78();
}

void Section07::s7_79_Stack_memory_reclaim_mechanism_using_thread_counting()
{
	Utils::printHeader("// Section 07.79 - Stack memory reclaim mechanism using thread counting");
	run_07_79();
}

void Section07::s7_80_Stack_memory_reclaim_mechanism_using_hazard_pointers()
{
	Utils::printHeader("// Section 07.80 - Stack memory reclaim mechanism using hazard pointers");
	run_07_80();
}

void Section07::s7_81_Stack_memory_reclaim_mechanism_using_reference_counting()
{
	Utils::printHeader("// Section 07.81 - Stack memory reclaim mechanism using reference counting");
	run_07_81();
}








