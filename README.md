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

-c [all|alloc|bench|none]
````

Graphs are automatically generated

Allocator options: `tcmalloc`, `jemalloc`, `libc`, `Hoard`, `SuperMalloc`, `ralloc`

Benchmark options: `t-test1`, `t-test2`, `larson`, `threadtest`, `SuperServer`, `shbench`

# To Run
````
For `-c`, independent of the choice, the benchmarks will still run. If you just want to compile things, go to the corresponding \
folder and use the Makefile in there.
````
