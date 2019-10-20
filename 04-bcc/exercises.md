# 04 - BCC

Exercises looking at custom BCC tools and the handy interop they provide.

## Exercise 1

Hello world, with debugging.

```sh
sudo ./hello_world.py
```

```python
BPF(text=source, debug=4).trace_print()
```


## Exercise 2

Create a less featureful version of `execsnoop-bpfcc`.

```
sudo ./mini_exec_snoop.py
```

## Exercise 3

Use `profile` to generate flame graphs. (Run for 30s. `-f` for "folded")

```sh
PID=$(pgrep nomad)
sudo profile-bpfcc -p $PID -f 30 > ~/profile.out

/opt/Flamegraph/flamegraph.pl ~/profile.out > ~/profile-graph.svg
scp workshop:profile-graph.svg .

# (open ./profile-graph.svg in a webbrowser)
```

## Exercise 4

Add reporting to runtime tracing tools via `usdt`.

Demo runtime tracing tools on our Python application:

```sh
sudo pythoncalls-bpfcc $(pgrep gunicorn | head -1)
sudo pythonflow-bpfcc $(pgrep gunicorn | head -1)
sudo pythongc-bpfcc $(pgrep gunicorn | head -1)
sudo pythonstat-bpfcc $(pgrep gunicorn | head -1)
```

But note what happens if we do these on a non-`usdt` configured Python:

```
Error attaching USDT probes: the specified pid might not contain the
given language's runtime, or the runtime was not built with the required
USDT probes. Look for a configure flag similar to --with-dtrace or
--enable-dtrace. To check which probes are present in the process, use the
tplist tool.
```

## Exercise 5

Copy the ulib for GC and modify to report metrics to Prometheus.

```
# copy the existing tool and then edit away!
cp /sbin/pythongc-bpfcc ./ugc-prometheus

sudo ./ugc-promtheus $(pgrep gunicorn | head -1)

# in another terminal
curl localhost:9001 | grep python
```
