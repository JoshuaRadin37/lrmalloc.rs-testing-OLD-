# ralloc-testing
Contains the testing scripts for the APF based memory allocator "ralloc"
# main testing script
The main testing script for this project is testing_script.py
This script runs permutations of synthetic test executables on different malloc libraries 
There are three options, '-help' which displays a manual on how to use this tool.
'-a' After which you include the names of the allocators you would like tested provided that they are supported by this implementation
'-t' After which you include the names of the tests you would like applied to the allocators you chose, there is no particualr order with which these options should be used.
Current implementation supports:-

Allocators :-

tcmalloc
jemalloc
ptmalloc
Hoard

Tests:-

t-test1
t-test2
larson
threadtest
# to build

To build the tests you can either run testing_script.py with the preferred arguments as mentioned above, or

cd benchmarks

make


This will make all the tests included in this package and you can run these tests individually

# argument varying instructions

To do work with non default parameters the program has to be ran on one test at a time, here is a quick glossary on what the parameters are for each test, and which parameters could be iterated on.

Larson:-  Parameters: <number-of-threads> <iterations> <num-objects> <work-interval> <object-size>

Iterable parameters : <number-of-threads>


