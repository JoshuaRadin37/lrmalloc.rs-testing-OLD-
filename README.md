# ralloc-benchmarking
Contains the testing scripts to perform benchmarking on `ralloc` and other allocators (for comparison purposes)

# Script
The main script for this project is `benchmarking.py`

This script runs simplifies the task of running specific benchmarks on desired allocators and collecting results.

There are currently four command line flags:
````
-a <allocator name>

-b <benchmark name>

-p <number of threads> Only works with `larson`, `t-test1`, and `t-test2`

--graph     The results of the tests would be outputed to output.txt and if applicable would be graphed at result.png. This option supports only the larson test for now.
````

Allocator options: `tcmalloc`, `jemalloc`, `ptmalloc`, `Hoard`, `SuperMalloc`

Benchmark options: `t-test1`, `t-test2`, `larson`, `threadtest`, `server` (from `SuperMalloc`), `shbench` (using `smrtheap`)

# To Build
````
cd benchmarks
make
````
This will make all the test executables, you can run these individually or use testing_script.py.


[This makes no sense. Will need to look into how each test is being run and do a proper mapping. this is a sloppy job]

# argument varying instructions

To do work with non default parameters the program has to be ran on one test at a time, here is a quick glossary on what the parameters are for each test, and which parameters could be iterated on.

Larson:-  Parameters: <number-of-threads> <iterations> <num-objects> <work-interval> <object-size>

Iterable parameters : <number-of-threads>