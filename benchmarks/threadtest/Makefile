include ../Makefile.inc

all : threadtest threadtest-hoard threadtest-tcmalloc threadtest-ptmalloc threadtest-jemalloc

TARGET = threadtest threadtest-hoard threadtest-tcmalloc threadtest-ptmalloc threadtest-jemalloc

threadtest-hoard: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o threadtest-hoard -lpthread

threadtest-tcmalloc: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(TCPATH) -Wl,-rpath=$(TCPATH) -ltcmalloc -o threadtest-tcmalloc -lpthread

threadtest-ptmalloc: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(MEMPATH)/ptmalloc3 -Wl,-rpath=$(MEMPATH)/ptmalloc3 -lptmalloc3 -o threadtest-ptmalloc -lpthread

threadtest-jemalloc: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o threadtest-jemalloc -lpthread

threadtest-super: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib -lsupermalloc -o threadtest-super -lpthread
threadtest: threadtest.cpp
	$(CXX) -std=c++14 $(CXXFLAGS) threadtest.cpp -o threadtest -lpthread
#	$(CXX) -std=c++14 $(CXXFLAGS) -fsized-deallocation threadtest.cpp -o $(TARGET) -lpthread

clean:
	rm -f $(TARGET)
