include ../Makefile.inc

all : t-test1-ptmalloc3

TARGET = t-test1-ptmalloc3

MEMPATH = ../../memory_allocators/

t-test1-ptmalloc3: t-test1.c
	$(CC) $(CCFLAGS) t-test1.c -L$(MEMPATH)/ptmalloc3/ -Wl,-rpath=$(MEMPATH)/ptmalloc3/ -lptmalloc3 -o t-test1-ptmalloc3 -lpthread



clean:
	rm -f $(TARGET)
