#!/usr/bin/python
from bcc import BPF

source = """
   int kprobe__sys_clone(void *ctx) {
       bpf_trace_printk("Hello, World!\\n");
       return 0;
   }
"""

BPF(text=source).trace_print()

# replace the above line with this one for debugging
# BPF(text=source, debug=4).trace_print()
