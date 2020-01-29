include ../Makefile.inc

TARGET = build

build:
	
	declare -A PATHS=($(ALLOCNAMES)); \
	for name in $${!PATHS[@]}; do \
		path=$${PATHS[$$name]}; \
		echo $$path; \
		$(CC) $(CCFLAGS) t-test2.$(CCEXT) -L$$path -Wl,-rpath=$$path -l$$name -o t-test2-$$name -lpthread; \
	done;

clean:
	rm -f t-test2-*
