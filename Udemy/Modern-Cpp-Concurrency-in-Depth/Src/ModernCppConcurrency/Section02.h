#pragma once

class Section02
{
public:
	// Section 02.20: Introduction to locking mechanisms

	// This sections tries to issue a problematic case of race condition.
	// to push an elemento to the top of a list you must update the pointer next
	// of your node, and update the pointer head from the list, so the new node will
	// be the new first element. If two thread tries to update the list at the 
	// same time, only one node will be pointed by the head pointer, a the other 
	// node will be lost.
	static void s2_21_mutexes();

	static void s2_24_thrad_safe_implementation();

	static void s2_25_thrad_safe_implementation_race_condition_inherit_from_the_interface();

private:
};

