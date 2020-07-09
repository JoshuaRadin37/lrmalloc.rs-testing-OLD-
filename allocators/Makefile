TARGET = build-Hoard build-jemalloc build-SuperMalloc build-lrmalloc-rs-global build-lrmalloc-rs-global_no_apf
CLEANERS = clean-Hoard clean-jemalloc clean-SuperMalloc clean-lrmalloc_rs_global clean-lrmalloc_rs_global_noapf

all:
	make $(TARGET)

# build-tcmalloc:
# 	cd tcmalloc/tcmalloc && ./configure && make

build-tcmalloc:
	cd gperftools && ./autogen.sh && ./configure && make && cd ..

build-Hoard:
	cd Hoard/src && make && cd ../..

build-jemalloc:
	cd jemalloc && ./autogen.sh && make && cd ..

# SuperMalloc requires editing or release/Makefile
build-SuperMalloc:
	cd SuperMalloc/release && make && cd ../..

# build-ralloc:
#	 cd ralloc && make && cd ..

Build-lrmalloc-rs-global:
	cd lrmalloc.rs; sed 's/static USE_APF: bool = false/static USE_APF: bool = true/' ./src/lib.rs
	cd lrmalloc.rs/lrmalloc-rs-global; sed 's/name = \"lrmalloc-rs-global_no_apf"/name = \"lrmalloc-rs-global\"/' Cargo.toml
	cargo build --manifest-path=lrmalloc.rs/Cargo.toml 

build-lrmalloc-rs-global_no_apf:
	cd lrmalloc.rs/; sed -i '/static USE_APF: bool = true/c\static USE_APF: bool = false' src/lib.rs
	cd lrmalloc-rs-global; sed -i '/name = \"lrmalloc-rs-global"/c\name = \"lrmalloc-rs-global_no_apf\"' Cargo.toml
	cargo build --manifest-path=lrmalloc.rs/Cargo.toml 

.PHONY:

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
