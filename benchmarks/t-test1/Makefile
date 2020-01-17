include ../Makefile.inc

all : t-test1-ptmalloc3 t-test1-hoard t-test1-tcmalloc t-test1-jemalloc t-test1-super

TARGET = t-test1-ptmalloc3 t-test1-hoard t-test1-tcmalloc t-test1-jemalloc t-test1-super

t-test1-ptmalloc3: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/ptmalloc3/ -Wl,-rpath=$(MEMPATH)/ptmalloc3/ -lptmalloc3 -o t-test1-ptmalloc3 -lpthread

t-test1-hoard: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o t-test1-hoard -lpthread

t-test1-tcmalloc: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/gperftools -Wl,-rpath=$(TCPATH) -ltcmalloc -o t-test1-tcmalloc -lpthread

t-test1-jemalloc: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o t-test1-jemalloc -lpthread

t-test1-super: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib -lsupermalloc -o t-test1-super -lpthread

clean:
	rm -f $(TARGET)
