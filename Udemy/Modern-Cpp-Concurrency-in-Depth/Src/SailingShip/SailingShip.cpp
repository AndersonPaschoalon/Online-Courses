// SailingShip.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>

#include "EngineCrew.h"
#include "Cleaners.h"
#include "Captain.h"

void menu();

int main()
{
    Captain captain;
    EngineCrew engineCrew;
    Cleaners cleanners;
    const int CMD_START_CLEANING = 1;
    const int CMD_FULL_SPEED = 2;
    const int CMD_STOP = 3;
    const int CMD_EXIT = 100;

    int opt = 0;
    while (true)
    {
        menu();

        std::string inputStr;
        std::cin >> inputStr;
        opt = atoi(inputStr.c_str());
        
        switch (opt)
        {
            case CMD_START_CLEANING:
            {
                captain.orderClean(cleanners);
                break;
            }
            case CMD_FULL_SPEED:
            {
                captain.orderFullSpeedAhead(engineCrew);
                break;
            }
            case CMD_STOP:
            {
                captain.orderStopTheEngine(engineCrew);
                break;
            }
            case CMD_EXIT:
            {
                break;
            }
            default:
            {
                break;
            }
        }

        if (opt == CMD_EXIT)
        {
            break;
        }
    }

   
}

void menu()
{
    std::cout << "CAPTAIN ORDERS" << std::endl;
    std::cout << "001 - START CLEANING" << std::endl;
    std::cout << "002 - FULL SPEED AHEAD" << std::endl;
    std::cout << "003 - STOP ENGINE" << std::endl;
    std::cout << "100 - EXIT" << std::endl;
}
