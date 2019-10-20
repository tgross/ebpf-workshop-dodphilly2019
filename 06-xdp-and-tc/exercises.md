# 06 - Networking

Exercises looking at eBPF and networking.

## Exercise 1

Try `tcpdump`:

```sh
# listen for DNS traffic
sudo tcpdump 'ip and udp port 53'

# in another terminal
nslookup example.com
```

Dump BPF bytecode:

```
sudo tcpdump -d 'ip and udp port 53'
```

## Exercise 2

Trace traffic passing through network namespaces.


```sh
cd ~/workshop/06-xdp-and-tc/tracepkt
less tracepkt.c
less tracepkt.py

# get our IP address
ip addr

# look at 1 ping packet
sudo python tracepkt.py $ip
```

Trace more by replacing the section at the bottom of `tracepkt.py`, and comment-out the section checking for ICMP (ping). Note we're not waiting till interrupt alone because of the high volume.

```python
    # # Make sure it is OUR ping process
    # if event.icmpid != PING_PID:
    #     return

...

    # # Launch a background ping process
    # with open('/dev/null', 'r') as devnull:
    #     ping = subprocess.Popen([
    #             '/bin/ping',
    #             '-c1',
    #             TARGET,
    #         ],
    #        stdout=devnull,
    #         stderr=devnull,
    #         close_fds=True,
    #    )
    # PING_PID = ping.pid

    print "%14s %16s %7s %-34s %s" % ('NETWORK NS', 'INTERFACE', 'TYPE', 'ADDRESSES', 'IPTABLES')

    # # Listen for event until the ping process has exited
    # while ping.poll() is None:
    #     b.kprobe_poll(10)

    # # Forward ping's exit code
    # sys.exit(ping.poll())

    count = 0
    while count < 100:
        try:
            b.kprobe_poll(10)
            count = += 1
        except KeyboardInterrupt:
            exit()
```

ref https://blog.yadutaf.fr/2017/07/28/tracing-a-packet-journey-using-linux-tracepoints-perf-ebpf/
ref https://github.com/yadutaf/tracepkt/blob/master/tracepkt.py


## Exercise 3

A traffic control program that drops all packets.

```sh
#include <linux/bpf.h>
#include <linux/pkt_cls.h>
#include "/src/linux-aws-5.0.0/tools/testing/selftests/bpf/bpf_helpers.h"

SEC("classifier")
int cmain(struct __sk_buff *skb)
{
  return TC_ACT_SHOT;
}

char _license[] SEC("license") = "GPL";
```

Compile the traffic control program and load it.

```
clang -target bpf -O2 -c hello_tc.c -o hello_tc.o
```

Important to note what interface we're loading programs to! Check out:

```sh
# list containers
docker ps
docker ps | awk '/nginx_metrics/{print $1}'
docker inspect $(docker ps | awk '/nginx_metrics/{print $1}')
docker inspect $(docker ps | awk '/nginx_metrics/{print $1}') \
   | jq '.[0].NetworkSettings.Networks'

# compare to host networking container:
docker inspect $(docker ps | awk '/nginx-/{print $1}') \
   | jq '.[0].NetworkSettings.Networks'

```

If we run TC_ACT_SHOT on all traffic on ens5... that's everything!
We'll load it onto `nginx_metrics` at the `docker0` interface instead:

```sh
# verify we have working traffic:
docker ps | grep nginx_metrics
curl 172.31.11.6:31411/metrics

sudo tc qdisc add dev docker0 clsact
sudo tc filter add \
    dev docker0 \      # device name
    ingress \
    bpf \
    da \               # direct-action
    obj hello_tc.o     # name of the object file

# verify we can't reach it anymore
curl 172.31.11.6:31411/metrics
```


## Exercise 4

Compile `bpftool`

```sh
src=/src/linux-aws-5.0.0
cd $src/tools/bpf/bpftool/
make
sudo make install
```

Look at all currently loaded BPF programs:

```sh
sudo bpftool prog

# pretty and/or in JSON
bpftool prog --json --pretty | jq .
```

Use `bpftool` to get the (post-verifier) BPF instructions of a specific program.


```sh
# get some metadata about the program
bpftool prog show id $id

# dump the instructions
bpftool prog dump xlated id $id

# let's get wild and visualize the program flow!
bpftool prog dump xlated id $id visual &> output.dot
dot -Tpng output.dot -o output.png
```

Let's now unload the `tc` program we loaded earlier:

```sh
sudo tc filter del dev docker0 ingress
sudo tc qdisc del dev docker0 clsact
```

## Exercise 5

We want to drop incoming traffic with XDP. Let's write a "hello `XDP_DROP`" program.

```sh
#include <linux/bpf.h>

int main()
{
    return XDP_DROP;
}
```

Compile the XDP program:

```sh
clang -target bpf -O2 -c hello_xdp_drop.c -o hello_xdp_drop.o

# take a look at the result!
llvm-objdump -S -no-show-raw-insn hello_xdp_drop.o

# hello_xdp_drop.o:       file format ELF64-BPF

# Disassembly of section .text:
# 0000000000000000 main:
#       0:       r0 = 1         # <- the return code for XDP_DROP
#       1:       exit
```

Again, important to note what interface we're loading programs to.
Load it with `iproute2` to `nginx_metrics`'s `docker0` interface instead:

```sh
# verify we have working traffic:
docker ps | grep nginx_metrics
curl 172.31.11.6:31411/metrics

sudo ip link set \
    dev docker0 \           # the device name
    xdp \                   # default (alt: xdpdrv or xdpoffload)
    obj hello_xdp_drop.o \  # the name of the object file
    sec .text               # default section name

# verify we can't reach it anymore
curl 172.31.11.6:31411/metrics
```

Look at the program in `bpftool`:

```
sudo bpftool prog
sudo bpftool prog show id $id

186: xdp  tag 57cd311f2e27366b
        loaded_at 2019-10-20T18:04:32+0000  uid 0
        xlated 16B  jited 35B  memlock 4096B

sudo bpftool prog dump xlated id $id
   0: (b7) r0 = 1
   1: (95) exit

# see the xdp flag for the interface in ip link
ip link
```

Unload the XDP program.

```sh
sudo ip link set dev docker0 xdp off

# see it's no longer there
sudo bpftool prog
```

## Exercise 6

Now let's drop incoming traffic (for Nginx) _just_ from the "attacking" client. This is going to be on the main network interface, we want to be more specific about what we block: just the src IP of the client. Parsing this is a bit beyond scope of this class, so we'll lean on someone who's done this work already.

```sh
cd ~/workshop/06-xdp-and-tc/oxdpus/pkg/xdp/prog
less xdp.c
```

`oxdpus` is a `gobpf`-based "toy" tool for loading a particular XDP program and modifying it with updated blocklists on the fly. Because a XDP program can be reloaded atomically, it just recreates the program with new blocklists.

Ref https://sematext.com/blog/ebpf-and-xdp-for-processing-packets-at-bare-metal-speed/

```
sudo oxdpus attach --dev ens5   # attach the empty program w/ empty blocklist
sudo bpftool prog

docker logs --tail 5 $(docker ps | awk '/nginx-/{print $1}')
sudo oxdpus add --ip $ip

# show logs have stopped
docker logs --tail 5 $(docker ps | awk '/nginx-/{print $1}')

# remove the program
sudo oxdpus detach --dev ens5
docker logs --tail 5 $(docker ps | awk '/nginx-/{print $1}')
```

Future work: try extending this blocklist application to include specific ports!
