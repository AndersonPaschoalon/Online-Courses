#include "Section06.h"
#include "Utils.h"
#include "SpinlockMutex.h";

void run_06_59();
void run_06_60();
void run_06_61();
void run_06_62();
void run_06_63();
void run_06_64();
void run_06_65();
void run_06_66();
void run_06_67();
void run_06_68();
void run_06_69();
void run_06_70();
void run_06_71();
void run_06_72();
void run_06_73();
void run_06_74();
void run_06_75();


//
// ----------------------------------------------------
//

void run_06_59()
{


}

//
// ----------------------------------------------------
//

void run_06_60()
{
	std::atomic_flag flag2 = ATOMIC_FLAG_INIT;

	std::cout << "1. Previous flag value : " << flag2.test_and_set() << std::endl;
	std::cout << "2. Previous flag value : " << flag2.test_and_set() << std::endl;

	flag2.clear();
	std::cout << "3. Previous flag value : " << flag2.test_and_set() << std::endl;
}

//
// ----------------------------------------------------
//

// Function on atomic bool
// * is_lock_free()
// * store()
// * load()
// * exchange(): replace the stored value with new one and atomically retrive the original one
// * compoare_exchange_weak()
// * compoare_exchange_string()

void s6_atomicbool_test01();
void s6_atomicbool_test02();

void run_06_61()
{
	s6_atomicbool_test01();
	s6_atomicbool_test02();
}

void s6_atomicbool_test01()
{
	// assaigned as true by default
	std::atomic<bool> flag_1;
	std::cout << "flag1 = " << flag_1 << std::endl;

	//// cannot copy construct
	//std::atomic<bool> flag_2(flag_1);

	//// cannot copy assignable
	//std::atomic<bool> flag_3 = flag_1;

	// construct using non atomic boolean value
	bool non_atomic_bool = true;
	std::atomic<bool> flag_4(non_atomic_bool);
	std::cout << "flag 4 = " << flag_4 << std::endl;

	// assing non atomic boolean value
	std::atomic<bool> flag_5 = non_atomic_bool;
	std::cout << "falg_5 = " << flag_5 << std::endl;
}

void s6_atomicbool_test02()
{
	std::atomic <bool> x(false);
	std::cout << "atomic boolean is implemented lock free - " << (x.is_lock_free() ? "yes" : "no") << std::endl;

	std::atomic<bool> y(true);

	// store operations 
	x.store(false);
	x.store(y);

	// load operations
	std::cout << "value of the atomic bool y - " << y.load() << std::endl;

	// exchange operation
	bool z = x.exchange(false);

	std::cout << "current value of atomic bool x = " << x.load() << std::endl;
	std::cout << "previous value of atomic bool x = " << z << std::endl;
}

//
// ----------------------------------------------------
//


void run_06_62()
{
	// std::atomic::compare_exchange_weak
	// (1)	
	// 
	// bool compare_exchange_weak (T& expected, T val,
	//            memory_order sync = memory_order_seq_cst) volatile noexcept;
	// bool compare_exchange_weak (T& expected, T val,
	//            memory_order sync = memory_order_seq_cst) noexcept;
	// 
	// (2)	
	// 
	// bool compare_exchange_weak (T& expected, T val,
	//            memory_order success, memory_order failure) volatile noexcept;
	// bool compare_exchange_weak (T& expected, T val,
	//            memory_order success, memory_order failure) noexcept;
	// 
	// Compare and exchange contained value (weak)
	// Compares the contents of the atomic object's contained value with expected:
	// - if true, it replaces the contained value with val (like store).
	// - if false, it replaces expected with the contained value .
	// 
	// The function always accesses the contained value to read it, and -if the
	// comparison is true- it then also replaces it. But the entire operation is
	// atomic: the value cannot be modified by other threads between the instant its
	// value is read and the moment it is replaced.
	// 
	// The memory order used in (2) depends on the result of the comparison: if true, 
	// it uses success; if false, it uses failure.
	// 
	// Note that this function compares directly the physical contents of the
	// contained value with the contents of expected; This may result in
	// failed comparisons for values that compare equal using operator== (if the
	// underlying type has padding bits, trap values, or alternate representations
	// of the same value), although this comparison shall converge rapidly in a loop
	// that preserves expected.
	// 
	// Unlike compare_exchange_strong, this weak version is allowed to fail
	// spuriously by returning false even when expected indeed compares equal to the
	// contained object. This may be acceptable behavior for certain looping 
	// algorithms, and may lead to significantly better performance on some 
	// platforms. On these spurious failures, the function returns false while not
	// modifying expected.
	// 
	// For non-looping algorithms, compare_exchange_strong is generally preferred.

}

