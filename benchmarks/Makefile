BENCHMARKS = t-test1 t-test2 larson threadtest shbench SuperServer

all:
	for benchmark in $(BENCHMARKS); do \
		cd $$benchmark && make && cd .. ; \
	done;

clean:
	for benchmark in $(BENCHMARKS); do \
		cd $$benchmark && make clean && cd .. ; \
	done;
