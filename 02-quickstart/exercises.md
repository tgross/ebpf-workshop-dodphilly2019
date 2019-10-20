# 02 - Quick Start

Exercises taking a quick tour of tracing, monitoring, and introspection tools provided by the BCC toolkit.

## Exercise 1

Walk through non-BPF tools; "the first 60 seconds on a machine".

```sh
uptime                # load averages
dmesg | tail          # recent system messages
vmstat 1              # virtual memory stats
mpstat -P ALL 1       # per-CPU utilization
pidstat 1             # top w/ rolling summary
iostat -xz 1          # block disk activity
free -m               # memory (esp. buffers and cache)
sar -n DEV 1          # network iface throughput
sar -n TCP,ETCP 1     # network TCP metrics
top                   # summary metrics
```

## Exercise 2

Walk through BCC tools; on Ubuntu (which is our workshop environment), these will all be suffixed with `-bpfcc`

```sh
ls /sbin/*-bpf        # list the BCC tools installed

execsnoop             # trace new process launches
opensnoop             # trace open() syscall
ext4slower            # trace slow filesystem calls
biolatency            # histogram of disk IO latency
biosnoop              # per-operation disk IO latency
cachestat             # file system cache stat summary
tcpconnect            # show each TCP connect() (outbound)
tcpaccept             # show each TCP accept() (inbound)
tcpretrans            # show each TCP retransmit
runqlat               # histogram of run queue latency
profile               # CPU profile
```

## Exercise 3

Debug the problem with our example application. The application is frequently restarting a worker process and spawning a large number of new connections to memcached on each restart.

```sh
sslsniff-bpfcc -p <nginx>   # check incoming traffic
tcpconnect-bpfcc -P 11211   # look at memcached connections
execsnoop-bpfcc             # look at new processes
```
