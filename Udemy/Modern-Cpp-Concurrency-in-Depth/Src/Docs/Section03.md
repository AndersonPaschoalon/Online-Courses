# Section 03: Communication between thread using condition variables

## Section 03.33

*   In C++ assynchronous operatin can be created via std::async 
    std::async(std::launch policy, Function&& f, Args&&... args);

*   Policies: 
    std::lanch::async => runs the function in another thread;  
    std::launch::deferred => is called when the future is called

*   Separated using vertical bar -- use both => the compiler will tell witch use

## Section 03.35

*   package_task: another way of creatiing async operations

*   the class templace std::packaged_task wraps anyu callable target so that it can be invoked asynchronously

*   Package task can be considered as much insider layer, than the async.

*   Theoretically speaking, you can even implement async using pakaged_task

*   Its return value or exeption thrown, is stored in a shared state which can be accessed through std::future objects.

*   packaged_task<ReturnType(ArgsTypes)>. Eg.: supouse a function int func(int a, int b) => std::packaged_task<int(int, int)> task(callableObject)

## Section 03.36

*   Each std::promise object is paired with a std::future object

*   A thread with access to the std::future object can wait for the result to be set, while another thread that has access to the corresponding std::primisse object can call set_value() to store the value and make the future ready.


## Section 03.37

*   The idea is that an exception on a thread can be propagated to another, if it is waiting the first one
to response.

## Section 03.38

*   Futures are objects of single use. If two threads try to use get() from the same future, the second one will throw and exception, since the resource was already consumed, and therefore is invalid. For this scenario, you have to use shared futures.


void run_03_38();
void s3_38_print_result(std::future<int>& fut);

void s3_38_print_result(std::future<int>& fut)
{
    std::cout << fut.get() << "\n";
}

void run_03_38()
{
    std::promise<int> prom;
    std::future<int> fut(prom.get_future());

    std::thread th1(s3_38_print_result, std::ref(fut));
    std::thread th2(s3_38_print_result, std::ref(fut));

    prom.set_value(5)

    th1.join(); 
    th2.join(); 
}


