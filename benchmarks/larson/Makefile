include ../Makefile.inc

MEMPATH = ../../memory_allocators

all: larson larson-hoard larson-jemalloc

TARGET = larson larson-hoard larson-jemalloc

larson: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -o larson -lpthread

larson-hoard: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o larson-hoard -lpthread


larson-jemalloc: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o larson-jemalloc -lpthread

clean:
	rm -f $(TARGET)