//
// ----------------------------------------------------
//


void run_06_63()
{
}

//
// ----------------------------------------------------
//


void run_06_64()
{
}

//
// ----------------------------------------------------
//


void run_06_65()
{
}

//
// ----------------------------------------------------
//


void run_06_66()
{
}

//
// ----------------------------------------------------
//
std::atomic<bool> s6_67_x = false;
std::atomic<bool> s6_67_y = false;
std::atomic<int> s6_67_z = 0;

void s6_67_write_x();
void s6_67_write_y();
void s6_67_read_x_then_y();
void s6_67_read_y_then_x();

void run_06_67()
{
	for (int i = 0; i < 50; i++)
	{
		s6_67_x = false;
		s6_67_y = false;
		s6_67_z = 0;

		std::thread thread_a(s6_67_write_x);
		std::thread thread_b(s6_67_write_y);
		std::thread thread_c(s6_67_read_x_then_y);
		std::thread thread_d(s6_67_read_y_then_x);

		thread_a.join();
		thread_b.join();
		thread_c.join();
		thread_d.join();

		printf("z is %d\n", s6_67_z.load());
	}



}

void s6_67_write_x()
{
	s6_67_x.store(true, std::memory_order_seq_cst);
}

void s6_67_write_y()
{
	s6_67_y.store(true, std::memory_order_seq_cst);
}

void s6_67_read_x_then_y()
{
	while (!s6_67_x.load(std::memory_order_seq_cst))
	{
	}
	if (s6_67_y.load(std::memory_order_seq_cst))
	{
		s6_67_z++;
	}

}

void s6_67_read_y_then_x()
{
	while (!s6_67_y.load(std::memory_order_seq_cst))
	{
	}
	if (s6_67_x.load(std::memory_order_seq_cst))
	{
		s6_67_z++;
	}
}


//
// ----------------------------------------------------
//


void run_06_68()
{
}

//
// ----------------------------------------------------
//

std::atomic<bool> s06_69_x;
std::atomic<bool> s06_69_y;
std::atomic<int> s06_69_z;

void s06_69_write_x_then_y();
void s06_69_read_y_then_x();

void run_06_69()
{
	for (int i = 0; i < 50; i++)
	{
		s06_69_x = false;
		s06_69_y = false;
		s06_69_z = 0;

		std::thread writer_thread(s06_69_write_x_then_y);
		std::thread reader_thread(s06_69_read_y_then_x);
		writer_thread.join();
		reader_thread.join();

		if (s06_69_z == 0)
		{
			printf("z value is %d\n", s06_69_z.load());
		}

	}
	printf("done\n");
}


void s06_69_write_x_then_y()
{
	s06_69_x.store(true, std::memory_order_relaxed);
	s06_69_y.store(true, std::memory_order_relaxed);
}

void s06_69_read_y_then_x()
{
	while (!s06_69_y.load(std::memory_order_relaxed));
	if (s06_69_x.load(std::memory_order_relaxed))
	{
		s06_69_z++;
	}
}

//
// ----------------------------------------------------
//


void run_06_70()
{
}

//
// ----------------------------------------------------
//


void run_06_71()
{
}

//
// ----------------------------------------------------
//


