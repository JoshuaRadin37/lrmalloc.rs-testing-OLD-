include ../Makefile.inc

TARGET = build

build:
	
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CXX) $(CXXFLAGS) threadtest.$(CXXEXT) -L$$path -Wl,-rpath=$$path -l$$name -o threadtest-$$name -lpthread; \
	done;

clean:
	rm -f threadtest-*
