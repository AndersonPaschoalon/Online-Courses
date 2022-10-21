# Section 01

## Memory Model Introduction
Memory Segments in C++
* Free Store (C it is called Heap!)
* Stack 
* Global Data
* Code



# Section 02: Elements on Modern C++

## RAII: Resource Acquisition Is initialization

Old C++ : **Rule of tree**: if you need to implement a destruction, than you NEED to implement a copy assignment and a copy constructor as Well (Destructor+CopyAssignment+CopyConstructor).

Modern C++: **Rule of Five**. Move semants has been introduced, you need to implement a move asignment and a move constructor as well.

SOLID Object -> when we store an instance of an object locally or is it part of another object, we just call this a solid object. 

## Smart pointers

Pointers types: 
*    `std::unique_ptr`, 
*    `std::shared_ptr`, 
*    `std::weak_ptr`

Deprecates old `std::auto_ptr`: sometimes had unexpected behaviour, replace these with std::unique_ptr

Smart pointers is a STACK BASED DATA STRUCT. Must be created on the stack, just like any standard library container. DONT EVER WRITE write `std::unique_ptr<double>* ptr`;

## UNIQUE POINTERS

Data struct stored on stack 
* Out of scope => delete pointer
* can create and return unique_ptr
* Not copyable => NEED DEEP COPY
* Clear ownership => Clear code
* Very samll overhead => Fast

Creting a Unique Pointer:
1.  `std:;make_unique<T>`
2.  `Consttructor`
3.  `.reset(T* ptr)`

----

Creating a unique Pointer

std::make_unique
* Best wat to create a unique pointer
* std::unique_ptr<foo> a = std::make_unique<foo>();
	* Creates object of type foo (default constructor) on free store and stores in unique pointer
* std::unique_ptr<foo> a = std::uinique_ptr<foo>(3.141, bar);
	* Creates object of type foo on free store, passing in 3.14 and bar to constryuctor and stores in unique pointer.
* Only available since C++14, your compiler may not support it yet...


Creating a Unique Pointer

std::unique_ptr<foo>(T* ptr);
* Creates a unique pointer from an existing pointer
* Takes ownership of pointer => Will delete this pointer later (DONT USE DELETE IN THE POINTER)
* std::unique_ptr<foo> a(new foo())


Creating a Unique Pointer using reset

reset(T* ptr)
	* Creates a unique pointer from an existing pointer
	* takes ownership of pointer => Will delete this pointer later
	* Deletes currently stored pointer (if any)
		* std::unique_ptr<foo> a;
		* a.reset(new foo());
	*  Reset without arguments will delete contents

Once you have a unique pointer, you can work with it much like any raw pointer

// Instantiation
std::unique_ptr<foo> a = std::make_unique<foo>();
// * Get Pointer
foo* contents = a.get()
a->bar() // Equals to a.get()->bar()
// Delete contents
a.reset()
// Check if empty
if(a) { /*Not empty*/ } else {/* Empty */}


* UNIQUE POINTER IS NOT COPYABLE!!!
		* To pass a pointer to a function you need to move it to the function
		* my_function(std::move(a));
		* Out of scope pointer will be emptied 
	* Pass by reference to "lend" out pointer
		* Passing const eference shows that pointer will not be deleted





# Section 03