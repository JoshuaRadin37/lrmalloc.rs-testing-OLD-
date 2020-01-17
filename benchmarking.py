import os
import sys

# Original Author : Shreif Abdallah
#         University of Rochester
#         Class of 2021

"""
Forked by:  Michael Chavrimootoo
            University of Rochester
            01/17/2020

Last edited by: Michael Chavrimootoo
                University of Rochester
                01/18/2020
"""

all_allocators = ["hoard", "jemalloc", "tcmalloc", "ptmalloc", "super"]
# all_allocators = ["hoard", "jemalloc", "tcmalloc", "ptmalloc", "super", "ralloc"]
all_benchmarks = ["t-test1", "t-test2", "larson", "threadtest", "shbench", "server"]
all_flags = ["-a", "-b", "-p", "--graph"]


def main():
    os.system("cd benchmarks && make clean && make")
    allocators = collect("allocator")
    run_benchmarks(collect("benchmark"), allocators)
    if "--graph" in sys.argv:
        make_graph("output.txt", allocators[0])


def get_defaults(what):
    if what == "allocator":
        return all_allocators
    if what == "benchmark":
        return all_benchmarks
    if what == "parameter":
        return [1]


def collect(what):
    flag = "-"+what[0]
    flags = list(filter(lambda x: x != flag, all_flags))

    results = []
    start = sys.argv.index(flag) + 1
    for arg in sys.argv[start:]:
        if arg in flags:
            break
        results.append(arg)
    if len(results) == 0:
        print("No {} chosen, running all {}s".format(what, what))
        return get_defaults(what)
    return results


# this function makes the command dictionary of key : benchmark name, and value : series of unix commands to run
# benchmark. Takes as input a parameters array
def make_dictionary(num_threads):
    benchmark_dirs = {
        "larson-hoard": "cd larson; ./larson-hoard 10 7 8 1000 10000 1 %s" % num_threads,
        "larson-ptmalloc": "cd larson; ./larson-ptmalloc  10 7 8 1000 10000 1 %s" % num_threads,
        "larson-jemalloc": "cd larson; ./larson-jemalloc  10 7 8 1000 10000 1 %s" % num_threads,
        "larson-super": "cd larson; ./larson-super 10 7 8 1000 10000 1 %s" % num_threads,
        "larson-tcmalloc": "cd larson; ./larson-tcmalloc 10 7 8 1000 10000 1 %s" % num_threads,
        "t-test1-hoard": "cd t-test1; ./t-test1-hoard %s 2 10000 10000 400 " % num_threads,
        "t-test1-ptmalloc": "cd t-test1; ./t-test1-ptmalloc %s 2 10000 10000 400 " % num_threads,
        "t-test1-jemalloc": "cd t-test1; ./t-test1-jemalloc %s 2 10000 10000 400 " % num_threads,
        "t-test1-super": "cd t-test1; ./t-test1-super %s 2 10000 10000 400 " % num_threads,
        "t-test1-tcmalloc": "cd t-test1; ./t-test1-tcmalloc %s 2 10000 10000 400 " % num_threads,
        "t-test2-hoard": "cd t-test2; ./t-test2-hoard %s 2 10000 10000 400 " % num_threads,
        "t-test2-ptmalloc": "cd t-test2; ./t-test2-ptmalloc %s 2 10000 10000 400 " % num_threads,
        "t-test2-jemalloc": "cd t-test2; ./t-test2-jemalloc %s 2 10000 10000 400 " % num_threads,
        "t-test2-super": "cd t-test2; ./t-test2-super %s 2 10000 10000 400 " % num_threads,
        "t-test2-tcmalloc": "cd t-test2; ./t-test2-tcmalloc %s 2 10000 10000 400 " % num_threads,
        "threadtest-hoard": "cd threadtest; ./threadtest-hoard %s 1000 10000 0 8" % num_threads,
        "threadtest-ptmalloc": "cd threadtest; ./threadtest-hoard %s 1000 10000 0 8" % num_threads,
        "threadtest-jemalloc": "cd threadtest; ./threadtest-hoard %s 1000 10000 0 8" % num_threads,
        "threadtest-super": "cd threadtest; ./threadtest-hoard %s 1000 10000 0 8" % num_threads,
        "threadtest-tcmalloc": "cd threadtest; ./threadtest-hoard %s 1000 10000 0 8" % num_threads,
        "shbench-hoard": "cd shbench; ./shbench-hoard 1",
        "shbench-ptmalloc": "cd shbench; ./shbench-ptmalloc 1",
        "shbench-jemalloc": "cd shbench; ./shbench-jemalloc 1",
        "shbench-super": "cd shbench; ./shbench-super 1",
        "shbench-tcmalloc": "cd shbench; ./shbench-tcmalloc 1",
        "server-hoard": "cd SuperServer; ./server-hoard",
        "server-ptmalloc": "cd SuperServer; ./server-hoard",
        "server-jemalloc": "cd SuperServer; ./server-hoard",
        "server-tcmalloc": "cd SuperServer; ./server-hoard",
        "server-super": "cd SuperServer; ./server-hoard"
    }

    return benchmark_dirs


# this function runs some benchmarks on some allocators, currently does not support varied parameters
#  currently only supports allocators = [hoard] and benchmarks = [larson]
def run_benchmarks(benchmarks, allocators):

    try:
        num_threads = int(collect("parameter")[0])
    except ValueError:
        print("Expected integer after -p flag")
        sys.exit()

    for allocator in allocators:
        for benchmark in benchmarks:
            bench_alloc = benchmark + "-" + allocator
            outfile = open("{}.txt".format(bench_alloc), "w")
            for i in range(num_threads):
                outfile.write("----------- START {} THREAD(S) -----------\n".format(i))
                benchmark_dirs = make_dictionary(i+1)
                print("Performing {} with {} thread(s)".format(bench_alloc, i))
                commands = benchmark_dirs.get(bench_alloc)
                output = os.popen(commands).read()
                print(output)
                outfile.write(output)
                outfile.write("----------- END {} THREAD(S) -----------\n\n".format(i))
            outfile.write("---- OVER ----\n")
            outfile.close()


# this function takes a textfile containing raw benchmark results, splits it up, and makes x and y array
# currently supports larson benchmarking with numthreads as a parameter
# TODO other benchmarks and other parameters
def make_graph(outfile, alloc):
    print("graph making begins")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    output = open(outfile)
    throughput_list = []
    threads_list = []
    line = output.readline()
    num_threads = 1
    benchmark = "none"
    alloc = "none"
    while line:
        word_list = line.split(" ")
        if "larson" in word_list:
            benchmark = "larson"
            while line and word_list[0] != "end":
                word_list = line.split(" ")
                if "Throughput" in word_list:
                    if word_list[2] == "":
                        throughput_list.append(eval(word_list[3]))
                    else:
                        throughput_list.append(eval(word_list[2]))
                    threads_list.append(num_threads)
                    num_threads = num_threads + 1
                line = output.readline()
    line = output.readline()
    print(throughput_list)
    print(threads_list)
    plt.xlabel("Number of Threads")
    plt.ylabel("Throughput")
    plt.title(benchmark + " - " + alloc)
    plt.plot(threads_list, throughput_list)
    plt.savefig("result.png")


if __name__ == "__main__":
    main()
