# ralloc-benchmarking
Contains the testing scripts to perform benchmarking of `ralloc` and other allocators

# Script
The main script for this project is `main.py`

This script runs simplifies the task of running specific benchmarks on desired allocators and collecting results.

There are currently four command line flags:
````
-a <allocator name>

-b <benchmark name>

-t <number of threads>
````

Allocator options: `tcmalloc`, `jemalloc`, `ptmalloc`, `Hoard`, `SuperMalloc`, `ralloc`

Benchmark options: `t-test1`, `t-test2`, `larson`, `threadtest`, `SuperServer`, `shbench`

# To Build
````
cd benchmarks
make
````
This will make all the test executables, you can run these individually or use `main.py`.
