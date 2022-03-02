# Section 09: Bonus section: parallel programming in massively parallel devices with CUDA


## Section 09.88. Elements of CUDA program


Steps of a Cuda program:

* Initialization of data from CPU
* Transfer data from CPU context to GPU context
* Kernel launch with need grid/block size
* Transfer results back to CPU context from GPU context
* Reclaim the memory from both CPU and GPU


Elements of a Cuda program

* Host code (CPU code)
* Device code (GPU code)


* Grid is a collection of all the thread lauch for the kernel

* Threads in a grid is a organized in groups called thread blocks.

* Launching a kernel function: 
Kernel name <<<number_of_blocks, thread_per_block>>>

Limitation of block size

y <= 1024
x <= 1024
z <= 64
x*y*z <= 1024



## Section 09.89




