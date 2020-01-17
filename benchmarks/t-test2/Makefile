include ../Makefile.inc

all : t-test2-ptmalloc3 t-test2-hoard t-test2-tcmalloc t-test2-jemalloc t-test2-super

TARGET = t-test2-ptmalloc3 t-test2-hoard t-test2-tcmalloc t-test2-jemalloc t-test2-super

t-test2-ptmalloc3: t-test2.c
	$(CC) $(CCFLAGS) t-test2.c -L$(MEMPATH)/ptmalloc3/ -Wl,-rpath=$(MEMPATH)/ptmalloc3/ -lptmalloc3 -o t-test2-ptmalloc3 -lpthread

t-test2-hoard: t-test2.c
	$(CC) $(CCFLAGS) t-test2.c -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o t-test2-hoard -lpthread

t-test2-tcmalloc: t-test2.c
	$(CC) $(CCFLAGS) t-test2.c -L$(TCPATH) -Wl,-rpath=$(TCPATH) -ltcmalloc -o t-test2-tcmalloc -lpthread

t-test2-jemalloc: t-test2.c
	$(CC) $(CCFLAGS) t-test2.c -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o t-test2-jemalloc -lpthread

t-test2-super: t-test2.c
	$(CC) $(CCFLAGS) t-test2.c -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib -lsupermalloc -o t-test2-super -lpthread
clean:
	rm -f $(TARGET)
