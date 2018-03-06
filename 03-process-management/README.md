Instructions for macOS
======================

My Environment
--------------

- MacBook Pro (2016)
- OS: macOS High Sierra v10.13.3
- Homebrew

Information of Object Files
---------------------------

Commands to display imformation of executables:

- Linux: `readelf`
- macOS: `objdump` or `gobjdump`

Install `gobjdump` via Homebrew:

    $ brew update && brew install binutils

### Output

    $ gobjdump -f /bin/sleep
    
    /bin/sleep:     ファイル形式 mach-o-x86-64
    アーキテクチャ: i386:x86-64, フラグ 0x00000012:
    EXEC_P, HAS_SYMS
    開始アドレス 0x0000000100000cd3

    $ LANG=C gobjdump -f /bin/sleep
    
    /bin/sleep:     file format mach-o-x86-64
    architecture: i386:x86-64, flags 0x00000012:
    EXEC_P, HAS_SYMS
    start address 0x0000000100000cd3

    $ objdump -h /bin/sleep
    
    /bin/sleep:     file format Mach-O 64-bit x86-64
    
    Sections:
    Idx Name          Size      Address          Type
      0 __text        000001cb 0000000100000cd3 TEXT
      1 __stubs       0000001e 0000000100000e9e TEXT
      2 __stub_helper 00000042 0000000100000ebc TEXT
      3 __const       000000a8 0000000100000f00 DATA
      4 __cstring     00000003 0000000100000fa8 DATA
      5 __unwind_info 00000050 0000000100000fac DATA
      6 __got         00000008 0000000100001000 DATA
      7 __nl_symbol_ptr 00000010 0000000100001008 DATA
      8 __la_symbol_ptr 00000028 0000000100001018 DATA

    $ gobjdump -h /bin/sleep
    
    /bin/sleep:     ファイル形式 mach-o-x86-64
    
    セクション:
    Idx Name          Size      VMA               LMA               File off  Algn
      0 .text         000001cb  0000000100000cd3  0000000100000cd3  00000cd3  2**0
                      CONTENTS, ALLOC, LOAD, CODE
      1 __TEXT.__stubs 0000001e  0000000100000e9e  0000000100000e9e  00000e9e  2**1
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
      2 __TEXT.__stub_helper 00000042  0000000100000ebc  0000000100000ebc  00000ebc  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
      3 .const        000000a8  0000000100000f00  0000000100000f00  00000f00  2**4
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      4 .cstring      00000003  0000000100000fa8  0000000100000fa8  00000fa8  2**0
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      5 __TEXT.__unwind_info 00000050  0000000100000fac  0000000100000fac  00000fac  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
      6 __DATA.__got  00000008  0000000100001000  0000000100001000  00001000  2**3
                      CONTENTS, ALLOC, LOAD, DATA
      7 __DATA.__nl_symbol_ptr 00000010  0000000100001008  0000000100001008  00001008  2**3
                      CONTENTS, ALLOC, LOAD, DATA
      8 __DATA.__la_symbol_ptr 00000028  0000000100001018  0000000100001018  00001018  2**3
                      CONTENTS, ALLOC, LOAD, DATA

Memory Maps
-----------

    $ sleep 10000 &
    [1] 29057
    $ vmmap 29057
    Process:         sleep [29057]
    Path:            /bin/sleep
    Load Address:    0x104b40000
    Identifier:      sleep
    Version:         ???
    Code Type:       X86-64
    Parent Process:  bash [26772]
    
    Date/Time:       2018-03-06 21:22:55.083 +0900
    Launch Time:     2018-03-06 21:22:28.467 +0900
    OS Version:      Mac OS X 10.13.3 (17D102)
    Report Version:  7
    Analysis Tool:   /usr/bin/vmmap
    ----
    
    Virtual Memory Map of process 29057 (sleep)
    Output report format:  2.4  -- 64-bit process
    VM page size:  4096 bytes
    
    ==== Non-writable regions for process 29057
    REGION TYPE                      START - END             [ VSIZE  RSDNT  DIRTY   SWAP] PRT/MAX SHRMOD PURGE    REGION DETAIL
    __TEXT                 0000000104b40000-0000000104b41000 [    4K     4K     0K     0K] r-x/rwx SM=COW          /bin/sleep
    __LINKEDIT             0000000104b42000-0000000104b45000 [   12K    12K     0K     0K] r--/rwx SM=COW          /bin/sleep
    MALLOC metadata        0000000104b47000-0000000104b48000 [    4K     4K     4K     0K] r--/rwx SM=ZER          DefaultMallocZone_0x104b47000 zone structure
    MALLOC guard page      0000000104b49000-0000000104b4a000 [    4K     0K     0K     0K] ---/rwx SM=ZER          
    MALLOC guard page      0000000104b4e000-0000000104b4f000 [    4K     0K     0K     0K] ---/rwx SM=ZER          
    MALLOC guard page      0000000104b4f000-0000000104b50000 [    4K     0K     0K     0K] ---/rwx SM=NUL          
    MALLOC guard page      0000000104b54000-0000000104b55000 [    4K     0K     0K     0K] ---/rwx SM=NUL          
    MALLOC metadata        0000000104b55000-0000000104b56000 [    4K     4K     4K     0K] r--/rwx SM=PRV          
    __TEXT                 00000001107f7000-0000000110842000 [  300K   300K     0K     0K] r-x/rwx SM=COW          /usr/lib/dyld
    __LINKEDIT             000000011087a000-0000000110895000 [  108K   108K     0K     0K] r--/rwx SM=COW          /usr/lib/dyld
    ...snip...
    
    ==== Writable regions for process 29057
    REGION TYPE                      START - END             [ VSIZE  RSDNT  DIRTY   SWAP] PRT/MAX SHRMOD PURGE    REGION DETAIL
    __DATA                 0000000104b41000-0000000104b42000 [    4K     4K     4K     0K] rw-/rwx SM=COW          /bin/sleep
    Kernel Alloc Once      0000000104b45000-0000000104b47000 [    8K     4K     4K     0K] rw-/rwx SM=PRV          
    MALLOC metadata        0000000104b48000-0000000104b49000 [    4K     4K     4K     0K] rw-/rwx SM=ZER          
    MALLOC metadata        0000000104b4a000-0000000104b4e000 [   16K    16K    16K     0K] rw-/rwx SM=ZER          
    MALLOC metadata        0000000104b50000-0000000104b54000 [   16K    16K    16K     0K] rw-/rwx SM=PRV          
    __DATA                 0000000110842000-0000000110845000 [   12K    12K    12K     0K] rw-/rwx SM=COW          /usr/lib/dyld
    __DATA                 0000000110845000-000000011087a000 [  212K     8K     8K     0K] rw-/rwx SM=PRV          /usr/lib/dyld
    ...snip...
    
    $ kill 29057
    [1]+  Terminated: 15          /bin/sleep 10000

