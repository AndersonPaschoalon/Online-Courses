//
//  main.cpp
//  FreeStoreVsHeap
//

#include <iostream>
#include "JarJar.h"

int main(int argc, const char * argv[])
{
    // Using the stack
    {
        JarJar binks;
    } // end of scope

    
    
    
    
    // Using the free store
    JarJar* freeStoreJarJar = new JarJar();
    delete freeStoreJarJar;
    
    
    
    
    // Using the heap
    JarJar* heapJarJar = (JarJar*)malloc(sizeof(JarJar));
    free(heapJarJar);
    
    return 0;
}
