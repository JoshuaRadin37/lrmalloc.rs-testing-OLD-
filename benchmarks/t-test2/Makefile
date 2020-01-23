include ../Makefile.inc
  
all: build

build:
	declare -A PATHS=($(ALLOCNAMES)); \
    for name in $${!PATHS[@]}; do \
        path=$${PATHS[$$name]}; \
        echo $$path; \
        $(CC) $(CCCFLAGS) t-test2.c -L$$path -Wl,-rpath=$$path -l$$name -o t-test2-$$name -lpthread; \
    done;

clean:
	rm -f $(TARGET)
