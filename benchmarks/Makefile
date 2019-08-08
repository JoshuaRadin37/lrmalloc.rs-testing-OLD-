TARGET = test-larson test-thread test-t1 test-t2 test-super test-shbench
all : test-larson test-thread test-t1 test-t2 test-super test-shbench

test-larson:
	(cd larson; make)
test-thread:
	(cd threadtest; make)
test-t1:
	(cd t-test1; make)
test-t2:
	(cd t-test2; make)
test-super:
	(cd SuperServer; make)
test-shbench:
	(cd shbench; make)
clean:
	(cd larson; make clean)
	(cd threadtest; make clean)
	(cd t-test1; make clean)
	(cd t-test2; make clean)
	(cd SuperServer; make clean)
	(cd shbench; make clean)
