# Exercises 3 - BPF VM

Exercises "doing it the hard way."


## Exercise 1

Build the hello world program.

```sh
make hello_world_1
```

Build the loader.

```sh
src=/src/linux-aws-5.0.0
cp Makefile-tools $src/samples/bpf/Makefile # <-- tweaked Makefile
cp loader.c $src/samples/bpf/
cp hello_world_kern.1.o $src/samples/bpf/hello_world_kern.o
cd $src

make oldconfig
# just hit enter a bunch, it's fine...

make headers_install
make samples/bpf/   # <-- the trailing slash matters!
```

Run the loader.

```sh
cd samples/bpf/

sudo ./loader

# we get an error:
#
# invalid relo for insn[11].code 0x85
# bpf_load_program() err=22
# last insn is not an exit or jmp
# The kernel didn't load the BPF program
```

What happened?

```sh
llvm-objdump -S -no-show-raw-insn hello_world_kern.o
```

Build a fixed hello world.

```sh
make hello_world_2
cd $src
make samples/bpf/
```

Take a look at the new object:

```sh
llvm-objdump -S -no-show-raw-insn hello_world_kern.o
```

Run it

```sh
sudo ./loader
```
