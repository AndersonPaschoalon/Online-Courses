#include "EngineCrew.h"
#include <iostream>
#include <chrono>
#include <thread>

EngineCrew::EngineCrew()
{
}

void EngineCrew::fullSpeedAhead()
{
	std::this_thread::sleep_for(std::chrono::milliseconds(1000));
	std::cout << "Finished fullSpeedAhead\n";
}

void EngineCrew::stopTheEngine()
{
	std::this_thread::sleep_for(std::chrono::milliseconds(1000));
	std::cout << "Finished stopTheEngine\n";
}
