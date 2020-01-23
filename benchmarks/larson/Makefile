include ../Makefile.inc

all: build

build:
	$(CXX) $(CXXFLAGS) larson.cpp -o larson -lpthread; \
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CXX) $(CXXFLAGS) larson.cpp -L$$path -Wl,-rpath=$$path -l$$name -o larson-$$name -lpthread; \
	done;

clean:
	rm -f $(TARGET)
