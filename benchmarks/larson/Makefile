include ../Makefile.inc

all: larson larson-hoard larson-jemalloc larson-tcmalloc larson-ptmalloc larson-super

TARGET = larson larson-hoard larson-jemalloc larson-tcmalloc larson-ptmalloc larson-super

larson: larson.cpp
	($(CXX) $(CXXFLAGS) larson.cpp -o larson -lpthread)

larson-hoard: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o larson-hoard -lpthread

larson-jemalloc: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o larson-jemalloc -lpthread

larson-ptmalloc: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/ptmalloc3 -Wl,-rpath=$(MEMPATH)/ptmalloc3 -lptmalloc3 -o larson-ptmalloc -lpthread

larson-super: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib -lsupermalloc -o larson-super -lpthread

larson-tcmalloc: larson.cpp
	$(CXX) $(CXXFLAGS) larson.cpp -L$(TCPATH) -Wl,-rpath=$(TCPATH) -ltcmalloc -o larson-tcmalloc -lpthread

clean:
	rm -f $(TARGET)
