from pathlib import Path
import os
import re
import asyncio
import ctypes
import Model.macros as macros

# /proc/partitions
# /proc/diskstats
# /proc/ioports
# /proc/iomem
# /sys/block
# inodes - files metadata


async def readStatxAsync(filename):
    libc = ctypes.CDLL("libc.so.6")
    libc.syscall.argtypes = (
        ctypes.c_int,
        ctypes.c_long,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_uint,
        ctypes.POINTER(macros.statx),
    )
    libc.syscall.restype = ctypes.c_int
    statxbuf = macros.statx()
    ctypes.memset(ctypes.pointer(statxbuf), 0xBF, ctypes.sizeof(statxbuf))

    statx_syscall = 332
    result = libc.syscall(
        statx_syscall,
        -100,
        filename,
        0,
        macros.mask,
        ctypes.byref(statxbuf),
    )
    if result == -1:
        print(f"error: {ctypes.get_errno()}, {os.strerror(ctypes.get_errno())}")
        quit(1)
    return filename, statxbuf


async def main():
    try:
        filename = [
            b"/home/abner",
            b"/",
            b"/proc",
            b"/home/linuxbrew",
            b"/home/abner/Downloads/lenovo_z_p_series_hmm_v1.0.pdf",
        ]
        return await asyncio.gather(*[readStatxAsync(file) for file in filename])
    except MemoryError as e:
        print(f"Error: {e}")
        quit(1)


if __name__ == "__main__":
    asyncio.run(main())
