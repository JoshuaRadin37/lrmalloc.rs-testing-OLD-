#!/usr/bin/env python3
import os
import sys
#global variables
allowed_allocators = ['hoard','jemalloc','tcmalloc','ptmalloc','super']
allowed_tests = ['larson', 'threadtest', 't-test1', 't-test2','server','shbench']
#this function cleans all the testing executables and remakes everything.
def make_start():
        
    print("Welcome to ralloc testing");
    makeCmd = 'make'
    cleanCmd = 'make clean'
    os.system(cleanCmd)
    os.system(makeCmd)
    testing_routine()
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
            if (i == '-a') or (i == '-p'):
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
            if (i == '-t') or (i =='-p'):
                break
            if (i not in allowed_allocators):
                raise Exception('{} is not an allowed allocator'.format(i))
                break
            allocators.append(i)
        if (len(allocators) == 0):
            print("No allocators were chosen, running with all all allocators")
            return allowed_allocators
        return allocators
#this function captures parameters from the command line and returns a parameter array, currently supports changing number of threads
#current convention is :
#0th index is number of threads to be used by multithreaded tests
def capture_parameters():
    #default values
    numthreads = 1
    parameter_array = [numthreads]
    #the user has decided to specify parameters 
    if('-p' in sys.argv):
        parameter_array = []
        numThreadIndex = sys.argv.index('-p') + 1;
        for i in (sys.argv[numThreadIndex:]):
            if (i == '-t') or (i =='-a'):
                break
            #TODO could do an eval step here and catch errors
            try:
                parameter_array.append(eval(i))
            except(ValueError, SyntaxError):
                print("The entered parameters are incorrect");

    return parameter_array

#this function makes the command dictionary of key : test name, and value : series of unix commands to run test
def make_dictionary(numthreads):
    
    test_dirs = {
                'larson-hoard':'cd larson; ./larson-hoard 10 7 8 1000 10000 1 %s' % numthreads,
                'larson-ptmalloc':'cd larson; ./larson-ptmalloc  10 7 8 1000 10000 1 1',
                'larson-jemalloc':'cd larson; ./larson-jemalloc  10 7 8 1000 10000 1 1',
                'larson-super':'cd larson; ./larson-super 10 7 8 1000 10000 1 1',
                'larson-tcmalloc':'cd larson; ./larson-tcmalloc 10 7 8 1000 10000 1 1',
              #  't-test1-hoard': ''
              #  't-test1-ptmalloc' : ''
              #  't-test1-jemalloc' : ''
              #  't-test1-super' : ''
              #  't-test2-hoard' : ''
              #  't-test2-ptmalloc' : ''
              #  't-test2-jemalloc' : ''
              #  't-test2-super'  : ''
              #  'server-hoard ' : ''
              #  'server-ptmalloc' : ''
              #  'server-jemalloc' : ''
              #  'server-super' : ''
              #  'threadtest-hoard' : ''
              #  'threadtest-ptmalloc' : ''
              #  'threadtest-jemalloc' : ''
              #  'threadtest-super'   : ''
              #  'shbench-hoard' : ''
              #  'shbench-ptmalloc' : ''
              #  'shbench-jemalloc' : ''
              #  'shbench-super' : ''
                 }

    return test_dirs
#this function runs some tests on some allocators, currently does not support varied parameters
#currently only supports allocators = [hoard] and tests = [larson]
def run_tests(tests, allocators):
    numthreads = capture_parameters()[0];

    #for each allocator, run tests
    #dictionary between tests and their locations
    for alloc in allocators:
        for test in tests:
            for i in range (1, numthreads+1):
                test_dirs = make_dictionary(i)
                test_key = test + "-" + alloc
                print(test_key)
                os.system(test_dirs.get(test_key))
testing_routine()
