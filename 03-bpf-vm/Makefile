MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -euc
CLANG		?= clang

dir := /src/linux-aws-5.0.0/samples/bpf

hello_world_1: hello_world_kern.1.o
	cp hello_world_kern.1.o $(dir)/hello_world_kern.o
	cp loader.c $(dir)/loader.c

hello_world_2: hello_world_kern.2.o
	cp hello_world_kern.2.o $(dir)/hello_world_kern.o
	cp loader.c $(dir)/loader.c

%.o: %.c
	$(CLANG) -O2 -target bpf \
		-I/usr/src/linux-headers-$(shell uname -r)/include \
		-I/usr/include/x86_64-linux-gnu \
		-c $< -o $@

clean:
	rm -f *.o
	touch *
