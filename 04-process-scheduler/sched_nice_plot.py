#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from subprocess import Popen, PIPE

import numpy as np
import matplotlib.pyplot as plt

from sched_plot import grep


def run(nprocs, total=100, resol=1):
    with Popen(map(str, ["./sched_nice", total, resol]),
               stdout=PIPE, encoding="ascii").stdout as f:
        data = np.array([ list(map(int, line.split()))
                          for line in grep(f, "est", reversed=True) ])
        proc, time, prog = data.T
    return proc, time, prog


def main(figsize=(8, 6)):
    nprocs = 2
    fig, axes = plt.subplots(2, 1, figsize=figsize)
    proc, time, prog = run(nprocs)
    for j in range(nprocs):
        mask = proc == j
        axes[0].plot(time[mask], proc[mask], ".")
        axes[1].plot(time[mask], prog[mask], ".")
    axes[0].set_ylim((0, nprocs-1))
    axes[0].set_ylabel("#proc")
    axes[1].set_ylabel("progress [%]")
    for ax in axes:
        ax.set_xlabel("time [ms]")
    plt.show()


if __name__ == "__main__":
    main()
