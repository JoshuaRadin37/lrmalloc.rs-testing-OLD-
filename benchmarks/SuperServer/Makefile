include ../Makefile.inc

TARGET = build

build:
	
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CXX) $(CXXFLAGS) SuperServer.$(CXXEXT) -L$$path -Wl,-rpath=$$path -l$$name -o SuperServer-$$name -lpthread; \
	done;

clean:
	rm -f SuperServer-*
