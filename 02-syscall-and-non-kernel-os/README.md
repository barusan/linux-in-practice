Instructions for macOS
======================

My Environment
--------------

- MacBook Pro (2016)
- OS: macOS High Sierra v10.13.3

System Calls (GUI)
------------------

System Trace in [Instruments](https://developer.apple.com/jp/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/index.html)

System Calls (CLI)
------------------

Command to show syscalls:

- Linux: `strace`
- macOS: `dtrace` or `dtruss`

Neither `dtrace` nor `dtruss` can be executed on a macOS by default because of System Integrity Protection (SIP).

### Enabling/Disabling dtrace

Nahum Shalman, [Enabling DTrace on macOS Sierra](http://blog.shalman.org/enabling-dtrace-on-macos-sierra/) (2017) Accecced on March 6, 2018.

1. Reboot into Recovery Mode (hold down ⌘R during boot)
2. Launch a shell and run:
  - `csrutil enable --without dtrace` to enable `dtrace`,
  - `csrutil enable` to disable `dtrace`
3. Reboot and allow machine to boot normally

Check the current status by running `csrutil status`.

    $ csrutil status
    System Integrity Protection status: enabled (Custom Configuration).
    
    Configuration:
            Apple Internal: disabled
            Kext Signing: enabled
            Filesystem Protections: enabled
            Debugging Restrictions: enabled
            DTrace Restrictions: disabled
            NVRAM Protections: enabled
            BaseSystem Verification: enabled
    
    This is an unsupported configuration, likely to break in the future and leave your machine in an unknown state.

Executables need to be built after DTrace Restrictions are disabled; we need to build Python.

Remember to restore the `csrutil` setting to `enabled` (i.e., `dtrace` not to be executed) after the experiment.

### Output

In C:

    $ cc -o hello hello.c
    $ sudo dtruss -f ./hello
    SYSCALL(args) 		 = return
    ...snip...
    getpid(0x0, 0x0, 0x0)		 = 3734 0
    stat64("/AppleInternal/XBS/.isChrooted\0", 0x7FFEED20E2B8, 0x0)		 = -1 Err#2
    stat64("/AppleInternal\0", 0x7FFEED20E350, 0x0)		 = -1 Err#2
    csops(0xE96, 0x7, 0x7FFEED20DDF0)		 = -1 Err#22
    sysctl([CTL_KERN, 14, 1, 3734, 0, 0] (4), 0x7FFEED20DF38, 0x7FFEED20DF30, 0x0, 0x0)		 = 0 0
    csops(0xE96, 0x7, 0x7FFEED20D6E0)		 = -1 Err#22
    getrlimit(0x1008, 0x7FFEED20F960, 0x0)		 = 0 0
    fstat64(0x1, 0x7FFEED20F978, 0x0)		 = 0 0
    write_nocancel(0x1, "hello world\n\0", 0xC)		 = 12 0

In Python:

    $ wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
    $ tar xJvf Python-3.6.4.tar.xz
    $ mkdir python
    $ cd Python-3.6.4
    $ ./configure --prefix=`pwd`/../python
    $ make -j5      ## you may have to install some other libraries to complete
    $ make install
    $ cd ..
    $ sudo dtruss ./python/bin/python3 ./hello.py
    SYSCALL(args) 		 = return
    ...snip...
    open_nocancel("./hello.py\0", 0x0, 0x1B6)		 = 3 0
    ioctl(0x3, 0x20006601, 0x0)		 = 0 0
    fstat64(0x3, 0x7FFEE23CA998, 0x0)		 = 0 0
    ioctl(0x3, 0x4004667A, 0x7FFEE23CA8D4)		 = -1 Err#25
    ioctl(0x3, 0x40487413, 0x7FFEE23CA8D8)		 = -1 Err#25
    lseek(0x3, 0x0, 0x1)		 = 0 0
    fstat64(0x3, 0x7FFEE23CA758, 0x0)		 = 0 0
    read_nocancel(0x3, "print(\"hello world\")\n\0", 0x10000)		 = 21 0
    lseek(0x3, 0x0, 0x1)		 = 21 0
    read_nocancel(0x3, "\0", 0x10000)		 = 0 0
    close_nocancel(0x3)		 = 0 0
    write(0x1, "hello world\n\0", 0xC)		 = 12 0
    sigaction(0x2, 0x7FFEE23CA8D8, 0x7FFEE23CA900)		 = 0 0
    madvise(0x10E3A6000, 0x400000, 0x9)		 = 0 0
    madvise(0x10DC6A000, 0x20000, 0x9)		 = 0 0
    madvise(0x10DFA6000, 0x400000, 0x9)		 = 0 0
    sigaltstack(0x0, 0x7FFEE23CA920, 0x0)		 = 0 0
    madvise(0x10DC09000, 0x20000, 0x9)		 = 0 0

CPU Monitoring
--------------

Activity Monitor in Instruments.
