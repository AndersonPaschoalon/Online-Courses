#include "Cleaners.h"
#include <iostream>
#include <chrono>
#include <thread>

Cleaners::Cleaners()
{
}

void Cleaners::clean()
{
	std::this_thread::sleep_for(std::chrono::milliseconds(10000));
	std::cout << "Finished cleanning\n";
}
