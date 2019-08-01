include ../Makefile.inc

MEMPATH = ../../memory_allocators

all: larson larson-hoard

TARGET = larson larson-hoard

larson: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -o larson -lpthread

larson-hoard: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o larson-hoard -lpthread

clean:
	rm -f $(TARGET)
