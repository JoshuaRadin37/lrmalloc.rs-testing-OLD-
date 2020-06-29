#!/usr/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import time
import re

"""
Forked and Maintained by:  Michael Chavrimootoo
                           University of Rochester
                           01/17/2020
"""

allocator_path_map = {
    "hoard": "Hoard/src",
    "jemalloc": "jemalloc/lib",
    "tcmalloc": "gperftools",
    "supermalloc": "SuperMalloc/release/lib",  # uses transactional memory
    "libc": "",  # instead of ptmalloc3
    # "ralloc": "ralloc/target/release"
    "lrmalloc_rs_global": "lrmalloc.rs/target/release",
    "lrmalloc_rs_global_no_apf": "lrmalloc.rs.noapf/target/release"
}
benchmark_param_list = {
    "larson": "5 8 32 1000 50 11 {}",
    "t-test1": "10 {} 10000 10000 400",
    "t-test2": "10 {} 10000 10000 400",
    "threadtest": "{} 50 30000 2 8",
    "shbench": "",
    "SuperServer": "{} 20"
}
all_allocators = allocator_path_map.keys()
all_benchmarks = benchmark_param_list.keys()
all_flags = ["-a", "-b", "-t", "--graph"]
new_dir = "results_{}".format(int(datetime.timestamp(datetime.now())))


def main():
    allocators, benchmarks, num_threads = parse_args()
    gen_benchmarks_makefiles(allocators, benchmarks)
    os.system("cd benchmarks && make")
    run_benchmarks(benchmarks, allocators, num_threads)
    os.system("cd benchmarks && make clean && rm Makefile*")
    os.system("echo \"Task {} ended\" | mail -s 'ralloc-benchmarking: task completed' mchavrim@u.rochester.edu".format(new_dir))


def is_threaded(benchmark):
    return benchmark != "shbench" # everything else is multi-threaded


def get_benchmark_lang_flag(benchmark):
    if benchmark in ["shbench", "t-test1", "t-test2"]:
        return "CC"
    return "CXX" # if benchmark in ["larson", "SuperServer", "threadtest"]


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
        lang_flag = get_benchmark_lang_flag(benchmark)
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
    os.chdir("graphs")
    os.mkdir(new_dir)
    os.chdir("../benchmarks")
    for benchmark in benchmarks:
        results = {}
        text_name = "{}_{}.txt".format(benchmark, new_dir.split("_")[1])
        outfile = open(text_name, "w")
        os.chdir(benchmark)
        threaded = is_threaded(benchmark)
        bounds = range(1, num_threads+1) if threaded else range(1, 2)
        for allocator in allocators:
            results[allocator] = []
            for n in bounds:
                start_line = "-------------- [START] {}-{} with {} thread{} --------------\n"\
                    .format(benchmark, allocator, n, "s" if threaded else "")
                outfile.write(start_line)
                cmd = "./{}-{} {}".format(benchmark, allocator, benchmark_param_list[benchmark].format(n))
                print(cmd)
                sum_throughput = 0.0
                num_trials = 3
                for i in range(num_trials):  # do an average over 3 measurements
                    try:
                        outfile.write("---- ))Start Iteration {} ----".format(i+1))
                        start = time.time()
                        process = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                        end = time.time()
                        output = process.stdout.decode("utf-8")
                        outfile.write(output+"\n")
                        throughput = int(re.search("Throughput\s*=\s*(\d+)", process.stdout.decode("utf-8")).group(1)) \
                            if benchmark == "larson" else 1.0
                        throughput = throughput/(end-start)
                    except AttributeError as e:
                        print(e)
                        print("Error processing results")
                        sys.exit()
                    outfile.write("Throughput: {}\n".format(throughput))
                    outfile.write("---- End  Iteration {} ----\n\n".format(i+1))
                    sum_throughput += throughput
                average = sum_throughput/num_trials
                outfile.write("#### Average Throughput: {} ####\n".format(average))
                results[allocator].append(average)
                outfile.write("-------------- [END] --------------\n")
#        if "--graph" in sys.argv:
        outfile.close()
        os.chdir("..")
        os.rename(text_name, "../graphs/{}/{}".format(new_dir, text_name))
        make_graph(benchmark, results, num_threads)
    os.chdir("..")
    print(new_dir)


def make_graph(benchmark, results, num_threads):
    print("Generating Graph")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as g
    
    g.ylabel("Throughput")
    g.title(benchmark)
    graph_name = "{}_{}.png".format(benchmark, new_dir.split("_")[1])
    threaded = is_threaded(benchmark)
    
    if threaded:
        g.xlabel("Number of Threads")
        thread_list = list(range(1, num_threads+1))
        fig = g.figure(1)
        sp = fig.add_subplot(111)
        for allocator, time_value in results.items():
            sp.plot(thread_list, time_value, label=allocator) # this might break in the future
        lgd = sp.legend(bbox_to_anchor=(1.04, 1), loc='upper left', ncol=1)
        # text = g.text(-0.2,1.05, "", transform=g.transAxes)
        # g.savefig(graph_name, bbox_extra_artists=(lgd,text), bbox_inches='tight')
        fig.savefig(graph_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
    else:
        g.xlabel("Allocator")
        x = range(len(results))
        times, x_label = [], []
        for allocator, time_value in results.items():
            times.append(time_value[0])
            x_label.append(allocator)
        g.bar(x, times)
        g.xticks(x, x_label)
        g.savefig(graph_name)
    g.close()
    os.rename(graph_name, "../graphs/{}/{}".format(new_dir, graph_name))


if __name__ == "__main__":
    main()
