include ../Makefile.inc

all : shbench-ptmalloc3 shbench-hoard shbench-tcmalloc shbench-jemalloc shbench-super

TARGET = shbench-ptmalloc3 shbench-hoard shbench-tcmalloc shbench-jemalloc shbench-super

shbench-ptmalloc3: shbench.c
	$(CC) $(CCFLAGS) shbench.c -L$(MEMPATH)/ptmalloc3/ -Wl,-rpath=$(MEMPATH)/ptmalloc3/ -lptmalloc3 -o shbench-ptmalloc3 -lpthread

shbench-hoard: shbench.c
	$(CC) $(CCFLAGS) shbench.c -L$(MEMPATH)/Hoard/src -Wl,-rpath=$(MEMPATH)/Hoard/src -lhoard -o shbench-hoard -lpthread

shbench-tcmalloc: shbench.c
	$(CC) $(CCFLAGS) shbench.c -L$(TCPATH) -Wl,-rpath=$(TCPATH) -ltcmalloc -o shbench-tcmalloc -lpthread

shbench-jemalloc: shbench.c
	$(CC) $(CCFLAGS) shbench.c -L$(MEMPATH)/jemalloc/lib -Wl,-rpath=$(MEMPATH)/jemalloc/lib -ljemalloc -o shbench-jemalloc -lpthread

shbench-super: shbench.c
	$(CC) $(CCFLAGS) shbench.c -L$(MEMPATH)/SuperMalloc/release/lib -Wl,-rpath=$(MEMPATH)/SuperMalloc/release/lib -lsupermalloc -o shbench-super -lpthread

clean:
	rm -f $(TARGET)
