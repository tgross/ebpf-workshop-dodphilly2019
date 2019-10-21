# eBPF Workshop

*A workshop given at DevOpsDays Philadelphia 2019*

## Running Yourself

This workshop has been designed around a deployment on AWS. Within a few weeks after the workshop, I hope to have a Vagrantfile in this repo which gets as close as possible to the working environment we had.


## Credits and Reference Material

If you've taken this workshop and want to dig into more, check out the following links.


#### Huge thanks!

David Calavera and Lorenzo Fontana's have a workshop at [workshop.bpf.sh](https://workshop.bpf.sh) to support their book [Linux Observability with BPF: Advanced Programming for Performance Analysis and Networking](https://www.amazon.com/Linux-Observability-BPF-Programming-Performance/dp/1492050202). Their workshop is GPL and available at https://github.com/bpftools/bpf-workshop. Although this DevOpsDays workshop has a slightly different take on the content, David and Lorenzo's workshop was definitely the starting point.


#### Blog posts

* [Tracing a packet journey using Linux tracepoints, perf and eBPF](https://blog.yadutaf.fr/2017/07/28/tracing-a-packet-journey-using-linux-tracepoints-perf-ebpf/) by Jean-Tiare Le Bigot

* [How to turn any syscall into an event: Introducing eBPF Kernel probes](https://blog.yadutaf.fr/2016/03/30/turn-any-syscall-into-event-introducing-ebpf-kernel-probes/) by Jean-Tiare Le Bigot

[The art of writing eBPF programs: a primer.](https://sysdig.com/blog/the-art-of-writing-ebpf-programs-a-primer/) by Gianluca Borello at Sysdig.

* [Load XDP programs using the ip (iproute2) command](https://fntlnz.wtf/post/xdp-ip-iproute/) by Lorenzo Fontana

[Why is the kernel community replacing iptables with BPF?](https://cilium.io/blog/2018/04/17/why-is-the-kernel-community-replacing-iptables/) by Thomas Graf of Cilium

* [Instrumenting CPython with DTrace and SystemTap](https://docs.python.org/3/howto/instrumentation.htm) by David Malcolm and Łukasz Langa

* [Custom port-based BPF firewall loader for systemd services](https://kailueke.gitlab.io/systemd-bpf-firewall-loader/) by Kai Lüke

* [Dive into BPF: a list of reading material](https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/) by Quentin Monnet

* [Network security for microservices with eBPF](https://medium.com/@beatrizmrg/network-security-for-microservices-with-ebpf-bis-478b40e7befa) by Beatriz Martínez Rubio

* [eBPF and XDP for Processing Packets at Bare-metal Speed](https://sematext.com/blog/ebpf-and-xdp-for-processing-packets-at-bare-metal-speed/) by Nedim Šabić of Sematext


#### Talks and Whitepapers

* [XDP in practice:
integrating XDP into our DDoS mitigation pipeline](https://netdevconf.info/2.1/papers/Gilberto_Bertin_XDP_in_practice.pdf) by Gilberto Bertin of Cloudflare

* [USDT Tracing report](https://bpf.sh/usdt-report-doc/) by Dale Hamel

* [BPF in LLVM and the Kernel](https://blog.linuxplumbersconf.org/2015/ocw/system/presentations/3249/original/bpf_llvm_2015aug19.pdf) by Alexei Starovoitov


#### Documentation:

* [Cilium docs](https://docs.cilium.io/en/stable/bpf/#) <-- these are _amazing_

* [bcc tutorial docs](https://github.com/iovisor/bcc/blob/master/docs/tutorial.md)

* [bpftrace reference guide](https://github.com/iovisor/bpftrace/blob/master/docs/reference_guide.md)


#### Saved my bacon during prep for this workshop:

* [Cilium docs](https://docs.cilium.io/en/stable/bpf/#) <-- did I mention these are amazing?

* [eBPF Basics](https://blog.raymond.burkholder.net/index.php?/archives/1000-eBPF-Basics.html) by Raymond Burkholder


#### Books:

* [BPF Performance Tools (book)](http://www.brendangregg.com/bpf-performance-tools-book.html) by Brendan Gregg


#### Interesting repos:

* [Awesome eBPF](https://github.com/zoidbergwill/awesome-ebpf): A curated list of awesome projects related to eBPF.

* https://github.com/kinvolk/bpf-exercises

* https://github.com/xdp-project/xdp-tutorial

* https://github.com/p-/socket-connect-bpf
