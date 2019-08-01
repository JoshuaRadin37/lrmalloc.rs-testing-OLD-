include ../Makefile.inc

all : threadtest threadtest-hoard

TARGET = threadtest threadtest-hoard

MEMPATH = ../../memory_allocators/

threadtest-hoard: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o threadtest-hoard -lpthread


threadtest: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -o threadtest -lpthread
#	$(CXX) -std=c++14 $(CXXFLAGS) -fsized-deallocation threadtest.cpp -o $(TARGET) -lpthread

clean:
	rm -f $(TARGET)
