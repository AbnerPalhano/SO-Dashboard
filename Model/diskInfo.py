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


def getFileType(stat):
    type = ""
    if macros.S_ISLNK(stat):
        type = "symbolic link"
    if macros.S_ISREG(stat):
        type = "regular file"
    if macros.S_ISDIR(stat):
        type = "directory"
    if macros.S_ISCHR(stat):
        type = "character device"
    if macros.S_ISBLK(stat):
        type = "block device"
    if macros.S_ISFIFO(stat):
        type = "FIFO"
    if macros.S_ISSOCK(stat):
        type = "socket"
    return type


def getPermissions(stat):
    isDir = "d" if (stat & macros.S_IFDIR) else "-"
    user = (
        ("r" if (stat & macros.S_IRUSR) else "-")
        + ("w" if (stat & macros.S_IWUSR) else "-")
        + ("x" if (stat & macros.S_IXUSR) else "-")
    )
    group = (
        ("r" if (stat & macros.S_IRGRP) else "-")
        + ("w" if (stat & macros.S_IWGRP) else "-")
        + ("x" if (stat & macros.S_IXGRP) else "-")
    )
    others = (
        ("r" if (stat & macros.S_IROTH) else "-")
        + ("w" if (stat & macros.S_IWOTH) else "-")
        + ("x" if (stat & macros.S_IXOTH) else "-")
    )
    return isDir + user + group + others


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
    filetype = getFileType(statxbuf.stx_mode)
    filePermissions = getPermissions(statxbuf.stx_mode)
    if result == -1:
        print(f"error: {ctypes.get_errno()}, {os.strerror(ctypes.get_errno())}")
        quit(1)
    return filename, [statxbuf, filetype, filePermissions]


async def main(basepath):
    try:
        if re.search("[..]", str(basepath)):
            basepath = bytes(os.path.dirname(os.path.dirname(basepath)))
        filenames = os.listdir(os.path.abspath(basepath))
        statx = await asyncio.gather(
            *[
                readStatxAsync(bytes(os.path.abspath(file)))
                for file in [os.path.join(basepath, file) for file in filenames]
            ]
        )
        return statx, basepath
    except MemoryError as e:
        print(f"Error: {e}")
        quit(1)


if __name__ == "__main__":
    ...
    asyncio.run(main(b"/"))