void run_06_72()
{
}

//
// ----------------------------------------------------
//


void run_06_73()
{
}

//
// ----------------------------------------------------
//


void run_06_74()
{
}

//
// ----------------------------------------------------
//

SpinlockMutex s6_75_mutex;

void s6_75_function();

void run_06_75()
{
	std::thread thread_1(s6_75_function);
	std::thread thread_2(s6_75_function);
	thread_1.join();
	thread_2.join();

}

void s6_75_function()
{
	std::lock_guard<SpinlockMutex> lg(s6_75_mutex);

	std::cout << std::this_thread::get_id() << ": hello " << std::endl;
	std::this_thread::sleep_for(std::chrono::microseconds(5000));
}

//
// ----------------------------------------------------
//


void Section06::s6_59_Introduction_to_atomic_operations()
{
	Utils::printHeader("// Section 06.59 - Introduction to atomic operations");
	run_06_59();
}

void Section06::s6_60_Functionality_of_stdatomic_flag()
{
	Utils::printHeader("// Section 06.60 - Functionality of std::atomic_flag");
	run_06_60();
}

void Section06::s6_61_Functionality_of_stdatomic_bool()
{
	Utils::printHeader("// Section 06.61 - Functionality of std::atomic_bool");
	run_06_61();
}

void Section06::s6_62_Explanation_of_compare_exchange_functions()
{
	Utils::printHeader("// Section 06.62 - Explanation of compare_exchange functions");
	run_06_62();
}

void Section06::s6_63_atomic_pointers()
{
	Utils::printHeader("// Section 06.63 - atomic pointers");
	run_06_63();
}

void Section06::s6_64_General_discussion_on_atomic_types()
{
	Utils::printHeader("// Section 06.64 - General discussion on atomic types");
	run_06_64();
}

void Section06::s6_65_Important_relationships_related_to_atomic_operations_between_threads()
{
	Utils::printHeader("// Section 06.65 - Section 06.65 - Important relationships related to atomic operations between threads");
	run_06_65();
}

void Section06::s6_66_Introduction_to_memory_ordering_options()
{
	Utils::printHeader("// Section 06.66 - Introduction to memory ordering options");
	run_06_66();
}

void Section06::s6_67_Discussion_on_memory_order_seq_cst()
{
	Utils::printHeader("// Section 06.67 - Discussion on memory_order_seq_cst");
	run_06_67();
}

void Section06::s6_68_Introduction_to_instruction_reordering()
{
	Utils::printHeader("// Section 06.68 - Introduction to instruction reordering");
	run_06_68();
}

void Section06::s6_69_Discussion_on_memory_order_relaxed()
{
	Utils::printHeader("// Section 06.69 - Discussion on memory_order_relaxed");
	run_06_69();
}

void Section06::s6_70_Discussion_on_memory_order_acquire_and_memory_order_release()
{
	Utils::printHeader("// Section 06.70 - Discussion on memory_order_acquire and memory_order_release");
	run_06_70();
}

void Section06::s6_71_Important_aspects_of_memory_order_acquire_and_memory_order_release()
{
	Utils::printHeader("// Section 06.71 - Important aspects of memory_order_acquire and memory_order_release");
	run_06_71();
}

void Section06::s6_72_Concept_of_transitive_synchronization()
{
	Utils::printHeader("// Section 06.72 - Concept of transitive synchronization");
	run_06_72();
}

void Section06::s6_73_Discussion_on_memory_order_consume()
{
	Utils::printHeader("// Section 06.73 - Discussion on memory_order_consume");
	run_06_73();
}

void Section06::s6_74_Concept_of_release_sequence()
{
	Utils::printHeader("// Section 06.74 - Concept of release sequence");
	run_06_74();
}

void Section06::s6_75_Implementation_of_spin_lock_mutex()
{
	Utils::printHeader("// Section 06.75 - Implementation of spin lock mutex");
	run_06_75();
}






