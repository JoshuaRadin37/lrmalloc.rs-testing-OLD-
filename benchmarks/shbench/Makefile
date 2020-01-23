include ../Makefile.inc

all: build

build:
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CXX) $(CXXFLAGS) shbench.c -L$$path -Wl,-rpath=$$path -l$$name -o shbench-$$name -lpthread; \
	done;

clean:
	rm -f $(TARGET)
