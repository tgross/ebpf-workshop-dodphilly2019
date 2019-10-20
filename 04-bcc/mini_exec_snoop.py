#!/usr/bin/python
# Derived from
# https://workshop.bpf.sh/exercises/mini_exec_snoop.py
# this follows the bcc-tools repo hello world example closely
# but hits AttributeError on the PerfEventArray access.
from bcc import BPF
from bcc.utils import printb
import ctypes as ct

bpf_source = """
#include <uapi/linux/ptrace.h>

BPF_PERF_OUTPUT(events);

struct data_t {
    char comm[16];
};

int on_syscall_execve(struct pt_regs *ctx,
    const char __user *filename,
    const char __user *const __user *__argv,
    const char __user *const __user *__envp)
{
  struct data_t data = {};
  bpf_get_current_comm(&data.comm, sizeof(data.comm));

  events.perf_submit(ctx, &data, sizeof(data));
  return 0;
}
"""

TASK_COMM_LEN = 16    # linux/sched.h

class Data(ct.Structure):
    _fields_ = [
        ("comm", ct.c_char * TASK_COMM_LEN)
    ]

def dump_data(cpu, data, size):
    event = ct.cast(data, ct.POINTER(Data)).contents
    printb(b"%-16s" % event.comm)


bpf = BPF(text=bpf_source)
execve_function = bpf.get_syscall_fnname("execve")
bpf.attach_kretprobe(event=execve_function, fn_name="on_syscall_execve")

bpf["events"].open_perf_buffer(dump_data)
while 1:
    bpf.perf_buffer_poll()
