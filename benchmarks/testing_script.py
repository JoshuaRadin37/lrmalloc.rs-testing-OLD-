#!/usr/bin/env python3
import os
import sys
#global variables
allowed_allocators = ['hoard','jemalloc','tcmalloc','ptmalloc', 'dlmalloc', 'ralloc']
allowed_tests = ['larson', 'threadtest', 't-test1', 't-test2']
#this function cleans all the testing executables and remakes everything.
def make_start():
        
    print("Welcome to ralloc testing");
    makeCmd = 'make'
    cleanCmd = 'make clean'
    os.system(cleanCmd)
    os.system(makeCmd)

def testing_routine():
    #required testing and allocators, by default set to perform all tests on all allocators
    required_testing = allowed_tests
    required_allocators = allowed_allocators

    #check the size of sys.argv
    if(len(sys.argv) == 1):
        #we have no specified allocator nor test, run all allocators on all tests
        print("running all allocators with all tests with default arguments")
    
    if( '-help' in (sys.argv)):
        print("Long helpful message")
    else:
            if ( '-t' in (sys.argv)):
                #we update the testing list
                required_testing = verify_tests()
            if ( '-a'  in (sys.argv)):
                #we update the allocators list
                required_allocators = verify_allocators()

            run_tests(required_testing, required_allocators)
#here we check what tests the user chose if the user used '-t' option
def verify_tests():

        #we compile a testing array and return it, if an error occurs we exit.
        tests = []
        tIndex = sys.argv.index('-t') + 1
        for i in (sys.argv[tIndex:]):
            if (i == '-a'):
                break
            if (i not in allowed_tests):
                raise Exception('{} is not an allowed test'.format(i))
                break
            tests.append(i)
        if (len(tests) == 0):
            print("No tests were chosen, running with all tests")
            return allowed_tests
        return tests


#here we check what allocators the user chose if the user used '-a' option
def verify_allocators():

        #we compile a testing array and return it, if an error occurs we exit.
        allocators = []
        aIndex = sys.argv.index('-a') + 1
        for i in (sys.argv[aIndex:]):
            if (i == '-t'):
                break
            if (i not in allowed_allocators):
                raise Exception('{} is not an allowed allocator'.format(i))
                break
            allocators.append(i)
        if (len(allocators) == 0):
            print("No allocators were chosen, running with all all allocators")
            return allowed_allocators
        return allocators
#this function runs some tests on some allocators, currently does not support varied parameters
#currently only supports allocators = [hoard] and tests = [larson]
def run_tests(tests, allocators):

    #for each allocator, run tests
    #dictionary between tests and their locations
    test_dirs = {
                'larson-hoard':'cd larson; ./larson-hoard 1 1 1 1 1 1 1'
            }
    for alloc in allocators:
        for test in tests:
            test_key = test + "-" + alloc
            print(test_key)
           # os.system(test_dirs.get(test_key))
testing_routine()
