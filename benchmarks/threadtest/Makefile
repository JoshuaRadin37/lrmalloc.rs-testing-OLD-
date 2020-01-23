include ../Makefile.inc
  
all: build

build:
	declare -A PATHS=($(ALLOCNAMES)); \
    for name in $${!PATHS[@]}; do \
        path=$${PATHS[$$name]}; \
        echo $$path; \
        $(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$$path -Wl,-rpath=$$path -l$$name -o threadtest-$$name -lpthread; \
    done;

clean:
	rm -f $(TARGET)
