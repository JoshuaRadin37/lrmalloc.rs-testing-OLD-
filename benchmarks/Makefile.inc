CC  := $(CC)
CXX := $(CXX)

CCFLAGS  := -g -O3 -DNDEBUG -I/common
CXXFLAGS := -g -O3 -DNDEBUG -I/common

CCEXT := c
CXXEXT := cpp

MEMPATH := ../../allocators

HPATH := $(MEMPATH)/Hoard/src
JEPATH := $(MEMPATH)/jemalloc/lib
TCPATH := $(MEMPATH)/gperftools/mylib/lib
PTPATH := $(MEMPATH)/ptmalloc3
SMPATH := $(MEMPATH)/SuperMalloc/release/lib
RPATH := $(MEMPATH)/ralloc/target/release

ALLOCPATHS = $(HPATH) $(JEPATH) $(TCPATH) $(PTPATH) $(SMPATH)
ALLOCNAMES = ["hoard"]='$(HPATH)' ["jemalloc"]='$(JEPATH)' ["tcmalloc"]='$(TCPATH)' ["ptmalloc3"]='$(PTPATH)' ["supermalloc"]='$(SMPATH)' ["ralloc"]='$(RPATH)'
# ALLOCNAMES = hoard jemalloc tcmalloc ptmalloc supermalloc
