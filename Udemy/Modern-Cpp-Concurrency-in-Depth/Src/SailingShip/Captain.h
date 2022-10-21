#pragma once
#include "Cleaners.h"
#include "EngineCrew.h"

class Captain
{
public:
	Captain();

	// Captain does not have to wait on this command until its done
	void orderClean(Cleaners& cl);

	//has to wait
	void orderFullSpeedAhead(EngineCrew& ec);
	void orderStopTheEngine(EngineCrew& ec);
private:
};

