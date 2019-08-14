# ralloc-testing
Contains the testing scripts for the APF based memory allocator "ralloc"
# main testing script
The main testing script for this project is testing_script.py

This script runs permutations of synthetic test executables on different malloc libraries 
There are four options

'-help' which displays a manual on how to use this tool.

'-a' After which you include the names of the allocators you would like tested provided that they are supported by this implementation

'-t' After which you include the names of the tests you would like applied to the allocators you chose, there is no particualr order with which these options should be used.

'-p' After which you mention the arguments that you would like varied. There is an associated convention to this option. Currently this option only allows for variance of number of threads used by a test. This only applies to tests where number of threads is a parameter (larson, t-test1, t-test2).

'-r' The results of the tests would be outputed to output.txt and if applicable would be graphed at result.png


Current implementation supports:-

Allocators :-

tcmalloc

jemalloc

ptmalloc

Hoard

SuperMalloc

Tests:-

t-test1

t-test2

larson

threadtest

server (from SuperMalloc)

shbench (using smrtheap)


# to build


cd benchmarks

make

This will make all the test executables, you can run these individually or use testing_script.py.


# argument varying instructions

To do work with non default parameters the program has to be ran on one test at a time, here is a quick glossary on what the parameters are for each test, and which parameters could be iterated on.

Larson:-  Parameters: <number-of-threads> <iterations> <num-objects> <work-interval> <object-size>

Iterable parameters : <number-of-threads>

# usage example

./testing_script.py -a hoard -t larson -p 16 -r

This command means to use the larson test on the allocator hoard and change the number of threads from 1 to 16 and plot the throughput (y axis) vs number of threads used (x axis).


