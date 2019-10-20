# 05 - bpftrace

Exercises looking at `bpftrace`

## Exercise 1

Walk through `bpftrace` tools; on Ubuntu (which is our workshop environment), these will all be suffixed with `.bt`

```sh
ls /sbin/*.bt        # list the bpftrace tools installed

execsnoop             # trace new process launches
opensnoop             # trace open() syscall
biolatency            # histogram of disk IO latency
biosnoop              # per-operation disk IO latency
tcpconnect            # show each TCP connect() (outbound)
tcpaccept             # show each TCP accept() (inbound)
tcpretrans            # show each TCP retransmit
runqlat               # histogram of run queue latency
```

## Exercise 2

Trace the read bytes of `vfs_read` via a `kretprobe`.

```
sudo bpftrace -e \
    'kretprobe:vfs_read { @bytes = lhist(retval, 0, 2000, 200); }'
```

Trace the read bytes of `vfs_read` via a `tracepoint`.

```
sudo bpftrace -e \
    'tracepoint:syscalls:sys_exit_read  { @bytes = lhist(args->ret, 0, 2000, 200); }'
```

## Exercise 3

Trace a userland function.

```sh
sudo bpftrace -e '
    uprobe:/usr/local/bin/nomad:*collectMemoryStats
    {
      @start[tid] = nsecs;
    }
    uretprobe:/usr/local/bin/nomad:*collectMemoryStats
    {
      $latns = (nsecs - @start[tid]);
      printf("%6d ns\n", $latns);
      delete(@start[tid]);
    }'
```
