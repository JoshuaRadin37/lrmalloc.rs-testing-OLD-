include ../Makefile.inc

all: server-super server-hoard server-ptmalloc server-jemalloc server-tcmalloc

TARGET = server-super server-hoard server-ptmalloc server-jemalloc server-tcmalloc

server-super: server.cc
	$(CXX) $(CXXFLAGS) server.cc -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib	-lsupermalloc -o server-super -lpthread

server-hoard: server.cc
	$(CXX) $(CXXFLAGS) server.cc -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o server-hoard -lpthread

server-ptmalloc: server.cc
	$(CXX) $(CXXFLAGS) server.cc -L$(MEMPATH)/ptmalloc3 -Wl,-rpath=$(MEMPATH)/ptmalloc3 -lptmalloc3 -o server-ptmalloc -lpthread

server-jemalloc: server.cc
	$(CXX) $(CXXFLAGS) server.cc -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o server-jemalloc -lpthread

server-tcmalloc: server.cc
	$(CXX) $(CXXFLAGS) server.cc -L$(TCPATH) -Wl,-rpath=$(TCPATH) -ltcmalloc -o server-tcmalloc -lpthread
clean:
	rm -f $(TARGET)
