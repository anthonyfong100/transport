all:

test-1:
	./run configs/1-1-basic.conf
	./run configs/1-2-normal.conf

test-2:
	./run configs/2-1-duplicates.conf