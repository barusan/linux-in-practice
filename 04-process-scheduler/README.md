Instructions for macOS
======================

My Environment
--------------

- MacBook Pro (2016)
- OS: macOS High Sierra v10.13.3
- Python 3.6.4
  - Numpy 1.14.1
  - matplotlib 2.2.0

CPU Affinity Settings
---------------------

`taskset` is a Linux command and not available on macOS.

[Instruments](https://developer.apple.com/jp/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/index.html) can change the number of active processor cores and the hyper-threading status.

    Instruments > Preferences > CPUs

Unlike `taskset`, Instruments cannot specify the CPU core that a process uses.

Process Scheduler
-----------------

`sched_plot.py` runs `sched` with different number of processes, and then plots the result.

    $ cc -o sched sched.py
    $ python3 sched_plot.py

The result depends on the number of active processor cores.

`sched_nice_plot.py` runs `sched_nice` and then plots the result.

    $ cc -o sched_nice sched_nice.py
    $ python3 sched_nice_plot.py
