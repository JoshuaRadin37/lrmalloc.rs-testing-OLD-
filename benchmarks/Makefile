TARGET = test-larson test-thread
all : test-larson test-thread test-t1

test-larson:
	(cd larson; make)
test-thread:
	(cd threadtest; make)
test-t1:
	(cd t-test1; make)
clean:
	(cd larson; make clean)
	(cd threadtest; make clean)
