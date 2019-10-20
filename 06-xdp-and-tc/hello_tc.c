#include <linux/bpf.h>
#include <linux/pkt_cls.h>
#include "/src/linux-aws-5.0.0/tools/testing/selftests/bpf/bpf_helpers.h"

SEC("classifier")
int cmain(struct __sk_buff *skb)
{
  return TC_ACT_SHOT;
}

char _license[] SEC("license") = "GPL";
