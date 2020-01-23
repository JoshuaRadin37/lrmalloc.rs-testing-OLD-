include ../Makefile.inc

all: build

build:
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CXX) $(CXXFLAGS) server.cc -L$$path -Wl,-rpath=$$path -l$$name -o server-$$name -lpthread; \
	done;

clean:
	rm -f $(TARGET)