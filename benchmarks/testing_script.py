#!/usr/bin/env python3
#Author : Shreif Abdallah
#         University of Rochester
#         Class of 2021
import os
import sys
import subprocess
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

            outfile = run_tests(required_testing, required_allocators)
            if ( '-r' in (sys.argv)):
                make_graph('output.txt')
#here we check what tests the user chose if the user used '-t' option
def verify_tests():

        #we compile a testing array and return it, if an error occurs we exit.
        tests = []
        tIndex = sys.argv.index('-t') + 1
        for i in (sys.argv[tIndex:]):
            if (i == '-a') or (i == '-p') or (i == '-r'):
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
            if (i == '-t') or (i =='-p') or (i == '-r'):
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
            if (i == '-t') or (i =='-a') or (i == '-r'):
                break
            #TODO could do an eval step here and catch errors
            try:
                parameter_array.append(eval(i))
            except(ValueError, SyntaxError):
                print("The entered parameters are incorrect");

    return parameter_array

#this function makes the command dictionary of key : test name, and value : series of unix commands to run test
#takes as input a parameters array
def make_dictionary(numthreads):

    
    test_dirs = {
                'larson-hoard':'cd larson; ./larson-hoard 10 7 8 1000 10000 1 %s' % numthreads,
                'larson-ptmalloc':'cd larson; ./larson-ptmalloc  10 7 8 1000 10000 1 %s' % numthreads,
                'larson-jemalloc':'cd larson; ./larson-jemalloc  10 7 8 1000 10000 1 %s' % numthreads, 
                'larson-super':'cd larson; ./larson-super 10 7 8 1000 10000 1 %s' % numthreads ,
                'larson-tcmalloc':'cd larson; ./larson-tcmalloc 10 7 8 1000 10000 1 %s' % numthreads ,
                't-test1-hoard': 'cd t-test1; ./t-test1-hoard %s 2 10000 10000 400 ' % numthreads ,
                't-test1-ptmalloc': 'cd t-test1; ./t-test1-ptmalloc %s 2 10000 10000 400 ' % numthreads ,
                't-test1-jemalloc': 'cd t-test1; ./t-test1-jemalloc %s 2 10000 10000 400 ' % numthreads ,
                't-test1-super': 'cd t-test1; ./t-test1-super %s 2 10000 10000 400 ' % numthreads , 
                't-test1-tcmalloc': 'cd t-test1; ./t-test1-tcmalloc %s 2 10000 10000 400 ' % numthreads , 
                't-test2-hoard': 'cd t-test2; ./t-test2-hoard %s 2 10000 10000 400 ' % numthreads ,
                't-test2-ptmalloc': 'cd t-test2; ./t-test2-ptmalloc %s 2 10000 10000 400 ' % numthreads ,
                't-test2-jemalloc': 'cd t-test2; ./t-test2-jemalloc %s 2 10000 10000 400 ' % numthreads ,
                't-test2-super': 'cd t-test2; ./t-test2-super %s 2 10000 10000 400 ' % numthreads ,
                't-test2-tcmalloc': 'cd t-test2; ./t-test2-tcmalloc %s 2 10000 10000 400 ' % numthreads ,
                'threadtest-hoard' : 'cd threadtest; ./threadtest-hoard %s 1000 10000 0 8' % numthreads ,
                'threadtest-ptmalloc' : 'cd threadtest; ./threadtest-hoard %s 1000 10000 0 8' % numthreads ,
                'threadtest-jemalloc' : 'cd threadtest; ./threadtest-hoard %s 1000 10000 0 8' % numthreads ,
                'threadtest-super' : 'cd threadtest; ./threadtest-hoard %s 1000 10000 0 8' % numthreads ,
                'threadtest-tcmalloc' : 'cd threadtest; ./threadtest-hoard %s 1000 10000 0 8' % numthreads ,
                'shbench-hoard' : 'cd shbench; ./shbench-hoard 1' ,
                'shbench-ptmalloc' : 'cd shbench; ./shbench-ptmalloc 1' ,
                'shbench-jemalloc' : 'cd shbench; ./shbench-jemalloc 1' ,
                'shbench-super' : 'cd shbench; ./shbench-super 1' ,
                'shbench-tcmalloc' : 'cd shbench; ./shbench-tcmalloc 1',
                'server-hoard' : 'cd SuperServer; ./server-hoard',
                'server-ptmalloc' : 'cd SuperServer; ./server-hoard',
                'server-jemalloc' : 'cd SuperServer; ./server-hoard',
                'server-tcmalloc' : 'cd SuperServer; ./server-hoard',
                'server-super' : 'cd SuperServer; ./server-hoard'
                 }

    return test_dirs

#this function runs some tests on some allocators, currently does not support varied parameters
#currently only supports allocators = [hoard] and tests = [larson]
def run_tests(tests, allocators):
    outfile = open('output.txt', 'w');
    numthreads = capture_parameters()[0]
    #for each allocator, run tests
    #dictionary between tests and their locations
    for alloc in allocators:
        for test in tests:
            #TODO could write a specific line with test name to the outfile, and then decide which algorithm to use based on this
            outfile.write(test+ " \n")
            for i in range (1, numthreads+1):
                test_dirs = make_dictionary(i)
                test_key = test + "-" + alloc
                print(test_key)
                commands = test_dirs.get(test_key)
                output = os.popen(commands).read()
                print(output)
                outfile.write(output)
            outfile.write("end \n")
    outfile.close()
#this function takes a textfile containing raw test results, splits it up, and makes x and y array
#currently supports larson testing with numthreads as a parameter
#TODO other tests and other parameters
def make_graph(outfile):
    print("graph making begins")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    output = open(outfile)
    throughput_list = []
    threads_list = []
    line = output.readline()
    numthreads = 1
    test = "none"
    while line:
        word_list = line.split(" ")
        if('larson' in word_list):
            test = "larson"
            while line and word_list[0] is not 'end':
                word_list = line.split(" ")
                if('Throughput' in word_list):
                    if(word_list[2] is ''):
                        throughput_list.append(word_list[3])
                    else:
                        throughput_list.append(word_list[2])
                    threads_list.append(numthreads)
                    numthreads = numthreads + 1
                line = output.readline()
    line = output.readline()
    print(throughput_list)
    print(threads_list)
    plt.xlabel("Number of Threads")
    plt.ylabel("Throughput (operations per second)")
    plt.title(test)
    plt.plot(threads_list,throughput_list)
    plt.savefig('result.png')
testing_routine()
