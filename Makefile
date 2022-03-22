all:

test-1:
	./run configs/1-1-basic.conf
	./run configs/1-2-normal.conf

test-2:
	./run configs/2-1-duplicates.conf

test-3:
	./run configs/3-1-jitter.conf
	./run configs/3-2-more-jitter.conf

test-4:
	./run configs/4-1-drops.conf
	./run configs/4-2-more-drops.conf

