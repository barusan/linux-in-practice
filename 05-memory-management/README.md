Instructions for macOS
======================

My Environment
--------------

- MacBook Pro (2016)
- OS: macOS High Sierra v10.13.3

Memory Map
----------

Check `vmmap` output instead of `/proc/${pid}/maps` because `/proc` is not available for macOS.

    $ cc -o mmap mmap.c
    $ ./mmap
    *** memory map before memory allocation ***
    ...snip...
    
    *** succeeded to allocate memory: address = 0x10983a000; size = 0x6400000 ***
    
    *** memory map after memory allocation ***
    ...snip...
    
    *** diff ***
    --- /tmp/vmmap.before   2018-03-10 00:01:26.000000000 +0900
    +++ /tmp/vmmap.after    2018-03-10 00:01:27.000000000 +0900
    ...snip...
    +VM_ALLOCATE (reserved) 000000010983a000-000000010fc3a000 [100.0M     0K     0K     0K] rw-/rwx SM=NUL          reserved VM address space (unallocated)
    ...snip...

    $ python -c "print(0x10fc3a000 - 0x10983a000)"
    104857600

File Map
--------

    $ echo hello > testfile
    $ cc -o filemap filemap.c
    $ ./filemap
    *** memory map before mapping file ***
    ...snip...
    
    *** succeeded to map file: address = 0x107b10000; size = 0x6400000 ***
    
    *** memory map after mapping file ***
    ...snip...
    
    *** diff ***
    --- /tmp/vmmap.before	2018-03-11 17:14:28.000000000 +0900
    +++ /tmp/vmmap.after	2018-03-11 17:14:29.000000000 +0900
    ...snip...
    +mapped file            0000000107b10000-000000010df10000 [100.0M     4K     0K     0K] rw-/rwx SM=PRV          /Users/barusan/linux-in-practice/05-memory-management/testfile
    
    *** file contens before overwrite mapped region: HELLO
    
    *** overwritten mapped region with: HELLO
    
    $ cat testfile
    HELLO

Demand Paging
-------------

Use Activity Monitor or Instruments instead of `sar`.

Copy on Write
-------------

`free` is a Linux command. `memory_pressure` is a possible alternative on macOS although it is originally a tool to apply real or simulate memory pressure.

    $ cc -o cow cow.c
    $ ./cow
    *** free memory info before fork ***:
    The system has 2147483648 (524288 pages with a page size of 4096).
    
    Stats: 
    Pages free: 1450092 
    Pages purgeable: 84905 
    Pages purged: 523123 
    
    ...snip...
    
    Page Q counts:
    Pages active: 1310592 
    Pages inactive: 671262 
    Pages speculative: 278389 
    Pages throttled: 0 
    Pages wired down: 483740 
    
    ...snip...
    
    System-wide memory free percentage: 88%
    *** child ps info before memory access ***:
    41810 ./cow  4370136    368      -      -
    *** free memory info before memory access ***:
    The system has 2147483648 (524288 pages with a page size of 4096).
    
    Stats: 
    Pages free: 1450094 
    Pages purgeable: 84905 
    Pages purged: 523123 
    
    ...snip...
    
    Page Q counts:
    Pages active: 1310655 
    Pages inactive: 671262 
    Pages speculative: 278390 
    Pages throttled: 0 
    Pages wired down: 483757 
    
    ...snip...
    
    System-wide memory free percentage: 88%
    *** child ps info after memory access ***:
    41810 ./cow  4371160 102784      -      -
    *** free memory info after memory access ***:
    The system has 2147483648 (524288 pages with a page size of 4096).
    
    Stats: 
    Pages free: 1424243 
    Pages purgeable: 84905 
    Pages purged: 523123 
    
    ...snip...
    
    Page Q counts:
    Pages active: 1336255 
    Pages inactive: 671262 
    Pages speculative: 278390 
    Pages throttled: 0 
    Pages wired down: 483806 
    
    ...snip...
    
    System-wide memory free percentage: 88%

Swap
----

On macOS, swap files are located at `/private/var/vm`.

    $ df -h /private/var/vm
    Filesystem     Size   Used  Avail Capacity iused               ifree %iused  Mounted on
    /dev/disk1s4  931Gi  1.0Gi  523Gi     1%       1 9223372036854775806    0%   /private/var/vm
    $ diskutil list disk1
    /dev/disk1 (synthesized):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      APFS Container Scheme -                      +999.6 GB   disk1
                                     Physical Store disk0s2
       1:                APFS Volume Macintosh HD            436.6 GB   disk1s1
       2:                APFS Volume Preboot                 20.0 MB    disk1s2
       3:                APFS Volume Recovery                509.8 MB   disk1s3
       4:                APFS Volume VM                      1.1 GB     disk1s4

Swap can be monitored using Activity Monitor or Instruments.
