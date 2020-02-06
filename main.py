#!/usr/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import time

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

allocator_path_map = {
    "hoard": "Hoard/src",
    "jemalloc": "jemalloc/lib",
    "tcmalloc": "gperftools/lib",
    "ptmalloc3": "ptmalloc3",
    "supermalloc": "SuperMalloc/release/lib",
    "ralloc": "ralloc/target/release"
}
benchmark_param_list = {
    "larson": " 10 7 8 1000 10000 1 {}",
    "t-test1": " {} 2 10000 10000 400",
    "t-test2": " {} 2 10000 10000 400",
    "threadtest": " {} 1000 10000 0 8",
    "shbench": " 1",
    "SuperServer": ""
}
all_allocators = allocator_path_map.keys()
all_benchmarks = benchmark_param_list.keys()
all_flags = ["-a", "-b", "-t", "--graph"]
new_dir = "results_{}".format(int(datetime.timestamp(datetime.now())))

def main():
    allocators, benchmarks, num_threads = parse_args()
    gen_benchmarks_makefiles(allocators, benchmarks)
    os.system("cd benchmarks && make > /dev/null")
    run_benchmarks(benchmarks, allocators, num_threads)
    os.system("cd benchmarks && make clean > /dev/null && rm Makefile*")


def get_benchmark_lang_flag(benchmark):
    if benchmark in ["shbench", "t-test1", "t-test2"]:
        return "CC"
    if benchmark in ["larson", "SuperServer", "threadtest"]:
        return "CXX"
    raise ValueError


def format_allocators_used(allocators):
    path_list = []
    array_path_list = []
    array_list = []
    for allocator in allocators:
        path_list.append("{}_path := $(MEMPATH)/{}".format(allocator, allocator_path_map[allocator]))
        array_path_list.append("$({}_path)".format(allocator))
        array_list.append("[\"{0}\"]='$({0}_path)'".format(allocator))

    return "\n".join(path_list), " ".join(array_path_list), " ".join(array_list)


def gen_benchmarks_makefiles(allocators, benchmarks):
    template = "" 
    with open("templates/inc_template", "r") as f:
        template = f.read()
    assert(template != "")
    os.chdir("benchmarks") 
    with open("Makefile.inc", "w") as f:
        f.write(template.format(*format_allocators_used(allocators)))
    os.chdir("..")
    
    template = "" 
    with open("templates/benchmarks_template", "r") as f:
        template = f.read()
    assert(template != "")
    os.chdir("benchmarks") 
    with open("Makefile", "w") as f:
        f.write(template.format(" ".join(benchmarks)))
    os.chdir("..")
    template = "" 
    with open("templates/makefile_template", "r") as f:
        template = f.read()
    assert(template != "")
    os.chdir("benchmarks")
    for benchmark in benchmarks:
        os.chdir(benchmark)
        try:
            lang_flag = get_benchmark_lang_flag(benchmark)
        except ValueError:
            sys.exit(3)
        with open("Makefile", "w") as f:
            f.write(template.format(lang_flag, benchmark))
        os.chdir("..")
    os.chdir("..")


def parse_args():
    def collect(what, i):
        lst = []
        while (i < len(sys.argv)) and (sys.argv[i] not in list(filter(lambda x: x != what, all_flags))):
            lst.append(sys.argv[i])
            i += 1
        return lst, i

    alloc, bench, threads = ([], )*3
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == "-a":
            assert(len(alloc) == 0)
            alloc, i = collect("-a", i+1)
        elif sys.argv[i] == "-b":
            assert(len(bench) == 0)
            bench, i = collect("-b", i+1)
        elif sys.argv[i] == "-t":
            assert(len(threads) == 0)
            threads, i = collect("-t", i+1)
            assert(len(threads) == 1)
        else:
            i += 1
    alloc = all_allocators if len(alloc) == 0 else alloc
    bench = all_benchmarks if len(bench) == 0 else bench
    try:
        threads = 16 if len(threads) == 0 else int(threads[0])
    except ValueError:
        print("-t expects an integer")
        sys.exit(2)
    return alloc, bench, threads

    
def run_benchmarks(benchmarks, allocators, num_threads):
    thread_list = list(range(1, num_threads+1))

    os.chdir("benchmarks")
    for benchmark in benchmarks:
        results = {}
        print(benchmark)
        for allocator in allocators:
            print(allocator)
            results[allocator] = []

            for n in thread_list:
                print("Thread {} starting".format(n))
                cmd = "./{0}/{0}-{1} {2}".format(benchmark, allocator, benchmark_param_list[benchmark].format(num_threads))
                start = time.time()
                try:
                    process = subprocess.run(cmd.split(" "), capture_output=True)
                    end = time.time()
                except FileNotFoundError:
                    sys.exit()
                print(end-start)
                results[allocator].append(end-start)
                print("Thread {} over".format(n))
#        if "--graph" in sys.argv:
        make_graph(benchmark, results, num_threads)
    os.chdir("..")


def make_graph(benchmark, results, num_threads):
    print("Generating Graph")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as g
    
    g.xlabel("Number of Threads")
    g.ylabel("Time/s")

    thread_list = list(range(1, num_threads+1))
    for allocator, time_value in results.items():
        g.plot(thread_list, time_value, label=allocator)
    
    g.legend()
    g.title(benchmark)
    graph_name = "{}_{}.png".format(benchmark, new_dir.split("_")[1])
    g.savefig(graph_name)
    os.rename(graph_name, "../graphs/{}".format(graph_name))

if __name__ == "__main__":
    main()
