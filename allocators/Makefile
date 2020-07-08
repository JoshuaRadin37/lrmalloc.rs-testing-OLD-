TARGET = build-Hoard build-ptmalloc build-jemalloc build-SuperMalloc build-lrmalloc_rs_global build-lrmalloc_rs_global_noapf
CLEANERS = clean-Hoard clean-ptmalloc clean-jemalloc clean-SuperMalloc clean-lrmalloc_rs_global clean-lrmalloc_rs_global_noapf

all:
	make $(TARGET)

# build-tcmalloc:
# 	cd tcmalloc/tcmalloc && ./configure && make

build-tcmalloc:
	cd gperftools && ./autogen.sh && ./configure && make && cd ..

build-hoard:
	cd Hoard/src && make && cd ../..

build-jemalloc:
	cd jemalloc && ./autogen.sh && make && cd ..

# SuperMalloc requires editing or release/Makefile
build-SuperMalloc:
	cd SuperMalloc/release && make && cd ../..

# build-ralloc:
#	 cd ralloc && make && cd ..

build-lrmalloc_rs_global:
	cd lrmalloc.rs/ && sed -i '/static USE_APF: bool = false/c\static USE_APF: bool = true' src/lib.rs &&\
	cd lrmalloc-rs-global &&  sed -i '/name = \"lrmalloc-rs-global-noapf"/c\name = \"lrmalloc-rs-global\"' Cargo.toml \
	&& cargo build && cd ../..

build-lrmalloc_rs_global_noapf:
	cd lrmalloc.rs/ && sed -i '/static USE_APF: bool = true/c\static USE_APF: bool = false' src/lib.rs &&\
	cd lrmalloc-rs-global &&  sed -i '/name = \"lrmalloc-rs-global"/c\name = \"lrmalloc-rs-global-noapf\"' Cargo.toml \
	&& cargo build && cd ../..

clean:
	make $(CLEANERS)

clean-tcmalloc:
	cd gperftools && make clean && make distclean && cd ..

clean-Hoard:
	cd Hoard/src && make clean && cd ../..

clean-jemalloc:
	cd jemalloc && make clean && cd ..

clean-SuperMalloc:
	cd SuperMalloc && make clean && cd ..

#clean-ralloc:
#	cd ralloc && make && cd ..

clean-lrmalloc_rs_global:
	cd lrmalloc.rs/lrmalloc-rs-global && cargo clean && cd ../..


# sed -i '/name = \"lrmalloc-rs-global-noapf"/c\name = \"lrmalloc-rs-global\"' Cargo.toml
# sed -i '/static USE_APF: bool = true;/c\static USE_APF: bool = false;' lib.rs
