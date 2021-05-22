#include "Captain.h"
#include <thread>



Captain::Captain()
{
}

void Captain::orderClean(Cleaners& cl)
{
	std::thread thread1(&Cleaners::clean, cl);
	thread1.detach();
}

void Captain::orderFullSpeedAhead(EngineCrew& ec)
{
	std::thread thread1(&EngineCrew::fullSpeedAhead, ec);
	if (thread1.joinable())
	{
		thread1.join();
	}
}

void Captain::orderStopTheEngine(EngineCrew& ec)
{
	std::thread thread1(&EngineCrew::stopTheEngine, ec);
	if (thread1.joinable())
	{
		thread1.join();
	}
}
