# Section 01: Thread management Guide

## Section.01.01-05

- Youtube
https://www.youtube.com/channel/UCMlGfpWw-RUdWX_JbLCukXg
https://www.youtube.com/channel/UCAczr0j6ZuiVaiGFZ4qxApw

- CompilerExplorer
https://godbolt.org/

- C++ compiler support
https://en.cppreference.com/w/cpp/compiler_support

- Course Code
https://github.com/kasunindikaliyanage/cpp_concurrency_masterclass


- Para linkar o programa a lib de threads:
```
-std=c++20 -fcoroutines -pthread
```

## Section.01.06

Properly constructed theread object represent an active trhead of execution in hardware level. 
Such a thread object is joinable. 

For any joinable thread, we must call either join or detach function

and after we made such  a call that thread object become non joinable

if you forgot to join or detach on joinable thread, then at the time of destructor call to that object std::terminat will be called

if any program have std::terminate call we refer such program as unsefe program


## Section.01.07

- Join bloqueia a thread principal ate a thread filha retornar.

- Detach permite que as thread executem independentemente.


## Section.01.08

RAII: Resource acquisition is initialization (Constructor acquire resources, destructor releases resources)


