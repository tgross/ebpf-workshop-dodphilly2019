#include <uapi/linux/bpf.h>
#include "/src/linux-aws-5.0.0/tools/testing/selftests/bpf/bpf_helpers.h"

#define SEC(NAME) __attribute__((section(NAME), used))

SEC("tracepoint/syscalls/sys_enter_execve")
int bpf_prog(void *ctx) {
  char msg[] = "Hello, BPF World!";
  bpf_trace_printk(msg, sizeof(msg));
return 0;
}

char _license[] SEC("license") = "GPL";
