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

all_allocators = ["hoard", "jemalloc", "tcmalloc", "ptmalloc3", "supermalloc", "ralloc"]
all_benchmarks = ["t-test1", "t-test2", "larson", "threadtest", "shbench", "SuperServer"]
all_flags = ["-a", "-b", "-p", "--graph"]
new_dir = "results_{}".format(int(datetime.timestamp(datetime.now())))

def main():
    gen_benchmarks_makefiles()
    os.system("cd benchmarks && make clean && make")
    allocators = collect("allocator")
    num_threads = int(collect("parameter")[0])
    results = run_benchmarks(collect("benchmark"), allocators, num_threads)
    if "--graph" in sys.argv:
        make_graph(results, num_threads)

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
    # currently using time command because we don't need super precise metrics
    return "./{0}/{0}-{1} {2}".format(benchmark, allocator, param_list[benchmark])
    #return "time ./{0}/{0}-{1} {2}".format(benchmark, allocator, param_list[benchmark])


def run_benchmarks(benchmarks, allocators, num_threads):
    thread_list = list(range(1, num_threads+1))
    os.mkdir(new_dir)

    """
        results -> allocators -> benchmarks -> [data; num_threads]  ; data is currently time
    """
    os.chdir("benchmarks")
    for benchmark in benchmarks:
        results = {}
        for allocator in allocators:
            results[allocator] = []
            bench_alloc = benchmark + "-" + allocator
            #outfile = open("{}.txt".format(bench_alloc), "w")

            for n in thread_list:
                #outfile.write("----------- START {} THREAD(S) -----------\n".format(n))
                cmd = generate_test_cmd(benchmark, allocator, n)
                start = time.time()
                proc = subprocess.run(cmd.split(" ")) #, capture_output=True)
                end = time.time()
                # _, stderr = map(lambda x: x.decode("utf-8"), (proc.stdout, proc.stderr))
                # outfile.write(stdout)
                # outfile.write("----------- END {} THREAD(S) -----------\n\n".format(n))
                #try:
                #    time = float(stderr.split("\n")[0].split(" ")[1])
                #except ValueError:
                #    print("Time command results could not be parsed")
                #    print(stderr)
                #    sys.exit(3)
    
                results[allocator].append(end-start)
            
            #outfile.write("---- OVER ----\n")
            #outfile.close()
        if "--graph" in sys.argv:
            make_graph(benchmark, results, num_threads)
    os.chdir("..")
    #os.system("mv benchmarks/*.txt {}".format(new_dir))

# Supports: 
# larson
# shbench
# SuperServer

#def parse_result(outfile):
#    output = open(outfile)
#    throughput = []
#    threads = []
#    num_threads = None
#    while line = output.readline():
#        line_list = line.split(" ")
#        if line_list[1] == "START" and line_list[3] == "THREAD(S)":
#            threads.append(int(line_list[2])
#        if line_list[0] == "Throughput:":
#            throughput.append(float(line_list[2]))
#    return (throughputs, threads)
#

"""
Todo: Add legend for charts
      Combine results to have single chart per allocator
"""

def make_graph(benchmark, results, num_threads):
    print("Generating Graph")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as g
    
   # coloring = {
   #     "hoard": "blue",  
   #     "jemalloc": "yellow",
   #     "ptmalloc3": "green",
   #     "supermalloc": "violet",
   #     "tcmalloc": "brown",
   #     "ralloc": "red"
   # }

    g.xlabel("Number of Threads")
    g.ylabel("Time/s")

    thread_list = list(range(1, num_threads+1))
    for allocator, time in results.items():
        g.plot(thread_list, time, label=allocator) #, color="tab:"+coloring[allocator], linelength=0.05)
    
    g.legend()
    g.title(benchmark)
    g.savefig("{}.png".format(benchmark))
    os.rename(*("{0}.png ../{1}/{0}.png".format(benchmark, new_dir).split(" ")))


if __name__ == "__main__":
    main()
