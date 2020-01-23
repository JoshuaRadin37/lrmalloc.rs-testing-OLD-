include ../Makefile.inc
  
all: build

build:
	declare -A PATHS=($(ALLOCNAMES)); \
    for name in $${!PATHS[@]}; do \
        path=$${PATHS[$$name]}; \
        echo $$path; \
        $(CC) $(CCCFLAGS) t-test1.c -L$$path -Wl,-rpath=$$path -l$$name -o t-test1-$$name -lpthread; \
    done;

clean:
	rm -f $(TARGET)
