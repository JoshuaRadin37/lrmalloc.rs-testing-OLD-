include ../Makefile.inc

TARGET = build

build:
	
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CC) $(CCFLAGS) t-test1.$(CCEXT) -L$$path -Wl,-rpath=$$path -l$$name -o t-test1-$$name -lpthread; \
	done;

clean:
	rm -f t-test1-*
