include ../Makefile.inc

TARGET = build

build:
	
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CC) $(CCFLAGS) shbench.$(CCEXT) -L$$path -Wl,-rpath=$$path -l$$name -o shbench-$$name -lpthread; \
	done;

clean:
	rm -f shbench-*
