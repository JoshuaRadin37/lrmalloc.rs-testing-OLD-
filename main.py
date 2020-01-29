#!/usr/bin/python3

import os
import sys
from datetime import datetime

# Original Author : Shreif Abdallah
#         University of Rochester
#         Class of 2021

"""
Forked by:  Michael Chavrimootoo
            University of Rochester
            01/17/2020

Maintained by:  Michael Chavrimootoo
                University of Rochester
"""

all_allocators = ["hoard", "jemalloc", "tcmalloc", "ptmalloc3", "supermalloc", "ralloc"]
all_benchmarks = ["t-test1", "t-test2", "larson", "threadtest", "shbench", "SuperServer"]
all_flags = ["-a", "-b", "-p", "--graph"]
new_dir = "results_{}".format(int(datetime.timestamp(datetime.now())))
#new_dir = "results_1580316919"

def main():
    gen_benchmarks_makefiles()
    os.system("cd benchmarks && make clean && make")
    allocators = collect("allocator")
    run_benchmarks(collect("benchmark"), allocators)
    if "--graph" in sys.argv:
        for allocator in all_allocators:
            make_graph("{}/larson-{}.txt".format(new_dir, allocator))

def get_benchmark_lang_flag(benchmark):
    if benchmark in ["shbench", "t-test1", "t-test2"]:
        return "CC"
    if benchmark in ["larson", "SuperServer", "threadtest"]:
        return "CXX"
    raise ValueError

def gen_benchmarks_makefiles():
    larson_simple = "$(CXX) $(CXXFLAGS) larson.cpp -o larson -lpthread; \\"
    with open("benchmarks_makefile_template", "r") as f:
        template = f.read()
    os.chdir("benchmarks") 
    for benchmark in all_benchmarks:
        try:
            lang_flag = get_benchmark_lang_flag(benchmark)
        except ValueError:
            print("Unsupported benchmark language")
            sys.exit(3)
        os.chdir(benchmark)
        with open("Makefile", "w") as f:
            f.write(template.format(benchmark, larson_simple if benchmark == "larson" else "", lang_flag))
        os.chdir("..")
    os.chdir("..")
    

def get_defaults(what):
    if what == "allocator":
        return all_allocators
    if what == "benchmark":
        return all_benchmarks
    if what == "parameter":
        return [16]


def collect_fail(what):
        print("No {} chosen, running all {}s".format(what, what))
        return get_defaults(what)

def collect(what):
    flag = "-"+what[0]
    flags = list(filter(lambda x: x != flag, all_flags))

    results = []
    try:
        start = sys.argv.index(flag) + 1
    except ValueError:
        return collect_fail(what)
    for arg in sys.argv[start:]:
        if arg in flags:
            break
        results.append(arg)
        
    if len(results) == 0:
        return collect_fail(what)
    return results


def generate_test_cmd(benchmark, allocator, num_threads):
    param_list = {
            "larson": " 10 7 8 1000 10000 1 {}".format(num_threads),
            "t-test1": " {} 2 10000 10000 400".format(num_threads),
            "t-test2": " {} 2 10000 10000 400".format(num_threads),
            "threadtest": " {} 1000 10000 0 8".format(num_threads),
            "shbench": " 1",
            "SuperServer": ""
    }
    return "cd {0} && ./{0}-{1} {2}".format(benchmark, allocator, param_list[benchmark])
    #cmd = {}
    #for allocator in all_allocators:
    #    for benchmark in all_benchmarks:
    #        cmd["{0}-{1}".format(benchmark, allocator)] = "cd {0} && ./{0}-{1} {2}".format(benchmark, allocator, param_list[benchmark])
    #
    #return cmd


def run_benchmarks(benchmarks, allocators):
    try:
        num_threads = int(collect("parameter")[0])
    except ValueError:
        print("Expected integer after -p flag")
        sys.exit()
    os.system("mkdir {}".format(new_dir))
    for allocator in allocators:
        for benchmark in benchmarks:
            bench_alloc = benchmark + "-" + allocator
            outfile = open("{}.txt".format(bench_alloc), "w")
            for i in range(num_threads):
                N=i+1
                outfile.write("----------- START {} THREAD(S) -----------\n".format(N))
                commands = generate_test_cmd(benchmark, allocator, N)
                print("Performing {} with {} thread(s)".format(bench_alloc, N))
                output = os.popen("cd benchmarks && {}".format(commands)).read()
                print(output)
                outfile.write(output)
                outfile.write("----------- END {} THREAD(S) -----------\n\n".format(N))
            outfile.write("---- OVER ----\n")
            outfile.close()
    
    os.system("mv *.txt {}".format(new_dir))


# this function takes a textfile containing raw benchmark results, splits it up, and makes x and y array
# currently supports larson benchmarking with numthreads as a parameter
# TODO other benchmarks and other parameters
def make_graph(outfile):
    print("graph making begins")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    output = open(outfile)
    throughput_list = []
    threads_list = []
    num_threads = 1
    benchmark = outfile.split("/")[1].split("-")[0]
    print("start reading {}".format(outfile))
    count = 1
    line = output.readline()
    while line:
        word_list = line.split(" ")
        while line and word_list[0] != "end":
            print("line {}".format(count))
            count += 1
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
    name = outfile.split("/")[1].split(".")[0]
    plt.title(name)
    plt.plot(threads_list, throughput_list)
    plt.savefig("{}/{}.png".format(new_dir, name))


if __name__ == "__main__":
    main()
