#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from subprocess import Popen, PIPE

import numpy as np
import matplotlib.pyplot as plt


def grep(file, string, reversed=False):
    for line in file:
        if ((string in line and not reversed)
            or (string not in line and reversed)):
            yield line


def run(nprocs, total=100, resol=1):
    with Popen(map(str, ["./sched", nprocs, total, resol]),
               stdout=PIPE, encoding="ascii").stdout as f:
        data = np.array([ list(map(int, line.split()))
                          for line in grep(f, "est", reversed=True) ])
        proc, time, prog = data.T
    return proc, time, prog


def main(figsize=(14, 8)):
    nproc_list = [1, 2, 4]
    fig, axes = plt.subplots(2, len(nproc_list), figsize=figsize)
    for i, nprocs in enumerate(nproc_list):
        proc, time, prog = run(nprocs)
        for j in range(nprocs):
            mask = proc == j
            axes[0,i].plot(time[mask], proc[mask], ".")
            axes[1,i].plot(time[mask], prog[mask], ".")
        axes[0,i].set_ylim((0, max(nproc_list)-1))
        axes[0,i].set_ylabel("#proc")
        axes[1,i].set_ylabel("progress [%]")
        for ax in axes[:,i]:
            ax.set_xlabel("time [ms]")
    plt.show()


if __name__ == "__main__":
    main()
