#!/usr/bin/env python3
import os
import sys
#global variables
allowed_allocators = ['Hoard','jemalloc','tcmalloc','ptmalloc', 'dlmalloc', 'ralloc']
allowed_tests = ['larson', 'cache-scratch', 't-test1', 't-test2']
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
    if( len(sys.argv) == 1 ):
        #we have no specified allocator nor test, run all allocators on all tests
        print("running all allocators with all tests with default arguments");
    elif ( '-help' in (sys.argv)):
        print("Long helpful message")
    elif ( '-t' in (sys.argv)):
        #we update the testing variable
        required_testing = verify_tests()
    elif ( '-a'  in (sys.argv)):
        print("You have chosen an allocator")
    else :
        print("no such option {} ".format(sys.argv[1]))

#here we check what tests the user chose if the user used '-t' option
def verify_tests():

        #we compile a testing array and return it, if an error occurs we exit.
        tests = []
        tIndex = sys.argv.index('-t') + 1
        print(tIndex)
        for i in (sys.argv[tIndex:]):
            if (i == '-a'):
                break
            if (i not in allowed_tests):
                raise Exception('{} is not an allowed test'.format(i))
                break
            tests.append(i)
        print(tests)
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
            if (i not in allowed_allocator):
                raise Exception('{} is not an allowed allocator'.format(i))
                break
            allocators.append(i)
        print(allocators)
        if (len(allocators) == 0):
            print("No allocators were chosen, running with all all allocators")
            return allowed_allocators
        return tests
testing_routine()
